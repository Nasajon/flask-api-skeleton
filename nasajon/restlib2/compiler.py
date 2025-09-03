#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Gerador de DTO e Entity a partir de um EDL JSON (v1.x).

Uso:
  python generator.py caminho/para/arquivo.edl.json

Saída:
  - Imprime no stdout os fontes do DTO e do Entity.
  - Também grava arquivos opcionais: <Entidade>DTO.py e <Entidade>Entity.py (se desejar, basta descomentar no final).

Notas de mapeamento (EDL -> RestLib):
- Campos obrigatórios: model.required  -> DTOField(not_null=True).
- Chave primária: properties[*].pk == true -> DTOField(pk=True) e @Entity(pk_field=...).
- Tipos/formatos: mapeados para types Python + validadores (uuid, datetime, date, int/float, bool, str).
- Resumo: todos os campos ficam com resume=True (ajuste se quiser outra política).
- Strings: se houver "length", vira max=length e strip=True; se houver restrições mínimas, usa min/maximum.
- Storage: table_name vem de model.storage.map; colunas físicas NÃO são escondidas (nenhum campo é omitido).
- Ordenação padrão: api.defaultSort (sinal "-" indica desc; aqui usamos só a lista de campos como default_order_fields).
- Convenções estruturais e chaves citadas da especificação EDL (model.required, properties, storage, api, etc.). :contentReference[oaicite:1]{index=1}
"""

import json
import sys
import textwrap
import keyword
from typing import Any, Dict, List, Tuple

# -----------------------
# Helpers de transformação
# -----------------------


def py_identifier(name: str) -> str:
    """Garante que o nome é um identificador Python válido."""
    n = name.strip().replace("-", "_")
    if not n.isidentifier() or keyword.iskeyword(n):
        n = f"{n}_"
    return n


def detect_pk(model_props: Dict[str, Any]) -> str:
    for logical, meta in model_props.items():
        if isinstance(meta, dict) and meta.get("pk") is True:
            return logical
    return ""


def to_python_type(prop: Dict[str, Any]) -> str:
    t = (prop.get("type") or "string").lower()
    fmt = (prop.get("format") or "").lower()

    if fmt in {"uuid"}:
        return "uuid.UUID"
    if t in {"datetime"}:
        return "datetime.datetime"
    if t in {"date"}:
        return "datetime.date"
    if t in {"integer"}:
        return "int"
    if t in {"number"}:
        return "float"
    if t in {"boolean"}:
        return "bool"
    # default
    return "str"


def dto_field_args(
    logical: str, prop: Dict[str, Any], required: List[str]
) -> Dict[str, Any]:
    args: Dict[str, Any] = {}

    # Política: sempre expor (resume=True) e nunca ocultar campos que existem na origem
    args["resume"] = True

    # PK / not_null
    if prop.get("pk") is True:
        args["pk"] = True
        args["not_null"] = True
    if logical in set(required):
        args["not_null"] = True

    # Strings: strip + limites
    t = (prop.get("type") or "string").lower()
    if t == "string":
        args["strip"] = True
        if "length" in prop:
            args["max"] = int(prop["length"])
        # mínimo (quando especificado)
        if "minimum" in prop:
            args["min"] = int(prop["minimum"])

    # Números
    if t in {"integer", "number"}:
        if "minimum" in prop:
            args["min"] = (
                int(prop["minimum"]) if t == "integer" else float(prop["minimum"])
            )
        if "maximum" in prop:
            args["max"] = (
                int(prop["maximum"]) if t == "integer" else float(prop["maximum"])
            )

    # Formatos especiais
    fmt = (prop.get("format") or "").lower()
    if fmt == "uuid":
        # aplica validator de uuid
        args["validator"] = "DTOFieldValidators().validate_uuid"
        # tamanho físico usual de uuid textual (36)
        args["min"] = 36
        args["max"] = 36

    # Default lógico (quando presente) — mantemos literal quando simples
    if "default" in prop and prop["default"] is not None:
        # Casos comuns no EDL: "now()" (datas) — deixe como callable se quiser adaptar
        default_val = prop["default"]
        if isinstance(default_val, (int, float, bool)):
            args["default_value"] = repr(default_val)
        elif isinstance(default_val, str) and default_val.endswith("()"):
            # manter como nome de função, será resolvido no import do projeto (ex.: datetime.datetime.now)
            # aqui, por segurança, deixamos literal string; o timekeeper real costuma vir do banco
            args["default_value"] = default_val
        else:
            args["default_value"] = repr(default_val)

    return args


def render_dto(edl: Dict[str, Any]) -> str:
    model = edl.get("model", {})
    props: Dict[str, Any] = model.get("properties", {}) or {}
    required: List[str] = model.get("required", []) or []
    entity_name_full = edl.get("id") or "Entity"
    # Monta um nome de classe lógico (última parte após ponto)
    class_base = entity_name_full.split(".")[-1]
    class_name = f"{class_base[0].upper()}{class_base[1:]}"
    dto_class = f"{class_name}DTO"

    # imports
    need_uuid = any(((p.get("format") or "").lower() == "uuid") for p in props.values())
    need_datetime = any(
        ((p.get("type") or "").lower() in {"datetime", "date"}) for p in props.values()
    )

    header_imports = [
        "from nsj_rest_lib.decorator.dto import DTO",
        "from nsj_rest_lib.descriptor.dto_field import DTOField",
        "from nsj_rest_lib.descriptor.dto_field_validators import DTOFieldValidators",
        "from nsj_rest_lib.dto.dto_base import DTOBase",
    ]
    if need_uuid:
        header_imports.insert(0, "import uuid")
    if need_datetime:
        header_imports.insert(0, "import datetime")

    lines: List[str] = []
    lines.extend(header_imports)
    lines.append("")
    lines.append("")
    lines.append("@DTO()")
    lines.append(f"class {dto_class}(DTOBase):")
    if not props:
        lines.append("    pass")
        return "\n".join(lines)

    for logical in props:
        meta = props[logical] or {}
        py_type = to_python_type(meta)
        field_args = dto_field_args(logical, meta, required)

        # Monta chamada DTOField(...)
        arg_parts = []
        for k, v in field_args.items():
            if k == "validator":
                arg_parts.append(f"{k}={v}")
            else:
                arg_parts.append(f"{k}={repr(v)}")
        args_str = ", ".join(arg_parts) if arg_parts else ""

        lines.append("")
        lines.append(f"    {py_identifier(logical)}: {py_type} = DTOField({args_str})")

    return "\n".join(lines)


def render_entity(edl: Dict[str, Any]) -> str:
    model = edl.get("model", {})
    props: Dict[str, Any] = model.get("properties", {}) or {}
    storage = model.get("storage", {}) or {}
    api = model.get("api", {}) or {}

    entity_name_full = edl.get("id") or "Entity"
    class_base = entity_name_full.split(".")[-1]
    class_name = f"{class_base[0].upper()}{class_base[1:]}"
    entity_class = f"{class_name}Entity"

    table_name = storage.get("map") or "schema.tabela"
    pk_field = detect_pk(props) or "id"

    # default_order_fields = api.defaultSort (limpa prefixos '-' e ignora campos desconhecidos)
    default_sort = []
    for item in api.get("defaultSort", []) or []:
        # remove prefixo de ordenação, mas mantemos apenas o nome lógico do campo
        fld = str(item).lstrip("+-")
        if fld in props:
            default_sort.append(fld)
    # fallback: se vazio, usa pk
    if not default_sort:
        default_sort = [pk_field] if pk_field else []

    # imports
    need_uuid = any(((p.get("format") or "").lower() == "uuid") for p in props.values())
    need_datetime = any(
        ((p.get("type") or "").lower() in {"datetime", "date"}) for p in props.values()
    )

    header_imports = [
        "from nsj_rest_lib.entity.entity_base import EntityBase",
        "from nsj_rest_lib.decorator.entity import Entity",
    ]
    if need_uuid:
        header_imports.insert(0, "import uuid")
    if need_datetime:
        header_imports.insert(0, "import datetime")

    lines: List[str] = []
    lines.extend(header_imports)
    lines.append("")
    lines.append("")
    lines.append("@Entity(")
    lines.append(f"    table_name={repr(table_name)},")
    lines.append(f"    pk_field={repr(py_identifier(pk_field))},")
    if default_sort:
        lines.append(
            f"    default_order_fields={[py_identifier(x) for x in default_sort]},"
        )
    lines.append(")")
    lines.append(f"class {entity_class}(EntityBase):")

    if not props:
        lines.append("    pass")
        return "\n".join(lines)

    for logical, meta in props.items():
        py_type = to_python_type(meta)
        # A Entity não usa DTOField; apenas anota e inicializa None
        lines.append(f"    {py_identifier(logical)}: {py_type} = None")

    return "\n".join(lines)


def generate_from_edl(edl: Dict[str, Any]) -> Tuple[str, str]:
    dto_code = render_dto(edl)
    entity_code = render_entity(edl)
    return dto_code, entity_code


# -----------------------
# CLI
# -----------------------


def main():
    if len(sys.argv) < 2:
        print("Uso: python generator.py caminho/para/arquivo.edl.json", file=sys.stderr)
        sys.exit(2)

    with open(sys.argv[1], "r", encoding="utf-8") as f:
        edl = json.load(f)

    dto_code, entity_code = generate_from_edl(edl)

    sep = "\n" + ("#" * 80) + "\n"
    print(sep + "# DTO\n" + sep)
    print(dto_code)
    print(sep + "# ENTITY\n" + sep)
    print(entity_code)

    # Opcional: gravar em arquivos
    # entity_name_full = edl.get("id") or "Entity"
    # class_base = entity_name_full.split(".")[-1]
    # with open(f"{class_base}DTO.py", "w", encoding="utf-8") as f_dto:
    #     f_dto.write(dto_code + "\n")
    # with open(f"{class_base}Entity.py", "w", encoding="utf-8") as f_ent:
    #     f_ent.write(entity_code + "\n")


if __name__ == "__main__":
    main()

from typing import Any

from nasajon.settings import application, APP_NAME, ESCOPO_RESTLIB2, logger
from nasajon.redis_config import get_redis

from nsj_gcf_utils.rest_error_util import format_json_error

from nsj_rest_lib.controller.controller_util import DEFAULT_RESP_HEADERS
from nsj_rest_lib.controller.list_route import ListRoute
from nsj_rest_lib.controller.get_route import GetRoute
from nsj_rest_lib.controller.post_route import PostRoute
from nsj_rest_lib.controller.put_route import PutRoute
from nsj_rest_lib.controller.patch_route import PatchRoute

COLLECTION_DYNAMIC_ROUTE = f"/{APP_NAME}/dynamic-lists/<entity_id>"
ONE_DYNAMIC_ROUTE = f"/{APP_NAME}/dynamic-lists/<entity_id>/<id>"

namespace = {}
compiled_entities_hashes = {}


class MissingEntityConfigException(Exception):
    pass


def load_entity_source(entity_id: str) -> tuple[str, str]:

    # Recuperando o código do DTO e Entity correspondente
    dto_class_name = get_redis("dto_class_name", ESCOPO_RESTLIB2, entity_id)
    source_dto = get_redis("dto", ESCOPO_RESTLIB2, entity_id)
    entity_class_name = get_redis("entity_class_name", ESCOPO_RESTLIB2, entity_id)
    source_entity = get_redis("entity", ESCOPO_RESTLIB2, entity_id)
    entity_hash = get_redis("hash", ESCOPO_RESTLIB2, entity_id)

    if (
        source_dto is None
        or source_entity is None
        or entity_hash is None
        or entity_class_name is None
        or dto_class_name is None
    ):
        raise MissingEntityConfigException()

    # Verificando se o Entity foi alterado
    if compiled_entities_hashes.get(
        entity_id
    ) is None or entity_hash != compiled_entities_hashes.get(entity_id):
        logger.debug(f"Carregando o código do Entity {entity_id} no namespace")

        # Executa o código da classe no namespace
        exec(source_dto, namespace)
        exec(source_entity, namespace)

        # Gravando o último hash compilado
        compiled_entities_hashes[entity_id] = entity_hash

    return dto_class_name, entity_class_name


@application.route(COLLECTION_DYNAMIC_ROUTE, methods=["GET"])
def list_dynamic(*args: Any, **kwargs: Any):
    # Recuperando o identificador da entidade
    if "entity_id" not in kwargs:
        msg = "Faltando parâmetro identificador da entidade na URL."
        return (format_json_error(msg), 400, {**DEFAULT_RESP_HEADERS})
    entity_id = kwargs.pop("entity_id")

    try:
        # Recuperando o código do DTO e Entity correspondente
        dto_class_name, entity_class_name = load_entity_source(entity_id)

        # Executando o list pelo RestLib
        route = ListRoute(
            url=COLLECTION_DYNAMIC_ROUTE,
            http_method="GET",
            dto_class=namespace[dto_class_name],
            entity_class=namespace[entity_class_name],
        )

        return route.handle_request(*args, **kwargs)
    except MissingEntityConfigException:
        msg = f"Entity configuration for {entity_id} not found."
        return (format_json_error(msg), 412, {**DEFAULT_RESP_HEADERS})


@application.route(ONE_DYNAMIC_ROUTE, methods=["GET"])
def get_dynamic(*args: Any, **kwargs: Any):
    # Recuperando o identificador da entidade
    if "entity_id" not in kwargs:
        msg = "Faltando parâmetro identificador da entidade na URL."
        return (format_json_error(msg), 400, {**DEFAULT_RESP_HEADERS})
    entity_id = kwargs.pop("entity_id")

    try:
        # Recuperando o código do DTO e Entity correspondente
        dto_class_name, entity_class_name = load_entity_source(entity_id)

        # Executando o list pelo RestLib
        route = GetRoute(
            url=ONE_DYNAMIC_ROUTE,
            http_method="GET",
            dto_class=namespace[dto_class_name],
            entity_class=namespace[entity_class_name],
        )

        return route.handle_request(*args, **kwargs)
    except MissingEntityConfigException:
        msg = f"Entity configuration for {entity_id} not found."
        return (format_json_error(msg), 412, {**DEFAULT_RESP_HEADERS})


@application.route(COLLECTION_DYNAMIC_ROUTE, methods=["POST"])
def post_dynamic(*args: Any, **kwargs: Any):
    # Recuperando o identificador da entidade
    if "entity_id" not in kwargs:
        msg = "Faltando parâmetro identificador da entidade na URL."
        return (format_json_error(msg), 400, {**DEFAULT_RESP_HEADERS})
    entity_id = kwargs.pop("entity_id")

    try:
        # Recuperando o código do DTO e Entity correspondente
        dto_class_name, entity_class_name = load_entity_source(entity_id)

        # Executando o list pelo RestLib
        route = PostRoute(
            url=COLLECTION_DYNAMIC_ROUTE,
            http_method="POST",
            dto_class=namespace[dto_class_name],
            entity_class=namespace[entity_class_name],
        )

        return route.handle_request(*args, **kwargs)
    except MissingEntityConfigException:
        msg = f"Entity configuration for {entity_id} not found."
        return (format_json_error(msg), 412, {**DEFAULT_RESP_HEADERS})


@application.route(ONE_DYNAMIC_ROUTE, methods=["PUT"])
def put_dynamic(*args: Any, **kwargs: Any):
    # Recuperando o identificador da entidade
    if "entity_id" not in kwargs:
        msg = "Faltando parâmetro identificador da entidade na URL."
        return (format_json_error(msg), 400, {**DEFAULT_RESP_HEADERS})
    entity_id = kwargs.pop("entity_id")

    try:
        # Recuperando o código do DTO e Entity correspondente
        dto_class_name, entity_class_name = load_entity_source(entity_id)

        # Executando o list pelo RestLib
        route = PutRoute(
            url=ONE_DYNAMIC_ROUTE,
            http_method="PUT",
            dto_class=namespace[dto_class_name],
            entity_class=namespace[entity_class_name],
        )

        return route.handle_request(*args, **kwargs)
    except MissingEntityConfigException:
        msg = f"Entity configuration for {entity_id} not found."
        return (format_json_error(msg), 412, {**DEFAULT_RESP_HEADERS})


@application.route(ONE_DYNAMIC_ROUTE, methods=["PATCH"])
def patch_dynamic(*args: Any, **kwargs: Any):
    # Recuperando o identificador da entidade
    if "entity_id" not in kwargs:
        msg = "Faltando parâmetro identificador da entidade na URL."
        return (format_json_error(msg), 400, {**DEFAULT_RESP_HEADERS})
    entity_id = kwargs.pop("entity_id")

    try:
        # Recuperando o código do DTO e Entity correspondente
        dto_class_name, entity_class_name = load_entity_source(entity_id)

        # Executando o list pelo RestLib
        route = PatchRoute(
            url=ONE_DYNAMIC_ROUTE,
            http_method="PATCH",
            dto_class=namespace[dto_class_name],
            entity_class=namespace[entity_class_name],
        )

        return route.handle_request(*args, **kwargs)
    except MissingEntityConfigException:
        msg = f"Entity configuration for {entity_id} not found."
        return (format_json_error(msg), 412, {**DEFAULT_RESP_HEADERS})

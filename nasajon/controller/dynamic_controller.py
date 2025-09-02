from typing import Any

from nasajon.settings import application, APP_NAME

from nsj_rest_lib.controller.list_route import ListRoute
from nsj_rest_lib.controller.get_route import GetRoute
from nsj_rest_lib.controller.post_route import PostRoute
from nsj_rest_lib.controller.put_route import PutRoute

COLLECTION_DYNAMIC_ROUTE = f"/{APP_NAME}/dynamic-lists"
ONE_DYNAMIC_ROUTE = f"/{APP_NAME}/dynamic-lists/<id>"


codigo_dinamico = """
import datetime
import uuid

from nsj_rest_lib.decorator.dto import DTO
from nsj_rest_lib.descriptor.dto_field import DTOField
from nsj_rest_lib.descriptor.dto_field_validators import DTOFieldValidators
from nsj_rest_lib.dto.dto_base import DTOBase


@DTO()
class ClienteDTO(DTOBase):

    id: uuid.UUID = DTOField(
        pk=True,
        resume=True,
        not_null=True,
        default_value=uuid.uuid4,
        strip=True,
        min=36,
        max=36,
        validator=DTOFieldValidators().validate_uuid,
    )

    codigo: int = DTOField(
        resume=True,
        not_null=True
    )

    nome: str = DTOField(
        resume=True,
        strip=True,
        not_null=True,
        min=1,
        max=100
    )

    documento: str = DTOField(
        resume=True,
        strip=True,
        not_null=True,
        min=1,
        max=14
    )

    created_at: datetime.datetime = DTOField(
        resume=True,
        not_null=True,
        default_value=datetime.datetime.now
    )

import datetime
import uuid

from nsj_rest_lib.entity.entity_base import EntityBase
from nsj_rest_lib.decorator.entity import Entity


@Entity(
    table_name="teste.cliente",
    pk_field="id",
    default_order_fields=["codigo", "nome"],
)
class ClienteEntity(EntityBase):
    id: uuid.UUID = None
    codigo: int = None
    nome: str = None
    documento: str = None
    created_at: datetime.datetime = None
"""


@application.route(COLLECTION_DYNAMIC_ROUTE, methods=["GET"])
def list_dynamic(*args: Any, **kwargs: Any):
    # cria um namespace isolado
    namespace = {}

    # executa o código da classe no namespace
    exec(codigo_dinamico, namespace)

    # Executando o list pelo RestLib
    route = ListRoute(
        url=COLLECTION_DYNAMIC_ROUTE,
        http_method="GET",
        dto_class=namespace["ClienteDTO"],
        entity_class=namespace["ClienteEntity"],
    )

    return route.handle_request(*args, **kwargs)


@application.route(ONE_DYNAMIC_ROUTE, methods=["GET"])
def get_dynamic(*args: Any, **kwargs: Any):
    # cria um namespace isolado
    namespace = {}

    # executa o código da classe no namespace
    exec(codigo_dinamico, namespace)

    # Executando o list pelo RestLib
    route = GetRoute(
        url=COLLECTION_DYNAMIC_ROUTE,
        http_method="GET",
        dto_class=namespace["ClienteDTO"],
        entity_class=namespace["ClienteEntity"],
    )

    return route.handle_request(*args, **kwargs)


@application.route(COLLECTION_DYNAMIC_ROUTE, methods=["POST"])
def post_dynamic(*args: Any, **kwargs: Any):
    # cria um namespace isolado
    namespace = {}

    # executa o código da classe no namespace
    exec(codigo_dinamico, namespace)

    # Executando o list pelo RestLib
    route = PostRoute(
        url=COLLECTION_DYNAMIC_ROUTE,
        http_method="GET",
        dto_class=namespace["ClienteDTO"],
        entity_class=namespace["ClienteEntity"],
    )

    return route.handle_request(*args, **kwargs)


@application.route(ONE_DYNAMIC_ROUTE, methods=["PUT"])
def put_dynamic(*args: Any, **kwargs: Any):
    # cria um namespace isolado
    namespace = {}

    # executa o código da classe no namespace
    exec(codigo_dinamico, namespace)

    # Executando o list pelo RestLib
    route = PutRoute(
        url=COLLECTION_DYNAMIC_ROUTE,
        http_method="GET",
        dto_class=namespace["ClienteDTO"],
        entity_class=namespace["ClienteEntity"],
    )

    return route.handle_request(*args, **kwargs)

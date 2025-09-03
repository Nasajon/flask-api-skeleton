from typing import Any

from nasajon.settings import application, APP_NAME
from nasajon.redis_config import get_redis

from nsj_rest_lib.controller.list_route import ListRoute
from nsj_rest_lib.controller.get_route import GetRoute
from nsj_rest_lib.controller.post_route import PostRoute
from nsj_rest_lib.controller.put_route import PutRoute

COLLECTION_DYNAMIC_ROUTE = f"/{APP_NAME}/dynamic-lists/<entity_id>"
ONE_DYNAMIC_ROUTE = f"/{APP_NAME}/dynamic-lists/<entity_id>/<id>"


@application.route(COLLECTION_DYNAMIC_ROUTE, methods=["GET"])
def list_dynamic(*args: Any, **kwargs: Any):
    # Recuperando o código do DTO e Entity correspondente
    entity_id = kwargs.pop("entity_id")

    source_dto = get_redis("dto", entity_id)
    source_entity = get_redis("entity", entity_id)

    # cria um namespace isolado
    namespace = {}

    # executa o código da classe no namespace
    exec(source_dto, namespace)
    exec(source_entity, namespace)

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

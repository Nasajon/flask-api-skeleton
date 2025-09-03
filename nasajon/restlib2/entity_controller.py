from nasajon.settings import APP_NAME, application
from nsj_rest_lib.controller.delete_route import DeleteRoute
from nsj_rest_lib.controller.get_route import GetRoute
from nsj_rest_lib.controller.list_route import ListRoute
from nsj_rest_lib.controller.post_route import PostRoute
from nsj_rest_lib.controller.put_route import PutRoute

from nasajon.redis_config import set_redis

from nasajon.restlib2.entity_dto import EntityDTO
from nasajon.restlib2.entity_entity import EntityEntity
from nasajon.restlib2.compiler import generate_from_edl

LIST_POST_ROUTE = f"/{APP_NAME}/restlib2/entities"
GET_PUT_ROUTE = f"/{APP_NAME}/restlib2/entities/<id>"


def compilar_entity(db, dto: EntityDTO, after_data):
    edl = dto.json_schema
    codigo = dto.codigo

    dto_code, entity_code = generate_from_edl(edl)

    set_redis("dto", codigo, dto_code)
    set_redis("entity", codigo, entity_code)


@application.route(LIST_POST_ROUTE, methods=["GET"])
@ListRoute(
    url=LIST_POST_ROUTE,
    http_method="GET",
    dto_class=EntityDTO,
    entity_class=EntityEntity,
)
def get_entities(request, response):
    return response


@application.route(GET_PUT_ROUTE, methods=["GET"])
@GetRoute(
    url=GET_PUT_ROUTE,
    http_method="GET",
    dto_class=EntityDTO,
    entity_class=EntityEntity,
)
def get_entity(request, response):
    return response


@application.route(LIST_POST_ROUTE, methods=["POST"])
@PostRoute(
    url=LIST_POST_ROUTE,
    http_method="POST",
    dto_class=EntityDTO,
    entity_class=EntityEntity,
    custom_after_insert=compilar_entity,
)
def post_entity(request, response):
    return response


@application.route(GET_PUT_ROUTE, methods=["PUT"])
@PutRoute(
    url=GET_PUT_ROUTE,
    http_method="PUT",
    dto_class=EntityDTO,
    entity_class=EntityEntity,
    custom_after_update=compilar_entity,
)
def put_entity(request, response):
    return response


@application.route(GET_PUT_ROUTE, methods=["DELETE"])
@DeleteRoute(
    url=GET_PUT_ROUTE,
    http_method="DELETE",
    dto_class=EntityDTO,
    entity_class=EntityEntity,
)
def delete_entity(request, response):
    return response

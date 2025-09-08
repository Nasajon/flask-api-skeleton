import json
import hashlib

from nasajon.settings import APP_NAME, application, logger
from nsj_rest_lib.controller.delete_route import DeleteRoute
from nsj_rest_lib.controller.get_route import GetRoute
from nsj_rest_lib.controller.list_route import ListRoute
from nsj_rest_lib.controller.post_route import PostRoute
from nsj_rest_lib.controller.put_route import PutRoute
from nsj_rest_lib.dto.after_insert_update_data import AfterInsertUpdateData

from nasajon.redis_config import set_redis

from nasajon.restlib2.entity_dto import EntityDTO
from nasajon.restlib2.entity_entity import EntityEntity
from nasajon.restlib2.compiler import generate_from_edl

LIST_POST_ROUTE = f"/{APP_NAME}/restlib2/entities"
GET_PUT_ROUTE = f"/{APP_NAME}/restlib2/entities/<id>"


def compilar_entity(codigo_entity: str, json_edl: dict[str, any], edl_hash: str):
    logger.debug(f"Compilando Entity {codigo_entity}, e salvando no Redis.")

    dto_class_name, dto_code, entity_class_name, entity_code = generate_from_edl(
        json_edl
    )

    set_redis("dto", codigo_entity, dto_code)
    set_redis("dto_class_name", codigo_entity, dto_class_name)
    set_redis("entity", codigo_entity, entity_code)
    set_redis("entity_class_name", codigo_entity, entity_class_name)
    set_redis("hash", codigo_entity, edl_hash)


def before_insert_entity(db, new_dto: EntityDTO):
    edl_new = new_dto.json_schema
    edl_new_str = json.dumps(edl_new, sort_keys=True, ensure_ascii=True, indent=4)
    edl_new_hash = hashlib.sha256(edl_new_str.encode("utf-8")).hexdigest()
    new_dto.content_hash = edl_new_hash
    return new_dto


def after_insert_entity(db, new_dto: EntityDTO, after_data: AfterInsertUpdateData):
    compilar_entity(new_dto.codigo, new_dto.json_schema, new_dto.content_hash)


def before_update_entity(db, old_dto: EntityDTO, new_dto: EntityDTO):
    before_insert_entity(db, new_dto)
    return new_dto


def after_update_entity(
    db, old_dto: EntityDTO, new_dto: EntityDTO, after_data: AfterInsertUpdateData
):
    if new_dto.content_hash != old_dto.content_hash:
        compilar_entity(new_dto.codigo, new_dto.json_schema, new_dto.content_hash)


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
    custom_before_insert=before_insert_entity,
    custom_after_insert=after_insert_entity,
)
def post_entity(request, response):
    return response


@application.route(GET_PUT_ROUTE, methods=["PUT"])
@PutRoute(
    url=GET_PUT_ROUTE,
    http_method="PUT",
    dto_class=EntityDTO,
    entity_class=EntityEntity,
    custom_before_update=before_update_entity,
    custom_after_update=after_update_entity,
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

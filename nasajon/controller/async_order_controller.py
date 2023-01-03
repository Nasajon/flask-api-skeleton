from flask import request
from pydantic import ValidationError

from nasajon.auth import auth
from nasajon.controller.controller_util import DEFAULT_RESP_HEADERS
from nasajon.dto.async_order_dto import AsyncOrderDTO
from nasajon.injector_factory import InjectorFactory
from nasajon.settings import application, logger, APP_NAME, MOPE_CODE

from nsj_gcf_utils.json_util import json_loads
from nsj_gcf_utils.rest_error_util import format_json_error

POST_ROUTE = f'/{APP_NAME}/{MOPE_CODE}/async-orders'


@application.route(POST_ROUTE, methods=['POST'])
@auth.requires_api_key_or_access_token()
def post_async_order():
    with InjectorFactory() as factory:
        try:
            data = request.get_data(as_text=True)
            data = json_loads(data)
            data = AsyncOrderDTO(**data)

            service = factory.async_order_service()
            service.enqueue(data)

            return ({}, 204, {**DEFAULT_RESP_HEADERS})
        except ValidationError as e:
            logger.exception(
                f"Erro ao interpretar json da Ordem Assincrona: {e}")
            return (format_json_error(e), 400, {**DEFAULT_RESP_HEADERS})
        except Exception as e:
            logger.exception(
                f"Erro desconhecido ao receber Ordem Assincrona: {e}")
            return (format_json_error(f'Erro desconhecido: {e}'), 500, {**DEFAULT_RESP_HEADERS})

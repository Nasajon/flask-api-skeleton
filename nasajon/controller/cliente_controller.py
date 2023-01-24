from flask import request
from pydantic import ValidationError

from nasajon.auth import auth
from nasajon.controller.controller_util import DEFAULT_RESP_HEADERS
from nasajon.dto.cliente_post import ClientePostDTO
from nasajon.injector_factory import InjectorFactory
from nasajon.settings import application, logger, APP_NAME, DEFAULT_PAGE_SIZE, MOPE_CODE

from nsj_gcf_utils.exception import NotFoundException
from nsj_gcf_utils.json_util import convert_to_dumps, json_dumps, json_loads
from nsj_gcf_utils.pagination_util import page_body, PaginationException
from nsj_gcf_utils.rest_error_util import format_json_error

GET_ROUTE = f'/{APP_NAME}/{MOPE_CODE}/clientes/<id>'
LIST_POST_ROUTE = f'/{APP_NAME}/{MOPE_CODE}/clientes'

@application.route(LIST_POST_ROUTE, methods=['GET'])
@auth.requires_api_key_or_access_token()
def get_clientes():
    value = request.args.get('search')

    with InjectorFactory() as factory:
        try:
            if value:
                service = factory.clientes_service()
                data = service.search(value)

                return (json_dumps(data), 200, {**DEFAULT_RESP_HEADERS})
            else:
                # Recuperando os parâmetros básicos
                base_url = request.base_url
                args = request.args
                limit = int(args.get('limit', DEFAULT_PAGE_SIZE))
                current_after = args.get('after') or args.get('offset')
                current_before = args.get('before')
                # Construindo os objetos
                service = factory.clientes_service()
                data = service.list(current_after, current_before, limit)
                dict_data = convert_to_dumps(data)

                page = page_body(
                    base_url=base_url,
                    limit=limit,
                    current_after=current_after,
                    current_before=current_before,
                    result=dict_data,
                    id_field='id'
                )

                return (json_dumps(page), 200, {**DEFAULT_RESP_HEADERS})
        except PaginationException as e:
            logger.exception(
                f"Erro de paginação na listagem de clientes: {e}")
            return (format_json_error(e), 400, {**DEFAULT_RESP_HEADERS})
        except Exception as e:
            logger.exception(
                f"Erro desconhecido na listagem de clientes: {e}")
            return (format_json_error(f'Erro desconhecido: {e}'), 500, {**DEFAULT_RESP_HEADERS})


@application.route(GET_ROUTE, methods=['GET'])
@auth.requires_api_key_or_access_token()
def get_cliente_by_id(id: str):
    with InjectorFactory() as factory:
        try:
            service = factory.clientes_service()
            data = service.get(id)

            return (json_dumps(data), 200, {**DEFAULT_RESP_HEADERS})
        except NotFoundException as e:
            logger.warning(
                f"Clientes não encontrado: {e}")
            return (format_json_error(f'{e}'), 404, {**DEFAULT_RESP_HEADERS})
        except Exception as e:
            logger.exception(
                f"Erro desconhecido na recuperação de um cliente: {e}")
            return (format_json_error(f'Erro desconhecido: {e}'), 500, {**DEFAULT_RESP_HEADERS})


@application.route(LIST_POST_ROUTE, methods=['POST'])
@auth.requires_api_key_or_access_token()
def post_cliente():
    with InjectorFactory() as factory:
        try:
            data = request.get_data(as_text=True)
            data = json_loads(data)
            data = ClientePostDTO(**data)

            service = factory.clientes_service()
            data_resp = service.insert(data)

            return (json_dumps(data_resp), 200, {**DEFAULT_RESP_HEADERS})
        except ValidationError as e:
            logger.warning(
                f"Erro desconhecido na interpretação do JSON de um novo cliente: {e}")
            return (format_json_error(e), 400, {**DEFAULT_RESP_HEADERS})
        except Exception as e:
            logger.exception(
                f"Erro desconhecido na gravação de um novo cliente: {e}")
            return (format_json_error(f'Erro desconhecido: {e}'), 500, {**DEFAULT_RESP_HEADERS})

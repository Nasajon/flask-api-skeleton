from app.dto.cliente_post import ClientePostDTO
from app.injector_factory import InjectorFactory
from app.settings import DEFAULT_PAGE_SIZE, flask_app, MOPE_CODE
from flask import request
from nsj_gcf_utils.exception import NotFoundException
from nsj_gcf_utils.json_util import convert_to_dumps, json_dumps, json_loads
from nsj_gcf_utils.pagination_util import page_body, PaginationException
from nsj_gcf_utils.rest_error_util import format_json_error
from app.oauth_config import require_oauth
from pydantic import ValidationError

GET_ROUTE = f'/{MOPE_CODE}/clientes/<id>'
LIST_POST_ROUTE = f'/{MOPE_CODE}/clientes'


@flask_app.route(LIST_POST_ROUTE, methods=['GET'])
@require_oauth()
def get_clientes():
    with InjectorFactory() as factory:
        try:
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

            return (json_dumps(page), 200, {})
        except PaginationException as e:
            return (format_json_error(e), 400, {})
        except Exception as e:
            return (format_json_error(f'Erro desconhecido: {e}'), 500, {})


@flask_app.route(GET_ROUTE, methods=['GET'])
@require_oauth()
def get_cliente_by_id(id: str):
    with InjectorFactory() as factory:
        try:
            service = factory.clientes_service()
            data = service.get(id)

            return (json_dumps(data), 200, {})
        except NotFoundException as e:
            return (format_json_error(f'{e}'), 404, {})
        except Exception as e:
            return (format_json_error(f'Erro desconhecido: {e}'), 500, {})


@flask_app.route(LIST_POST_ROUTE, methods=['POST'])
@require_oauth()
def post_cliente():
    with InjectorFactory() as factory:
        try:
            data = request.get_data(as_text=True)
            data = json_loads(data)
            data = ClientePostDTO(**data)

            service = factory.clientes_service()
            data_resp = service.insert(data)

            return (json_dumps(data_resp), 200, {})
        except ValidationError as e:
            return (format_json_error(e), 400, {})
        except Exception as e:
            return (format_json_error(f'Erro desconhecido: {e}'), 500, {})

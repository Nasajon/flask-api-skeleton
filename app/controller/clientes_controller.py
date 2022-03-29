from app.injector_factory import InjectorFactory
from app.settings import DEFAULT_PAGE_SIZE, flask_app, MOPE_CODE
from flask import request
from nsj_gcf_utils.json_util import convert_to_dumps, json_dumps
from nsj_gcf_utils.pagination_util import page_body, PaginationException

LIST_ROUTE = f'/{MOPE_CODE}/clientes'


@flask_app.route(LIST_ROUTE, methods=['GET'])
def get_clientes():
    # Recuperando os parâmetros básicos
    base_url = request.base_url
    args = request.args
    limit = int(args.get('limit', DEFAULT_PAGE_SIZE))
    current_after = args.get('after') or args.get('offset')
    current_before = args.get('before')

    with InjectorFactory() as factory:
        try:
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
            # TODO Tratar exceptions
            pass

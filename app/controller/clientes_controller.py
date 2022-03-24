from app.injector_factory import InjectorFactory
from app.settings import flask_app, MOPE_CODE
from nsj_gcf_utils.json_util import json_dumps

LIST_ROUTE = f'{MOPE_CODE}/clientes'


@flask_app.route(LIST_ROUTE)
def get_clientes():
    with InjectorFactory() as factory:
        clientes_service = factory.clientes_service()
        clientes = clientes_service.list()
        result = json_dumps(clientes)
        return [200, result, {}]

from app.injector_factory import InjectorFactory
from app.settings import flask_app, MOPE_CODE

GET_ROUTE = f'{MOPE_CODE}/clientes'


@flask_app.route(GET_ROUTE)
def get_clientes():
    with InjectorFactory() as factory:
        clientes_service = factory.clientes_service()
        clientes = clientes_service.list()
        # json = clientes.to

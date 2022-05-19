from flask import Flask
from nasajon import settings

from nasajon.views.cliente_view import Cliente
from nasajon.views.ping_view import Ping


# Configurando o Flask
flask_app = Flask('app')
flask_app.config["JSON_AS_ASCII"] = False


# Endpoints
LIST_POST_ROUTE_CLIENTE = f'/{settings.MOPE_CODE}/clientes'
LIST_POST_ROUTE_PING = f'/{settings.MOPE_CODE}/ping'


# Rotas
flask_app.add_url_rule(LIST_POST_ROUTE_CLIENTE,
                       view_func=Cliente.as_view('cliente'))

flask_app.add_url_rule(LIST_POST_ROUTE_PING, view_func=Ping.as_view('ping'))

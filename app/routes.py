from app import settings
from app.views.cliente_view import Cliente
from flask import Flask


# Rotas
LIST_POST_ROUTE = f'/{settings.MOPE_CODE}/clientes'

# Configurando o Flask
flask_app = Flask('app')

flask_app.add_url_rule(LIST_POST_ROUTE, view_func=Cliente.as_view('cliente'))

flask_app.config["JSON_AS_ASCII"] = False

from flask import jsonify, request
from flask.views import MethodView
from nsj_gcf_utils.json_util import json_loads
from nasajon.oauth_config import require_oauth


class Ping(MethodView):
    @require_oauth()
    def get(self):
        # Procurando o parâmetro "ping" na requisição GET:
        if not ('ping' in request.args):
            # Se não achar, ensina como usar:

            return (
                'PING! (v1) Obs: Para melhorar o teste passe um parâmetro "ping" na requisição. ex: api/ping?ping=algum_texto')

        # Retorna uma resposta ecoando o ping
        return ('PONG! Você passou "{}"'.format(request.args['ping']))

    @require_oauth()
    def post(self):
        data = request.get_data(as_text=True)
        # Montando o dicionário de saída:
        saida = dict()
        if not ('ping' in data):
            saida["msg"] = 'Para melhorar o teste passe um parâmetro "ping" num json no corpo da requisição.'
        else:
            data = json_loads(data)
            saida["msg"] = 'PONG! Você passou "{}"'.format(
                data['ping'])

        # Retornando a response em formato de dict:
        return saida

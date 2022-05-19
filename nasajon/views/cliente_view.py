from flask import jsonify, request
from flask.views import MethodView
from nsj_gcf_utils.pagination_util import page_body, PaginationException
from nsj_gcf_utils.rest_error_util import format_json_error
from nasajon.oauth_config import require_oauth
from pydantic import ValidationError


class Cliente(MethodView):
    @require_oauth()
    def get(self):
        try:
            # Recuperando os parâmetros básicos
            args = request.args
            # Construindo os objetos
            retorno = [{'Nome': 'André', 'Idade': '21'},
                       {'Nome': 'João', 'Idade': '29'}]

            return (jsonify(retorno), 200, {})
        except PaginationException as e:
            return (format_json_error(e), 400, {})
        except Exception as e:
            return (format_json_error(f'Erro desconhecido: {e}'), 500, {})

    @require_oauth()
    def post(self):
        return 'TESTE POST'

    @require_oauth()
    def put(self):
        return 'TESTE PUT'

    @require_oauth()
    def patch(self):
        return 'TESTE PATCH'

    @require_oauth()
    def delete(self):
        return 'TESTE DELETE'

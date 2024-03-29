from authlib.integrations.flask_oauth2 import current_token

from nasajon.auth import auth
from nasajon.controller.controller_util import DEFAULT_RESP_HEADERS
from nasajon.settings import application, APP_NAME

from nsj_gcf_utils.json_util import json_dumps

GET_ROUTE = f'/{APP_NAME}/token-info'


@application.route(GET_ROUTE, methods=['GET'])
@auth.requires_api_key_or_access_token()
def get_tokeninfo():
    return (json_dumps(current_token), 200, {**DEFAULT_RESP_HEADERS})

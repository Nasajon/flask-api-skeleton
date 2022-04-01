from app.settings import flask_app
from authlib.integrations.flask_oauth2 import current_token
from nsj_gcf_utils.json_util import json_dumps
from app.oauth_config import require_oauth

GET_ROUTE = f'/token-info'


@flask_app.route(GET_ROUTE, methods=['GET'])
@require_oauth()
def get_tokeninfo():
    return (json_dumps(current_token), 200, {})

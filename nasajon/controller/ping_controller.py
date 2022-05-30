from nasajon.settings import application, APIKEY_VALIDATE_URL
from nsj_gcf_utils.json_util import json_dumps
from nasajon.api_key_authentication import require_apikey

GET_ROUTE = f'/ping'


@application.route(GET_ROUTE, methods=['GET'])
@require_apikey(APIKEY_VALIDATE_URL)
def get_ping():
    return (json_dumps({"msg": "Pong!"}), 200, {})

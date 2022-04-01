import requests
from authlib.oauth2.rfc7662 import IntrospectTokenValidator
from authlib.integrations.flask_oauth2 import ResourceProtector
from app.settings import OAUTH_CLIENT_ID, OAUTH_CLIENT_SECRET, OAUTH_TOKEN_INTROSPECTION_URL


class MyIntrospectTokenValidator(IntrospectTokenValidator):
    def introspect_token(self, token_string):
        url = OAUTH_TOKEN_INTROSPECTION_URL
        data = {'token': token_string, 'token_type_hint': 'access_token'}
        auth = (OAUTH_CLIENT_ID, OAUTH_CLIENT_SECRET)
        resp = requests.post(url, data=data, auth=auth)
        resp.raise_for_status()
        return resp.json()


require_oauth = ResourceProtector()
# only bearer token is supported currently
require_oauth.register_token_validator(MyIntrospectTokenValidator())

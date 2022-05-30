from functools import wraps
from flask import request, abort
import requests


def require_apikey(validation_url, sistemas_validos=[]):
    def decorator_apikey(api_function):
        @wraps(api_function)
        def decorated_function(*args, **kwargs):
            apikey = request.headers.get('apikey')

            if apikey is None or apikey == '':
                apikey = request.headers.get('X-API-Key')

            response = requests.post(validation_url,
                                     headers={
                                         "Content-Type": "application/x-www-form-urlencoded", 'apikey': apikey},
                                     data=f'apikey={apikey}')

            if response.status_code != 200:
                abort(response.status_code)

            resposta = response.json()

            if len(sistemas_validos) == 0:
                return api_function(*args, **kwargs)
            elif resposta['sistema']['id'] in sistemas_validos:
                return api_function(*args, **kwargs)
            else:
                abort(401)
        return decorated_function
    return decorator_apikey

import ptvsd
import os
import logging
import sys
import time

from flask import Flask

# Lendo variáveis de ambiente
APP_NAME = os.environ['APP_NAME']
DEBUG = bool(os.getenv('DEBUG', 'False'))
MOPE_CODE = os.environ['MOPE_CODE']

DATABASE_HOST = os.environ['DATABASE_HOST']
DATABASE_PASS = os.environ['DATABASE_PASS']
DATABASE_PORT = os.environ['DATABASE_PORT']
DATABASE_NAME = os.environ['DATABASE_NAME']
DATABASE_USER = os.environ['DATABASE_USER']

DEFAULT_PAGE_SIZE = int(os.getenv('DEFAULT_PAGE_SIZE', 20))

OAUTH_CLIENT_ID = os.environ['OAUTH_CLIENT_ID']
OAUTH_CLIENT_SECRET = os.environ['OAUTH_CLIENT_SECRET']
OAUTH_TOKEN_INTROSPECTION_URL = os.environ['OAUTH_TOKEN_INTROSPECTION_URL']

APIKEY_VALIDATE_URL = os.getenv('APIKEY_VALIDATE_URL')

# Configurando o logger
logger = logging.getLogger(APP_NAME)
if DEBUG:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler(sys.stdout)

console_format = logging.Formatter(
    '%(name)s - %(levelname)s - %(message)s')
file_format = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_format)

logger.addHandler(console_handler)


def log_time(msg: str):
    """Decorator para monitoria de performance de métodos (via log)."""

    def decorator(function):
        def wrapper(*arg, **kwargs):
            t = time.time()
            res = function(*arg, **kwargs)
            logger.info(f'----- {str(time.time()-t)} seconds --- {msg}')
            return res

        return wrapper

    return decorator


# Importando e abrindo ouvinte para conexão remota
ptvsd.enable_attach(("0.0.0.0", 5678))

# Configurando o Flask
application = Flask('app')

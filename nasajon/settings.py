import ptvsd
import os
import logging
import logging_loki
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

DIRETORIO_URL = os.environ['DIRETORIO_URL']
PROFILE_URL = os.environ['PROFILE_URL']
API_KEY = os.environ['API_KEY']
GRAFANA_URL = os.environ['GRAFANA_URL']
AMBIENTE = os.environ['AMBIENTE']

RABBITMQ_HOST = os.environ['RABBITMQ_HOST']
RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT', 5672))
RABBITMQ_HTTP_PORT = int(os.getenv('RABBITMQ_HTTP_PORT', 15672))
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'guest')
RABBITMQ_PASS = os.getenv('RABBITMQ_PASS', 'guest')
RABBITMQ_VHOST = os.environ['RABBITMQ_VHOST']

ASYNC_QUEUE_NAME = os.environ['ASYNC_QUEUE_NAME']
ASYNC_QUEUE_TTL = int(os.getenv('ASYNC_QUEUE_TTL', 86400))
ASYNC_QUEUE_DELAY = int(os.getenv('ASYNC_QUEUE_DELAY', 900))

# Configurando o logger
logger = logging.getLogger(APP_NAME)
if DEBUG:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler(sys.stdout)
loki_handler = logging_loki.LokiHandler(url=GRAFANA_URL, tags={AMBIENTE.upper(
) + "_flask_api_skeleton": AMBIENTE.lower() + "_log"}, version="1",)

console_format = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

console_handler.setFormatter(console_format)

logger.addHandler(console_handler)
logger.addHandler(loki_handler)


def log_time(msg: str):
    """Decorator para monitoria de performance de métodos (via log)."""

    def decorator(function):
        def wrapper(*arg, **kwargs):
            t = time.perf_counter()
            res = function(*arg, **kwargs)
            logger.debug(
                f'{msg} - Tempo de resposta: {str(round(time.perf_counter()-t, 3))} segundos.')
            return res

        return wrapper

    return decorator


# Importando e abrindo ouvinte para conexão remota
ptvsd.enable_attach(("0.0.0.0", 5678))

# Configurando o Flask
application = Flask('app')

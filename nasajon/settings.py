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

DIRETORIO_URL = os.environ['DIRETORIO_URL']
PROFILE_URL = os.environ['PROFILE_URL']
API_KEY = os.environ['API_KEY']

LOG_FILE_PATH = os.getenv(
    'LOG_FILE_PATH', f"/var/log/nasajon/exec.log")

# Configurando o logger
logger = logging.getLogger(APP_NAME)
if DEBUG:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler(
    filename=LOG_FILE_PATH)

console_format = logging.Formatter(
    '%(name)s - %(levelname)s - %(message)s')
file_format = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

console_handler.setFormatter(console_format)
file_handler.setFormatter(file_format)

logger.addHandler(console_handler)
logger.addHandler(file_handler)


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

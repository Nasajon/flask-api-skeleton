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
        def wrapper(*arg):
            t = time.time()
            res = function(*arg)
            logger.info(f'----- {str(time.time()-t)} seconds --- {msg}')
            return res

        return wrapper

    return decorator


# Configurando o Flask
flask_app = Flask('app')

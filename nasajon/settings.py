import ptvsd
import os
import logging
import logging_loki
import sys
import time

from flask import Flask

# Lendo variáveis de ambiente
APP_NAME = os.environ["APP_NAME"]
LOG_DEBUG = os.getenv("LOG_DEBUG", "False").upper() == "TRUE"
MOPE_CODE = os.environ["MOPE_CODE"]

DATABASE_HOST = os.environ["DATABASE_HOST"]
DATABASE_PASS = os.environ["DATABASE_PASS"]
DATABASE_PORT = os.environ["DATABASE_PORT"]
DATABASE_NAME = os.environ["DATABASE_NAME"]
DATABASE_USER = os.environ["DATABASE_USER"]

DEFAULT_PAGE_SIZE = int(os.getenv("DEFAULT_PAGE_SIZE", 20))

DIRETORIO_URL = os.environ["DIRETORIO_URL"]
PROFILE_URL = os.environ["PROFILE_URL"]
API_KEY = os.environ["API_KEY"]
GRAFANA_URL = os.getenv("GRAFANA_URL")
ENV = os.environ["ENV"]

RABBITMQ_HOST = os.environ["RABBITMQ_HOST"]
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", 5672))
RABBITMQ_HTTP_PORT = int(os.getenv("RABBITMQ_HTTP_PORT", 15672))
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "guest")
RABBITMQ_VHOST = os.environ["RABBITMQ_VHOST"]

ASYNC_QUEUE_NAME = os.environ["ASYNC_QUEUE_NAME"]
ASYNC_QUEUE_TTL = int(os.getenv("ASYNC_QUEUE_TTL", 86400))
ASYNC_QUEUE_DELAY = int(os.getenv("ASYNC_QUEUE_DELAY", 900))

# Configurando o logger
logger = logging.getLogger(APP_NAME)
if LOG_DEBUG:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

log_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(log_format)
logger.addHandler(console_handler)

if GRAFANA_URL is not None and GRAFANA_URL.strip() != "":
    loki_handler = logging_loki.LokiHandler(
        url=GRAFANA_URL,
        tags={ENV.upper() + "_flask_api_skeleton": ENV.lower() + "_log"},
        version="1",
    )
    loki_handler.setFormatter(log_format)
    logger.addHandler(loki_handler)


def log_time(msg: str):
    """Decorator para monitoria de performance de métodos (via log)."""

    def decorator(function):
        def wrapper(*arg, **kwargs):
            t = time.perf_counter()
            res = function(*arg, **kwargs)
            logger.debug(
                f"{msg} - Tempo de resposta: {str(round(time.perf_counter()-t, 3))} segundos."
            )
            return res

        return wrapper

    return decorator


# Importando e abrindo ouvinte para conexão remota
ptvsd.enable_attach(("0.0.0.0", 5678))

# Configurando o Flask
application = Flask("app")

# Configurando o sentry
try:
    import sentry_sdk
    from sentry_sdk.integrations.logging import LoggingIntegration

    SENTRY_DSN = os.getenv(
        "SENTRY_DSN",
    )

    if SENTRY_DSN is not None and SENTRY_DSN.strip() != "":
        sentry_logging = LoggingIntegration(
            level=logging.INFO,  # Capture info and above as breadcrumbs
            event_level=logging.ERROR,  # Send errors as events
        )
        sentry_sdk.init(
            dsn=SENTRY_DSN,
            integrations=[sentry_logging],
            # Set traces_sample_rate to 1.0 to capture 100%
            # of transactions for performance monitoring.
            # We recommend adjusting this value in production.
            traces_sample_rate=1.0,
            # By default the SDK will try to use the SENTRY_RELEASE
            # environment variable, or infer a git commit
            # SHA as release, however you may want to set
            # something more human-readable.
            # release="myapp@1.0.0",
        )

        logger.info("SENTRY CARREGADO")
except Exception as e:
    logger.exception(f"Erro configurando o Sentry: {e}")

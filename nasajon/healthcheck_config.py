import base64
import requests

from healthcheck import HealthCheck

from nasajon.injector_factory import InjectorFactory
from nasajon.settings import application, APP_NAME, RABBITMQ_HOST, RABBITMQ_HTTP_PORT, RABBITMQ_USER, RABBITMQ_PASS

health = HealthCheck()

# Adicionando a validação de banco de dados


def database():
    with InjectorFactory() as factory:
        sql = "SELECT 1"

        factory.db_adapter().execute_query(sql)

        return True, "Banco de dados OK"


health.add_check(database)

# Adicionando a validação do RabbitMQ


def rabbit_mq():
    rabbit_url = f"{RABBITMQ_HOST}:{RABBITMQ_HTTP_PORT}/api/healthchecks/node"
    if rabbit_url[0:4] != 'http':
        rabbit_url = 'http://' + rabbit_url

    credentials = f"{RABBITMQ_USER}:{RABBITMQ_PASS}"
    credentials = credentials.encode('utf8')
    credentials = base64.b64encode(credentials)
    credentials = credentials.decode('utf8')

    headers = {
        "Authorization": f"Basic {credentials}"
    }

    response = requests.get(rabbit_url, headers=headers)

    if response.status_code == 200:
        return True, "RabbitMQ OK"
    else:
        return False, f"Falha de comunicação com o RabbitMQ"


health.add_check(rabbit_mq)

# Registrando a rota do HealthCheck
application.add_url_rule(f"/{APP_NAME}/healthcheck", "healthcheck",
                         view_func=lambda: health.run())

import os
import pika
import sys

from pydantic import BaseModel, ValidationError

from nasajon.settings import logger, RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_VHOST
from nasajon.exception import TTLMessageException

from nsj_gcf_utils.json_util import json_loads


class AsyncWorkerBase:

    def __init__(self, async_queue_name: str, dto_class: BaseModel, queue_ttl=86400, queue_delay=900):
        super().__init__()
        self._async_queue_name = async_queue_name
        self._async_queue_name_delay = f"{async_queue_name}_delay"
        self._dto_class = dto_class
        self._queue_ttl = queue_ttl * 1000
        self._queue_delay = queue_delay * 1000

    def execute(self, msg_obj: BaseModel):
        """
        Este método deve ser sobrescrito na subclasse.

        Ele deve ser o responsável pelo processamento da mensagem (contida no objeto de modelo recebido).
        """
        pass

    def callback(self, ch, method, properties, body):
        try:
            try:
                logger.info("Nova mensagem recebida.")
                tries = self._get_message_try_number(properties)
                logger.info(
                    f"Número de vezes da mensagem na fila de processamento: {tries+1}.")

                logger.debug(f"Dados da mensagem: {body}")

                data_str = body.decode('utf-8')
                data = json_loads(data_str)
                data = self._dto_class(**data)

                self.execute(data)

                logger.info("Mensagem processada.")

                ch.basic_ack(delivery_tag=method.delivery_tag)
            except ValidationError as e:
                self._check_message_ttl(properties)
                logger.exception(f"Erro interpretando o JSON da mensagem: {e}")
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            except Exception as e:
                self._check_message_ttl(properties)
                logger.exception(
                    f"Erro desconhecido processando a mensagem: {e}")
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        except TTLMessageException as e:
            logger.exception(
                f"{e}\nDados da mensagem descartada: {data_str}")
            ch.basic_ack(delivery_tag=method.delivery_tag)

    def _get_message_try_number(self, properties):
        """
        Recupera o número de vezes que a mensagem entrou na fila de processamento
        """

        if properties.headers is None:
            return 0

        x_death = properties.headers.setdefault('x-death', [{}])
        retries = x_death[0].get('count', 1)

        return retries

    def _check_message_ttl(self, properties):
        """
        Verifica se a mensagem excedeu o TTL da fila (para descarte final da mesma)
        """

        retries = self._get_message_try_number(properties)
        if retries <= 0:
            return

        time_in_queue = (retries - 1) * self._queue_delay

        if time_in_queue >= self._queue_ttl:
            raise TTLMessageException(
                f"Mensagem descartada por exceder o TTL. Quantidade de tentativas: {retries}. TTL: {self._queue_ttl}. Retry delay: {self._queue_delay}.")

    def main(self):
        try:
            logger.info("Iniciando o worker...")

            with pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=RABBITMQ_HOST,
                    virtual_host=RABBITMQ_VHOST,
                    port=RABBITMQ_PORT
                )
            ) as connection:
                channel = connection.channel()

                # Criando a fila para processamento das mensagens
                channel.queue_declare(
                    queue=self._async_queue_name,
                    durable=True,
                    arguments={
                        "x-message-ttl": self._queue_ttl,
                        'x-dead-letter-exchange': '',
                        'x-dead-letter-routing-key': self._async_queue_name_delay
                    }
                )

                # Criando a fila de mortos (para atraso dos erros)
                channel.queue_declare(
                    queue=self._async_queue_name_delay,
                    durable=True,
                    arguments={
                        "x-message-ttl": self._queue_delay,
                        'x-dead-letter-exchange': '',
                        'x-dead-letter-routing-key': self._async_queue_name
                    }
                )

                channel.basic_qos(prefetch_count=1)
                channel.basic_consume(queue=self._async_queue_name,
                                      on_message_callback=self.callback)

                logger.info(
                    f"Worker {self.__class__.__name__} iniciado. Precione CTRL+C para sair.")
                logger.info(
                    f"Aguardando por uma mensagem...")
                channel.start_consuming()
        except KeyboardInterrupt:
            logger.info('Keyboard Interrupt (worker interrompido).')
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)

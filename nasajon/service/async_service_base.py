import pika

from pydantic import BaseModel

from nasajon.settings import logger, RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_VHOST

from nsj_gcf_utils.json_util import json_dumps


class AsynServiceBase:

    def __init__(self, async_queue_name: str, queue_ttl=86400, queue_delay=900):
        super().__init__()
        self._async_queue_name = async_queue_name
        self._async_queue_name_delay = f"{async_queue_name}_delay"
        self._queue_ttl = queue_ttl * 1000
        self._queue_delay = queue_delay * 1000

    def handle_message_befor_enqueue(self, msg: BaseModel) -> BaseModel:
        return msg

    def enqueue(self, msg: BaseModel):

        msg = self.handle_message_befor_enqueue(msg)

        with pika.BlockingConnection(
            pika.ConnectionParameters(
                host=RABBITMQ_HOST,
                virtual_host=RABBITMQ_VHOST,
                port=RABBITMQ_PORT)
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

            # Publicando a mensagem (e garantindo o roteamento para a fila de mortos)
            channel.basic_publish(
                exchange='',
                routing_key=self._async_queue_name,
                body=json_dumps(msg),
                properties=pika.BasicProperties(
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                )
            )
            logger.info("Nova mensagem enfileirada.")
            logger.debug(f"Dados da mensagem enfileirada: {json_dumps(msg)}")

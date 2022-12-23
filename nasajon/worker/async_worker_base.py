import pika

from pydantic import BaseModel, ValidationError

from nasajon.settings import logger, ASYNC_QUEUE_NAME, RABBITMQ_HOST, RABBITMQ_VHOST

from nsj_gcf_utils.json_util import json_loads


class AsyncWorkerBase:
    def __init__(self, dto_class: BaseModel):
        super().__init__()
        self._dto_class = dto_class

    def execute(self, msg_obj: BaseModel):
        """
        Este método deve ser sobrescrito na subclasse.

        Ele deve ser o responsável pelo processamento da mensagem (contida no objeto de modelo recebido).
        """
        pass

    def callback(self, ch, method, properties, body):
        try:
            logger.info("Nova mensagem recebida.")
            logger.debug(f"Dados da mensagem: {body}")

            data = body.decode('utf-8')
            data = json_loads(data)
            data = self._dto_class(**data)

            self.execute(data)

            logger.info("Mensagem processada.")

            ch.basic_ack(delivery_tag=method.delivery_tag)
        except ValidationError as e:
            logger.exception(f"Erro interpretando o JSON da mensagem: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag)
        except Exception as e:
            logger.exception(
                f"Erro desconhecido processamento a mensagem: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag)

    def main(self):
        logger.info("Iniciando o worker...")

        with pika.BlockingConnection(
            pika.ConnectionParameters(
                host=RABBITMQ_HOST,
                virtual_host=RABBITMQ_VHOST
            )
        ) as connection:
            channel = connection.channel()

            channel.queue_declare(queue=ASYNC_QUEUE_NAME, durable=True)

            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue=ASYNC_QUEUE_NAME,
                                  on_message_callback=self.callback)

            logger.info(
                f"Worker {self.__class__.__name__} iniciado. Precione CTRL+C para sair.")
            logger.info(
                f"Aguardando por uma mensagem...")
            channel.start_consuming()
import pika

from nasajon.dto.async_order_dto import AsyncOrderDTO
from nasajon.settings import logger, ASYNC_QUEUE_NAME, RABBITMQ_HOST, RABBITMQ_VHOST

from nsj_gcf_utils.json_util import json_dumps


class AsynOrderService:

    def enqueue_order(self, order: AsyncOrderDTO):

        with pika.BlockingConnection(
            pika.ConnectionParameters(
                host=RABBITMQ_HOST,
                virtual_host=RABBITMQ_VHOST
            )
        ) as connection:
            channel = connection.channel()

            channel.queue_declare(queue=ASYNC_QUEUE_NAME, durable=True)

            channel.basic_publish(
                exchange='',
                routing_key=ASYNC_QUEUE_NAME,
                body=json_dumps(order),
                properties=pika.BasicProperties(
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                )
            )
            logger.info("Nova ordem enfileirada.")
            logger.debug(f"Dados da ordem enfileirada: {json_dumps(order)}")

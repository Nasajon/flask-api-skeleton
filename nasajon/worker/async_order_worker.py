import time
import random

from nasajon.dto.async_order_dto import AsyncOrderDTO
from nasajon.settings import logger, ASYNC_QUEUE_NAME, ASYNC_QUEUE_TTL, ASYNC_QUEUE_DELAY
from nasajon.worker.async_worker_base import AsyncWorkerBase


class AsyncOrderWorker(AsyncWorkerBase):

    def __init__(self):
        super().__init__(
            ASYNC_QUEUE_NAME,
            AsyncOrderDTO,
            queue_ttl=ASYNC_QUEUE_TTL,
            queue_delay=ASYNC_QUEUE_DELAY
        )

    def execute(self, order: AsyncOrderDTO):
        logger.info(f"Informação recebida para processamento: {order.msg}")
        time.sleep(1)

        if random.random() >= 0.5:
            raise Exception('Teste de erro (aleatório) para simular o delay.')


if __name__ == '__main__':
    AsyncOrderWorker().main()

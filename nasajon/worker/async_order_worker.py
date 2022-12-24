import time

from nasajon.dto.async_order_dto import AsyncOrderDTO
from nasajon.settings import logger, ASYNC_QUEUE_NAME, ASYNC_QUEUE_TTL
from nasajon.worker.async_worker_base import AsyncWorkerBase


class AsyncOrderWorker(AsyncWorkerBase):

    def __init__(self):
        super().__init__(
            ASYNC_QUEUE_NAME,
            AsyncOrderDTO,
            queue_ttl=ASYNC_QUEUE_TTL
        )

    def execute(self, order: AsyncOrderDTO):
        logger.info(f"Informação recebida para processamento: {order.msg}")
        time.sleep(5)


if __name__ == '__main__':
    AsyncOrderWorker().main()

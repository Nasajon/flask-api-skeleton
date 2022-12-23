import sys
import os
import time

from nasajon.dto.async_order_dto import AsyncOrderDTO
from nasajon.settings import logger
from nasajon.worker.async_worker_base import AsyncWorkerBase


class AsyncOrderWorker(AsyncWorkerBase):

    def __init__(self):
        super().__init__(AsyncOrderDTO)

    def execute(self, order: AsyncOrderDTO):
        logger.info(f"Informação recebida para processamento: {order.msg}")
        time.sleep(5)


if __name__ == '__main__':
    try:
        AsyncOrderWorker().main()
    except KeyboardInterrupt:
        logger.info('Keyboard Interrupt (worker interrompido).')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

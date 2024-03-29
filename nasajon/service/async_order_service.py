from nasajon.service.async_service_base import AsynServiceBase
from nasajon.settings import ASYNC_QUEUE_NAME, ASYNC_QUEUE_TTL, ASYNC_QUEUE_DELAY


class AsynOrderService(AsynServiceBase):

    def __init__(self):
        super().__init__(
            ASYNC_QUEUE_NAME,
            queue_ttl=ASYNC_QUEUE_TTL,
            queue_delay=ASYNC_QUEUE_DELAY
        )

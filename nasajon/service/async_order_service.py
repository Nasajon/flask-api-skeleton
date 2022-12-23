from nasajon.dto.async_order_dto import AsyncOrderDTO
from nasajon.service.async_service_base import AsynServiceBase
from nasajon.settings import ASYNC_QUEUE_NAME


class AsynOrderService(AsynServiceBase):

    def __init__(self):
        super().__init__(ASYNC_QUEUE_NAME)

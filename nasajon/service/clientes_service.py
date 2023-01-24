import uuid

from nasajon.dao.clientes_dao import ClientesDAO
from nasajon.dto.cliente_get_dto import ClienteGetDTO
from nasajon.dto.cliente_post import ClientePostDTO
from nasajon.dto.cliente_post_resp import ClientePostResponseDTO
from nasajon.entity.cliente import Cliente
from nsj_gcf_utils.dto_util import convert_to


class ClientesService:
    _dao: ClientesDAO

    def __init__(self, dao: ClientesDAO):
        self._dao = dao

    def get(
        self,
        id: uuid.UUID
    ):
        return convert_to(
            self._dao.get(id),
            ClienteGetDTO
        )

    def list(
        self,
        after: uuid.UUID,
        before: uuid.UUID,
        limit: int
    ):
        return convert_to(
            self._dao.list(after, before, limit),
            ClienteGetDTO
        )

    def insert(
        self,
        cliente: ClientePostDTO
    ) -> ClientePostResponseDTO:
        model = convert_to(cliente, Cliente)
        return convert_to(
            self._dao.insert(model),
            ClientePostResponseDTO
        )
    
    def search(
        self,
        value: str
    ):
        return convert_to(
            self._dao.search(value),
            ClienteGetDTO
        )

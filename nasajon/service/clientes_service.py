import uuid
from datetime import datetime, timedelta, timezone

from nasajon.dao.clientes_dao import ClientesDAO
from nasajon.service.filas.fila_cliente import FilaCliente
from nasajon.dto.cliente_get_dto import ClienteGetDTO
from nasajon.dto.cliente_post import ClientePostDTO
from nasajon.dto.cliente_post_resp import ClientePostResponseDTO
from nasajon.entity.cliente import Cliente
from nsj_gcf_utils.dto_util import convert_to

class ClientesService:
    _dao: ClientesDAO
    _fila_cliente : FilaCliente

    def __init__(
        self, dao: ClientesDAO,
        _fila_cliente : FilaCliente
    ):
        self._dao = dao
        self._fila_cliente = _fila_cliente

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

        try:
            self._dao.begin()

            model = convert_to(cliente, Cliente)
            model = self._dao.insert(model)
            dto = convert_to(model, ClientePostResponseDTO)

            #enfileira
            self._fila_cliente.enfileira(model.id)

            return dto

        except:
            self._dao.rollback()
            raise
        finally:
            self._dao.commit()

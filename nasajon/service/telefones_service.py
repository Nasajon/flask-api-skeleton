import uuid
from datetime import datetime, timedelta, timezone

from nasajon.dao.telefones_dao import TelefonesDAO
from nasajon.service.filas.fila_cliente import FilaCliente
from nasajon.dto.telefone_get_dto import TelefoneGetDTO
from nasajon.dto.telefone_post import TelefonePostDTO
from nasajon.dto.telefone_post_resp import TelefonePostResponseDTO
from nasajon.entity.telefone import Telefone
from nsj_gcf_utils.dto_util import convert_to
from nsj_gcf_utils.json_util import json_dumps

#from nsj_queue_lib.settings import logger

class TelefonesService:
    _dao: TelefonesDAO
    _fila_cliente : FilaCliente

    def __init__(self, dao: TelefonesDAO, _fila_cliente : FilaCliente):
        self._dao = dao
        self._fila_cliente = _fila_cliente


    def get(
        self,
        id: uuid.UUID
    ):
        return convert_to(
            self._dao.get(id),
            TelefoneGetDTO
        )

    def list(
        self,
        after: uuid.UUID,
        before: uuid.UUID,
        limit: int
    ):
        return convert_to(
            self._dao.list(after, before, limit),
            TelefoneGetDTO
        )

    def list_by_cliente(
        self,
        cliente: uuid.UUID
    ):
        return convert_to(
            self._dao.list_by_cliente(cliente),
            TelefoneGetDTO
        )

    def insert(
        self,
        telefone: TelefonePostDTO
    ) -> TelefonePostResponseDTO:

        try:
            self._dao.begin()

            model = convert_to(telefone, Telefone)
            model = self._dao.insert(model)
            dto = convert_to(model, TelefonePostResponseDTO)

            self._fila_cliente.enfileira(model.cliente)

            return dto

        except:
            self._dao.rollback()
            raise
        finally:
            self._dao.commit()

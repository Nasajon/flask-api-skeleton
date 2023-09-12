import uuid
from datetime import datetime, timedelta, timezone

from nasajon.dao.contatos_dao import ContatosDAO
from nasajon.dto.contato_get_dto import ContatoGetDTO
from nasajon.dto.contato_post import ContatoPostDTO
from nasajon.dto.contato_post_resp import ContatoPostResponseDTO
from nasajon.entity.contato import Contato
from nsj_gcf_utils.dto_util import convert_to
from nsj_gcf_utils.json_util import json_dumps

from nsj_queue_lib.settings import logger

class ContatosService:
    _dao: ContatosDAO

    def __init__(self, dao: ContatosDAO):
        self._dao = dao

    def get(
        self,
        id: uuid.UUID
    ):
        return convert_to(
            self._dao.get(id),
            ContatoGetDTO
        )

    def list(
        self,
        after: uuid.UUID,
        before: uuid.UUID,
        limit: int
    ):
        return convert_to(
            self._dao.list(after, before, limit),
            ContatoGetDTO
        )

    def insert(
        self,
        contato: ContatoPostDTO
    ) -> ContatoPostResponseDTO:
        model = convert_to(contato, Contato)
        return convert_to(
            self._dao.insert(model),
            ContatoPostResponseDTO
        )

    def update(
        self,
        contato: ContatoPostDTO
    ) -> ContatoPostResponseDTO:
        model = convert_to(contato, Contato)
        return convert_to(
            self._dao.update(model),
            ContatoPostResponseDTO
        )
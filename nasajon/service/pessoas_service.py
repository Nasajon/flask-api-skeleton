import uuid

from nasajon.dao.pessoas_dao import PessoasDAO
from nasajon.dto.pessoa_get_dto import PessoaGetDTO
from nasajon.dto.pessoa_post import PessoaPostDTO
from nasajon.dto.pessoa_post_resp import PessoaPostResponseDTO
from nasajon.entity.pessoa import Pessoa
from nsj_gcf_utils.dto_util import convert_to


class PessoasService:
    _dao: PessoasDAO

    def __init__(self, dao: PessoasDAO):
        self._dao = dao

    def get(
        self,
        id: uuid.UUID
    ):
        return convert_to(
            self._dao.get(id),
            PessoaGetDTO
        )

    def list(
        self,
        after: uuid.UUID,
        before: uuid.UUID,
        limit: int
    ):
        return convert_to(
            self._dao.list(after, before, limit),
            PessoaGetDTO
        )

    def insert(
        self,
        pessoa: PessoaPostDTO
    ) -> PessoaPostResponseDTO:
        model = convert_to(pessoa, Pessoa)
        return convert_to(
            self._dao.insert(model),
            PessoaPostResponseDTO
        )

    def update(
        self,
        pessoa: PessoaPostDTO
    ) -> PessoaPostResponseDTO:
        model = convert_to(pessoa, Pessoa)
        return convert_to(
            self._dao.update(model),
            PessoaPostResponseDTO
        )

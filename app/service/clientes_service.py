from app.dao.clientes_dao import ClientesDAO
from app.dto.cliente_get_dto import ClienteGetDTO
from nsj_gcf_utils.dto_util import convert_to


class ClientesService:
    _dao: ClientesDAO

    def __init__(self, dao: ClientesDAO):
        self._dao = dao

    def list(self):
        return convert_to(self._dao.list(), ClienteGetDTO)

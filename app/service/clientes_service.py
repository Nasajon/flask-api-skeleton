from app.dao.clientes_dao import ClientesDAO


class ClientesService:
    _dao: ClientesDAO

    def __init__(self, dao: ClientesDAO):
        self._dao = dao

    def list(self):
        return self._dao.list()

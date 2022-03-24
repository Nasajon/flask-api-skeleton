from app.settings import log_time
from app.entity.cliente import Cliente

from nsj_gcf_utils.db_adapter2 import DBAdapter2
from typing import List


class ClientesDAO:
    _db: DBAdapter2

    def __init__(self, db: DBAdapter2 = None):
        self._db = db

    @log_time('Listando clientes do banco de dados.')
    def list(self) -> List[Cliente]:
        """
        Recupera a lista completa de clientes.
        """

        query = """
        select
            id, nome, documento, created_at
        from
            teste.cliente
        """

        resp = self._db.execute_query_to_model(query, Cliente)

        return resp

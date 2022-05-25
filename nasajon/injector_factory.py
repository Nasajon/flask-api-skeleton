from sqlalchemy.engine.base import Connection


class InjectorFactory:
    _db_connection: Connection

    def __enter__(self):
        from nasajon.db_pool_config import db_pool
        self._db_connection = db_pool.connect()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._db_connection.close()

    def db_adapter(self):
        from nsj_gcf_utils.db_adapter2 import DBAdapter2
        return DBAdapter2(self._db_connection)

    # DAOs
    def clientes_dao(self):
        from nasajon.dao.clientes_dao import ClientesDAO
        return ClientesDAO(self.db_adapter())

    # SERVICES
    def clientes_service(self):
        from nasajon.service.clientes_service import ClientesService
        return ClientesService(self.clientes_dao())

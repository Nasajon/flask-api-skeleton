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

    def pessoas_dao(self):
        from nasajon.dao.pessoas_dao import PessoasDAO
        return PessoasDAO(self.db_adapter())

    def telefones_dao(self):
        from nasajon.dao.telefones_dao import TelefonesDAO
        return TelefonesDAO(self.db_adapter())

    def contatos_dao(self):
        from nasajon.dao.contatos_dao import ContatosDAO
        return ContatosDAO(self.db_adapter())


    # SERVICES
    def clientes_service(self):
        from nasajon.service.clientes_service import ClientesService
        return ClientesService(self.clientes_dao(), self.fila_clientes())

    def pessoas_service(self):
        from nasajon.service.pessoas_service import PessoasService
        return PessoasService(self.pessoas_dao())

    def telefones_service(self):
        from nasajon.service.telefones_service import TelefonesService
        return TelefonesService(self.telefones_dao(), self.fila_clientes())

    def contatos_service(self):
        from nasajon.service.contatos_service import ContatosService
        return ContatosService(self.contatos_dao())

    def async_order_service(self):
        from nasajon.service.async_order_service import AsynOrderService
        return AsynOrderService()

    # Filas
    def fila_clientes(self):
        from nasajon.service.filas.fila_cliente import FilaCliente
        return FilaCliente(self._db_connection)

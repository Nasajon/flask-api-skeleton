import uuid

from app.settings import log_time
from app.entity.cliente import Cliente

from nsj_gcf_utils.db_adapter2 import DBAdapter2
from typing import List


class ClientesDAO:
    _db: DBAdapter2

    def __init__(self, db: DBAdapter2 = None):
        self._db = db

    def get(self, id: uuid.UUID):
        query = """
        select
            id, codigo, nome, documento, created_at
        from
            teste.cliente
        where
            id = :id
        """

        resp = self._db.execute_query_to_model(query, Cliente, id=id)

        return resp

    # @log_time('Listando clientes do banco de dados.')
    # TODO Corrigir implementação do decorator
    def list(
        self,
        after: uuid.UUID,
        before: uuid.UUID,
        limit: int
    ) -> List[Cliente]:
        """
        Recupera a lista completa de clientes.
        """

        # Recuperando dados para paginacao
        codigo_after = None
        nome_after = None
        codigo_before = None
        nome_before = None

        if after is not None:
            after_obj = self.get(after)
            if len(after_obj) > 0:
                codigo_after = after_obj[0].codigo
                nome_after = after_obj[0].nome
        elif before is not None:
            before_obj = self.get(before)
            if len(before_obj) > 0:
                codigo_before = before_obj[0].codigo
                nome_before = before_obj[0].nome

        # Order by default
        order_by = """
        order by
            codigo, nome, id
        """
        desc = False

        # Organizando o where
        where = ''
        if after is not None:
            where = f"""
            where
                codigo > :codigo_after
                or (codigo = :codigo_after and nome > :nome_after)
                or (codigo = :codigo_after and nome = :nome_after and id > :after)
            """
        elif before is not None:
            where = f"""
            where
                codigo < :codigo_before
                or (codigo = :codigo_before and nome < :nome_before)
                or (codigo = :codigo_before and nome = :nome_before and id <= :before)
            """
            order_by = """
            order by
                codigo desc, nome desc, id desc
            """
            desc = True

        # Montando a query em si
        query = f"""
        select
            id, codigo, nome, documento, created_at
        from
            teste.cliente
        {where}
        {order_by}
        limit {limit}
        """

        resp = self._db.execute_query_to_model(
            query,
            Cliente,
            codigo_after=codigo_after,
            nome_after=nome_after,
            codigo_before=codigo_before,
            nome_before=nome_before,
            after=after,
            before=before
        )

        if desc:
            resp.reverse()

        return resp

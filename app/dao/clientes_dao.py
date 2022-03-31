import uuid

from app.settings import log_time
from app.entity.cliente import Cliente

from nsj_gcf_utils.db_adapter2 import DBAdapter2
from nsj_gcf_utils.exception import NotFoundException
from typing import List


class ClientesDAO:
    _db: DBAdapter2

    def __init__(self, db: DBAdapter2 = None):
        self._db = db

    def get(self, id: uuid.UUID) -> Cliente:
        """
        Recupera um cliente por meio de seu ID.
        """

        sql = """
        select
            id, codigo, nome, documento, created_at
        from
            teste.cliente
        where
            id = :id
        """

        resp = self._db.execute_query_to_model(sql, Cliente, id=id)

        if len(resp) <= 0:
            raise NotFoundException(f'Cliente com id {id} não encontrado.')

        return resp[0]

    # @log_time('Listando clientes do banco de dados.')
    # TODO Corrigir implementação do decorator
    def list(
        self,
        after: uuid.UUID,
        before: uuid.UUID,
        limit: int
    ) -> List[Cliente]:
        """
        Recupera uma lista paginada de clientes.
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
        sql = f"""
        select
            id, codigo, nome, documento, created_at
        from
            teste.cliente
        {where}
        {order_by}
        limit {limit}
        """

        resp = self._db.execute_query_to_model(
            sql,
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

    def insert(self, cliente: Cliente):
        """
        Insere um cliente no banco de dados
        """

        sql = """
        insert into teste.cliente
        (id, nome, documento)
        values
        (:id, :nome, :documento)
        returning codigo, created_at
        """

        new_id = (cliente.id if cliente.id is not None else uuid.uuid4())
        rowcount, returning = self._db.execute(
            sql,
            id=new_id,
            nome=cliente.nome,
            documento=cliente.documento,
        )

        if rowcount <= 0:
            raise Exception(
                'Erro inserindo Cliente no banco de dados')

        cliente.id = new_id
        cliente.codigo = returning[0]['codigo']
        cliente.created_at = returning[0]['created_at']

        return cliente

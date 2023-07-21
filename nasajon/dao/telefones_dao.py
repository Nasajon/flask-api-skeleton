import uuid

from nasajon.settings import log_time
from nasajon.entity.telefone import Telefone

from nsj_gcf_utils.db_adapter2 import DBAdapter2
from nsj_gcf_utils.exception import NotFoundException
from typing import List


class TelefonesDAO:
    _db: DBAdapter2

    def __init__(self, db: DBAdapter2 = None):
        self._db = db

    def begin(self):
        """
        Inicia uma transação no banco de dados
        """
        self._db.begin()

    def commit(self):
        """
        Faz commit na transação corrente no banco de dados (se houver uma).

        Não dá erro, se não houver uma transação.
        """
        self._db.commit()

    def rollback(self):
        """
        Faz rollback da transação corrente no banco de dados (se houver uma).

        Não dá erro, se não houver uma transação.
        """
        self._db.rollback()

    def in_transaction(self) -> bool:
        """
        Verifica se há uma transação em aberto no banco de dados
        (na verdade, verifica se há no DBAdapter, e não no BD em si).
        """
        return self._db.in_transaction()

    def get(self, id: uuid.UUID) -> Telefone:
        """
        Recupera um telefone por meio de seu ID.
        """

        sql = """
        select
            id, cliente, descricao, principal, tipo, ddd, numero, ramal, created_at
        from
            teste.telefone
        where
            id = :id
        """

        resp = self._db.execute_query_to_model(sql, Telefone, id=id)

        if len(resp) <= 0:
            raise NotFoundException(f'Telefone com id {id} não encontrado.')

        return resp[0]

    def list(
        self,
        after: uuid.UUID,
        before: uuid.UUID,
        limit: int
    ) -> List[Telefone]:
        """
        Recupera uma lista paginada de telefones.
        """

        # Recuperando dados para paginacao
        ddd_after = None
        numero_after = None
        ddd_before = None
        numero_before = None

        if after is not None:
            after_obj = self.get(after)
            if len(after_obj) > 0:
                ddd_after = after_obj[0].ddd
                numero_after = after_obj[0].numero
        elif before is not None:
            before_obj = self.get(before)
            if len(before_obj) > 0:
                ddd_before = before_obj[0].ddd
                numero_before = before_obj[0].numero

        # Order by default
        order_by = """
        order by
            ddd, numero, id
        """
        desc = False

        # Organizando o where
        where = ''
        if after is not None:
            where = """
            where
                ddd > :ddd_after
                or (ddd = :ddd_after and nome > :numero_after)
                or (ddd = :ddd_after and nome = :numero_after and id > :after)
            """
        elif before is not None:
            where = """
            where
                ddd < :ddd_before
                or (ddd = :ddd_before and nome < :numero_before)
                or (ddd = :ddd_before and nome = :numero_before and id <= :before)
            """
            order_by = """
            order by
                ddd desc, numero desc, id desc
            """
            desc = True

        # Montando a query em si
        sql = f"""
        select
            id, cliente, descricao, principal, tipo, ddd, numero, ramal, created_at
        from
            teste.telefone
        {where}
        {order_by}
        limit {limit}
        """

        resp = self._db.execute_query_to_model(
            sql,
            Telefone,
            ddd_after=ddd_after,
            numero_after=numero_after,
            ddd_before=ddd_before,
            numero_before=numero_before,
            after=after,
            before=before
        )

        if desc:
            resp.reverse()

        return resp

    def list_by_cliente(
        self,
        cliente: uuid.UUID
    ) -> List[Telefone]:
        """
        Recupera uma lista de telefones.
        """

        # Order by default
        order_by = """
        order by
            ddd, numero, id
        """

        # Organizando o where
        where = 'WHERE cliente = :cliente'

        # Montando a query em si
        sql = f"""
        select
            id, cliente, descricao, principal, tipo, ddd, numero, ramal, created_at
        from
            teste.telefone
        {where}
        {order_by}
        """

        resp = self._db.execute_query_to_model(
            sql,
            Telefone,
            cliente=cliente,
        )

        return resp

    def insert(self, telefone: Telefone):
        """
        Insere uma pessoa no banco de dados
        """

        sql = """
        insert into teste.telefone
        (id, cliente, descricao, principal, tipo, ddd, numero, ramal)
        values
        (:id, :cliente, :descricao, :principal, :tipo, :ddd, :numero, :ramal)
        returning numero, created_at
        """

        new_id = (telefone.id if telefone.id is not None else uuid.uuid4())
        rowcount, returning = self._db.execute(
            sql,
            id=new_id,
            cliente=telefone.cliente,
            descricao=telefone.descricao,
            principal=telefone.principal,
            tipo=telefone.tipo,
            ddd=telefone.ddd,
            numero=telefone.numero,
            ramal=telefone.ramal
        )

        if rowcount <= 0:
            raise Exception(
                'Erro inserindo Pessoa no banco de dados')

        telefone.id = new_id
        telefone.created_at = returning[0]['created_at']

        return telefone

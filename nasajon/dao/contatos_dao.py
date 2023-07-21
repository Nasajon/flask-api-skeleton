import uuid

from nasajon.settings import log_time
from nasajon.entity.contato import Contato

from nsj_gcf_utils.db_adapter2 import DBAdapter2
from nsj_gcf_utils.exception import NotFoundException
from typing import List


class ContatosDAO:
    _db: DBAdapter2

    def __init__(self, db: DBAdapter2 = None):
        self._db = db

    def get(self, id: uuid.UUID) -> Contato:
        """
        Recupera um Contato por meio de seu ID.
        """

        sql = """
        select
            id, pessoa, descricao, principal, tipo, ddd, numero, ramal, created_at
        from
            faturamento.contato
        where
            id = :id
        """

        resp = self._db.execute_query_to_model(sql, Contato, id=id)

        if len(resp) <= 0:
            raise NotFoundException(f'Contato com id {id} não encontrado.')

        return resp[0]

    def list(
        self,
        after: uuid.UUID,
        before: uuid.UUID,
        limit: int
    ) -> List[Contato]:
        """
        Recupera uma lista paginada de contatos.
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
            id, pessoa, descricao, principal, tipo, ddd, numero, ramal, created_at
        from
            faturamento.contato
        {where}
        {order_by}
        limit {limit}
        """

        resp = self._db.execute_query_to_model(
            sql,
            Contato,
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

    def insert(self, contato: Contato):
        """
        Insere um contato no banco de dados
        """

        sql = """
        insert into faturamento.contato
        (id, pessoa, descricao, principal, tipo, ddd, numero, ramal)
        values
        (:id, :cliente, :descricao, :principal, :tipo, :ddd, :numero, :ramal)
        returning numero, created_at
        """

        new_id = (contato.id if contato.id is not None else uuid.uuid4())
        rowcount, returning = self._db.execute(
            sql,
            id=new_id,
            cliente=contato.cliente,
            descricao=contato.descricao,
            principal=contato.principal,
            tipo=contato.tipo,
            ddd=contato.ddd,
            numero=contato.numero,
            ramal=contato.ramal
        )

        if rowcount <= 0:
            raise Exception(
                'Erro inserindo Contato no banco de dados')

        contato.id = new_id
        contato.created_at = returning[0]['created_at']

        return contato

    def update(self, contato: Contato):
        """
        Atualiza um contato no banco de dados
        """

        sql = """
        UPDATE
            faturamento.contato
        SET
            pessoa=:cliente,
            descricao=:descricao,
            principal=:principal,
            tipo=:tipo,
            ddd=:ddd,
            numero=:numero,
            ramal=:ramal
        WHERE
            id=:id
        """

        rowcount, returning = self._db.execute(
            sql,
            id=contato.id,
            cliente=contato.cliente,
            descricao=contato.descricao,
            principal=contato.principal,
            tipo=contato.tipo,
            ddd=contato.ddd,
            numero=contato.numero,
            ramal=contato.ramal
        )

        if rowcount <= 0:
            raise Exception(
                'Erro atualizando Contato no banco de dados')

        return contato

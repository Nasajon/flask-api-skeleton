import sys
from sqlalchemy.engine.base import Connection

class Main:

    _db_connection: Connection

    def run(self, nome : str):

        campos = self._campos(nome)

        for campo in campos:
            pass


    def __enter__(self):
        import os
        import sqlalchemy

        DATABASE_HOST = os.environ['DATABASE_HOST']
        DATABASE_PASS = os.environ['DATABASE_PASS']
        DATABASE_PORT = os.environ['DATABASE_PORT']
        DATABASE_NAME = os.environ['DATABASE_NAME']
        DATABASE_USER = os.environ['DATABASE_USER']

        database_conn_url = f'postgresql+pg8000://{DATABASE_USER}:{DATABASE_PASS}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}'

        # Creating database connection pool
        self._db_connection = sqlalchemy.create_engine(
        database_conn_url,
        pool_size=5,
        max_overflow=2,
        pool_timeout=30,
        pool_recycle=1800
    )

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._db_connection.close()


    def _db_adapter(self):
        from nsj_gcf_utils.db_adapter2 import DBAdapter2
        return DBAdapter2(self._db_connection)

    def _campos(self, nome : str):
        _db = self._db_adapter()

        sql = """
            SELECT column_name,data_type
            FROM information_schema.columns
            WHERE concat(table_schema,'.',table_name) = :nome
            ORDER BY ordinal_position
        """

        rowcount, returning = _db.execute(sql,nome=nome)

        if rowcount <= 0:
            raise Exception(
                'Metadados inexistentes para "{nome}"')

        return returning[0]

    def gerar_arquivo(nome_arquivo, conteudo):
        try:
            with open(nome_arquivo, 'w') as arquivo:
                arquivo.write(conteudo)
            print(f"Arquivo '{nome_arquivo}' gerado com sucesso!")
        except Exception as e:
            print(f"Ocorreu um erro ao gerar o arquivo: {e}")


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print(
            """Faltando parâmetros do nome para geração. Modo de uso:
    python -m main <nome>

    Parêmetros adicionais serão ignorados."""
        )
        sys.exit(1)

    Main().run(sys.argv[1])

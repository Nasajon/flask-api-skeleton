import uuid
import requests

from nsj_queue_lib.worker_pub_sub_base import (
    WorkerPubSubBase,
    Subscriber
)

from nsj_queue_lib.settings import logger

from nasajon.client.pessoa_client import PessoaClient

from nasajon.injector_factory import InjectorFactory

from nasajon.settings import INDEX_DB_URL, INDEX_PESSOAS_LIST

class WorkerSincroniaClientes(WorkerPubSubBase):

    _pessoa_client: PessoaClient

    def __init__(self):
        super().__init__()
        self._pessoa_client = PessoaClient()

    def _transforma_cliente_para_indice(self, cliente, telefones):

        _resumo_cliente = f"{cliente.codigo} {cliente.nome} {cliente.documento}"

        _resumo_telefones = ""
        for tel in telefones:
            _resumo_telefones += f" {tel.descricao} {'principal' if tel.principal else ''} {tel.tipo} (0{tel.ddd}) {tel.numero}"

        _dados = { "resumo" : f"{_resumo_cliente},{_resumo_telefones}" }

        return _dados

    @Subscriber("api_faturamento_pessoas")
    def sinc_cliente(
        self,
        payload: dict[str, any],
        subscription: dict[str, any],
        tarefa: dict[str, any],
        bd_conn):

        logger.info(f"Iniciando o envio para a api  de clientes da tarefa com  ID: {tarefa['id']}")

        _cliente_id = payload['publication']

        with InjectorFactory() as factory:
            cliente = factory.clientes_service().get(_cliente_id)

        pessoa = self._pessoa_client.recupera_pessoa(cliente.id)
        if not pessoa is None:
            self._pessoa_client.atualiza_pessoa(cliente)
        else:
            self._pessoa_client.cria_pessoa(cliente)

        # Salva dados relacionados
        with InjectorFactory() as factory:
            telefones = factory.telefones_service().list_by_cliente(_cliente_id)

        for telefone in telefones:
            contato = self._pessoa_client.recupera_contato(telefone.id)
            if not contato is None:
                self._pessoa_client.atualiza_contato(telefone)
            else:
                self._pessoa_client.cria_contato(telefone)

        logger.info("Envio para a api para api efetuado sucesso")

    @Subscriber("api_indice_pessoas")
    def sinc_indice(
        self,
        payload: dict[str, any],
        subscription: dict[str, any],
        tarefa: dict[str, any],
        bd_conn):

        logger.info(f"Iniciando envio dos dados para o índice da tarefa com  ID: {tarefa['id']}")

        _cliente_id = payload['publication']

        with InjectorFactory() as factory:
            cliente = factory.clientes_service().get(_cliente_id)
            telefones = factory.telefones_service().list_by_cliente(_cliente_id)

        response = requests.put(
            f"{INDEX_DB_URL}/{INDEX_PESSOAS_LIST}/_doc/{_cliente_id}",
            json=self._transforma_cliente_para_indice(cliente, telefones),
            timeout=5
        )

        if not response.status_code in [200, 201]:
            raise Exception(f"Erro no request para índice: {response.status_code} {response.text}.")

        logger.info("Envio para o índice Efetuado sucesso")


    def execute(self, payload: str, tarefa: dict[str, any], bd_conn) -> str:
        try:
            print("Worker Sincronia Clientes, iniciando tarefas...")
            super().execute(payload, tarefa, bd_conn)
        finally:
            print("Worker Sincronia Clientes, finalizando...")


if __name__ == "__main__":
    WorkerSincroniaClientes().run()

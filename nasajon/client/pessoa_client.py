import uuid
import requests

from nsj_gcf_utils.json_util import convert_to_dumps

from nasajon.dto.pessoa_post import PessoaPostDTO
from nasajon.dto.contato_post import ContatoPostDTO

from nasajon.settings import API_PESSOAS_URL, API_CONTATOS_URL

class PessoaClient:

    _api_timeout = 5
    _endpoint_pessoas = API_PESSOAS_URL
    _endpoint_contatos = API_CONTATOS_URL

    def cria_pessoa(self, pessoa):

        response = requests.post(
            self._endpoint_pessoas,
            json=convert_to_dumps(pessoa),
            timeout=self._api_timeout
        )

        if not response.status_code in [200, 201]:
            raise Exception(
                f"Erro no request para Api de Pessoas: {response.status_code} {response.text}."
            )

    def atualiza_pessoa(self, pessoa):
        response = requests.put(
            self._endpoint_pessoas,
            json=convert_to_dumps(pessoa),
            timeout=self._api_timeout
        )

        if not response.status_code in [200, 201]:
            raise Exception(
                f"Erro no request para Api de Pessoas: {response.status_code} {response.text}."
            )

    def cria_contato(self, contato):
        response = requests.post(
            self._endpoint_contatos,
            json=convert_to_dumps(contato),
            timeout=self._api_timeout
        )

        if not response.status_code in [200, 201]:
            raise Exception(
                f"Erro no request para Api de contatos: {response.status_code} {response.text}."
            )

    def atualiza_contato(self, contato):
        response = requests.put(
            self._endpoint_contatos,
            json=convert_to_dumps(contato),
            timeout=self._api_timeout
        )

        if not response.status_code in [200, 201]:
            raise Exception(
                f"Erro no request para Api de contatos: {response.status_code} {response.text}."
            )

    def recupera_pessoa(self, pessoa: uuid.UUID):
        response = requests.get(
            f"{self._endpoint_pessoas}/{pessoa}",
            timeout=self._api_timeout
        )

        if response.status_code == 200:
            return PessoaPostDTO(**response.json())
        elif response.status_code == 404:
            return None
        else:
            raise Exception(
                f"Erro no request para Api de pessoas: {response.status_code} {response.text}."
            )

    def recupera_contato(self, contato: uuid.UUID):
        response = requests.get(
            f"{self._endpoint_contatos}/{contato}",
            timeout=self._api_timeout
        )

        if response.status_code == 200:
            return ContatoPostDTO(**response.json())
        elif response.status_code == 404:
            return None
        else:
            raise Exception(
                f"Erro no request para Api de contatos: {response.status_code} {response.text}."
            )

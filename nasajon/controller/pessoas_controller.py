from flask import request

from elasticsearch import Elasticsearch

from pydantic import ValidationError

from nsj_gcf_utils.exception import NotFoundException
from nsj_gcf_utils.json_util import convert_to_dumps, json_dumps, json_loads
from nsj_gcf_utils.pagination_util import page_body, PaginationException
from nsj_gcf_utils.rest_error_util import format_json_error

from nasajon.controller.controller_util import DEFAULT_RESP_HEADERS
from nasajon.dto.pessoa_post import PessoaPostDTO
from nasajon.injector_factory import InjectorFactory
from nasajon.settings import APP_NAME, DEFAULT_PAGE_SIZE, application, MOPE_CODE

from nasajon.settings import INDEX_DB_URL, INDEX_PESSOAS_LIST

GET_ROUTE = f'/{APP_NAME}/{MOPE_CODE}/pessoas/<id>'
LIST_POST_ROUTE = f'/{APP_NAME}/{MOPE_CODE}/pessoas'
LIST_INDEX_ROUTE = f'/{APP_NAME}/{MOPE_CODE}/indice/pessoas'

def result_from(data = None):

    return {
        "next": None,
        "prev": None,
        "result": data
    }

@application.route(LIST_INDEX_ROUTE, methods=['GET'])
#@require_oauth()
def get_pessoas_indice():

    args = request.args

    # Conectar ao Elasticsearch
    cliente_elastic = Elasticsearch(f"{INDEX_DB_URL}")

    # Termo de pesquisa aproximada
    termo_pesquisa_aproximada = args.get("query","")

    limit = int(args.get("limit", 20))
    offset = int(args.get("offset", 0))

    consulta = None
    if termo_pesquisa_aproximada is not None and termo_pesquisa_aproximada!="":
        # Consulta
        consulta = {
            "match": {
                "resumo": {
                    "query": f"{termo_pesquisa_aproximada}",
                    "fuzziness": 1
                }
            }
        }
    else:
        consulta = {
            "match_all": {}
        }

    # Realizar a busca no índice "INDEX_PESSOAS_LIST"
    resultado = cliente_elastic.search(index=INDEX_PESSOAS_LIST, query=consulta, size=limit, from_=offset)

    # Processar o resultado da busca
    dados=[]
    print(resultado["hits"]["hits"])
    for hit in resultado["hits"]["hits"]:
        _doc = hit["_source"]
        _doc['id'] = hit["_id"]
        dados.append(_doc)

    return (json_dumps(result_from(dados)), 200, {**DEFAULT_RESP_HEADERS})

@application.route(LIST_POST_ROUTE, methods=['GET'])
#@require_oauth()
def get_pessoas():
    with InjectorFactory() as factory:
        try:
            # Recuperando os parâmetros básicos
            base_url = request.base_url
            args = request.args
            limit = int(args.get('limit', DEFAULT_PAGE_SIZE))
            current_after = args.get('after') or args.get('offset')
            current_before = args.get('before')

            # Construindo os objetos
            service = factory.pessoas_service()
            data = service.list(current_after, current_before, limit)
            dict_data = convert_to_dumps(data)

            page = page_body(
                base_url=base_url,
                limit=limit,
                current_after=current_after,
                current_before=current_before,
                result=dict_data,
                id_field='id'
            )

            return (json_dumps(page), 200, {**DEFAULT_RESP_HEADERS})
        except PaginationException as e:
            return (format_json_error(e), 400, {**DEFAULT_RESP_HEADERS})
        except Exception as e:
            return (format_json_error(f'Erro desconhecido: {e}'), 500, {**DEFAULT_RESP_HEADERS})


@application.route(GET_ROUTE, methods=['GET'])
#@require_oauth()
def get_pessoa_by_id(id: str):
    with InjectorFactory() as factory:
        try:
            service = factory.pessoas_service()
            data = service.get(id)

            return (json_dumps(data), 200, RESPONSE_HEADERS)
        except NotFoundException as e:
            return (format_json_error(f'{e}'), 404, RESPONSE_HEADERS)
        except Exception as e:
            return (format_json_error(f'Erro desconhecido: {e}'), 500, {**DEFAULT_RESP_HEADERS})


@application.route(LIST_POST_ROUTE, methods=['POST'])
#@require_oauth()
def post_pessoa():
    with InjectorFactory() as factory:
        try:
            data = request.get_data(as_text=True)
            data = json_loads(data)
            data = PessoaPostDTO(**data)

            service = factory.pessoas_service()
            data_resp = service.insert(data)

            return (json_dumps(data_resp), 200, RESPONSE_HEADERS)
        except ValidationError as e:
            return (format_json_error(e), 400, RESPONSE_HEADERS)
        except Exception as e:
            return (format_json_error(f'Erro desconhecido: {e}'), 500, {**DEFAULT_RESP_HEADERS})


@application.route(LIST_POST_ROUTE, methods=['PUT'])
#@require_oauth()
def put_pessoa():
    with InjectorFactory() as factory:
        try:
            data = request.get_data(as_text=True)
            data = json_loads(data)
            data = PessoaPostDTO(**data)

            service = factory.pessoas_service()
            data_resp = service.update(data)

            return (json_dumps(data_resp), 200, RESPONSE_HEADERS)
        except ValidationError as e:
            return (format_json_error(e), 400, RESPONSE_HEADERS)
        except Exception as e:
            return (format_json_error(f'Erro desconhecido: {e}'), 500, {**DEFAULT_RESP_HEADERS})

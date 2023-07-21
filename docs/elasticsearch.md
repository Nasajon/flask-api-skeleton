
# Visão geral

O Elasticsearch é um mecanismo de busca e análise de dados distribuído. Usado como um índice de dados para este exemplo. Sua escolha foi baseada no fato de além de ser amplamente utilizado no mercado, possui suporte a funcionalidade de Full Text Search além de ser extremamente veloz e escalável.

A Principal premissa neste projeto é que os índices (tal como uma tabela de banco relacional) possam atender a Api's de busca e filtro (List apis) e até mesmo um cache de leitura de dados bem superior a velocidade do SQL.

## Utilização neste projeto

Referenciando o documento que trata da comunicação assíncrona, uma vez indexado um dado se torna disponível para consulta.

As consultas podem ser efetuadas tanto na api de pessoas quanto no Kibana, que é uma um front-end de administração, dashboards e consultas para o Elastic.

No projeto de exemplo, as dados da api de clientes são indexados como `faturamento.pessoas`, cuja configuração do índice pode ser consultada no arquivo [pessoas_mapping.json](../database/pessoas_mapping.json).

## Iniciando um índice

O primeiro passo para o uso da ferramenta é enviar dados a um índice e efetuar consultas. É possível começar a utilizar um índice sem criar seu mapeamento, que é uma espécie de DDL do índice, o que é chamado de [mapeamento dinâmico](https://www.elastic.co/guide/en/elasticsearch/reference/current/dynamic-mapping.html). Embora muito útil, é por vezes desencorajado na documentação, pois mesmo que se possa fazer uso de configuração global previamente estabelecida e/ou templates existe uma tendência para a generalização,

Dado que algumas informações sobre o índice são construídas no momento que o dado é indexado, pode ser necessário [reindexar](#reindexação) estes dados para compatibilizar os dados já adicionados. A depender do cenário esta operação poderá ser muito custosa em termos computacionais ou envolver criar um novo índice e mover os dados.

### indexando dados sem mapeamento

Para criar um índice sem mapear basta adicionar dados ao mesmo.

No exemplo abaixo estamos criando um índice chamado ```teste_sem_map``` cujo ID será ```1``` e com campo ```valor = meu primeiro documento```


```http
POST http://localhost:9200/teste_sem_map/_doc/1
content-type: application/json

{
  "valor": "meu primeiro documento"
}
```

resposta:

```http
HTTP/1.1 200 OK
X-elastic-product: Elasticsearch
content-type: application/json
content-encoding: gzip
content-length: 132

{
  "_index": "teste_sem_map",
  "_id": "1",
  "_version": 3,
  "result": "updated",
  "_shards": {
    "total": 2,
    "successful": 1,
    "failed": 0
  },
  "_seq_no": 2,
  "_primary_term": 1
}
```

Após a criação já pode-se [buscar o documento](#efetua-a-busca-em-um-índice) ou efetuar um GET pelo ID do mesmo.

### indexando dados com mapeamento

Mapeamentos permitem que se diga explicitamente os campos que se deseja utilizar e seus tipos, bem como regras que possibilitam restringir ou não campo extras, remoção de stop words, stemming, tokenização, dados vetorizados, geospaciais entre outros conceitos.

Para iniciar nosso índice do exemplo, basta fazer esta chamada para api:

```http
curl -XPUT 'http://localhost:9200/faturamento.pessoa' -d @../database/pessoas_mapping.json --header "Content-Type: application/json"
```

Esse comando cria o índice no respeitando as regras existentes no arquivo [pessoas_mapping.json](../database/pessoas_mapping.json)

Para efeito de teste pode-se usar um [Dump](../database/dump.json) de exemplo através da [api de bulk](#cargas-massivas-de-dados), abaixo:

```http
curl -XPUT 'http://localhost:9200/faturamento.pessoa/_bulk' -d @../database/dump.json --header "Content-Type: application/json"
```

Após estes passos o índice já estará criado com dados de exemplo para consulta:

```http
GET http://localhost:9200/faturamento.pessoa/_search
```

### Consulta por Api

 Poderá ser usada a seguinte chamada para consultar dados já indexados na api de pessoas através da query string `query`.

```http
GET http://localhost/api/1234/indice/pessoas?query=valor_da_consulta
Accept: application/json
```

### Consulta pelo Kibana

Para consultar dados no Kibana acesse a página do console de dev tools (http://localhost:5601/app/dev_tools#/console) e utiliza o comando abaixo:


```json
GET faturamento.pessoa/_search
{
  "query": {
    "match": {
      "resumo": {
        "query": "valor_da_consulta"
      }
    }
  },"explain": false
}
```

O exemplo considera a consulta no índice `faturamento.pessoa` através da [Search Api](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-search.html) utilizando o padrão de consulta [Query DSL](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html) do Elastic.


## Referência de comandos:

Aqui uma lista dos comandos básicos mais utilizados, o que não substitui a documentação oficial.

> Os comandos exemplificados abaixo estão no padrão aceito pelo [console do Kibana](#consulta-pelo-kibana), mas poderão ser executados via Api Rest.

Dado um índice com nome **meu_indice**:

### Cria/Atualiza dados no índice

Cria um documento com o id `060fc71e-b69a-4e9a-83ef-edc784cb8847`.

```json
PUT meu_indice/_doc/060fc71e-b69a-4e9a-83ef-edc784cb8847
{
  "nome": "Fulano de Tal",
  "codigo": 4,
  "documento": "00000000000",
  "created_at": "2023-07-19T12:01:41.150928"
}
```

A criação e atualização de dados seguem o mesmo princípio, onde na atualização o campo interno "version" é incrementado.

### Efetua a busca em um índice

As consultas do ElasticSearch são extremamente poderosas, para demais informações consultar a documentação oficial.

No exemplo abaixo o equivalente a um ```SELECT SQL```


```json
GET meu_indice/_search
{
  "query": {
    "match_all": {}
  },
  "explain":true
}
```

O parâmetro explain, é opcional e é usado para retornar os critérios de seleção que foram usados para montar o retorno.

### Ver as configurações de mapeamento

Retorna o mapeamento do indice, que é um json equivalente a um DDL de uma tabela.

Aqui pode ser conferido um exemplo de mapeamento utilizado no exemplo.

```json
GET meu_indice/_mapping
```

### Ver as configurações do indice

Retorna as configurações do indice, tais como número, de fragmentos, configurações de limpeza,transformação e indexação de dados etc.

```json
GET meu_indice/_settings
```

### Informações gerais sobre  o indice

Retorna  as Configurações e Mapeamento do índice.

```json
GET meu_indice
```

### Dropa um índice

Similar a um ```DROP database```.

```json
DELETE meu_indice
```

### Analisa o comportamento do índice quanto a Tokenização

Esse comando permite que se simule como uma busca irá ser processada para um determinado contexto. Muito útil para simular como uma determinada configuração se comporta sem necessariamente implementá-la no índice.

> Exemplo 01 - Simulando em um índice

Neste exemplo está sendo analisando a busca para um índice, o que significa que o texto de busca será sujeito as regras de mapeamento deste, embora seja possível adicionar configurações extras para efeito de simulação.

```json
GET meu_indice/_analyze
{
  "field": "campo_a_ser_analizado",
  "text": "como você me tokeniza: carros-voadores"
}
```

> Exemplo 02 - Simulando de forma global

Neste exemplo a simulação é feita sem necessariamente apontar para um índice, de forma que podemos passar uma configuração que se deseja testar.

No exemplo, estamos simulando a análise de texto usando o filtro [Edge N-Gramas](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-edgengram-tokenfilter.html)

```json
GET _analyze
{
  "tokenizer": "standard",
  "filter": [{
          "type": "edge_ngram",
          "min_gram": 5,
          "max_gram": 10
        }],
  "text": "como você me tokeniza: carros-voadores"
}
```

### Executar querys em SQL

O Elasticsearch aceita querys em um formato SQL, com suporte a maioria dos comandos ANSI.

```json
POST _sql?format=txt
{
  "query": """
  SELECT * FROM "meu_indice"
  """
}
```

### Coverte uma query SQL para DSL

É possível converter um comando no formato SQL para o formato de [DSL nativo](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html).

```json
POST _sql/translate
{
  "query": """SELECT * FROM "meu_indice" """
}
```

### Reindexação



Cria um novo índice Copiando os dados originais.

```json
POST _reindex
{
  "source": { "index": "meu_indice"},
  "dest":  { "index" : "meu_indice_tmp"}
}
```

Apaga indice antigo

```json
DELETE meu_indice
```

Recria com novo mapeamento

```json
PUT meu_indice
{
  ...//Json de configuração do Mapeamento
}
```

Retorna os dados de volta

```json
POST _reindex
{
  "source": { "index": "meu_indice_tmp"},
  "dest":  { "index" : "meu_indice"}
}
```

## Cargas massivas de dados

O elastic search permite a carga massiva de dados através do Bulk API.

Basicamente precisa-se para cada linha que será inserida replicar as linhas dedados como no exemplo:

```json
PUT meu_indice/_bulk // Chamando a api de bulk para o índice "meu_indice"
{ "index": { "_id": "123456" }} // Id do regitro (obrigatório)
{ "resumo" : "lorem ipsum dolor..." } // Dados que Serão indexados
```

## Informaçẽos gerais
Para consumo de informações sobre o índice e configurações recomentada-se o uso da _cat api e derivações

```
GET _cat
```
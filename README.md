# flask-api-skeleton

## Introdução
Projeto esqueleto de exemplo, para programação de APIs por meio do "framework web" Python: __Flask__ (*).

Esse projeto deve ser usado como base para APIs maiores, isto é, APIs com características como: diversos endpoints, manipulação de entidades em banco, validação de dados de entrada e controle de autenticação/autorização OAuth.

Projetos menores, do tipo micro serviços em formato REST não carecem, necessariamente, de todo ferramental aqui aplicado, e portanto podem ser ainda mais simplificados (planeja-se providenciar, no futuro, outro skeleton para microserviços deste tipo).

Por fim, vale destacar que o próprio skeleton já foi desenvolvido como um API de exemplo "completa", capaz de gerir um cadastro fictício de clientes, e portanto contém os seguintes endpoints:

* `GET /1234/clientes` - Listagem páginada de clientes
* `GET /1234/clientes/{id}` - Retrieve de um único cliente
* `POST /1234/clientes` - Gravação de um novo cliente
* `GET /token-info` - Retorna um JSON contendo as informações básicas contidas no Acess Tokeb recebido.

_(*) Cabe fazer a ressalva de que o Flask é veículado na web como framework web, uma vez que implemente o necessário para efetiva comunicação HTTP, além de contar com diversas bibliotecas adicionais, capazes de prover funcionalidades adicionais comuns aos frameworks web. Mesmo assim, diferente de outros frameworks, o Flask não impõe padrões rígidos ao programador, e é distribuído de modo extremamente minimalista (carecendo da instalação de muitos complementos). Logo, pode-se também dizer, com certa razoabilidade, que o Flask se apresenta mais como uma biblioteca web, do que como um framework de fato (a não ser pelo fato de implementar o ciclo básico da comunicação HTTP, deixando para o programador tarefas mais alto nível). E, essa resslava é importante para justificar a liberdade de organização do repositório (conforme apresentado a seguir)._
## Ambiente de Desenvolvimento

Por hora, o ambiente de desenvovimento do projeto ainda não conta com imagem docker para execução do Flask (o que se deseja providenciar um breve).

Assim, será apresentada a configuração de um ambiente local (usado docker apenas para o BD).

### Passos para configuração

1. Clone o projeto:

> git clone git@github.com:Nasajon/flask-api-skeleton.git

2. Crie uma cópia local do arquivo `.env.dist`, renomeando a mesma para `.env`.
3. Ajuste as variáveis de ambiente sem conteúdo, no arquivo `.env.fist` (consulte a seção sobre "Variáveis de ambiente" mais à frente).
4. Crie um ambiente virtual python3:
> python3 -m venv .venv
5. Inicie o ambiente virtual.
> ./.venv/source/bin/activate
6. Instale as dependências do projeto.
> pip install -r requirements.txt
7. Inicie o BD pelo docker 
> docker-copmose up -d postgres
8. Inicie o servidor de desenvolvimento do flask:
> make run_local

### Testes manuais

Para testar a disponibilidade dos serviços (após iniciar o configurar e iniciar o ambiente), foram preparadas alguns exemplos de chamada aos enpoints, por meio dos arquivos `.rest`, contidos no diretório `rest` deste repositório.

Para usar estes exemplos por meio do VSCode, deve-se instalar a extensão _Rest Client_  (implementada por _Huachao Mao_).

Como os endpoints de exemplo requerem autenticação, é preciso portanto usar em primeiro lugar o arquivo `rest/autenticacao.rest`, obtendo, por meio deste, um _access_token_ a ser inserido no header `Authorization` dos dmais endpoints (substituindo os asterísticos escritos após o termo `Bearer`).

A saber, a extensão _Rest Client_ cria um link _Send Request_ abaixo dos comentários de cada chamada preparada, e aceita a discriminação dos headers e do corpo em formato texto (muito similiar ao próprio padrão HTTP). Assim, ao clicar em _Send Request_, uma requisição HTTP é enviada para a URL dada (dispensando o uso de outras ferramentas, como o Postman ou Insomnia).

### Variáveis de ambiente

O projeto esqueleto vem definido já depente das seguintes variáveis de ambiente:

#### Variáveis gerais

| Variável          | Obrigatória         | Descrição                                                                                                                                                                            |
| ----------------- | ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| APP_NAME          | Sim                 | Nome da aplicação. Usada para nomear o logger padrão do sistema.                                                                                                                     |
| DEBUG             | Não (padrão: False) | Define se a aplicação será executada em modo debug (por hora, só afeta o nível de log a ser impresso, sendo _Info_ caso _False_, e _Debug_ em caso _True_).                          |
| MOPE_CODE         | Sim                 | Código MOPE coberto pela aplicação (usado nos controllers de rotas, podendo ser adicionado nas rotas de modo hard coded, caso se precise de mais de um código numa mesma aplicação). |
| DEFAULT_PAGE_SIZE | Não (padrão: 20)    | Quantidade máxima de items retonardos numa página de dados                                                                                                                           |

#### Variáveis de banco

| Variável      | Obrigatória | Descrição                                  |
| ------------- | ----------- | ------------------------------------------ |
| DATABASE_HOST | Sim         | IP ou nome do host, para conexão com o BD. |
| DATABASE_PASS | Sim         | Senha para conexão com o BD.               |
| DATABASE_PORT | Sim         | Porta para conexão com o BD.               |
| DATABASE_NAME | Sim         | Nome do BD, para .                         |
| DATABASE_USER | Sim         | Usuário para conexão com o BD.             |

#### Variáveis OAuth

| Variável                      | Obrigatória | Descrição                                                                                                                                                                                                                   |
| ----------------------------- | ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| OAUTH_CLIENT_ID               | Sim         | Client ID para comunicação com o Authentication Server (no padrão OAuth), e validação de cada `acess_token` recebido (por meio do padrão _Token Introspection_.                                                             |
| OAUTH_CLIENT_SECRET           | Sim         | Cliente Secret para validação dos tokens (complementar ao Cliente ID, acima descrito).                                                                                                                                      |
| OAUTH_TOKEN_INTROSPECTION_URL | Sim         | URL para o endpoint de _Token Instrospection_, do Authentication Server ([ver nosso guidelines](https://github.com/Nasajon/Arquitetura/blob/master/Backend/arquitetura-de-APIs/padroes-seguranca.md#token-instrospection)). |

### Estrutura de diretórios

O projeto foi organizado com a seguinte sugestão de padrão (apenas os artefatos mais significativos serão apresentados):

```
- app (diretório raiz do código fonte)
|- controller (implementação das rotas disponibilizadas pelo aplicação)
|- dao (implementação das classes de comunicação com o BD, centralizando as queries SQL)
|- dto (data transfer object: classes de modelo utilizadas para definir os formatos de entrada e saída do sistema)
|- entity (classes modelo espelhando as entidades de acordo com o formato do banco de dados; sendo o único tipo de classe utilizada nos DAOs)
|- service (implementação das regras de negócio, e manipulação dos modelos, contendo inclusive as conversões DTOs <=> Entity)
|- db_poll_config.py (configuração do poll de conexões com o BD)
|- injector_factory.py (controlador de injeção de dependências, que deve crescer manualmente, sendo capaz de instanciar as classes de modo hierárquico, provendo, por meio dos construtores, as dependências necessárias a cada classe)
|- main.py (PONTO DE ENTRADA principal da aplicação; cada novo controller deve ser importado neste arquivo, para que suas rotas de fato existam na aplicaçao em execução)
|- oauht_config.py (implementação da autorização; é deste arquivo que se deve importar o decorator "require_oauth" a ser adicionado em cada método de definição das rotas da aplicação)
|- settings.py (configuração geral da aplicação, lendo variáveis de ambiente, instanciando a "aplicação flask", instanciando o logger, etc)
- database (diretório para fins didáticos, contendo um esqueleto de BD utilizado pela imagem docker "postgres")
- rest (diretório com exemplos de chamadas aos endpoints implementados)
- .env.dist (arquivo base para definição das variáveis de ambiente)
- docker-compose.yml (configuração das imagens docker utilizadas no projeto)
- Makefile (arquivo para automação dos scripts uteis em tempo de desenvolvimento)
- README.md (o presente arquivo)
- requirements.txt (arquivo de declaração das dependências do projeto, conforme padrão pip do python)
```

### Banco de dados

A aplicação de exemplo disponibilizada, conta com apenas uma tabela de banco, com a seguinte estrutura:

#### Tabela teste.cliente

| Coluna     | Tipo                  | Valor Default      | Descrição                                                                                            |
| ---------- | --------------------- | ------------------ | ---------------------------------------------------------------------------------------------------- |
| id         | uuid not null         | uuid_generate_v4() | Chave primária da entidade                                                                           |
| codigo     | bigserial not null    | Não definido       | Código numérico único da entidade (chave canditada, e talvez primária, do ponto de vista do usuário) |
| nome       | varchar(100) not null | Não definido       | Nome do cliente                                                                                      |
| documento  | varchar(14) not null  | Não definido       | Documento de identificação d cliente                                                                 |
| created_at | timestamp not null    | now()              | Data e hora de criação do registro                                                                   |


### Imagens docker

Por hora, apenas está sendo utilizada uma imagem docker (ver arquivo `docker-compose.yml`)

* __postgres:11.5__: Imagem para instanciação do BD de exemplo da aplicação.

## Padrões de Projeto Adotados

A aplicação desenvolvida como exmplo, conta com os seguintes recursos (que podem ser usados como design patters, ou apenas como exemplo de possível implementação):

### Entrada e saída de dados

Ficou definido o uso das seguintes ferramentas, para entrada e saída de dados:

#### DTOs

Optou-se por utilizar classes de modelo, para representar o formato dos objetos JSON esperados tanto na entrada, como na saída dos dados.

Esse padrão obriga escrever muitas classes de modelo, e eventualmente mais de uma classe para um único endpoint (como é o caso das rotas POST).

Esse exceço de objetos pode parecer burocrático, mas se encaixa muito bem com o uso da biblioteca `pydantic` (comentada a seguir), e também tem sido com sucesso em conjunto com outros frameworks web famosos (como o Java Spring).

No "pior caso", cada rota pode conter seu próprio DTO de entrada (deinindo o formato específico esperado, bem como as obrigatoriedades de propriedades), e também seu próprio DTO de saída (retornando apenas os dados que interessam a rota em questão).

Caso hajam muitos DTOs, sugere-se organizar o diretório `app/dto` em subdiretórios (por rota).

Por fim, vale destacar que esse formato pode parece difícil de usar, mas, em linguagens como python, a conversão entre DTOs e fáil o suficiente para ser pouco influente (e evita erros imprevistos). Além disso, o utilitário `dto_util` foi providenciado (no pacote _nsj_gcf_utils_, declarado no _requirements.txt_) para estas conversões (conforme pode-se ver na implementação do `ClientesService`).

#### Pydantic

A biblioteca "pydantic" é definida, em seu site, como: _"Data validation and settings management using python type annotations."_

No presente projeto, apenas as características de validação dos dados está sendo aproveitada.

Em resumo, para rotas com entrada de daos JSON (geralmente POST ou PUT), o pydantic é invocado para carga do respectivo DTO com os dados recebidos em JSON.

Assim, quase sem implementação adicional, é possível garantir que os dados recebidos respeitam as definições realizadas no respectivo DTO (contemplando obrigatoriedade de campos, validação de tipos, validações de tamanho, e até permitindo validações implementadas manualmente).

Note no DTO de exemplo `ClientePostDTO`, que, para uso pydantic, os DTOs de entrada devem herdar da classe `BaseModel`, do próprio pydantic.

### Paginação

O projeto de exemplo implementa o padrão de paginação (obrigatório para o ERP 4), e definido no [guidelines da Nasajon](https://github.com/Nasajon/Arquitetura/blob/master/Backend/arquitetura-de-APIs/padroes-resposta.md#requisi%C3%A7%C3%B5es-paginadas).

Para facilitar esta implementação, foi providenciado o utilitário `pagination_util`, no pacote _nsj_gcf_utils_, cujo uso pode ser visto na classe de exemplo `clientes_controller.py`, no método `get_clientes` (também pode-se consultar a documentação do método `page_body` do utilitário referenciado).

### Manipulação de banco

Para manipulação de banco, se utilizou o `SQLAchemy` para controle do pool de conexões, em conjunto com o padrão de projeto DAO (Data Aceess Object).

Além disso, é importante destacar que foi providenciado o utilitáio `DBAdapter2` (do pacote _nsj_gcf_utils_), para execução de queries no BD.

A saber, o `DBAdapter2` é uma evolução do `DBAdpater` (desenolvido no projeto JobMangaer), suportando agora as seguintes features:

* Uso de parâmetros nomeados nas queries (padrão `:id`, para definir um parâmetro de entrada id).
* Envio de parâmetros por meio de _kwargs_, para os método de execução de queries (na versão anterior, os parâmetros eram passados numa lista python).
* Suporte a execução de queries insert ou update, com cláusula sql _returning_.

### Autenticação

Por hora, apenas a autenticação está desenvolvida na aplicação de exemplo (espera-se providenciar em breve a autorização).

Para cumprir o requisito de autenticação, por meio do OAuth (se integrando com o Authentication Server da Nasajon, implementado por meio do KeyCloack), foi utilizada a biblioteca python `Authlib` (muito popular na comunidade python).

Diferentemente de outras aplicações Nasajon, o biblioteca `Authlib` acaba por exigir o termo "Bearer" no token de autenticação, passado para as rotas, por meio do header "Authorization" (o que na verdade é um padrão de mercado, para idetificação do tipo de token passado).

Além disso, em lugar de se validar os tokens recebidos por meio da rota OAuth _UserInfo_, se optou pela utilização da rota OAuth _Token Introspection_, por ser esta mais segura para o _Athentication Server_. Sugere-se [ver nosso guidelines](https://github.com/Nasajon/Arquitetura/blob/master/Backend/arquitetura-de-APIs/padroes-seguranca.md#token-instrospection).

Por fim, para definir que uma rota requer autenticação, é preciso utilizar o decorator `require_oauth` no cabecalho do respectivo método de implementação da rota (sugere-se ver os exemplos contidos no arquivo `app/controller/clientes_controller.py`).
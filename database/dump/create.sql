CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

create schema teste;

create table teste.cliente (
	id uuid not null default uuid_generate_v4(),
	codigo bigserial not null,
	nome varchar(100) not null,
	documento varchar(14) not null,
	created_at timestamp without time zone not null default now(),
	CONSTRAINT teste_cliente_pkey PRIMARY KEY (id)
);

insert into teste.cliente (id, nome, documento) values
('87393f6b-6062-453a-8325-15ce513da1d9' , 'Fulano', '00000000000'),
('d1ef508a-5635-41c4-8dab-4477e69a6273' , 'Ciclano', '11111111111');


create table teste.telefone (
	id uuid not null default uuid_generate_v4(),
	cliente uuid not null,
	descricao varchar(150),
	principal boolean,
	tipo text,-- enum("fixo", "celular", "fax", "voip") not null,
	ddd varchar(2),
	numero varchar(20) not null,
	ramal varchar(12),
	created_at timestamp without time zone not null default now(),
  PRIMARY KEY (id),
  FOREIGN KEY (cliente) REFERENCES teste.cliente (id)
);

insert into teste.telefone (id, cliente, descricao, principal, tipo, ddd, numero, ramal) values
('87393f6b-6062-453a-8325-15ce513da1d1' , '87393f6b-6062-453a-8325-15ce513da1d9', 'Telefone Fulano 01',  true,  'fixo', '21', '11111-1111', null),
('87393f6b-6062-453a-8325-15ce513da1d2' , '87393f6b-6062-453a-8325-15ce513da1d9', 'Telefone Fulano 02',  false, 'fixo', '21', '22222-2222', null),
('87393f6b-6062-453a-8325-15ce513da1d3' , '87393f6b-6062-453a-8325-15ce513da1d9', 'Telefone Fulano 03',  false, 'fixo', '21', '33333-2222', null),
('87393f6b-6062-453a-8325-15ce513da1d4' , '87393f6b-6062-453a-8325-15ce513da1d9', 'Telefone Fulano 04',  false, 'fixo', '21', '44444-2222', null),
('87393f6b-6062-453a-8325-15ce513da1d5' , '87393f6b-6062-453a-8325-15ce513da1d9', 'Telefone Fulano 05',  false, 'fixo', '21', '55555-2222', null),
('d1ef508a-5635-41c4-8dab-4477e69a6271' , 'd1ef508a-5635-41c4-8dab-4477e69a6273', 'Telefone Ciclano 01',  true,  'fixo', '21', '11111-1111', null),
('d1ef508a-5635-41c4-8dab-4477e69a6272' , 'd1ef508a-5635-41c4-8dab-4477e69a6273', 'Telefone Ciclano 02',  false, 'fixo', '21', '22222-2222', null),
('d1ef508a-5635-41c4-8dab-4477e69a6273' , 'd1ef508a-5635-41c4-8dab-4477e69a6273', 'Telefone Ciclano 03',  false, 'fixo', '21', '33333-2222', null),
('d1ef508a-5635-41c4-8dab-4477e69a6274' , 'd1ef508a-5635-41c4-8dab-4477e69a6273', 'Telefone Ciclano 04',  false, 'fixo', '21', '44444-2222', null),
('d1ef508a-5635-41c4-8dab-4477e69a6275' , 'd1ef508a-5635-41c4-8dab-4477e69a6273', 'Telefone Ciclano 05',  false, 'fixo', '21', '55555-2222', null);


-- esquema da base de dados remota
create schema faturamento;

-- tabela de pessoa remota, que irá receber a cópia do cliente
create table faturamento.pessoa (
	id uuid not null default uuid_generate_v4(),
	codigo bigserial not null,
	nome varchar(100) not null,
	documento varchar(14) not null,
	created_at timestamp without time zone not null default now(),
	PRIMARY KEY (id)
);

create table faturamento.contato (
	id uuid not null default uuid_generate_v4(),
	pessoa uuid not null,
	descricao varchar(150),
	principal boolean,
	tipo text, -- enum("fixo", "celular", "fax", "voip") not null,
	ddi varchar(2),
	ddd varchar(2),
	numero varchar(20) not null,
	ramal varchar(12),
	created_at timestamp without time zone not null default now(),
  PRIMARY KEY (id),
  FOREIGN KEY (pessoa) REFERENCES faturamento.pessoa (id)
);


-- Tabela da fila de clientes
create table fila_cliente (
    id bigserial primary key,
    id_inicial int8,
    data_hora_inicial timestamp with time zone default clock_timestamp(),
    data_hora timestamp with time zone default clock_timestamp(),
    origem varchar(150),
    destino varchar(150),
    processo varchar(250),
    chave_externa varchar(100),
    proxima_tentativa timestamp with time zone,
    tentativa int default 1,
    status varchar(100) default 'pendente',
    reenfileirado boolean default false,
    estouro_tentativas boolean default false,
    mensagem varchar(500),
    id_anterior int8,
    data_hora_anterior timestamp with time zone,
    status_anterior varchar(100),
    mensagem_anterior varchar(500),
    payload text,
    tenant int8,
    grupo_empresarial varchar(40),
    payload_hash bytea,
    pub_sub boolean default false not null,
    publication_id int8,
    subscriber_id varchar(100),
    dead boolean default False not null,
    live_id int8
);

-- Índices da tabela de fila
create index "idx_fila_cliente_status" on fila_cliente (status);
create index "idx_fila_cliente_status_tentativa_data_hora" on fila_cliente (status, tentativa, data_hora);
create index "idx_fila_cliente_data_hora" on fila_cliente (data_hora);
create index "idx_fila_cliente_chave_externa_payload_hash_status" on fila_cliente (chave_externa, payload_hash, status);

-- Trigger para notificar inserções na fila
CREATE OR REPLACE FUNCTION public.notify_fila_cliente_insert()
RETURNS TRIGGER AS $$
DECLARE
    channel_name text := 'fila_cliente';
BEGIN
    PERFORM pg_notify(channel_name, '');
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_insert_fila_cliente
AFTER INSERT ON fila_cliente
FOR EACH ROW
WHEN (NEW.data_hora <= clock_timestamp() and NEW.status <> 'agendada')
EXECUTE FUNCTION public.notify_fila_cliente_insert();

-- Tabela de assinaturas, para o caso de uso pub_sub
create table fila_cliente_subscriber(
	id varchar(100) NOT NULL PRIMARY KEY,
	tenant int8,
	grupo_empresarial varchar(40),
	processo varchar(250) NOT NULL,
	url VARCHAR(2048),
	http_method VARCHAR(8),
	headers json,
	ativo boolean not null default true,
	created_at timestamp with time zone not null default now()
);
create index "idx_fila_cliente_subscriber_tenant_grupo_empresarial_processo" on fila_cliente_subscriber (tenant, grupo_empresarial, processo);

-- Dados paro o exemplo de atualização em api remota e atualizaçção de índice
INSERT INTO fila_cliente_subscriber(id, processo, url, http_method) VALUES
('api_faturamento_pessoas', 'sinc_faturamento_pessoas', null, null),
('api_indice_pessoas'     , 'sinc_faturamento_pessoas', null, null);
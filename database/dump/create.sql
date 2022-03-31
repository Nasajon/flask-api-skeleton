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

insert into teste.cliente (nome, documento) values ('Fulano', '123456');
insert into teste.cliente (nome, documento) values ('Ciclano', '456789');

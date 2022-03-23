CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

create schema teste;

create table teste.cliente (
	id uuid not null default uuid_generate_v4(),
	nome varchar(100) not null,
	documento varchar not null,
	created_at timestamp without time zone not null,
	CONSTRAINT teste_cliente_pkey PRIMARY KEY (id)
);

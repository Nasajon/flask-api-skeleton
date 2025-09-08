create schema restlib2;

create table restlib2.entity (
    id uuid not null default uuid_generate_v4(),
    escopo varchar(100) not null,
    codigo varchar(100) not null,
    descricao varchar(500) not null,
    json_schema jsonb not null,
    content_hash varchar(300) not null,
    created_at timestamp without time zone not null default now(),
    CONSTRAINT restlib2_entity_pkey PRIMARY KEY (id)
);
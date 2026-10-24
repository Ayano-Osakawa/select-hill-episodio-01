-- Banco didático do episódio 1; não é o banco interno do jogo.
CREATE TABLE locais (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    regiao TEXT NOT NULL,
    ordem INTEGER NOT NULL
);

CREATE TABLE pessoas (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL
);

CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,

    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    cargo TEXT NOT NULL,

    senha TEXT NOT NULL,

    perfil TEXT NOT NULL DEFAULT 'visualizacao',

    ativo BOOLEAN DEFAULT TRUE,

    criado_em TIMESTAMP DEFAULT NOW(),

    CONSTRAINT chk_perfil
    CHECK (perfil IN ('master', 'editor', 'visualizacao', 'exportador'))
);
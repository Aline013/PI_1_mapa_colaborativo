CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE pontos (
    id SERIAL PRIMARY KEY,
    nome TEXT NOT NULL,

    -- localização
    estado TEXT,
    cidade TEXT,
    altitude NUMERIC(8,2),

    -- dados do lúpulo
    lupulo TEXT,
    oleos_essenciais NUMERIC(5,2),
    alfa_acidos NUMERIC(5,2),

    -- dados da cerveja
    estilo_cerveja TEXT,
    teor_alcoolico NUMERIC(4,2) CHECK (teor_alcoolico >= 0),
    ibu NUMERIC(5,2) CHECK (ibu >= 0),
    kcal_100ml NUMERIC(6,2) CHECK (kcal_100ml >= 0),

    -- geoespacial
    coordenada GEOMETRY(Point, 4674) NOT NULL,

    -- derivados automáticos
    latitude DOUBLE PRECISION
        GENERATED ALWAYS AS (ST_Y(coordenada)) STORED,

    longitude DOUBLE PRECISION
        GENERATED ALWAYS AS (ST_X(coordenada)) STORED,

    criado_em TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_pontos_coordenada
ON pontos
USING GIST (coordenada);
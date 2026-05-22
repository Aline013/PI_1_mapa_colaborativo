from sqlalchemy import Column, Integer, String, Numeric, DateTime
from geoalchemy2 import Geometry
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from datetime import datetime

Base = declarative_base()


class Ponto(Base):

    __tablename__ = "pontos"

    id = Column(Integer, primary_key=True)

    nome = Column(String, nullable=False)
    estado = Column(String, nullable=False)
    cidade = Column(String, nullable=False)
    lupulo = Column(String, nullable=False)
    altitude = Column(Numeric, nullable=True)

    oleos_essenciais = Column(Numeric, nullable=True)

    alfa_acidos = Column(Numeric, nullable=True)

    estilo_cerveja = Column(String, nullable=True)

    teor_alcoolico = Column(Numeric, nullable=True)

    ibu = Column(Numeric, nullable=True)

    kcal_100ml = Column(Numeric, nullable=True)

    coordenada = Column(
        Geometry("POINT", srid=4674),
        nullable=False
    )

    criado_em = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

class Usuario(Base):

    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True)

    nome = Column(String, nullable=False)

    email = Column(String, unique=True, nullable=False)

    cargo = Column(String, nullable=False)

    senha = Column(String, nullable=False)

    perfil = Column(String, nullable=False)

    ativo = Column(Boolean, default=True)

    criado_em = Column(DateTime, default=datetime.utcnow)
from pydantic import BaseModel
from typing import Optional


class PontoCreate(BaseModel):

    nome: str
    estado: str
    cidade: str

    latitude: float
    longitude: float

    altitude: Optional[float] = None

    lupulo: Optional[str]

    oleos_essenciais: Optional[float] = None
    alfa_acidos: Optional[float] = None

    estilo_cerveja: Optional[str] = None

    teor_alcoolico: Optional[float] = None

    ibu: Optional[float] = None

    kcal_100ml: Optional[float] = None

class UsuarioCreate(BaseModel):

    nome: str
    email : str
    cargo : str
    senha : str
    perfil : str



   
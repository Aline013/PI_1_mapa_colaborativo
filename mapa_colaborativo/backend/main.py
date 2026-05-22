from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from jose import jwt
from jose import JWTError
from datetime import datetime, timedelta

from database import SessionLocal
from models import Ponto
from models import Usuario
from schemas import UsuarioCreate
from schemas import PontoCreate

from geoalchemy2.functions import ST_MakePoint
from geoalchemy2.functions import ST_SetSRID
from jose import JWTError, jwt

from passlib.context import CryptContext

from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm

from fastapi import HTTPException, status

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()
app.mount(
    "/static",
    StaticFiles(directory="../frontend"),
    name="static"
)


SECRET_KEY = "chave_super_secreta"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def criar_token(dados: dict):

    dados_token = dados.copy()

    expiracao = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    dados_token.update({
        "exp": expiracao
    })

    token = jwt.encode(
        dados_token,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)

app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)
def get_usuario_logado(
    token: str = Depends(oauth2_scheme)
):

    credenciais_exception = HTTPException(

        status_code=401,

        detail="Token inválido",

        headers={
            "WWW-Authenticate": "Bearer"
        }
    )

    try:

        payload = jwt.decode(

            token,

            SECRET_KEY,

            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")

        if email is None:

            raise credenciais_exception

        return payload

    except JWTError:

        raise credenciais_exception
    
    return token
def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

def gerar_hash_senha(senha):

    return pwd_context.hash(senha)

@app.get("/")
def home():

    return {
        "mensagem": "API do mapa colaborativo funcionando"
    }

@app.get("/")
def frontend():

    return FileResponse(
        "../frontend/index.html"
    )

@app.get("/pontos")
def listar_pontos(db: Session = Depends(get_db)):

    query = text("""
        SELECT
            id,
            nome,
            estado,
            cidade,
            altitude,
            lupulo,
            oleos_essenciais,
            alfa_acidos,
            estilo_cerveja,
            teor_alcoolico,
            ibu,
            kcal_100ml,
            ST_Y(coordenada) AS latitude,
            ST_X(coordenada) AS longitude
        FROM pontos
    """)

    resultado = db.execute(query).mappings().all()

    pontos = []

    for row in resultado:

        pontos.append({
            "id": row.id,
            "nome": row.nome,
            "estado": row.estado,
            "cidade": row.cidade,
            "altitude": row.altitude,
            "lupulo": row.lupulo,
            "oleos_essenciais": row.oleos_essenciais,
            "alfa_acidos": row.alfa_acidos,
            "estilo_cerveja": row.estilo_cerveja,
            "teor_alcoolico": row.teor_alcoolico,
            "ibu": row.ibu,
            "kcal_100ml": row.kcal_100ml,
            "latitude": row.latitude,
            "longitude": row.longitude
        })

    return pontos

@app.post("/pontos")
def criar_ponto(
    ponto: PontoCreate,
    usuario = Depends(get_usuario_logado),
    db: Session = Depends(get_db)
):

    novo_ponto = Ponto(
        nome=ponto.nome,
        estado=ponto.estado,
        cidade=ponto.cidade,
        altitude=ponto.altitude,
        lupulo=ponto.lupulo,
        oleos_essenciais=ponto.oleos_essenciais,
        alfa_acidos=ponto.alfa_acidos,
        estilo_cerveja=ponto.estilo_cerveja,
        teor_alcoolico=ponto.teor_alcoolico,
        ibu=ponto.ibu,
        kcal_100ml=ponto.kcal_100ml,
        coordenada=ST_SetSRID(
            ST_MakePoint(ponto.longitude, ponto.latitude),
            4674
        )
    )

    db.add(novo_ponto)
    db.commit()
    db.refresh(novo_ponto)

    return {
        "id": novo_ponto.id,
        "mensagem": "Ponto criado com sucesso"
    }
@app.delete("/pontos/{id}")
def deletar_ponto(
    id: int,
    db: Session = Depends(get_db)
):

    ponto = db.query(Ponto).filter(
        Ponto.id == id
    ).first()

    if not ponto:

        return {
            "erro": "Ponto não encontrado"
        }

    db.delete(ponto)

    db.commit()

    return {
        "mensagem": "Ponto deletado com sucesso"
    }
@app.put("/pontos/{id}")
def atualizar_ponto(
    id: int,
    ponto: PontoCreate,
    db: Session = Depends(get_db)
):

    ponto_db = db.query(Ponto).filter(
        Ponto.id == id
    ).first()

    if not ponto_db:

        return {
            "erro": "Ponto não encontrado"
        }

    ponto_db.nome = ponto.nome
    ponto_db.estado = ponto.estado
    ponto_db.cidade = ponto.cidade

    ponto_db.altitude = ponto.altitude

    ponto_db.lupulo = ponto.lupulo

    ponto_db.oleos_essenciais = ponto.oleos_essenciais
    ponto_db.alfa_acidos = ponto.alfa_acidos

    ponto_db.estilo_cerveja = ponto.estilo_cerveja

    ponto_db.teor_alcoolico = ponto.teor_alcoolico

    ponto_db.ibu = ponto.ibu

    ponto_db.kcal_100ml = ponto.kcal_100ml

    ponto_db.coordenada = ST_SetSRID(
        ST_MakePoint(
            ponto.longitude,
            ponto.latitude
        ),
        4674
    )

    db.commit()

    return {
        "mensagem": "Ponto atualizado com sucesso"
    }

@app.get("/usuarios")
def listar_usuarios(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    usuarios = db.query(Usuario).all()

    resultado = []

    for usuario in usuarios:

        resultado.append({

            "id": usuario.id,

            "nome": usuario.nome,

            "email": usuario.email,

            "cargo": usuario.cargo,

            "perfil": usuario.perfil,

            "ativo": usuario.ativo,

            "criado_em": usuario.criado_em
        })

    return resultado

def verificar_senha(
    senha,
    hash_senha
):

    return pwd_context.verify(
        senha,
        hash_senha
    )

@app.get("/teste-token")
def teste_token(
    usuario = Depends(get_usuario_logado)
):
    return {
        "token": token
    }
@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    usuario = db.query(Usuario).filter(
        Usuario.email == form_data.username
    ).first()

    if not usuario:

        raise HTTPException(
            status_code=401,
            detail="Usuário não encontrado"
        )

    senha_correta = verificar_senha(
        form_data.password,
        usuario.senha
    )

    if not senha_correta:

        raise HTTPException(
            status_code=401,
            detail="Senha inválida"
        )

    token = criar_token({

        "sub": usuario.email,

        "perfil": usuario.perfil
    })

    return {

        "access_token": token,

        "token_type": "bearer"
    }
@app.post("/usuarios")
def criar_usuario(
    usuario: UsuarioCreate,
    db: Session = Depends(get_db)
):

    novo_usuario = Usuario(
        
        nome=usuario.nome,

        email=usuario.email,

        cargo =usuario.cargo,

        senha=gerar_hash_senha(usuario.senha),

        perfil=usuario.perfil,

        ativo=True,
        
    )

    db.add(novo_usuario)

    db.commit()

    db.refresh(novo_usuario)

    return {

        "id": novo_usuario.id,

        "nome": novo_usuario.nome,

        "email": novo_usuario.email,

        "cargo": novo_usuario.cargo,

        "perfil": novo_usuario.perfil

    }
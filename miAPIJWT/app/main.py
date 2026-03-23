from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.openapi.utils import get_openapi
from typing import Optional
import asyncio
from pydantic import BaseModel, Field

from jose import JWTError, jwt
import bcrypt
from datetime import datetime, timedelta, timezone

SECRET_KEY = "mi_clave_secreta_muy_segura_para_jwt_2024"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 0

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/token")

usuarios_db = {
    "IvanMoreno": {
        "username": "IvanMoreno",
        "hashed_password": bcrypt.hashpw("Hola1234".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    }
}

class crear_usuario(BaseModel):
    id: int = Field(..., gt=0, description="Identificador de usuario")
    nombre: str = Field(..., min_length=3, max_length=50, example="Elizabeth")
    edad: int = Field(..., ge=1, le=123, description="Edad válida entre 1 y 123")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

def verificar_password(password_plano: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password_plano.encode("utf-8"), password_hash.encode("utf-8"))

def autenticar_usuario(username: str, password: str):
    usuario = usuarios_db.get(username)
    if not usuario:
        return None
    if not verificar_password(password, usuario["hashed_password"]):
        return None
    return usuario

def crear_token_acceso(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    payload = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    payload.update({"exp": expire})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def obtener_usuario_actual(token: str = Depends(oauth2_scheme)) -> str:
    credencial_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credencial_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credencial_exception

    usuario = usuarios_db.get(token_data.username)
    if usuario is None:
        raise credencial_exception

    return token_data.username

app = FastAPI(
    title="miApi con OAuth2 + JWT",
    description="Ivan Moreno – FastAPI con autenticación JWT",
    version="2.0.0"
)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"]["BearerAuth"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            if "security" in method:
                method["security"].append({"BearerAuth": []})
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

usuarios = [
    {"id": 1, "nombre": "Diego", "edad": 38},
    {"id": 2, "nombre": "Dafne", "edad": 20},
    {"id": 3, "nombre": "Ana",   "edad": 20},
]

@app.post("/v1/token", response_model=Token, tags=["Autenticación"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Devuelve un Bearer token con vigencia máxima de 30 minutos."""
    usuario = autenticar_usuario(form_data.username, form_data.password)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = crear_token_acceso(
        data={"sub": usuario["username"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": token, "token_type": "bearer"}

@app.get("/", tags=["Inicio"])
async def holaMundo():
    return {"mensaje": "Hola mundo – FastAPI con JWT"}

@app.get("/v1/bienvenidos", tags=["Inicio"])
async def bienvenidos():
    return {"mensaje": "Bienvenidos"}

@app.get("/v1/promedio", tags=["Calificaciones"])
async def promedio():
    await asyncio.sleep(3)
    return {"Calificacion": "8.5", "estatus": "200"}

@app.get("/v1/usuario/{id}", tags=["Parámetros"])
async def consultaUno(id: int):
    await asyncio.sleep(1)
    return {"Resultado": "Usuario encontrado", "id": id, "estatus": "200"}

@app.get("/v1/usuarios/", tags=["Parámetro Opcional"])
async def consultaOp(id: Optional[int] = None):
    await asyncio.sleep(1)
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return {"Usuario encontrado": id, "Datos": usuario}
        return {"Mensaje": "Usuario no encontrado"}
    return {"Aviso": "No se proporcionó id"}

@app.get("/v1/usuario/", tags=["CRUD HTTP"])
async def consulta():
    return {"status": "200", "total": len(usuarios), "data": usuarios}

@app.post("/v1/usuario/", tags=["CRUD HTTP"], status_code=status.HTTP_201_CREATED)
async def crea_usuario(usuario: crear_usuario):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(status_code=400, detail="El id ya existe")
    usuarios.append(usuario.dict())
    return {"mensaje": "Usuario agregado correctamente", "usuario": usuario}

@app.put("/v1/usuario/{id}", tags=["CRUD HTTP – Protegido"])
async def actualizar_usuario(
    id: int,
    usuario_actualizado: dict,
    usuario_actual: str = Depends(obtener_usuario_actual)   
):
    """Actualiza un usuario. Requiere Bearer Token válido."""
    for i, usuario in enumerate(usuarios):
        if usuario["id"] == id:
            usuarios[i]["nombre"] = usuario_actualizado.get("nombre", usuario["nombre"])
            usuarios[i]["edad"]   = usuario_actualizado.get("edad",   usuario["edad"])
            return {
                "mensaje": f"Usuario actualizado por {usuario_actual}",
                "status":  "200",
                "usuario": usuarios[i]
            }
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.delete("/v1/usuario/{id}", tags=["CRUD HTTP – Protegido"])
async def eliminar_usuario(
    id: int,
    usuario_actual: str = Depends(obtener_usuario_actual)   
):
    """Elimina un usuario. Requiere Bearer Token válido."""
    for i, usuario in enumerate(usuarios):
        if usuario["id"] == id:
            eliminado = usuarios.pop(i)
            return {
                "mensaje": f"Usuario eliminado por {usuario_actual}",
                "status":  "200",
                "usuario": eliminado
            }
    raise HTTPException(status_code=404, detail="Usuario no encontrado")
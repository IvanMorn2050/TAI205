#1.importaciones
from fastapi import FastAPI

#2. Inicialización APP
app = FastAPI()

#3. Endpoints
@app.get("/")
async def hola_mundo():
    return {"mensaje": "Hola mundo FASTAPI"}

@app.get("/bienvenido")
async def bienvenido():
    return {"mensaje2": "Bienvenido"}
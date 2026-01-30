#1. importaciones
from fastapi import FastAPI
from typing import Optional
import asyncio

#2.Inicialización APP
app=FastAPI(
    title='Mi primer API', 
    description="Ivan Moreno",
    version='1.0.0'
    )


#BD ficticia
usuarios=[
    {"id":"1","nombre":"Diego","edad":"38"},
    {"id":"2","nombre":"Dafne","edad":"20"},
    {"id":"3","nombre":"Ana","edad":"20"}
]

#3.Endpoints
@app.get("/", tags=['Inicio'])
async def holaMundo():
    return {"mensaje":"Hola mundo FASTAPI"}

@app.get("v1/bienvenidos", tags=['Inicio'])
async def bien():
    return {"mensaje":"Bienvenidos"}    

@app.get("/v1/promedio", tags=['Calificaciones'])
async def promedio():
    await asyncio.sleep(3)   #simulación de peticion, consultaBD..
    return {
            "Claificacion":"8.5",
            "estatus":"200"
            }

@app.get("v1/usuario/{id}", tags=['Parametros'])
async def consultaUno(id:int):
    await asyncio.sleep(3)
    return {
        "Resultado":"Usuario encontrado",
        "estatus":"200"
        }

@app.get("/v1/usuarios/", tags=['Parametro Opcional'])
async def consultaOp(id:Optional[int]=None):
    await asyncio.sleep(2)
    if id is not None:
        for usuario in usuarios:
            if usuario["id"]==str(id):
                return {"Usuario encontrado":id,"Datos":usuario}
        return {"Mensaje":"Usuario no encontrado"}
    else:
        return {"Aviso":"No se proporciono id"}
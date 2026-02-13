#1.importaciones
from fastapi import FastAPI,status,HTTPException
from typing import Optional
import asyncio
#2. Inicialización APP
app = FastAPI()

#3. Endpoints
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


@app.get("/v1/usuario/", tags=['CRUD HTTP'])
async def consulta():
    return{
        "status":"200",
        "total":len(usuarios),
        "data": usuarios
    }

@app.post("/v1/usuario/", tags=['CRUD HTTP'])
async def crea_usuario(usuario:dict):
    for usr in usuarios:
        if usr["id"] == usuario.get("id"): 
            raise HTTPException(
                status_code=400,
                detail= "El id ya existe"
            )
    usuarios.append(usuario)
    return{
        "mensaje":"Usuario agregado correctamente",
        "status":"200",
        "usuario":usuario
    }

@app.put("/v1/usuario/{id}", tags=['CRUD HTTP'])
async def actualizar_usuario(id: int, usuario_actualizado: dict):

    for i, usuario in enumerate(usuarios):
        if usuario["id"] == str(id):

            usuarios[i]["nombre"] = usuario_actualizado.get("nombre", usuario["nombre"])
            usuarios[i]["edad"] = usuario_actualizado.get("edad", usuario["edad"])

            return {
                "mensaje": "Usuario actualizado correctamente",
                "status": "200",
                "usuario": usuarios[i]
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )

@app.delete("/v1/usuario/{id}", tags=['CRUD HTTP'])
async def eliminar_usuario(id: int):

    for i, usuario in enumerate(usuarios):
        if usuario["id"] == str(id):

            usuario_eliminado = usuarios.pop(i)

            return {
                "mensaje": "Usuario eliminado correctamente",
                "status": "200",
                "usuario": usuario_eliminado
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )

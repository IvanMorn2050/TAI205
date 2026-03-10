from fastapi import FastAPI,status,HTTPException,Depends
from pydantic import BaseModel, Field 
import asyncio
from typing import Optional 
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets 
from datetime import datetime

app = FastAPI(
    Title = "Examen 2do",
    description="Ivan Moreno Morales 205"
)

habitaciones = [
    {"id":1, "tipo_habitacion":"Sencilla", "estado": "Disponible"},
    {"id":2,"tipo_habitacion":"Doble", "estado": "Ocupado"},
    {"id":3,"tipo_habitacion":"Suite", "estado": "Disponible"},
    {"id":4,"tipo_habitacion":"Suite", "estado": "Ocupado"},
    {"id":5,"tipo_habitacion":"Doble", "estado": "Disponible"},
    {"id":6,"tipo_habitacion":"Sencilla", "estado": "Ocupado"}
    ]

reservas=[
    {"id":1, "nombre": "Ivan Moreno", "fecha_entrada":9-3-2026, "fecha_salida":15-3-2026, "tipo_habitacion": "Doble", "estancia":8, "estado_reserva": "Pendiente"},
    {"id":1, "nombre": "Katherine Moreno", "fecha_entrada":10-3-2026, "fecha_salida":14-3-2026, "tipo_habitacion": "Suite", "estancia":8, "estado_reserva": "Confirmado"},
]
class crear_reserva(BaseModel):
    nombre: str = Field(..., min_length=5, max_length=50)
    fecha_entrada: datetime = Field(...,gt=9-3-2026)   
    fecha_salida: datetime = Field(...,gt=16-3-2026)
    tipo_habitacion: str = Field(..., min_length=5, max_length=50)
    estancia: int = Field(..., gt=7)
    estado_reserva: str= Field(..., pattern="^(Disponible|Ocupado)$")

seguridad = HTTPBasic()

def verificar_peticion(credenciales:HTTPBasicCredentials=Depends(seguridad)):
    userAuth=secrets.compare_digest(credenciales.username,"hotel")
    passAuth=secrets.compare_digest(credenciales.password,"r2026")

    if not (userAuth and passAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHERIZED,
            detail ="Crdenciales no autorizadas" 
            )
    return credenciales.username

@app.post("/v1/reserva/", tags=["Reservas"])
async def crea_reserva(reserva:crear_reserva,userAuth:str=Depends(verificar_peticion)):
    for r in reservas: 
        if r[{"id"}] == reserva.id:
            raise HTTPException(
                status_code= 400,
                detail = "La reserva ya existe"
            )
    reservas.append(reserva)
    return{
        "mensaje": "Reserva creada exitosamente",
        "status":"200",
        "reserva":reserva
    }

@app.get("/v1/reserva/",tags=["Reservas"])
async def listar_reservas():
    disponibles = [
        reserva for reserva in reservas
        if reserva["estado"] == "Disponible"
    ]
    return{
        "total":len(disponibles),
        "data":disponibles
    }

@app.get("/v1/reserva/{id}",tags=["Reservas"])
async def buscar_reserva (id:int):
    resultado = [
        reserva for reserva in reservas
        if reserva in reserva["id"]
    ]
    return{
        "total": len(resultado),
        "data": resultado
    }

@app.put("/v1/reserva/confirmar/{id}",tags=["Reservas"])
async def confirmar_reserva(id_int):
    for r, reserva in enumerate(reservas):
        if reserva ["id"] == id:
            for reserva in reserva:
                if reserva["id"] == reserva ["reserva_id"]:
                    reserva ["estado"] = "Confirmado"
                    break 
            del reservas[r]
            return{
                "mensaje": "Reserva confirmada correctamente",
                "status":200
            }
    raise HTTPException(
        status_code=409,
        detail="La reserva no existe"
    )

@app.delete("/v1/reserva/cancelar/{id}",tags=["Reservas"])
async def cancelar_reserva(id:int, userAuth:str=Depends(verificar_peticion)):
    for r, reserva in enumerate(reservas):
        if reserva["id"] == id:
            reserva_cancelada = reservas.pop(r)

            return {
                "mensaje":"Reserva cancelada",
                "status": 200,
                "usuario": reserva_cancelada
            }
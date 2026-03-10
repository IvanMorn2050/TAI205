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
    {"id":1, "nombre": "Ivan Moreno", "estado_reserva": "Pendiente"},
    {"id":2, "nombre": "Katherine Moreno", "estado_reserva": "Confirmado"},
]
class crear_reserva(BaseModel):
    nombre: str = Field(..., min_length=5, max_length=50, example="Ivan Moreno")
    fecha_entrada: datetime = Field(...,)
    fecha_salida: datetime = Field(...,)
    tipo_habitacion: str = Field(..., min_length=5, max_length=50, example ="Sencilla, Doble, Suite",)
    estancia: int = Field(..., gt=7, example="7")

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
async def crea_reserva(reserva:crear_reserva):
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

@app.get("/v1/reserva")
async def listar_reservas():
    disponibles = [
        reserva for reserva in reservas
        if reserva["estado"] == "Disponible"
    ]
    return{
        "total":len(disponibles),
        "data":disponibles
    }

@app.get("/v1/reserva/{id}")
async def buscar_reserva (id:int):
    resultado = [
        reserva for reserva in reservas
        if reserva in reserva["id"]
    ]
    return{
        "total": len(resultado),
        "data": resultado
    }

@app.put("/v1/reserva/confirmar/{id}")
async def confirmar_reserva(id_int):
    for r, reserva in enumerate(reservas):
        if reserva ["id"] == id:
            for reserva in reserva:
                
from fastapi import FastAPI, status, HTTPException
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

app = FastAPI(
    title="Repaso",
    description="Ivan Moreno",
    version="1.0.0"
)

usuarios = [
    {"id": 1, "nombre": "Diego", "correo": "diego@correo.com"},
    {"id": 2, "nombre": "Dafne", "correo": "dafne@correo.com"},
    {"id": 3, "nombre": "Ana", "correo": "ana@correo.com"}
]

libros = [
    {"id": 1,"nombre": "IT","autor": "Stephen King","estado": "disponible","año_libro": 1986,"num_paginas": 1138},
    {"id": 2,"nombre": "Cien años de soledad","autor": "García Márquez","estado": "prestado","año_libro": 1967,"num_paginas": 417},
    {"id": 3,"nombre": "Don Quijote","autor": "Cervantes","estado": "disponible","año_libro": 1605,"num_paginas": 863}
]

prestamos = [
    {"id": 1, "usuario_id": 1, "libro_id": 2}
]

class Usuario(BaseModel):
    id: int = Field(..., gt=0)

    nombre: str = Field(...,min_length=3,max_length=50)
    correo: str = Field(...,pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")

class Libro(BaseModel):
    id: int = Field(..., gt=0)

    nombre: str = Field(...,min_length=2,max_length=100)
    autor: str = Field(..., min_length=3)
    estado: str = Field(...,pattern="^(disponible|prestado)$")
    año_libro: int = Field(...,gt=1450,le=datetime.now().year)
    num_paginas: int = Field(...,gt=1)

class Prestamo(BaseModel):
    id: int = Field(..., gt=0)

    usuario_id: int = Field(..., gt=0)
    libro_id: int = Field(..., gt=0)

@app.post("/v1/libro/", status_code=status.HTTP_201_CREATED)
async def registrar_libro(libro: Libro):

    if not libro.nombre.strip():
        raise HTTPException(
            status_code=400,
            detail="Nombre del libro no válido"
        )

    for lb in libros:
        if lb["id"] == libro.id or lb["nombre"] == libro.nombre:
            raise HTTPException(
                status_code=400,
                detail="El libro ya existe"
            )
    libros.append(libro.model_dump())
    return {
        "mensaje": "Libro registrado correctamente",
        "libro": libro
    }

@app.get("/v1/libro/")
async def listar_libros():
    disponibles = [
        libro for libro in libros
        if libro["estado"] == "disponible"
    ]
    return {
        "total": len(disponibles),
        "data": disponibles
    }

@app.get("/v1/libro/buscar/{nombre}")
async def buscar_libro(nombre: str):
    resultado = [
        libro for libro in libros
        if nombre.lower() in libro["nombre"].lower()
    ]
    return {
        "total": len(resultado),
        "data": resultado
    }

@app.post("/v1/prestamo/", status_code=status.HTTP_201_CREATED)
async def registrar_prestamo(prestamo: Prestamo):
    usuario = None
    for usr in usuarios:
        if usr["id"] == prestamo.usuario_id:
            usuario = usr
            break
    if not usuario:
        raise HTTPException(
            status_code=400,
            detail="Usuario no existe"
        )

    libro = None
    for lb in libros:
        if lb["id"] == prestamo.libro_id:
            libro = lb
            break
    if not libro:
        raise HTTPException(
            status_code=400,
            detail="Libro no existe"
        )
    if libro["estado"] == "prestado":
        raise HTTPException(
            status_code=409,
            detail="El libro ya está prestado"
        )
    libro["estado"] = "prestado"
    prestamos.append(prestamo.model_dump())
    return {
        "mensaje": "Préstamo registrado correctamente",
        "prestamo": prestamo
    }

@app.put("/v1/prestamo/devolver/{id}")
async def devolver_libro(id: int):
    for i, prestamo in enumerate(prestamos):
        if prestamo["id"] == id:
            for libro in libros:
                if libro["id"] == prestamo["libro_id"]:
                    libro["estado"] = "disponible"
                    break
            del prestamos[i]
            return {
                "mensaje": "Libro devuelto correctamente",
                "status": 200
            }
    raise HTTPException(
        status_code=409,
        detail="El préstamo no existe"
    )

@app.delete("/v1/prestamo/{id}")
async def eliminar_prestamo(id: int):
    for i, prestamo in enumerate(prestamos):
        if prestamo["id"] == id:
            del prestamos[i]
            return {
                "mensaje": "Préstamo eliminado correctamente",
                "status": 200
            }
    raise HTTPException(
        status_code=409,
        detail="El registro de préstamo no existe"
    )
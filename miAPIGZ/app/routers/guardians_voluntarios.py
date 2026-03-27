from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.guardian_models import Voluntario
from app.models.guardian_schemas import CrearVoluntario, ActualizarVoluntario

routerVol = APIRouter(
    prefix="/v1/voluntarios",
    tags=['CRUD HTTP - Voluntarios']
)

@routerVol.get("/", response_model=dict)
async def obtener_voluntarios(db: Session = Depends(get_db)):
    """Obtener todos los voluntarios"""
    query_voluntarios = db.query(Voluntario).all()
    return {
        "status": "200",
        "total": len(query_voluntarios),
        "data": query_voluntarios
    }

@routerVol.get("/{id}")
async def obtener_voluntario(id: int, db: Session = Depends(get_db)):
    """Obtener un voluntario por ID"""
    voluntario = db.query(Voluntario).filter(Voluntario.ID == id).first()
    if not voluntario:
        raise HTTPException(status_code=404, detail="Voluntario no encontrado")
    return {
        "status": "200",
        "data": voluntario
    }

@routerVol.post("/", status_code=status.HTTP_201_CREATED)
async def crear_voluntario(voluntario_data: CrearVoluntario, db: Session = Depends(get_db)):
    """Crear un nuevo voluntario"""
    voluntario_nuevo = Voluntario(
        ID_Usuario=voluntario_data.ID_Usuario,
        Nivel_Experiencia=voluntario_data.Nivel_Experiencia,
        Estatus=voluntario_data.Estatus,
        Horario_disponibilidad=voluntario_data.Horario_disponibilidad
    )
    db.add(voluntario_nuevo)
    db.commit()
    db.refresh(voluntario_nuevo)
    return {
        "status": "201",
        "mensaje": "Voluntario creado correctamente",
        "data": voluntario_nuevo
    }

@routerVol.put("/{id}")
async def actualizar_voluntario(id: int, voluntario_actualizado: ActualizarVoluntario, db: Session = Depends(get_db)):
    """Actualizar un voluntario"""
    voluntario = db.query(Voluntario).filter(Voluntario.ID == id).first()
    if not voluntario:
        raise HTTPException(status_code=404, detail="Voluntario no encontrado")

    for field, value in voluntario_actualizado.dict(exclude_unset=True).items():
        setattr(voluntario, field, value)

    db.commit()
    db.refresh(voluntario)
    return {
        "status": "200",
        "mensaje": "Voluntario actualizado correctamente",
        "data": voluntario
    }

@routerVol.delete("/{id}")
async def eliminar_voluntario(id: int, db: Session = Depends(get_db)):
    """Eliminar un voluntario"""
    voluntario = db.query(Voluntario).filter(Voluntario.ID == id).first()
    if not voluntario:
        raise HTTPException(status_code=404, detail="Voluntario no encontrado")

    db.delete(voluntario)
    db.commit()
    return {
        "status": "200",
        "mensaje": "Voluntario eliminado correctamente"
    }

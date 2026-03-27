from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.guardian_models import Recursos
from app.models.guardian_schemas import CrearRecurso, ActualizarRecurso

routerR = APIRouter(
    prefix="/v1/recursos",
    tags=['CRUD HTTP - Recursos']
)

@routerR.get("/", response_model=dict)
async def obtener_recursos(db: Session = Depends(get_db)):
    """Obtener todos los recursos"""
    query_recursos = db.query(Recursos).all()
    return {
        "status": "200",
        "total": len(query_recursos),
        "data": query_recursos
    }

@routerR.get("/{id}")
async def obtener_recurso(id: int, db: Session = Depends(get_db)):
    """Obtener un recurso por ID"""
    recurso = db.query(Recursos).filter(Recursos.ID == id).first()
    if not recurso:
        raise HTTPException(status_code=404, detail="Recurso no encontrado")
    return {
        "status": "200",
        "data": recurso
    }

@routerR.post("/", status_code=status.HTTP_201_CREATED)
async def crear_recurso(recurso_data: CrearRecurso, db: Session = Depends(get_db)):
    """Crear un nuevo recurso"""
    recurso_nuevo = Recursos(
        Nombre_Recurso=recurso_data.Nombre_Recurso,
        Categoria=recurso_data.Categoria,
        Cantidad_Disponible=recurso_data.Cantidad_Disponible,
        Ubicacion_Almacen=recurso_data.Ubicacion_Almacen
    )
    db.add(recurso_nuevo)
    db.commit()
    db.refresh(recurso_nuevo)
    return {
        "status": "201",
        "mensaje": "Recurso creado correctamente",
        "data": recurso_nuevo
    }

@routerR.put("/{id}")
async def actualizar_recurso(id: int, recurso_actualizado: ActualizarRecurso, db: Session = Depends(get_db)):
    """Actualizar un recurso"""
    recurso = db.query(Recursos).filter(Recursos.ID == id).first()
    if not recurso:
        raise HTTPException(status_code=404, detail="Recurso no encontrado")

    for field, value in recurso_actualizado.dict(exclude_unset=True).items():
        setattr(recurso, field, value)

    db.commit()
    db.refresh(recurso)
    return {
        "status": "200",
        "mensaje": "Recurso actualizado correctamente",
        "data": recurso
    }

@routerR.delete("/{id}")
async def eliminar_recurso(id: int, db: Session = Depends(get_db)):
    """Eliminar un recurso"""
    recurso = db.query(Recursos).filter(Recursos.ID == id).first()
    if not recurso:
        raise HTTPException(status_code=404, detail="Recurso no encontrado")

    db.delete(recurso)
    db.commit()
    return {
        "status": "200",
        "mensaje": "Recurso eliminado correctamente"
    }

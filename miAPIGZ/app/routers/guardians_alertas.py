from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.guardian_models import Alertas
from app.models.guardian_schemas import CrearAlerta, ActualizarAlerta

routerAl = APIRouter(
    prefix="/v1/alertas",
    tags=['CRUD HTTP - Alertas']
)

@routerAl.get("/", response_model=dict)
async def obtener_alertas(db: Session = Depends(get_db)):
    """Obtener todas las alertas"""
    query_alertas = db.query(Alertas).all()
    return {
        "status": "200",
        "total": len(query_alertas),
        "data": query_alertas
    }

@routerAl.get("/{id}")
async def obtener_alerta(id: int, db: Session = Depends(get_db)):
    """Obtener una alerta por ID"""
    alerta = db.query(Alertas).filter(Alertas.ID == id).first()
    if not alerta:
        raise HTTPException(status_code=404, detail="Alerta no encontrada")
    return {
        "status": "200",
        "data": alerta
    }

@routerAl.post("/", status_code=status.HTTP_201_CREATED)
async def crear_alerta(alerta_data: CrearAlerta, db: Session = Depends(get_db)):
    """Crear una nueva alerta"""
    alerta_nueva = Alertas(
        Titulo=alerta_data.Titulo,
        Mensaje=alerta_data.Mensaje,
        Nivel_Alerta=alerta_data.Nivel_Alerta,
        ID_Emisor=alerta_data.ID_Emisor
    )
    db.add(alerta_nueva)
    db.commit()
    db.refresh(alerta_nueva)
    return {
        "status": "201",
        "mensaje": "Alerta creada correctamente",
        "data": alerta_nueva
    }

@routerAl.put("/{id}")
async def actualizar_alerta(id: int, alerta_actualizada: ActualizarAlerta, db: Session = Depends(get_db)):
    """Actualizar una alerta"""
    alerta = db.query(Alertas).filter(Alertas.ID == id).first()
    if not alerta:
        raise HTTPException(status_code=404, detail="Alerta no encontrada")

    for field, value in alerta_actualizada.dict(exclude_unset=True).items():
        setattr(alerta, field, value)

    db.commit()
    db.refresh(alerta)
    return {
        "status": "200",
        "mensaje": "Alerta actualizada correctamente",
        "data": alerta
    }

@routerAl.delete("/{id}")
async def eliminar_alerta(id: int, db: Session = Depends(get_db)):
    """Eliminar una alerta"""
    alerta = db.query(Alertas).filter(Alertas.ID == id).first()
    if not alerta:
        raise HTTPException(status_code=404, detail="Alerta no encontrada")

    db.delete(alerta)
    db.commit()
    return {
        "status": "200",
        "mensaje": "Alerta eliminada correctamente"
    }

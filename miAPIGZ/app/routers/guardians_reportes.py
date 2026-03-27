from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.guardian_models import Reporte
from app.models.guardian_schemas import CrearReporte, ActualizarReporte

routerRep = APIRouter(
    prefix="/v1/reportes",
    tags=['CRUD HTTP - Reportes']
)

@routerRep.get("/", response_model=dict)
async def obtener_reportes(db: Session = Depends(get_db)):
    """Obtener todos los reportes"""
    query_reportes = db.query(Reporte).all()
    return {
        "status": "200",
        "total": len(query_reportes),
        "data": query_reportes
    }

@routerRep.get("/{id}")
async def obtener_reporte(id: int, db: Session = Depends(get_db)):
    """Obtener un reporte por ID"""
    reporte = db.query(Reporte).filter(Reporte.ID == id).first()
    if not reporte:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    return {
        "status": "200",
        "data": reporte
    }

@routerRep.post("/", status_code=status.HTTP_201_CREATED)
async def crear_reporte(reporte_data: CrearReporte, db: Session = Depends(get_db)):
    """Crear un nuevo reporte"""
    reporte_nuevo = Reporte(
        Lugar=reporte_data.Lugar,
        ID_Voluntario=reporte_data.ID_Voluntario,
        ID_Zona_Afectada=reporte_data.ID_Zona_Afectada,
        Estatus=reporte_data.Estatus,
        Prioridad=reporte_data.Prioridad,
        Descripcion_Emergencia=reporte_data.Descripcion_Emergencia
    )
    db.add(reporte_nuevo)
    db.commit()
    db.refresh(reporte_nuevo)
    return {
        "status": "201",
        "mensaje": "Reporte creado correctamente",
        "data": reporte_nuevo
    }

@routerRep.put("/{id}")
async def actualizar_reporte(id: int, reporte_actualizado: ActualizarReporte, db: Session = Depends(get_db)):
    """Actualizar un reporte"""
    reporte = db.query(Reporte).filter(Reporte.ID == id).first()
    if not reporte:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")

    for field, value in reporte_actualizado.dict(exclude_unset=True).items():
        setattr(reporte, field, value)

    db.commit()
    db.refresh(reporte)
    return {
        "status": "200",
        "mensaje": "Reporte actualizado correctamente",
        "data": reporte
    }

@routerRep.delete("/{id}")
async def eliminar_reporte(id: int, db: Session = Depends(get_db)):
    """Eliminar un reporte"""
    reporte = db.query(Reporte).filter(Reporte.ID == id).first()
    if not reporte:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")

    db.delete(reporte)
    db.commit()
    return {
        "status": "200",
        "mensaje": "Reporte eliminado correctamente"
    }

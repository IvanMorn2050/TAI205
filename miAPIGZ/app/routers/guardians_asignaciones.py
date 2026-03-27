from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.guardian_models import AsignacionRecursos, Recursos, Reporte
from app.models.guardian_schemas import CrearAsignacionRecurso

routerAsig = APIRouter(
    prefix="/v1/asignaciones",
    tags=['CRUD HTTP - Asignaciones']
)

@routerAsig.get("/", response_model=dict)
async def obtener_asignaciones(db: Session = Depends(get_db)):
    """Obtener todas las asignaciones de recursos"""
    query_asignaciones = db.query(AsignacionRecursos).all()
    return {
        "status": "200",
        "total": len(query_asignaciones),
        "data": query_asignaciones
    }

@routerAsig.get("/{id}")
async def obtener_asignacion(id: int, db: Session = Depends(get_db)):
    """Obtener una asignación por ID"""
    asignacion = db.query(AsignacionRecursos).filter(AsignacionRecursos.ID == id).first()
    if not asignacion:
        raise HTTPException(status_code=404, detail="Asignación no encontrada")
    return {
        "status": "200",
        "data": asignacion
    }

@routerAsig.post("/", status_code=status.HTTP_201_CREATED)
async def crear_asignacion(asignacion_data: CrearAsignacionRecurso, db: Session = Depends(get_db)):
    """Crear una nueva asignación de recursos"""
    # Verificar que el reporte existe
    reporte = db.query(Reporte).filter(Reporte.ID == asignacion_data.ID_Reporte).first()
    if not reporte:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")

    # Verificar que el recurso existe
    recurso = db.query(Recursos).filter(Recursos.ID == asignacion_data.ID_Recurso).first()
    if not recurso:
        raise HTTPException(status_code=404, detail="Recurso no encontrado")

    # Verificar disponibilidad
    if recurso.Cantidad_Disponible < asignacion_data.Cantidad_Asignada:
        raise HTTPException(
            status_code=400,
            detail=f"No hay suficiente cantidad disponible. Disponible: {recurso.Cantidad_Disponible}"
        )

    asignacion_nueva = AsignacionRecursos(
        ID_Reporte=asignacion_data.ID_Reporte,
        ID_Recurso=asignacion_data.ID_Recurso,
        Cantidad_Asignada=asignacion_data.Cantidad_Asignada
    )

    # Descontar del inventario
    recurso.Cantidad_Disponible -= asignacion_data.Cantidad_Asignada

    db.add(asignacion_nueva)
    db.commit()
    db.refresh(asignacion_nueva)

    return {
        "status": "201",
        "mensaje": "Asignación creada correctamente",
        "data": asignacion_nueva
    }

@routerAsig.delete("/{id}")
async def eliminar_asignacion(id: int, db: Session = Depends(get_db)):
    """Eliminar una asignación (devuelve recursos)"""
    asignacion = db.query(AsignacionRecursos).filter(AsignacionRecursos.ID == id).first()
    if not asignacion:
        raise HTTPException(status_code=404, detail="Asignación no encontrada")

    # Obtener el recurso para devolverlo
    recurso = db.query(Recursos).filter(Recursos.ID == asignacion.ID_Recurso).first()
    if recurso:
        recurso.Cantidad_Disponible += asignacion.Cantidad_Asignada

    db.delete(asignacion)
    db.commit()

    return {
        "status": "200",
        "mensaje": "Asignación eliminada y recursos devueltos"
    }

from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.guardian_models import ZonaAfectada
from app.models.guardian_schemas import CrearZonaAfectada, ActualizarZonaAfectada

routerZ = APIRouter(
    prefix="/v1/zonas-afectadas",
    tags=['CRUD HTTP - Zonas']
)

@routerZ.get("/", response_model=dict)
async def obtener_zonas(db: Session = Depends(get_db)):
    """Obtener todas las zonas afectadas"""
    query_zonas = db.query(ZonaAfectada).all()
    return {
        "status": "200",
        "total": len(query_zonas),
        "data": query_zonas
    }

@routerZ.get("/{id}", response_model=dict)
async def obtener_zona(id: int, db: Session = Depends(get_db)):
    """Obtener una zona por ID"""
    zona = db.query(ZonaAfectada).filter(ZonaAfectada.ID == id).first()
    if not zona:
        raise HTTPException(status_code=404, detail="Zona no encontrada")
    return {
        "status": "200",
        "data": zona
    }

@routerZ.post("/", status_code=status.HTTP_201_CREATED)
async def crear_zona(zona_data: CrearZonaAfectada, db: Session = Depends(get_db)):
    """Crear una nueva zona afectada"""
    zona_nueva = ZonaAfectada(
        Nombre_Zona=zona_data.Nombre_Zona,
        Coordenadas=zona_data.Coordenadas,
        Tipo_Zona=zona_data.Tipo_Zona,
        Poblacion_Afectada=zona_data.Poblacion_Afectada,
        Nivel_Gravedad=zona_data.Nivel_Gravedad,
        Impacto_Medio=zona_data.Impacto_Medio
    )
    db.add(zona_nueva)
    db.commit()
    db.refresh(zona_nueva)
    return {
        "status": "201",
        "mensaje": "Zona creada correctamente",
        "data": zona_nueva
    }

@routerZ.put("/{id}")
async def actualizar_zona(id: int, zona_actualizada: ActualizarZonaAfectada, db: Session = Depends(get_db)):
    """Actualizar una zona"""
    zona = db.query(ZonaAfectada).filter(ZonaAfectada.ID == id).first()
    if not zona:
        raise HTTPException(status_code=404, detail="Zona no encontrada")

    for field, value in zona_actualizada.dict(exclude_unset=True).items():
        setattr(zona, field, value)

    db.commit()
    db.refresh(zona)
    return {
        "status": "200",
        "mensaje": "Zona actualizada correctamente",
        "data": zona
    }

@routerZ.delete("/{id}")
async def eliminar_zona(id: int, db: Session = Depends(get_db)):
    """Eliminar una zona"""
    zona = db.query(ZonaAfectada).filter(ZonaAfectada.ID == id).first()
    if not zona:
        raise HTTPException(status_code=404, detail="Zona no encontrada")

    db.delete(zona)
    db.commit()
    return {
        "status": "200",
        "mensaje": "Zona eliminada correctamente"
    }

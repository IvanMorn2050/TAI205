#1.importaciones
from fastapi import FastAPI
from app.routers import varios
from app.routers.guardians_usuarios import routerU as guardianUsuarios
from app.routers.guardians_zonas import routerZ as guardianZonas
from app.routers.guardians_recursos import routerR as guardianRecursos
from app.routers.guardians_reportes import routerRep as guardianReportes
from app.routers.guardians_voluntarios import routerVol as guardianVoluntarios
from app.routers.guardians_alertas import routerAl as guardianAlertas
from app.routers.guardians_blog import routerBl as guardianBlog
from app.routers.guardians_asignaciones import routerAsig as guardianAsignaciones
from app.data.db import engine, Base
from app.data import usuario
from app.data.guardian_models import (
    Usuario, Blog, ConocimientosTecnicos, Puestos, TipoEvidencia,
    ZonaAfectada, Recursos, ContenidoBlog, Curriculum, Voluntario,
    Reporte, AsignacionRecursos, Alertas, DetalleConocimientos, Evidencia
)

# Crear todas las tablas
usuario.Base.metadata.create_all(bind=engine)
Base.metadata.create_all(bind=engine)

#2. Inicialización APP
app=FastAPI(
    title='Guardian Zero 2 API',
    description="API de Reporte de Emergencias - Ivan Moreno",
    version='2.0.0'
    )

#3. Endpoints - Original
app.include_router(varios.routerV)

#4. Endpoints - Guardian Zero 2
app.include_router(guardianUsuarios)
app.include_router(guardianZonas)
app.include_router(guardianRecursos)
app.include_router(guardianReportes)
app.include_router(guardianVoluntarios)
app.include_router(guardianAlertas)
app.include_router(guardianBlog)
app.include_router(guardianAsignaciones)



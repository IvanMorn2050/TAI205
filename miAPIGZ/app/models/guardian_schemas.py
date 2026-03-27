from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

# Modelos para USUARIO
class CrearUsuario(BaseModel):
    Nombre: str = Field(..., min_length=1, max_length=100)
    Telefono: Optional[str] = Field(None, max_length=15)
    Email: Optional[str] = None
    Direccion: Optional[str] = None
    Contraseña: str = Field(..., min_length=3)
    Rol: str = Field("Civil", pattern="^(Administrador|Especialista|Voluntario|Civil)$")

class ActualizarUsuario(BaseModel):
    Nombre: Optional[str] = None
    Telefono: Optional[str] = None
    Email: Optional[str] = None
    Direccion: Optional[str] = None
    Rol: Optional[str] = None

class UsuarioResponse(BaseModel):
    ID: int
    Nombre: str
    Email: Optional[str]
    Rol: str
    Fecha_Registro: datetime

    class Config:
        from_attributes = True

# Modelos para BLOG
class CrearBlog(BaseModel):
    Titulo: Optional[str] = None
    Descripcion: Optional[str] = None

class ActualizarBlog(BaseModel):
    Titulo: Optional[str] = None
    Descripcion: Optional[str] = None

# Modelos para ZONA_AFECTADA
class CrearZonaAfectada(BaseModel):
    Nombre_Zona: str = Field(..., max_length=255)
    Coordenadas: Optional[str] = None
    Tipo_Zona: Optional[str] = None
    Poblacion_Afectada: Optional[int] = None
    Nivel_Gravedad: str = Field("Estable", pattern="^(Estable|Moderado|Critico|Desastre Total)$")
    Impacto_Medio: Optional[str] = None

class ActualizarZonaAfectada(BaseModel):
    Nombre_Zona: Optional[str] = None
    Coordenadas: Optional[str] = None
    Tipo_Zona: Optional[str] = None
    Poblacion_Afectada: Optional[int] = None
    Nivel_Gravedad: Optional[str] = None
    Impacto_Medio: Optional[str] = None

# Modelos para RECURSOS
class CrearRecurso(BaseModel):
    Nombre_Recurso: str = Field(..., max_length=100)
    Categoria: str = Field(..., pattern="^(Viveres|Herramientas|Medico|Transporte)$")
    Cantidad_Disponible: int = Field(default=0)
    Ubicacion_Almacen: Optional[str] = None

class ActualizarRecurso(BaseModel):
    Nombre_Recurso: Optional[str] = None
    Categoria: Optional[str] = None
    Cantidad_Disponible: Optional[int] = None
    Ubicacion_Almacen: Optional[str] = None

# Modelos para REPORTE
class CrearReporte(BaseModel):
    Lugar: Optional[str] = None
    ID_Voluntario: Optional[int] = None
    ID_Zona_Afectada: Optional[int] = None
    Estatus: str = Field("Pendiente", pattern="^(Pendiente|Validado|En Proceso|Finalizado)$")
    Prioridad: str = Field("Media", pattern="^(Baja|Media|Alta|Critica)$")
    Descripcion_Emergencia: Optional[str] = None

class ActualizarReporte(BaseModel):
    Lugar: Optional[str] = None
    Estatus: Optional[str] = None
    Prioridad: Optional[str] = None
    Descripcion_Emergencia: Optional[str] = None

# Modelos para VOLUNTARIO
class CrearVoluntario(BaseModel):
    ID_Usuario: int
    Nivel_Experiencia: Optional[str] = None
    Estatus: str = Field("Activo", pattern="^(Activo|Inactivo|En Mision)$")
    Horario_disponibilidad: str

class ActualizarVoluntario(BaseModel):
    Nivel_Experiencia: Optional[str] = None
    Estatus: Optional[str] = None
    Horario_disponibilidad: Optional[str] = None

# Modelos para ALERTAS
class CrearAlerta(BaseModel):
    Titulo: str = Field(..., max_length=150)
    Mensaje: str
    Nivel_Alerta: str = Field("Informativa", pattern="^(Informativa|Precaucion|Evacuacion)$")
    ID_Emisor: Optional[int] = None

class ActualizarAlerta(BaseModel):
    Titulo: Optional[str] = None
    Mensaje: Optional[str] = None
    Nivel_Alerta: Optional[str] = None

# Modelos para CONOCIMIENTOS_TECNICOS
class CrearConocimiento(BaseModel):
    Nombre: str = Field(..., max_length=255)

# Modelos para ASIGNACION_RECURSOS
class CrearAsignacionRecurso(BaseModel):
    ID_Reporte: int
    ID_Recurso: int
    Cantidad_Asignada: int = Field(..., ge=1)

# Modelos para EVIDENCIA
class CrearEvidencia(BaseModel):
    Archivo_Ruta: Optional[str] = None
    Tipo_Evidencia_ID: Optional[int] = None
    ID_Reporte: Optional[int] = None

from sqlalchemy import Column, Integer, String, Text, DateTime, TIMESTAMP, Enum, LargeBinary, Date, Numeric, text
from sqlalchemy.orm import relationship
from app.data.db import Base
import datetime

# 1. TABLA: USUARIO
class Usuario(Base):
    __tablename__ = "usuario"

    ID = Column(Integer, primary_key=True, index=True)
    Nombre = Column(String(100), nullable=False)
    Telefono = Column(String(15), nullable=True)
    Email = Column(String(100), nullable=True, unique=True)
    Direccion = Column(Text, nullable=True)
    Contraseña = Column(String(128), nullable=False, default='temp_password')
    Rol = Column(Enum('Administrador', 'Especialista', 'Voluntario', 'Civil', name='rol_enum'), default='Civil')
    Fecha_Registro = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    FotoPerfil = Column(LargeBinary, nullable=True)

    # Relaciones
    curriculum = relationship("Curriculum", back_populates="usuario")
    voluntario = relationship("Voluntario", back_populates="usuario")
    alertas = relationship("Alertas", back_populates="emisor")

# 2. TABLA: BLOG
class Blog(Base):
    __tablename__ = "blog"

    ID_Blog = Column(Integer, primary_key=True, index=True)
    Titulo = Column(String(100), nullable=True)
    Descripcion = Column(String(100), nullable=True)

    # Relaciones
    contenido_blog = relationship("ContenidoBlog", back_populates="blog")

# 3. TABLA: CONOCIMIENTOS TÉCNICOS
class ConocimientosTecnicos(Base):
    __tablename__ = "conocimientos_tecnicos"

    ID = Column(Integer, primary_key=True, index=True)
    Nombre = Column(String(255), nullable=False)

    # Relaciones
    detalle_conocimientos = relationship("DetalleConocimientos", back_populates="conocimiento")

# 4. TABLA: PUESTOS
class Puestos(Base):
    __tablename__ = "puestos"

    ID = Column(Integer, primary_key=True, index=True)
    Tipo_Puesto = Column(String(100), nullable=True)

# 5. TABLA: TIPO EVIDENCIA
class TipoEvidencia(Base):
    __tablename__ = "tipo_evidencia"

    ID = Column(Integer, primary_key=True, index=True)
    Tipo_Evidencia = Column(String(100), nullable=True)

    # Relaciones
    evidencia = relationship("Evidencia", back_populates="tipo_evidencia_obj")

# 6. TABLA: ZONA AFECTADA
class ZonaAfectada(Base):
    __tablename__ = "zona_afectada"

    ID = Column(Integer, primary_key=True, index=True)
    Nombre_Zona = Column(String(255), nullable=True)
    Coordenadas = Column(Text, nullable=True)
    Tipo_Zona = Column(String(100), nullable=True)
    Poblacion_Afectada = Column(Integer, nullable=True)
    Nivel_Gravedad = Column(Enum('Estable', 'Moderado', 'Critico', 'Desastre Total', name='nivel_gravedad_enum'), default='Estable')
    Fecha_Evaluacion = Column(Date, nullable=True)
    Impacto_Medio = Column(Text, nullable=True)

    # Relaciones
    reporte = relationship("Reporte", back_populates="zona_afectada")

# 7. TABLA: RECURSOS
class Recursos(Base):
    __tablename__ = "recursos"

    ID = Column(Integer, primary_key=True, index=True)
    Nombre_Recurso = Column(String(100), nullable=False)
    Categoria = Column(Enum('Viveres', 'Herramientas', 'Medico', 'Transporte', name='categoria_enum'), nullable=False)
    Cantidad_Disponible = Column(Integer, default=0)
    Ubicacion_Almacen = Column(String(255), nullable=True)

    # Relaciones
    asignacion_recursos = relationship("AsignacionRecursos", back_populates="recurso")

# 8. TABLA: CONTENIDO BLOG
class ContenidoBlog(Base):
    __tablename__ = "contenido_blog"

    ID_Contenido_Blog = Column(Integer, primary_key=True, index=True)
    Contenido = Column(String(1000), nullable=True)
    ID_Blog = Column(Integer, nullable=True)

    # Relaciones (ForeignKey management in models)
    blog = relationship("Blog", back_populates="contenido_blog", foreign_keys=[ID_Blog])

# 9. TABLA: CURRICULUM
class Curriculum(Base):
    __tablename__ = "curriculum"

    ID = Column(Integer, primary_key=True, index=True)
    ID_Usuario = Column(Integer, nullable=True)
    Descripcion_CV = Column(Text, nullable=True)

    # Relaciones
    usuario = relationship("Usuario", back_populates="curriculum", foreign_keys=[ID_Usuario])
    detalle_conocimientos = relationship("DetalleConocimientos", back_populates="curriculum")

# 10. TABLA: VOLUNTARIO
class Voluntario(Base):
    __tablename__ = "voluntario"

    ID = Column(Integer, primary_key=True, index=True)
    ID_Usuario = Column(Integer, nullable=True)
    Nivel_Experiencia = Column(String(50), nullable=True)
    Estatus = Column(Enum('Activo', 'Inactivo', 'En Mision', name='voluntario_estatus_enum'), default='Activo')
    Horario_disponibilidad = Column(String(500), nullable=False)

    # Relaciones
    usuario = relationship("Usuario", back_populates="voluntario", foreign_keys=[ID_Usuario])
    reporte = relationship("Reporte", back_populates="voluntario")

# 11. TABLA: REPORTE
class Reporte(Base):
    __tablename__ = "reporte"

    ID = Column(Integer, primary_key=True, index=True)
    Fecha = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    Lugar = Column(String(255), nullable=True)
    ID_Voluntario = Column(Integer, nullable=True)
    ID_Zona_Afectada = Column(Integer, nullable=True)
    Estatus = Column(Enum('Pendiente', 'Validado', 'En Proceso', 'Finalizado', name='reporte_estatus_enum'), default='Pendiente')
    Prioridad = Column(Enum('Baja', 'Media', 'Alta', 'Critica', name='prioridad_enum'), default='Media')
    Descripcion_Emergencia = Column(Text, nullable=True)

    # Relaciones
    voluntario = relationship("Voluntario", back_populates="reporte", foreign_keys=[ID_Voluntario])
    zona_afectada = relationship("ZonaAfectada", back_populates="reporte", foreign_keys=[ID_Zona_Afectada])
    asignacion_recursos = relationship("AsignacionRecursos", back_populates="reporte")
    evidencia = relationship("Evidencia", back_populates="reporte")

# 12. TABLA: ASIGNACIÓN DE RECURSOS
class AsignacionRecursos(Base):
    __tablename__ = "asignacion_recursos"

    ID = Column(Integer, primary_key=True, index=True)
    ID_Reporte = Column(Integer, nullable=False)
    ID_Recurso = Column(Integer, nullable=False)
    Cantidad_Asignada = Column(Integer, nullable=False)
    Fecha_Entrega = Column(TIMESTAMP, default=datetime.datetime.utcnow)

    # Relaciones
    reporte = relationship("Reporte", back_populates="asignacion_recursos", foreign_keys=[ID_Reporte])
    recurso = relationship("Recursos", back_populates="asignacion_recursos", foreign_keys=[ID_Recurso])

# 13. TABLA: ALERTAS
class Alertas(Base):
    __tablename__ = "alertas"

    ID = Column(Integer, primary_key=True, index=True)
    Titulo = Column(String(150), nullable=False)
    Mensaje = Column(Text, nullable=False)
    Nivel_Alerta = Column(Enum('Informativa', 'Precaucion', 'Evacuacion', name='nivel_alerta_enum'), default='Informativa')
    Fecha_Emision = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    ID_Emisor = Column(Integer, nullable=True)

    # Relaciones
    emisor = relationship("Usuario", back_populates="alertas", foreign_keys=[ID_Emisor])

# 14. TABLA: DETALLE CONOCIMIENTOS
class DetalleConocimientos(Base):
    __tablename__ = "detalle_conocimientos"

    ID = Column(Integer, primary_key=True, index=True)
    ID_CV = Column(Integer, nullable=True)
    ID_Conocimiento = Column(Integer, nullable=True)
    Anios_Experiencia = Column(Integer, nullable=True)

    # Relaciones
    curriculum = relationship("Curriculum", back_populates="detalle_conocimientos", foreign_keys=[ID_CV])
    conocimiento = relationship("ConocimientosTecnicos", back_populates="detalle_conocimientos", foreign_keys=[ID_Conocimiento])

# 15. TABLA: EVIDENCIA
class Evidencia(Base):
    __tablename__ = "evidencia"

    ID = Column(Integer, primary_key=True, index=True)
    Archivo_Ruta = Column(Text, nullable=True)
    Fecha_Captura = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    Tipo_Evidencia_ID = Column(Integer, nullable=True)
    ID_Reporte = Column(Integer, nullable=True)

    # Relaciones
    tipo_evidencia_obj = relationship("TipoEvidencia", back_populates="evidencia", foreign_keys=[Tipo_Evidencia_ID])
    reporte = relationship("Reporte", back_populates="evidencia", foreign_keys=[ID_Reporte])

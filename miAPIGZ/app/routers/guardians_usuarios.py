from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.guardian_models import Usuario
from app.models.guardian_schemas import CrearUsuario, ActualizarUsuario, UsuarioResponse

routerU = APIRouter(
    prefix="/v1/usuarios",
    tags=['CRUD HTTP - Usuarios']
)

@routerU.get("/", response_model=dict)
async def obtener_usuarios(db: Session = Depends(get_db)):
    """Obtener todos los usuarios"""
    query_usuarios = db.query(Usuario).all()
    return {
        "status": "200",
        "total": len(query_usuarios),
        "data": query_usuarios
    }

@routerU.get("/{id}", response_model=dict)
async def obtener_usuario(id: int, db: Session = Depends(get_db)):
    """Obtener un usuario por ID"""
    usuario = db.query(Usuario).filter(Usuario.ID == id).first()
    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )
    return {
        "status": "200",
        "data": usuario
    }

@routerU.post("/", status_code=status.HTTP_201_CREATED, response_model=dict)
async def crear_usuario(usuario_data: CrearUsuario, db: Session = Depends(get_db)):
    """Crear un nuevo usuario"""
    # Verificar si el email ya existe
    if usuario_data.Email:
        usuario_existente = db.query(Usuario).filter(Usuario.Email == usuario_data.Email).first()
        if usuario_existente:
            raise HTTPException(
                status_code=400,
                detail="El email ya está registrado"
            )

    usuario_nuevo = Usuario(
        Nombre=usuario_data.Nombre,
        Telefono=usuario_data.Telefono,
        Email=usuario_data.Email,
        Direccion=usuario_data.Direccion,
        Contraseña=usuario_data.Contraseña,
        Rol=usuario_data.Rol
    )
    db.add(usuario_nuevo)
    db.commit()
    db.refresh(usuario_nuevo)

    return {
        "status": "201",
        "mensaje": "Usuario agregado correctamente",
        "data": usuario_nuevo
    }

@routerU.put("/{id}", response_model=dict)
async def actualizar_usuario(id: int, usuario_actualizado: ActualizarUsuario, db: Session = Depends(get_db)):
    """Actualizar un usuario"""
    usuario = db.query(Usuario).filter(Usuario.ID == id).first()
    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    if usuario_actualizado.Nombre:
        usuario.Nombre = usuario_actualizado.Nombre
    if usuario_actualizado.Telefono:
        usuario.Telefono = usuario_actualizado.Telefono
    if usuario_actualizado.Email:
        usuario.Email = usuario_actualizado.Email
    if usuario_actualizado.Direccion:
        usuario.Direccion = usuario_actualizado.Direccion
    if usuario_actualizado.Rol:
        usuario.Rol = usuario_actualizado.Rol

    db.commit()
    db.refresh(usuario)

    return {
        "status": "200",
        "mensaje": "Usuario actualizado correctamente",
        "data": usuario
    }

@routerU.delete("/{id}", response_model=dict)
async def eliminar_usuario(id: int, db: Session = Depends(get_db)):
    """Eliminar un usuario"""
    usuario = db.query(Usuario).filter(Usuario.ID == id).first()
    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    db.delete(usuario)
    db.commit()

    return {
        "status": "200",
        "mensaje": "Usuario eliminado correctamente",
        "data": usuario
    }

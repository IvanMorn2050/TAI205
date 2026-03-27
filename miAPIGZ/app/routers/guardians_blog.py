from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.guardian_models import Blog
from app.models.guardian_schemas import CrearBlog, ActualizarBlog

routerBl = APIRouter(
    prefix="/v1/blog",
    tags=['CRUD HTTP - Blog']
)

@routerBl.get("/", response_model=dict)
async def obtener_blogs(db: Session = Depends(get_db)):
    """Obtener todos los blogs"""
    query_blogs = db.query(Blog).all()
    return {
        "status": "200",
        "total": len(query_blogs),
        "data": query_blogs
    }

@routerBl.get("/{id}")
async def obtener_blog(id: int, db: Session = Depends(get_db)):
    """Obtener un blog por ID"""
    blog = db.query(Blog).filter(Blog.ID_Blog == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog no encontrado")
    return {
        "status": "200",
        "data": blog
    }

@routerBl.post("/", status_code=status.HTTP_201_CREATED)
async def crear_blog(blog_data: CrearBlog, db: Session = Depends(get_db)):
    """Crear un nuevo blog"""
    blog_nuevo = Blog(
        Titulo=blog_data.Titulo,
        Descripcion=blog_data.Descripcion
    )
    db.add(blog_nuevo)
    db.commit()
    db.refresh(blog_nuevo)
    return {
        "status": "201",
        "mensaje": "Blog creado correctamente",
        "data": blog_nuevo
    }

@routerBl.put("/{id}")
async def actualizar_blog(id: int, blog_actualizado: ActualizarBlog, db: Session = Depends(get_db)):
    """Actualizar un blog"""
    blog = db.query(Blog).filter(Blog.ID_Blog == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog no encontrado")

    for field, value in blog_actualizado.dict(exclude_unset=True).items():
        setattr(blog, field, value)

    db.commit()
    db.refresh(blog)
    return {
        "status": "200",
        "mensaje": "Blog actualizado correctamente",
        "data": blog
    }

@routerBl.delete("/{id}")
async def eliminar_blog(id: int, db: Session = Depends(get_db)):
    """Eliminar un blog"""
    blog = db.query(Blog).filter(Blog.ID_Blog == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog no encontrado")

    db.delete(blog)
    db.commit()
    return {
        "status": "200",
        "mensaje": "Blog eliminado correctamente"
    }

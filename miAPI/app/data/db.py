from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os 

#definimos la url de conexion con el contenedor
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://admin:123456@postgres:5432/DB_miapi"
)

#creamos un motor de conexion 
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush = False,
    bind = engine
)

#instaciamos la base declarativa del modelo
Base = declarative_base()

#funcion para manejo de sesiones por perticion
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close
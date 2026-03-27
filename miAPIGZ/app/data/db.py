from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

#definimos la url de conexion para MySQL
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:@localhost:3306/guardian_zero2"
)

#creamos un motor de conexion
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush = False,
    bind = engine
)

#instaciamos la base declarativa del modelo
Base = declarative_base()

#funcion para manejo de sesiones por peticion
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
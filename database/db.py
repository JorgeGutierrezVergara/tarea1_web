from sqlalchemy import create_engine, Column, Integer, BigInteger, String, ForeignKey, DateTime, Enum, TIMESTAMP, desc
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from contextlib import contextmanager
import json

DB_NAME = "tarea2"
DB_USERNAME = "cc5002"
DB_PASSWORD = "programacionweb"
DB_HOST = "localhost"
DB_PORT = 3306

DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=engine)


Base = declarative_base()

class Region(Base):
    __tablename__ = 'region' 
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)
    comunas = relationship('Comuna', backref='region', lazy=True)

class Comuna(Base):
    __tablename__ = 'comuna'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)
    region_id = Column(Integer, ForeignKey('region.id'), nullable=False) 
    
    actividades = relationship('Actividad', backref='comuna', lazy=True)


class Comentario(Base):
    __tablename__ = 'comentario'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(80), nullable=False)
    texto = Column(String(300), nullable=False)
    fecha = Column(TIMESTAMP, nullable=False)
    actividad_id = Column(Integer, ForeignKey('actividad.id'), nullable=False)

class Actividad(Base):
    __tablename__ = 'actividad'
    id = Column(Integer, primary_key=True, autoincrement=True)
    comuna_id = Column(Integer, ForeignKey('comuna.id'), nullable=False)
    sector = Column(String(100), nullable=True)
    nombre = Column(String(200), nullable=False) 
    email = Column(String(100), nullable=False)
    celular = Column(String(15), nullable=True)
    dia_hora_inicio = Column(DateTime, nullable=False)
    dia_hora_termino = Column(DateTime, nullable=True)
    descripcion = Column(String(500), nullable=True)

    comentarios = relationship('Comentario', backref='actividad', lazy=True, cascade="all, delete-orphan", order_by=desc(Comentario.fecha))

    fotos = relationship('Foto', backref='actividad_obj', lazy=True, cascade="all, delete-orphan")
    contactos = relationship('ContactarPor', backref='actividad_obj', lazy=True, cascade="all, delete-orphan")
    temas_asociados = relationship('ActividadTema', backref='actividad_obj', lazy=True, cascade="all, delete-orphan")

class Foto(Base):
    __tablename__ = 'foto'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ruta_archivo = Column(String(300), nullable=False)
    nombre_archivo = Column(String(300), nullable=False)
    actividad_id = Column(Integer, ForeignKey('actividad.id'), primary_key=True, nullable=False) # Parte de la PK compuesta

    def __repr__(self):
        return f"<Foto {self.id} para Actividad {self.actividad_id}: {self.nombre_archivo}>"

class ContactarPor(Base):
    __tablename__ = 'contactar_por'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(Enum('whatsapp', 'telegram', 'X', 'instagram', 'tiktok', 'otra'), nullable=False)
    identificador = Column(String(150), nullable=False)
    actividad_id = Column(Integer, ForeignKey('actividad.id'), primary_key=True, nullable=False)

class ActividadTema(Base):
    __tablename__ = 'actividad_tema'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tema = Column(Enum('música', 'deporte', 'ciencias', 'religión', 'política', 'tecnología', 'juegos', 'baile', 'comida', 'otro'), nullable=False)
    glosa_otro = Column(String(15), nullable=True) 
    actividad_id = Column(Integer, ForeignKey('actividad.id'), primary_key=True, nullable=False)


@contextmanager
def get_db_session(): 
    db_session = SessionLocal()
    try:
        yield db_session
        db_session.commit()
    except Exception:
        db_session.rollback()
        raise
    finally:
        db_session.close()

## Funciones base de datos

def obtener_todas_las_regiones_bd(db_session):
    try:
        regiones = db_session.query(Region).order_by(Region.nombre).all()
        regiones_data = [{'id': r.id, 'nombre': r.nombre} for r in regiones]
        return regiones_data
    except Exception as e:
        print(f"Error al obtener regiones: {e}")
        return []

def obtener_todas_las_comunas_bd(db_session):
    try:
        comunas = db_session.query(Comuna).order_by(Comuna.nombre).all()
        comunas_data = [{'id': c.id, 'nombre': c.nombre, 'region_id': c.region_id} for c in comunas]
        return comunas_data
    except Exception as e:
        print(f"Error al obtener comunas: {e}")
        return []

def crear_tablas_bd():
    Base.metadata.create_all(bind=engine)
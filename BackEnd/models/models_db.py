"""SQLAlchemy ORM models generated from Instalación.v0.1.sql

All tables are mapped as declarative classes with:
- __init__ methods for easy instantiation
- Foreign key relationships
- Proper type hints and constraints
"""
from database import db
from sqlalchemy.orm import relationship
from datetime import date, datetime
from decimal import Decimal
from typing import Optional, List
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, LargeBinary, ForeignKey, BigInteger, Boolean


# `Money` is a PostgreSQL-specific type; provide a safe fallback so the
# module can be imported in environments where the dialect type isn't available.
try:
    from sqlalchemy.dialects.postgresql import MONEY as Money
except Exception:
    # Fallback to Numeric for better type handling than String
    from sqlalchemy import Numeric
    Money = Numeric(precision=19, scale=2)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# ============ Core Tables ============

class Institucion(db.Model):
    __tablename__ = 'institucion'
    
    id = Column(Integer, primary_key=True)
    descripcion = Column(Text, nullable=False)
    pais = Column(String)
    
    def __init__(self, descripcion: str, pais: Optional[str] = None, id: Optional[Integer] = None):
        self.id = id
        self.descripcion = descripcion
        self.pais = pais
    
    # personas = relationship('Personal', back_populates='institucion_ref')
    revistas = relationship('Revista', back_populates='editorial_ref')
    articulos = relationship('Articulo', back_populates='editorial_ref')
    libros = relationship('Libro', back_populates='editorial_ref')
    contratos_adoptante = relationship('Contrato', back_populates='adoptante_ref', foreign_keys='Contrato.adoptante')
    contratos_demandante = relationship('Contrato', back_populates='demandante_ref', foreign_keys='Contrato.demandante')
    participaciones = relationship('Participacion', back_populates='institucion_ref', foreign_keys='Participacion.institucion')
    actividades_docentes = relationship('ActividadDocente', back_populates='institucion_ref')
    distinciones = relationship('Distincion', back_populates='institucion_ref')
    erogaciones = relationship('Erogacion', back_populates='institucion_ref')


class Documentacion(db.Model):
    __tablename__ = 'documentacion'
    
    id = Column(BigInteger, primary_key=True)
    binario = Column(LargeBinary)
    texto = Column(Text)
    
    def __init__(self, binario: Optional[bytes] = None, texto: Optional[str] = None, id: Optional[BigInteger] = None):
        self.id = id
        self.binario = binario
        self.texto = texto
    
    revistas = relationship('Revista', back_populates='documentacion_ref')
    articulos = relationship('Articulo', back_populates='documentacion_ref')
    libros = relationship('Libro', back_populates='documentacion_ref')



class LoginCredentials(db.Model):
    __tablename__ = 'login_credentials'
    
    email = Column(String, primary_key=True)
    clave = Column(LargeBinary, nullable=False)
    activo = Column(Boolean, default=True)

    def __init__(self, email: str, clave: str):
        self.email = email
        self.clave = clave
        self.activo = True


# Equipamiento is imported from models.equipamiento


class Revista(db.Model):
    __tablename__ = 'revista'
    
    id = Column(BigInteger, primary_key=True)
    nombre = Column(String, nullable=False)
    issn = Column(String, nullable=False)
    fecha = Column(Date, nullable=False)
    editorial = Column(Integer, ForeignKey('institucion.id'), nullable=False)
    numero = Column(String)
    documentacion = Column(BigInteger, ForeignKey('documentacion.id'), nullable=False)
    
    def __init__(self, nombre: str, issn: str, fecha: date, editorial: int, documentacion: int,
                 numero: Optional[str] = None, id: Optional[BigInteger] = None):
        self.id = id
        self.nombre = nombre
        self.issn = issn
        self.fecha = fecha
        self.editorial = editorial
        self.numero = numero
        self.documentacion = documentacion
    
    editorial_ref = relationship('Institucion', back_populates='revistas')
    documentacion_ref = relationship('Documentacion', back_populates='revistas')
    proyecto_revistas = relationship('ProyectoRevista', back_populates='revista_ref')


class Articulo(db.Model):
    __tablename__ = 'articulo'
    
    id = Column(BigInteger, primary_key=True)
    nombre = Column(String, nullable=False)
    issn = Column(String, nullable=False)
    fecha = Column(Date, nullable=False)
    editorial = Column(Integer, ForeignKey('institucion.id'), nullable=False)
    numero = Column(String)
    pais = Column(String)
    copia = Column(String)
    documentacion = Column(BigInteger, ForeignKey('documentacion.id'), nullable=False)
    
    def __init__(self, nombre: str, issn: str, fecha: date, editorial: int, documentacion: int,
                 numero: Optional[str] = None, pais: Optional[str] = None, copia: Optional[str] = None,
                 id: Optional[BigInteger] = None):
        self.id = id
        self.nombre = nombre
        self.issn = issn
        self.fecha = fecha
        self.editorial = editorial
        self.numero = numero
        self.pais = pais
        self.copia = copia
        self.documentacion = documentacion
    
    editorial_ref = relationship('Institucion', back_populates='articulos')
    documentacion_ref = relationship('Documentacion', back_populates='articulos')
    proyecto_articulos = relationship('ProyectoArticulo', back_populates='articulo_ref')


class Libro(db.Model):
    __tablename__ = 'libro'
    
    id = Column(BigInteger, primary_key=True)
    nombre = Column(String)
    isbn = Column(String, nullable=False)
    fecha = Column(Date, nullable=False)
    editorial = Column(Integer, ForeignKey('institucion.id'), nullable=False)
    tomo = Column(String)
    capitulo = Column(String)
    pais = Column(String)
    documentacion = Column(BigInteger, ForeignKey('documentacion.id'), nullable=False)
    
    def __init__(self, isbn: str, fecha: date, editorial: int, documentacion: int, nombre: Optional[str] = None,
                 tomo: Optional[str] = None, capitulo: Optional[str] = None, pais: Optional[str] = None,
                 id: Optional[BigInteger] = None):
        self.id = id
        self.nombre = nombre
        self.isbn = isbn
        self.fecha = fecha
        self.editorial = editorial
        self.tomo = tomo
        self.capitulo = capitulo
        self.pais = pais
        self.documentacion = documentacion
    
    editorial_ref = relationship('Institucion', back_populates='libros')
    documentacion_ref = relationship('Documentacion', back_populates='libros')
    proyecto_libros = relationship('ProyectoLibro', back_populates='libro_ref')


class ProyectoLibro(db.Model):
    __tablename__ = 'proyecto_libro'
    
    id = Column(BigInteger, primary_key=True)
    proyecto = Column(Integer, ForeignKey('proyecto.id'), nullable=False)
    libro = Column(BigInteger, ForeignKey('libro.id'), nullable=False)
    
    def __init__(self, proyecto: int, libro: int, id: Optional[BigInteger] = None):
        self.id = id
        self.proyecto = proyecto
        self.libro = libro
    
    proyecto_ref = relationship('Proyecto', back_populates='proyecto_libros')
    libro_ref = relationship('Libro', back_populates='proyecto_libros')


class ProyectoRevista(db.Model):
    __tablename__ = 'proyecto_revista'
    
    id = Column(BigInteger, primary_key=True)
    proyecto = Column(Integer, ForeignKey('proyecto.id'), nullable=False)
    revista = Column(BigInteger, ForeignKey('revista.id'), nullable=False)
    
    def __init__(self, proyecto: int, revista: int, id: Optional[BigInteger] = None):
        self.id = id
        self.proyecto = proyecto
        self.revista = revista
    
    proyecto_ref = relationship('Proyecto', back_populates='proyecto_revistas')
    revista_ref = relationship('Revista', back_populates='proyecto_revistas')


class ProyectoArticulo(db.Model):
    __tablename__ = 'proyecto_articulo'
    
    id = Column(BigInteger, primary_key=True)
    proyecto = Column(Integer, ForeignKey('proyecto.id'), nullable=False)
    articulo = Column(BigInteger, ForeignKey('articulo.id'), nullable=False)
    
    def __init__(self, proyecto: int, articulo: int, id: Optional[BigInteger] = None):
        self.id = id
        self.proyecto = proyecto
        self.articulo = articulo
    
    proyecto_ref = relationship('Proyecto', back_populates='proyecto_articulos')
    articulo_ref = relationship('Articulo', back_populates='proyecto_articulos')


# Bibliografia is imported from models.bibliografia


class Contrato(db.Model):
    __tablename__ = 'contrato'
    
    id = Column(BigInteger, primary_key=True)
    adoptante = Column(Integer, ForeignKey('institucion.id'), nullable=False)
    demandante = Column(Integer, ForeignKey('institucion.id'))
    tipo = Column(Integer, ForeignKey('tipo_contrato.id'), nullable=False)
    monto = Column(Money, nullable=False)
    denominacion = Column(String, nullable=False)
    descripcion = Column(Text)
    
    def __init__(self, adoptante: int, tipo: int, monto, denominacion: str, demandante: Optional[int] = None,
                 descripcion: Optional[str] = None, id: Optional[BigInteger] = None):
        self.id = id
        self.adoptante = adoptante
        self.demandante = demandante
        self.tipo = tipo
        self.monto = monto
        self.denominacion = denominacion
        self.descripcion = descripcion
    
    adoptante_ref = relationship('Institucion', back_populates='contratos_adoptante', foreign_keys=[adoptante])
    demandante_ref = relationship('Institucion', back_populates='contratos_demandante', foreign_keys=[demandante])
    # tipo_contrato_ref = relationship('TipoContrato', back_populates='contratos')


class Participacion(db.Model):
    __tablename__ = 'participacion'
    
    id = Column(BigInteger, primary_key=True)
    grupo = Column(Integer, ForeignKey('grupo.id'), nullable=False)
    personal = Column(Integer)
    rol = Column(BigInteger, ForeignKey('rol_participacion.id'), nullable=False)
    institucion = Column(Integer, ForeignKey('institucion.id'), nullable=False)
    
    def __init__(self, grupo: int, rol: int, institucion: int, personal: Optional[int] = None,
                 id: Optional[BigInteger] = None):
        self.id = id
        self.grupo = grupo
        self.personal = personal
        self.rol = rol
        self.institucion = institucion
    
    grupo_ref = relationship('Grupo', back_populates='participaciones')
    # rol_participacion_ref = relationship('RolParticipacion', back_populates='participaciones')
    institucion_ref = relationship('Institucion', back_populates='participaciones', foreign_keys=[institucion])
    participacion_personas = relationship('ParticipacionPersona', back_populates='participacion_ref')


class ParticipacionPersona(db.Model):
    __tablename__ = 'participacion_persona'
    
    id = Column(BigInteger, primary_key=True)
    participacion = Column(BigInteger, ForeignKey('participacion.id'), nullable=False)
    persona = Column(Integer, ForeignKey('persona.id'), nullable=False)
    
    def __init__(self, participacion: int, persona: int, id: Optional[BigInteger] = None):
        self.id = id
        self.participacion = participacion
        self.persona = persona
    
    participacion_ref = relationship('Participacion', back_populates='participacion_personas')
    # persona_ref = relationship('Persona', back_populates='participacion_personas')

class Distincion(db.Model):
    __tablename__ = 'distincion'
    
    id = Column(BigInteger, primary_key=True)
    proyecto = Column(Integer, ForeignKey('proyecto.id'), nullable=False)
    persona = Column(Integer, ForeignKey('persona.id'))
    grupo = Column(Integer, ForeignKey('grupo.id'))
    fecha = Column(Date, nullable=False)
    institucion = Column(Integer, ForeignKey('institucion.id'), nullable=False)
    
    def __init__(self, proyecto: int, fecha: date, institucion: int, persona: Optional[int] = None,
                 grupo: Optional[int] = None, id: Optional[BigInteger] = None):
        self.id = id
        self.proyecto = proyecto
        self.persona = persona
        self.grupo = grupo
        self.fecha = fecha
        self.institucion = institucion
    
    proyecto_ref = relationship('Proyecto', back_populates='distinciones')
    # persona_ref = relationship('Persona', back_populates='distinciones', foreign_keys=[persona])
    grupo_ref = relationship('Grupo', back_populates='distinciones', foreign_keys=[grupo])
    institucion_ref = relationship('Institucion', back_populates='distinciones')


class Erogacion(db.Model):
    __tablename__ = 'erogacion'
    
    id = Column(BigInteger, primary_key=True)
    institucion = Column(Integer, ForeignKey('institucion.id'), nullable=False)
    tipo = Column(Integer, ForeignKey('tipo_erogacion.id'), nullable=False)
    fecha = Column(DateTime, nullable=False)
    descripción = Column(Text)
    monto = Column(Money, nullable=False)
    comprobante = Column(LargeBinary, nullable=False)
    
    def __init__(self, institucion: int, tipo: int, fecha: datetime, monto, comprobante: bytes,
                 descripción: Optional[str] = None, id: Optional[BigInteger] = None):
        self.id = id
        self.institucion = institucion
        self.tipo = tipo
        self.fecha = fecha
        self.descripción = descripción
        self.monto = monto
        self.comprobante = comprobante
    
    institucion_ref = relationship('Institucion', back_populates='erogaciones')
    # tipo_erogacion_ref = relationship('TipoErogacion', back_populates='erogaciones')

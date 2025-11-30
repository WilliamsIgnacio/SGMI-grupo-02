from database import db
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, LargeBinary, ForeignKey, BigInteger, Boolean
from sqlalchemy.orm import relationship
from datetime import date, datetime
from decimal import Decimal
from typing import Optional, List

class Grupo(db.Model):
    __tablename__ = 'grupo'
    
    id = Column(Integer, primary_key=True)
    sigla = Column(String, nullable=False)
    nombre = Column(String, nullable=False)
    objetivos = Column(Text, nullable=False)
    organigrama = Column(String)
    consejo_ejecutivo = Column(String)
    unidad_academica = Column(String)
    
    def __init__(self, sigla: str, nombre: str, objetivos: str, organigrama: Optional[str] = None,
                 consejo_ejecutivo: Optional[str] = None, unidad_academica: Optional[str] = None,
                 id: Optional[Integer] = None):
        self.id = id
        self.sigla = sigla
        self.nombre = nombre
        self.objetivos = objetivos
        self.organigrama = organigrama
        self.consejo_ejecutivo = consejo_ejecutivo
        self.unidad_academica = unidad_academica
    
    proyectos = relationship('Proyecto', back_populates='grupo_ref')
    persona_grupos = relationship('PersonaGrupo', back_populates='grupo_ref', cascade="all, delete-orphan")
    equipamientos = relationship('Equipamiento', back_populates='grupo_ref')
    bibliografias = relationship('Bibliografia', back_populates='grupo_ref')
    participaciones = relationship('Participacion', back_populates='grupo_ref')
    distinciones = relationship('Distincion', back_populates='grupo_ref', foreign_keys='Distincion.grupo')

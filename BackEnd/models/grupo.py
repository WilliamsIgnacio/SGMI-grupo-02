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
    correo_electronico = Column(String)
    director = Column(String)
    vicedirector = Column(String)
    consejo_ejecutivo = Column(String)
    unidad_academica = Column(String)
    activo = Column(Boolean)
    
    

    proyectos = relationship('Proyecto', back_populates='grupo_ref')
    persona_grupos = relationship('PersonaGrupo', back_populates='grupo_ref', cascade="all, delete-orphan")
    equipamientos = relationship('Equipamiento', back_populates='grupo_ref')
    bibliografias = relationship('Bibliografia', back_populates='grupo_ref')
    participaciones = relationship('Participacion', back_populates='grupo_ref')
    distinciones = relationship('Distincion', back_populates='grupo_ref', foreign_keys='Distincion.grupo')


    def to_dict(self):
        return {
            'id': self.id,
            'sigla': self.sigla,
            'nombre': self.nombre,
            'objetivos': self.objetivos,
            'organigrama': self.organigrama,
            'correoElectronico': self.correo_electronico,
            'director': self.director,
            'vicedirector': self.vicedirector,
            'consejo_ejecutivo': self.consejo_ejecutivo,
            'unidad_academica': self.unidad_academica,
            'activo': self.activo
        }
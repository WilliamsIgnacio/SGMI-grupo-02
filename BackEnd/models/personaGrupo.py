from database import db
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, LargeBinary, ForeignKey, BigInteger, Boolean
from sqlalchemy.orm import relationship
from datetime import date, datetime
from decimal import Decimal
from typing import Optional, List
try:
    from sqlalchemy.dialects.postgresql import MONEY as Money
except Exception:
    # Fallback to String for environments without PostgreSQL dialect installed.
    Money = String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


class PersonaGrupo(db.Model):
    __tablename__ = 'persona_grupo'
    
    id = Column(BigInteger, primary_key=True)
    grupo = Column(Integer, ForeignKey('grupo.id'), nullable=False)
    persona = Column(Integer, ForeignKey('persona.id'), nullable=False)
    institucion = Column(Integer, ForeignKey('institucion.id'), nullable=False)
    rol = Column(BigInteger, ForeignKey('rol_grupo.id'), nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date)
    
    def __init__(self, grupo: int, persona: int, institucion: int, rol: int, fecha_inicio: date,
                 fecha_fin: Optional[date] = None, id: Optional[BigInteger] = None):
        self.id = id
        self.grupo = grupo
        self.persona = persona
        self.institucion = institucion
        self.rol = rol
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
    
    grupo_ref = relationship('Grupo', back_populates='persona_grupos')
    # persona_ref = relationship('Persona', back_populates='persona_grupos')
    institucion_ref = relationship('Institucion', back_populates='persona_grupos', foreign_keys=[institucion])
    # rol_grupo_ref = relationship('RolGrupo', back_populates='persona_grupos')

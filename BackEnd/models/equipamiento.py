"""Modelo Equipamiento - Equipamiento e infraestructura del grupo de investigación"""
from database import db
from datetime import date
from typing import Optional
from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

try:
    from sqlalchemy.dialects.postgresql import MONEY as Money
except Exception:
    Money = String


class Equipamiento(db.Model):
    __tablename__ = 'equipamiento'
    
    id = Column(BigInteger, primary_key=True)
    denominacion = Column(String, nullable=False)
    fechaIngreso = Column(Date, nullable=False)
    monto = Column(Money, nullable=False)
    descripción = Column(Text)
    grupo = Column(Integer, ForeignKey('grupo.id'), nullable=False)
    actividad = Column(BigInteger)
    proyecto = Column(BigInteger)
    
    def __init__(self, denominacion: str, fechaIngreso: date, monto, grupo: int,
                 descripción: Optional[str] = None, actividad: Optional[BigInteger] = None,
                 proyecto: Optional[BigInteger] = None, id: Optional[BigInteger] = None):
        self.id = id
        self.denominacion = denominacion
        self.fechaIngreso = fechaIngreso
        self.monto = monto
        self.descripción = descripción
        self.grupo = grupo
        self.actividad = actividad
        self.proyecto = proyecto
    
    grupo_ref = relationship('Grupo', back_populates='equipamientos')

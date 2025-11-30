"""Modelo Bibliografia - Bibliografía del grupo de investigación"""
from database import db
from datetime import date
from typing import Optional
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship


class Bibliografia(db.Model):
    __tablename__ = 'bibliografia'
    
    id = Column(Integer, primary_key=True)
    titulo = Column(String, nullable=False)
    autores = Column(String, nullable=False)
    editorial = Column(String, nullable=False)
    fecha = Column(Date, nullable=False)
    grupo = Column(Integer, ForeignKey('grupo.id'), nullable=False)
    
    def __init__(self, titulo: str, autores: str, editorial: str, fecha: date, grupo: int,
                 id: Optional[Integer] = None):
        self.id = id
        self.titulo = titulo
        self.autores = autores
        self.editorial = editorial
        self.fecha = fecha
        self.grupo = grupo
    
    grupo_ref = relationship('Grupo', back_populates='bibliografias')

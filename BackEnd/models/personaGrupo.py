from database import db
from sqlalchemy import Column, Integer, String, Date, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


class PersonaGrupo(db.Model):
    __tablename__ = 'persona_grupo'
    
    id = Column(BigInteger, primary_key=True)
    grupo = Column(Integer, ForeignKey('grupo.id'), nullable=False)
    persona = Column(Integer, ForeignKey('persona.id'), nullable=False)

    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date)
    
    grupo_ref = relationship('Grupo', back_populates='persona_grupos')
    persona_ref = relationship('Personal', back_populates='persona_grupos')

    def to_dict(self):
        return {
            'id': self.id,
            'grupo': self.grupo,
            'persona': {
                'id': self.persona,
                'nombre': self.persona_ref.nombre,
                'apellido': self.persona_ref.apellido,
                'horas': self.persona_ref.horas,
                'object_type': self.persona_ref.__class__.__name__
            },
            'fecha_inicio': self.fecha_inicio,
            'fecha_fin': self.fecha_fin,
        }


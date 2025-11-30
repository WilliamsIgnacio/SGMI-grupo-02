from database import db
from sqlalchemy.orm import relationship

class Proyecto(db.Model):
    __tablename__ = 'proyecto'

    id = db.Column(db.Integer, primary_key=True)

    codigo = db.Column(db.String(50), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200), nullable=True)
    tipo = db.Column(db.String(50), nullable=False)
    logros = db.Column(db.String(200), nullable=True)
    dificultades = db.Column(db.String(200), nullable=True)

    fechaInicio = db.Column('fecha_inicio', db.Date, nullable=False)
    fechaFin = db.Column('fecha_fin', db.Date, nullable=True)

    grupoId = db.Column('grupo', db.Integer, db.ForeignKey('grupo.id'))
    
    # Relationships
    grupo_ref = relationship('Grupo', back_populates='proyectos')
    proyecto_libros = relationship('ProyectoLibro', back_populates='proyecto_ref')
    proyecto_revistas = relationship('ProyectoRevista', back_populates='proyecto_ref')
    proyecto_articulos = relationship('ProyectoArticulo', back_populates='proyecto_ref')
    distinciones = relationship('Distincion', back_populates='proyecto_ref', foreign_keys='Distincion.proyecto')

    def to_dict(self):
        return {
            'id': self.id,
            'codigo': self.codigo,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'tipo': self.tipo,
            'logros': self.logros,
            'dificultades': self.dificultades,
            'fechaInicio': self.fechaInicio.isoformat() if self.fechaInicio else None,
            'fechaFin': self.fechaFin.isoformat() if self.fechaFin else None,
            'grupoId': self.grupoId
        }
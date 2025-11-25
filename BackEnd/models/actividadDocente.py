from app import db

class ActividadDocente(db.Model):
    __tablename__ = 'actividad_docente'

    id = db.Column(db.Integer, primary_key=True)
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)
    rol = db.Column(db.String(50)) 
    
    # FK
    personal_id = db.Column('persona', db.Integer, db.ForeignKey('persona.id'))
    institucion_id = db.Column('institucion', db.Integer) 

    def to_dict(self):
        return {
            'id': self.id,
            'fecha_inicio': self.fecha_inicio.isoformat() if self.fecha_inicio else None,
            'fecha_fin': self.fecha_fin.isoformat() if self.fecha_fin else None,
            'rol': self.rol,
            'persona_id': self.persona_id,
            'institucion_id': self.institucion_id
        }
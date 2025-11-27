from app import db

class ActividadDocente(db.Model):
    __tablename__ = 'actividad_docente'

    id = db.Column(db.Integer, primary_key=True)
    fechaInicio = db.Column(db.Date)
    fechaFin = db.Column(db.Date)
    rol = db.Column(db.String(50)) 
    
    # FK
    personalId = db.Column('persona', db.Integer, db.ForeignKey('persona.id'))
    institucionId = db.Column('institucion', db.Integer) 

    def to_dict(self):
        return {
            'id': self.id,
            'fechaInicio': self.fechaInicio.isoformat() if self.fechaInicio else None,
            'fechaFin': self.fechaFin.isoformat() if self.fechaFin else None,
            'rol': self.rol,
            'personaId': self.personalId,
            'institucionId': self.institucionId
        }
from database import db

class GradoAcademico(db.Model):
    __tablename__ = 'grado_academico'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre
        }
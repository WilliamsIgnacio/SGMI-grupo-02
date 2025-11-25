from app import db

class Personal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    horas = db.Column(db.Integer, nullable=False)

    # FK
    gradoAcademicoId = db.Column('grado_academico', db.Integer, db.ForeignKey('grado_academico.id'))
    institucion = db.Column(db.Integer)

    #Relaciones
    grado = db.relationship('GradoAcademico', backref='personales')
    actividades = db.relationship('ActividadDocente', backref='personal', lazy=True)

    #OBJ Type
    objectType = db.Column(db.String(50))
    
    #Investigador
    categoria = db.Column(db.String(50), nullable=True)
    incentivo = db.Column(db.String(50), nullable=True)
    dedicacion = db.Column(db.String(50), nullable=True)

    #Profesional
    especialidad = db.Column(db.String(100), nullable=True)
    descripcion = db.Column(db.String(200), nullable=True)

    #Becario, Soporte o Visitante
    rol = db.Column(db.String(50), nullable=True)

    __mapper_args__ = {
        'polymorphic_identity':'personal',
        'polymorphic_on':objectType
    }

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'horas': self.horas,
            'gradoAcademico': self.gradoAcademico,
            'institucion': self.institucion,
            'objectType': self.objectType,
            'categoria': self.categoria,
            'incentivo': self.incentivo,
            'dedicacion': self.dedicacion,
            'especialidad': self.especialidad,
            'descripcion': self.descripcion
        }
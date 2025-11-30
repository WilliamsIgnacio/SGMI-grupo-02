from database import db

class Personal(db.Model):
    __tablename__ = 'persona'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    horas = db.Column(db.Integer, nullable=False)

    # FK
    gradoAcademicoId = db.Column('grado_academico', db.Integer, db.ForeignKey('grado_academico.id'))
    institucionId = db.Column('institucion', db.Integer)

    #Relaciones
    grado = db.relationship('GradoAcademico', backref='personales')
    actividadesDocente = db.relationship('ActividadDocente', backref='personal', lazy=True)
    persona_grupos = db.relationship('PersonaGrupo', back_populates='persona_ref', cascade="all, delete-orphan")

    #OBJ Type
    objectType = db.Column('object_type', db.String(50))
    
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
            'gradoAcademicoId': self.gradoAcademicoId,
            'institucionId': self.institucionId,
            'objectType': self.objectType,
        }
    
class Becario(Personal):
    __mapper_args__ = {
        'polymorphic_identity': 'becario'
    }
    
    def to_dict(self):
        data = super().to_dict()
        data['rol'] = self.rol
        return data
    
class Soporte(Personal):
    __mapper_args__ = {
        'polymorphic_identity': 'soporte'
    }
    
    def to_dict(self):
        data = super().to_dict()
        data['rol'] = self.rol
        return data
    
class Visitante(Personal):
    __mapper_args__ = {
        'polymorphic_identity': 'visitante'
    }
    
    def to_dict(self):
        data = super().to_dict()
        data['rol'] = self.rol
        return data

class Investigador(Personal):
    __mapper_args__ = {
        'polymorphic_identity': 'investigador'
    }

    def to_dict(self):
        data = super().to_dict()
        data['categoria'] = self.categoria
        data['incentivo'] = self.incentivo
        data['dedicacion'] = self.dedicacion
        return data

class Profesional(Personal):
    __mapper_args__ = {
        'polymorphic_identity': 'profesional'
    }
    
    def to_dict(self):
        data = super().to_dict()
        data['especialidad'] = self.especialidad
        data['descripcion'] = self.descripcion
        return data

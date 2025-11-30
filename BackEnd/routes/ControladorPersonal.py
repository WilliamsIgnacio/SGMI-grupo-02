"""Controlador de Personal - API endpoints for managing personal (staff/researchers).

Uses Flask-SQLAlchemy models from models package to handle CRUD operations
on Personal, ActividadDocente, and related entities.
"""

from datetime import date
from flask import Blueprint, request, jsonify
from flask.views import MethodView
from database import db
from models.personal import Personal, Investigador, Profesional, Becario, Soporte, Visitante
from models.actividadDocente import ActividadDocente
from models.gradoAcademico import GradoAcademico
from models.models_db import Institucion, LoginCredentials

# Create blueprint for personal management routes
personal_bp = Blueprint('personal_bp', __name__)


class ControladorPersonal(MethodView):
    """Controller for Personal (Persona) CRUD operations."""

    def crearPersonal(self, data):
        """Create a new Personal entry with polymorphic type."""
        grado = data.get('gradoAcademicoId')
        if grado:
            gradoObj = GradoAcademico.query.filter_by(id=grado).first()
            if not gradoObj:
                raise ValueError("Grado Académico no encontrado")
        
        institucion = data.get('institucionId')
        if institucion:
            institucionObj = Institucion.query.filter_by(id=institucion).first()
            if not institucionObj:
                raise ValueError("Institución no encontrada")
        
        object_type = data.get('objectType')
        
        try:
            # Create appropriate subclass based on object_type
            if object_type == 'investigador':
                nuevoPersonal = Investigador(
                    nombre=data.get('nombre'),
                    apellido=data.get('apellido'),
                    horas=data.get('horas'),
                    gradoAcademicoId=data.get('gradoAcademicoId'),
                    institucionId=data.get('institucionId'),
                    categoria=data.get('categoria'),
                    incentivo=data.get('incentivo'),
                    dedicacion=data.get('dedicacion')
                )
            elif object_type == 'profesional':
                nuevoPersonal = Profesional(
                    nombre=data.get('nombre'),
                    apellido=data.get('apellido'),
                    horas=data.get('horas'),
                    gradoAcademicoId=data.get('gradoAcademicoId'),
                    institucionId=data.get('institucionId'),
                    especialidad=data.get('especialidad'),
                    descripcion=data.get('descripcion')
                )
            elif object_type == 'becario':
                nuevoPersonal = Becario(
                    nombre=data.get('nombre'),
                    apellido=data.get('apellido'),
                    horas=data.get('horas'),
                    gradoAcademicoId=data.get('gradoAcademicoId'),
                    institucionId=data.get('institucionId'),
                    rol=data.get('rol')
                )
            elif object_type == 'soporte':
                nuevoPersonal = Soporte(
                    nombre=data.get('nombre'),
                    apellido=data.get('apellido'),
                    horas=data.get('horas'),
                    gradoAcademicoId=data.get('gradoAcademicoId'),
                    institucionId=data.get('institucionId'),
                    rol=data.get('rol')
                )
            elif object_type == 'visitante':
                nuevoPersonal = Visitante(
                    nombre=data.get('nombre'),
                    apellido=data.get('apellido'),
                    horas=data.get('horas'),
                    gradoAcademicoId=data.get('gradoAcademicoId'),
                    institucionId=data.get('institucionId'),
                    rol=data.get('rol')
                )
            else:
                # Generic Personal
                nuevoPersonal = Personal(
                    nombre=data.get('nombre'),
                    apellido=data.get('apellido'),
                    horas=data.get('horas'),
                    gradoAcademicoId=data.get('gradoAcademicoId'),
                    institucionId=data.get('institucionId')
                )
            
            db.session.add(nuevoPersonal)
            db.session.flush()  # Get ID without committing
            
            # Create LoginCredentials if email provided
            if data.get('email'):
                loginCreds = LoginCredentials(
                    email=data['email'],
                    clave=data.get('clave', ''),
                    persona=nuevoPersonal.id,
                    activo=True
                )
                db.session.add(loginCreds)
            
            db.session.commit()
            return nuevoPersonal
        except Exception as e:
            db.session.rollback()
            raise e

    def modificarPersonal(self, id, data):
        """Update an existing Personal entry."""
        personal = Personal.query.filter_by(id=id).first()
        if not personal:
            return None
        
        try:
            if 'gradoAcademicoId' in data:
                grado = data.get('gradoAcademicoId')
                if grado:
                    gradoObj = GradoAcademico.query.filter_by(id=grado).first()
                    if not gradoObj:
                        raise ValueError("Grado Académico no encontrado")
                    personal.gradoAcademicoId = grado
            
            if 'institucionId' in data:
                institucion = data.get('institucionId')
                if institucion:
                    institucionObj = Institucion.query.filter_by(id=institucion).first()
                    if not institucionObj:
                        raise ValueError("Institución no encontrada")
                    personal.institucionId = institucion
            
            # Update common fields
            personal.nombre = data.get('nombre', personal.nombre)
            personal.apellido = data.get('apellido', personal.apellido)
            personal.horas = data.get('horas', personal.horas)
            
            # Update polymorphic fields based on type
            if personal.objectType == 'investigador':
                personal.categoria = data.get('categoria', personal.categoria)
                personal.incentivo = data.get('incentivo', personal.incentivo)
                personal.dedicacion = data.get('dedicacion', personal.dedicacion)
            elif personal.objectType == 'profesional':
                personal.especialidad = data.get('especialidad', personal.especialidad)
                personal.descripcion = data.get('descripcion', personal.descripcion)
            elif personal.objectType in ['becario', 'soporte', 'visitante']:
                personal.rol = data.get('rol', personal.rol)
            
            db.session.commit()
            return personal
        except Exception as e:
            db.session.rollback()
            raise e

    def eliminarPersonal(self, id):
        """Delete a Personal entry."""
        personal = Personal.query.filter_by(id=id).first()
        if not personal:
            return False
        
        try:
            db.session.delete(personal)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e

    # HTTP Methods
    def get(self, id=None):
        """GET method for listing all or retrieving one Personal."""
        if id is None:
            # List all with optional filtering
            object_type = request.args.get('objectType')
            query = Personal.query
            if object_type:
                query = query.filter_by(objectType=object_type)
            
            personal_list = query.all()
            return jsonify([p.to_dict() for p in personal_list]), 200
        else:
            # Get single Personal
            personal = Personal.query.filter_by(id=id).first()
            if personal:
                return jsonify(personal.to_dict()), 200
            else:
                return jsonify({"error": "Personal no encontrado"}), 404

    def post(self):
        """POST method for creating new Personal."""
        data = request.get_json()
        try:
            nuevoPersonal = self.crearPersonal(data)
            return jsonify({
                "mensaje": "Personal creado exitosamente",
                "personal": nuevoPersonal.to_dict()
            }), 201
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
        except Exception as e:
            return jsonify({"error": "Error al crear: " + str(e)}), 500

    def put(self, id):
        """PUT method for updating Personal."""
        data = request.get_json()
        try:
            personal = self.modificarPersonal(id, data)
            if not personal:
                return jsonify({"error": "Personal no encontrado"}), 404
            return jsonify({
                "mensaje": "Personal actualizado exitosamente",
                "personal": personal.to_dict()
            }), 200
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
        except Exception as e:
            return jsonify({"error": "Error al modificar: " + str(e)}), 500

    def delete(self, id):
        """DELETE method for deleting Personal."""
        try:
            exito = self.eliminarPersonal(id)
            if not exito:
                return jsonify({"error": "Personal no encontrado"}), 404
            return jsonify({"mensaje": "Personal eliminado exitosamente"}), 200
        except Exception as e:
            return jsonify({"error": "Error al eliminar: " + str(e)}), 500


class ControladorActividadDocente(MethodView):
    """Controller for ActividadDocente CRUD operations."""

    def get(self, persona_id, actividad_id=None):
        """GET actividades docentes for a persona."""
        if actividad_id is None:
            # List all actividades for this persona
            actividades = ActividadDocente.query.filter_by(personalId=persona_id).all()
            return jsonify([act.to_dict() for act in actividades]), 200
        else:
            # Get specific actividad
            actividad = ActividadDocente.query.filter_by(
                id=actividad_id, 
                personalId=persona_id
            ).first()
            if actividad:
                return jsonify(actividad.to_dict()), 200
            else:
                return jsonify({"error": "Actividad docente no encontrada"}), 404

    def post(self, persona_id):
        """POST new actividad docente for a persona."""
        data = request.get_json()
        
        # Validate persona exists
        personal = Personal.query.filter_by(id=persona_id).first()
        if not personal:
            return jsonify({"error": "Personal no encontrado"}), 404
        
        # Validate institucion if provided
        if data.get('institucionId'):
            institucion = Institucion.query.filter_by(id=data['institucionId']).first()
            if not institucion:
                return jsonify({"error": "Institución no encontrada"}), 404
        
        try:
            nuevaActividad = ActividadDocente(
                personalId=persona_id,
                rol=data.get('rol'),
                institucionId=data.get('institucionId'),
                fechaInicio=date.fromisoformat(data['fechaInicio']) if data.get('fechaInicio') else None,
                fechaFin=date.fromisoformat(data['fechaFin']) if data.get('fechaFin') else None
            )
            db.session.add(nuevaActividad)
            db.session.commit()
            
            return jsonify({
                "mensaje": "Actividad docente creada exitosamente",
                "actividad": nuevaActividad.to_dict()
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "Error al crear: " + str(e)}), 500

    def put(self, persona_id, actividad_id):
        """PUT update actividad docente."""
        data = request.get_json()
        
        actividad = ActividadDocente.query.filter_by(
            id=actividad_id, 
            personalId=persona_id
        ).first()
        
        if not actividad:
            return jsonify({"error": "Actividad docente no encontrada"}), 404
        
        try:
            actividad.rol = data.get('rol', actividad.rol)
            actividad.institucionId = data.get('institucionId', actividad.institucionId)
            
            if 'fechaInicio' in data:
                actividad.fechaInicio = date.fromisoformat(data['fechaInicio']) if data['fechaInicio'] else None
            if 'fechaFin' in data:
                actividad.fechaFin = date.fromisoformat(data['fechaFin']) if data['fechaFin'] else None
            
            db.session.commit()
            
            return jsonify({
                "mensaje": "Actividad docente actualizada exitosamente",
                "actividad": actividad.to_dict()
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "Error al actualizar: " + str(e)}), 500

    def delete(self, persona_id, actividad_id):
        """DELETE actividad docente."""
        actividad = ActividadDocente.query.filter_by(
            id=actividad_id, 
            personalId=persona_id
        ).first()
        
        if not actividad:
            return jsonify({"error": "Actividad docente no encontrada"}), 404
        
        try:
            db.session.delete(actividad)
            db.session.commit()
            return jsonify({"mensaje": "Actividad docente eliminada exitosamente"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "Error al eliminar: " + str(e)}), 500


# Create view instances
personal_view = ControladorPersonal.as_view('controlador_personal')
actividad_docente_view = ControladorActividadDocente.as_view('controlador_actividad_docente')

# Register Personal routes
personal_bp.add_url_rule('/', defaults={'id': None}, view_func=personal_view, methods=['GET'])
personal_bp.add_url_rule('/', view_func=personal_view, methods=['POST'])
personal_bp.add_url_rule('/<int:id>', view_func=personal_view, methods=['GET', 'PUT', 'DELETE'])

# Register ActividadDocente routes
personal_bp.add_url_rule(
    '/<int:persona_id>/actividades-docente', 
    defaults={'actividad_id': None},
    view_func=actividad_docente_view, 
    methods=['GET', 'POST']
)
personal_bp.add_url_rule(
    '/<int:persona_id>/actividades-docente/<int:actividad_id>',
    view_func=actividad_docente_view,
    methods=['GET', 'PUT', 'DELETE']
)



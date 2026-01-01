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


# Create view instances
personal_view = ControladorPersonal.as_view('controlador_personal')
actividad_docente_view = ControladorActividadDocente.as_view('controlador_actividad_docente')

# Register Personal routes
personal_bp.add_url_rule('/', defaults={'id': None}, view_func=personal_view, methods=['GET'])
personal_bp.add_url_rule('/<int:id>', view_func=personal_view, methods=['GET'])

# Register ActividadDocente routes
personal_bp.add_url_rule(
    '/<int:persona_id>/actividades-docente', 
    defaults={'actividad_id': None},
    view_func=actividad_docente_view, 
    methods=['GET']
)
personal_bp.add_url_rule(
    '/<int:persona_id>/actividades-docente/<int:actividad_id>',
    view_func=actividad_docente_view,
    methods=['GET']
)



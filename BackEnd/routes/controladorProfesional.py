from flask import Blueprint, jsonify, request
from flask.views import MethodView
from app import db
from models.personal import Personal

profesional_bp = Blueprint('profesional_bp', __name__)

class ControladorProfesional(MethodView):
    def get(self):
        profesionales = Personal.query.filter_by(objectType='profesional').all()
        return jsonify([profesional.to_dict() for profesional in profesionales])
    
    def post(self):
        data = request.get_json()

        try: 
            nuevoProfesional = Personal(
                nombre=data['nombre'],  
                apellido=data['apellido'],
                horas=data['horas'],
                gradoAcademicoId=data['gradoAcademicoId'],
                institucion=data['institucion'],

                objectType='profesional',
                
                especialidad=data['especialidad'],
                descripcion=data['descripcion']
            )

            db.session.add(nuevoProfesional)
            db.session.commit()

            return jsonify({
                'message': 'Profesional creado exitosamente',
                'profesional': nuevoProfesional.to_dict()
            }), 201
        
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Error al crear el profesional', 'error': str(e)}), 500
        
profesional_view = ControladorProfesional.as_view('controlador_profesional')

#api
profesional_bp.add_url_rule('/api/profesionales', view_func=profesional_view, methods=['GET', 'POST'])
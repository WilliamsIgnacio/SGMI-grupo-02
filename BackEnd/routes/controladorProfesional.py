from flask import Blueprint, jsonify, request
from flask.views import MethodView
from app import db
from models.personal import Profesional

profesional_bp = Blueprint('profesional_bp', __name__)

class ControladorProfesional(MethodView):
    def get(self, id=None):
        if id is None:
            profesionales = Profesional.query.all()
            profesionales_list = [profesional.to_dict() for profesional in profesionales]
            return jsonify(profesionales_list), 200
        else:
            profesional = Profesional.query.filter_by(id=id).first()
            if profesional:
                return jsonify(profesional.to_dict()), 200
            else:
                return jsonify({'message': 'Profesional no encontrado'}), 404
    
    def post(self):
        data = request.get_json()

        try: 
            nuevoProfesional = Profesional(
                nombre=data['nombre'],  
                apellido=data['apellido'],
                horas=data['horas'],
                gradoAcademicoId=data['gradoAcademicoId'],
                institucion=data['institucion'],
                
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
        
    def put(self, id):
        profesional = Profesional.query.filter_by(id=id).first()
        if not profesional:
            return jsonify({'message': 'Profesional no encontrado'}), 404
        
        data = request.get_json()
        try:
            profesional.nombre = data.get('nombre', profesional.nombre)
            profesional.apellido = data.get('apellido', profesional.apellido)
            profesional.horas = data.get('horas', profesional.horas)
            profesional.gradoAcademicoId = data.get('gradoAcademicoId', profesional.gradoAcademicoId)
            profesional.institucionId = data.get('institucionId', profesional.institucionId)

            profesional.especialidad = data.get('especialidad', profesional.especialidad)
            profesional.descripcion = data.get('descripcion', profesional.descripcion)

            db.session.commit()

            return jsonify({
                'message': 'Profesional actualizado exitosamente',
                'profesional': profesional.to_dict()
            }), 200
        
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Error al actualizar el profesional', 'error': str(e)}), 500
        
    def delete(self, id):
        profesional = Profesional.query.filter_by(id=id).first()
        if not profesional:
            return jsonify({'message': 'Profesional no encontrado'}), 404
        
        try:
            db.session.delete(profesional)
            db.session.commit()
            return jsonify({'message': 'Profesional eliminado exitosamente'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Error al eliminar el profesional', 'error': str(e)}), 500
        
profesional_view = ControladorProfesional.as_view('controlador_profesional')

#api
profesional_bp.add_url_rule('/', defaults={'id': None}, view_func=profesional_view, methods=['GET'])
profesional_bp.add_url_rule('/', view_func=profesional_view, methods=['POST'])
profesional_bp.add_url_rule('/<int:id>', view_func=profesional_view, methods=['GET', 'PUT', 'DELETE'])
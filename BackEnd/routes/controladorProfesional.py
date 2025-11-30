from flask import Blueprint, jsonify, request
from flask.views import MethodView
from database import db
from models.personal import Profesional
from models.gradoAcademico import GradoAcademico

profesional_bp = Blueprint('profesional_bp', __name__)

class ControladorProfesional(MethodView):
    def crearProfesional(self, data):
        grado = data.get('gradoAcademicoId')
        gradoObj = GradoAcademico.query.filter_by(id=grado).first()
        if not gradoObj:
            raise ValueError("Grado Académico no encontrado")
        try:
            nuevoProfesional = Profesional(
                nombre=data.get('nombre'),  
                apellido=data.get('apellido'),
                horas=data.get('horas'),
                gradoAcademicoId=data.get('gradoAcademicoId'),
                institucionId=data.get('institucionId'),
                
                especialidad=data.get('especialidad'),
                descripcion=data.get('descripcion')
            )

            db.session.add(nuevoProfesional)
            db.session.commit()
            return nuevoProfesional
        except Exception as e:
            db.session.rollback()
            raise e
        
    def modificarProfesional(self, id, data):
        profesional = Profesional.query.filter_by(id=id).first()
        if not profesional:
            return None
        try:
            if 'gradoAcademicoId' in data:
                grado = data.get('gradoAcademicoId')
                gradoObj = GradoAcademico.query.filter_by(id=grado).first()
                if not gradoObj:
                    raise ValueError("Grado Académico no encontrado")
                
                profesional.gradoAcademicoId = gradoObj.id

            profesional.nombre = data.get('nombre', profesional.nombre)
            profesional.apellido = data.get('apellido', profesional.apellido)
            profesional.horas = data.get('horas', profesional.horas)
            profesional.institucionId = data.get('institucionId', profesional.institucionId)

            profesional.especialidad = data.get('especialidad', profesional.especialidad)
            profesional.descripcion = data.get('descripcion', profesional.descripcion)

            db.session.commit()
            return profesional
        except Exception as e:
            db.session.rollback()
            raise e
        
    def eliminarProfesional(self, id):
        profesional = Profesional.query.filter_by(id=id).first()
        if not profesional:
            return False
        try:
            db.session.delete(profesional)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e

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
                return jsonify({'mensaje': 'Profesional no encontrado'}), 404
    
    def post(self):
        data = request.get_json()
        try: 
            nuevoProfesional = self.crearProfesional(data)
            return jsonify({
                'mensaje': 'Profesional creado exitosamente',
                'profesional': nuevoProfesional.to_dict()
            }), 201
        except ValueError as ve:
            return jsonify({'mensaje': str(ve)}), 400
        
        except Exception as e:
            return jsonify({'mensaje': 'Error al crear' + str(e)}), 500
        
    def put(self, id):
        data = request.get_json()
        try:
            profesional = self.modificarProfesional(id, data)
            if not profesional:
                return jsonify({'mensaje': 'Profesional no encontrado'}), 404

            return jsonify({
                'mensaje': 'Profesional actualizado exitosamente',
                'profesional': profesional.to_dict()
            }), 200
        except ValueError as ve:
            return jsonify({'mensaje': str(ve)}), 400
        
        except Exception as e:
            return jsonify({'Error al modificar': str(e)}), 500
        
    def delete(self, id):
        try:
            eliminado = self.eliminarProfesional(id)
            if not eliminado:
                return jsonify({'mensaje': 'Profesional no encontrado'}), 404

            return jsonify({'mensaje': 'Profesional eliminado exitosamente'}), 200
        except Exception as e:
            return jsonify({'Error al eliminar': str(e)}), 500
        
profesional_view = ControladorProfesional.as_view('controlador_profesional')

#api
profesional_bp.add_url_rule('/', defaults={'id': None}, view_func=profesional_view, methods=['GET'])
profesional_bp.add_url_rule('/', view_func=profesional_view, methods=['POST'])
profesional_bp.add_url_rule('/<int:id>', view_func=profesional_view, methods=['GET', 'PUT', 'DELETE'])
from flask import Blueprint, jsonify, request
from flask.views import MethodView
from models.gradoAcademico import GradoAcademico
from database import db

grado_academico_bp = Blueprint('grado_academico_bp', __name__)

class ControladorGradoAcademico(MethodView):
    def crearGrado(self, data):
        if not data.get('nombre'):
            raise ValueError('Faltan campos obligatorios (nombre)')
        try:
            nuevoGrado = GradoAcademico(
                nombre=data.get('nombre')
            )
            db.session.add(nuevoGrado)
            db.session.commit()
            return nuevoGrado
        except Exception as e:
            db.session.rollback()
            raise e
        
    def modificarGrado(self, id, data):
        grado = GradoAcademico.query.get(id)
        if not grado:
            raise ValueError('Grado Academico no encontrado')
        
        try:
            if 'nombre' in data:
                grado.nombre = data.get('nombre', grado.nombre)
            db.session.commit()
            db.session.refresh(grado)
            return grado
        except Exception as e:
            db.session.rollback()
            raise e
        
    def eliminarGrado(self, id):
        grado = GradoAcademico.query.get(id)
        if not grado:
            return False
        try:
            db.session.delete(grado)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise Exception("No se puede eliminar el grado porque está siendo utilizado por personal.")
        
    def get(self, id=None):
        if id:
            grado = GradoAcademico.query.get(id)
            if grado:
                return jsonify(grado.to_dict()), 200
            return jsonify({'message': 'Grado Academico no encontrado'}), 404
        else:
            grados = GradoAcademico.query.all()
            return jsonify([grado.to_dict() for grado in grados]), 200
        
    def post(self):
        data = request.get_json()
        try:
            nuevoGrado = self.crearGrado(data)
            return jsonify({
                'mensaje': 'Grado creado exitosamente',
                'grado': nuevoGrado.to_dict()
            }), 201
        except ValueError as ve:
            return jsonify({'error': str(ve)}), 400
        except Exception as e:
            return jsonify({'error': 'Error al crear el grado', 'detalle': str(e)}), 500
    
    def put(self, id):
        data = request.get_json()
        try:
            grado = self.modificarGrado(id, data)
            if not grado:
                return jsonify({'message': 'Grado Academico no encontrado'}), 404
            return jsonify({
                'mensaje': 'Grado modificado exitosamente',
                'grado': grado.to_dict()
            }), 200
        except Exception as e:
            return jsonify({'error': 'Error al modificar el grado', 'detalle': str(e)}), 400
    
    def delete(self, id):
        try:
            exito = self.eliminarGrado(id)
            if exito:
                return jsonify({'mensaje': 'Grado eliminado exitosamente'}), 200
            else:
                return jsonify({'message': 'Grado Academico no encontrado'}), 404
        except Exception as e:
            return jsonify({'error': 'Error al eliminar el grado', 'detalle': str(e)}), 400
    
grado_view = ControladorGradoAcademico.as_view('controlador_grado_academico')

# Rutas
grado_academico_bp.add_url_rule('/', defaults={'id': None}, view_func=grado_view, methods=['GET'])
grado_academico_bp.add_url_rule('/', view_func=grado_view, methods=['POST'])
grado_academico_bp.add_url_rule('/<int:id>', view_func=grado_view, methods=['GET', 'PUT', 'DELETE'])
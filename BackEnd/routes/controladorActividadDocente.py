from flask import Blueprint, jsonify, request
from flask.views import MethodView
from services.AdminActividadDocente import AdminActividadDocente
from database import db


actividad_docente_bp = Blueprint('actividad_docente_bp', __name__)
service = AdminActividadDocente()

class ControladorActividadDocente(MethodView):
    def get(self, id = None):

        #Por default trae todas las actividades
        if id is None:
            actividades = service.obtener_todas()
            return jsonify([actividad.to_dict() for actividad in actividades]), 200
        
        #Si se agrega un id a la ruta hace un select de esa actividad
        actividad = service.obtener_por_id(id)

        if actividad:
            return jsonify(actividad.to_dict()), 200
        return jsonify({"error": "Actividad docente no encontrada"})
    

    def post(self):
        data = request.get_json()
        try:
            nueva = service.crear(data)
            return jsonify({
                'mensaje': 'Creada con exito',
                'actividad': nueva.to_dict()
            }), 201
        
        except ValueError as error:
            return jsonify({'error': str(error)}), 400
        
        except Exception as excepcion:
            db.session.rollback()
            return jsonify({'error': 'Error interno', 'detalle': str(excepcion)}), 500
        

    def put(self, id):
        data = request.get_json()
        
        try:
            actividad = service.modificar(id, data)
            return jsonify({'mensaje': 'Modificada con exito', 'actividad': actividad.to_dict()}), 200
        
        except ValueError as error:
            return jsonify({'error': str(error)}), 404
        
        except Exception as excepcion:
            db.session.rollback()
            return jsonify({'error': 'Error al actualizar', 'detalle': str(excepcion)}),400

    def delete(self, id):
        try:
            if service.eliminar(id):
                return jsonify({'mensaje': 'Eliminada con exito'}), 200
            else:
                return jsonify({'error': 'Actividad docente no encontrada'})
        
        except Exception as excepcion:
            db.session.rollback()
            return jsonify({'error': 'Error al eliminar', 'detalle': str(excepcion)}), 400


actividad_view = ControladorActividadDocente.as_view('controlador_actividad_docente')
actividad_docente_bp.add_url_rule('/', defaults={'id': None}, view_func=actividad_view, methods=['GET'])
actividad_docente_bp.add_url_rule('/', view_func=actividad_view, methods=['POST'])
actividad_docente_bp.add_url_rule('/<int:id>', view_func=actividad_view, methods=['GET', 'PUT', 'DELETE'])
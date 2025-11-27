from flask import Blueprint, jsonify, request
from flask.views import MethodView
from datetime import datetime
from models.actividadDocente import ActividadDocente
from database import db

actividad_docente_bp = Blueprint('actividad_docente_bp', __name__)

def convertir_fecha(fecha_texto):
    if not fecha_texto:
        return None
    try:
        return datetime.strptime(fecha_texto, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        return None

class ControladorActividadDocente(MethodView):
    def get(self, id=None):
        if id is None:
            actividades = ActividadDocente.query.all()
            return jsonify([actividad.to_dict() for actividad in actividades]), 200
        else:
            actividad = ActividadDocente.query.get(id)
            if actividad:
                return jsonify(actividad.to_dict()), 200
            else:
                return jsonify({"error": "Actividad Docente no encontrada"}), 404
    
    def post(self):
        data = request.get_json()
        if not data.get('personalId') or not data.get('institucionId'):
             return jsonify({'error': 'Faltan campos obligatorios (personalId, institucionId)'}), 400

        try:
            nueva_actividad = ActividadDocente(
                fechaInicio=convertir_fecha(data.get('fechaInicio')),
                fechaFin=convertir_fecha(data.get('fechaFin')),
                rol=data.get('rol'),
                personalId=data.get('personalId'),
                institucionId=data.get('institucionId')
            )
            
            db.session.add(nueva_actividad)
            db.session.commit()
            
            return jsonify({
                'mensaje': 'Actividad Docente creada exitosamente',
                'actividad': nueva_actividad.to_dict()
            }), 201
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Error al crear la actividad', 'detalle': str(e)}), 400

    def put(self, id):
        actividad = ActividadDocente.query.get(id)
        if not actividad:
            return jsonify({'error': 'Actividad Docente no encontrada'}), 404
        
        data = request.get_json()
        try:
            if 'fechaInicio' in data:
                actividad.fechaInicio = convertir_fecha(data.get('fechaInicio'))
            if 'fechaFin' in data:
                actividad.fechaFin = convertir_fecha(data.get('fechaFin'))
            
            actividad.rol = data.get('rol', actividad.rol)
            actividad.personalId = data.get('personalId', actividad.personalId)
            actividad.institucionId = data.get('institucionId', actividad.institucionId)
            
            db.session.commit()
            return jsonify({
                'mensaje': 'Actividad Docente actualizada exitosamente',
                'actividad': actividad.to_dict()
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Error al actualizar la actividad', 'detalle': str(e)}), 400

    def delete(self, id):
        actividad = ActividadDocente.query.get(id)
        if not actividad:
            return jsonify({'error': 'Actividad Docente no encontrada'}), 404
        
        try:
            db.session.delete(actividad)
            db.session.commit()
            return jsonify({'mensaje': 'Actividad Docente eliminada exitosamente'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Error al eliminar la actividad', 'detalle': str(e)}), 400

actividad_view = ControladorActividadDocente.as_view('controlador_actividad_docente')

# api
actividad_docente_bp.add_url_rule('/', defaults={'id': None}, view_func=actividad_view, methods=['GET'])
actividad_docente_bp.add_url_rule('/', view_func=actividad_view, methods=['POST'])
actividad_docente_bp.add_url_rule('/<int:id>', view_func=actividad_view, methods=['GET', 'PUT', 'DELETE'])
from flask import Blueprint, jsonify, request
from flask.views import MethodView
from datetime import datetime
from database import db
from models.proyecto import Proyecto
from models.grupo import Grupo

proyecto_bp = Blueprint('proyecto_bp', __name__)

def convertirFecha(fechaTexto):
    if not fechaTexto:
        return None
    try:
        return datetime.strptime(fechaTexto, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        return None
    
class ControladorProyecto(MethodView):
    def crearProyecto(self, data):
        if not data.get('codigo') or not data.get('nombre'):
            raise ValueError('Faltan campos obligatorios: codigo y nombre')
        
        if data.get('grupoId'):
            grupo = Grupo.query.get(data['grupoId'])
            if not grupo:
                raise ValueError('El grupoId proporcionado no existe')
        try:
            nuevoProyecto = Proyecto(
                codigo=data.get('codigo'),
                nombre=data.get('nombre'),
                descripcion=data.get('descripcion'),
                tipo=data.get('tipo'),
                logros=data.get('logros'),
                dificultades=data.get('dificultades'),
                fechaInicio=convertirFecha(data.get('fechaInicio')),
                fechaFin=convertirFecha(data.get('fechaFin')),
                grupoId=data.get('grupoId')
            )
            db.session.add(nuevoProyecto)
            db.session.commit()
            return nuevoProyecto
        except Exception as e:
            db.session.rollback()
            raise e
        
    def modificarProyecto(self, id, data):
        proyecto = Proyecto.query.get(id)
        if not proyecto:
            raise ValueError('Proyecto no encontrado')
        
        try: 
            proyecto.codigo = data.get('codigo', proyecto.codigo)
            proyecto.nombre = data.get('nombre', proyecto.nombre)
            proyecto.descripcion = data.get('descripcion', proyecto.descripcion)
            proyecto.tipo = data.get('tipo', proyecto.tipo)
            proyecto.logros = data.get('logros', proyecto.logros)
            proyecto.dificultades = data.get('dificultades', proyecto.dificultades)

            fechaInicio = convertirFecha(data.get('fechaInicio'))
            fechaFin = convertirFecha(data.get('fechaFin'))
            if fechaInicio:
                proyecto.fechaInicio = fechaInicio
            if fechaFin:
                proyecto.fechaFin = fechaFin

            if data.get('grupoId'):
                grupo = Grupo.query.get(data['grupoId'])
                if not grupo:
                    raise ValueError('El grupoId proporcionado no existe')
                proyecto.grupoId = data.get('grupoId', proyecto.grupoId)

            db.session.commit()
            db.session.refresh(proyecto)
            return proyecto
        except Exception as e:
            db.session.rollback()
            raise e
    
    def eliminarProyecto(self, id):
        proyecto = Proyecto.query.get(id)
        if not proyecto:
            return False
        
        try:
            db.session.delete(proyecto)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e


    def get(self, id=None):
        if id is None:
            proyectos = Proyecto.query.all()
            return jsonify([proyecto.to_dict() for proyecto in proyectos])
        else:
            proyecto = Proyecto.query.get(id)
            if proyecto:
                return jsonify(proyecto.to_dict())
            else:
                return jsonify({'message': 'Proyecto no encontrado'}), 404

    def post(self):
        data = request.get_json()

        try:
            nuevoProyecto = self.crearProyecto(data)

            return jsonify({
                'message': 'Proyecto creado exitosamente',
                'proyecto': nuevoProyecto.to_dict()
            }), 201
        except ValueError as ve:
            return jsonify({'message': str(ve)}), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Error al crear el proyecto', 'error': str(e)}), 500

    def put(self, id):
        data = request.get_json()       

        try:
            proyecto = self.modificarProyecto(id, data)
            if not proyecto:
                return jsonify({'message': 'Proyecto no encontrado'}), 404

            return jsonify({
                'message': 'Proyecto modificado exitosamente',
                'proyecto': proyecto.to_dict()
            })
        except ValueError as ve:
            return jsonify({'message': str(ve)}), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Error al modificar el proyecto', 'error': str(e)}), 500
    
    def delete(self, id):
        try:
            exito = self.eliminarProyecto(id)
            if not exito:
                return jsonify({'message': 'Proyecto no encontrado'}), 404

            return jsonify({'message': 'Proyecto eliminado exitosamente'})
        except Exception as e:
            return jsonify({'message': 'Error al eliminar el proyecto', 'error': str(e)}), 500
        
proyecto_view = ControladorProyecto.as_view('controlador_proyecto')

proyecto_bp.add_url_rule('/', defaults={'id': None}, view_func=proyecto_view, methods=['GET',])
proyecto_bp.add_url_rule('/', view_func=proyecto_view, methods=['POST',])

proyecto_bp.add_url_rule('/<int:id>', view_func=proyecto_view, methods=['GET', 'PUT', 'DELETE'])

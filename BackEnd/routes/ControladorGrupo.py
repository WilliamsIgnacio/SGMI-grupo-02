from datetime import date
from sqlalchemy.exc import IntegrityError
from flask import Blueprint, request, jsonify
from flask.views import MethodView

#MODELOS
from database import db
from services.AdminGrupo import AdminGrupo
from models.grupo import Grupo


grupos_bp = Blueprint('grupos', __name__, url_prefix='/api/grupos')
administrador = AdminGrupo()

class ControladorGrupo(MethodView):

    def get(self, id = None):

        if id is None:
            lista_grupos = administrador.obtenerTodosGrupos()
            respuesta = jsonify([grupo.to_dict() for grupo in lista_grupos])
            return respuesta, 200
        
        else:
            grupo = administrador.obtenerUnGrupo(id)

            if grupo:
                respuesta = jsonify(grupo.to_dict())
                return respuesta, 200

            else:
                respuesta = jsonify({"error" : "Grupo no encontrado"}), 404


    def post(self):

        data = request.get_json()

        try:
            nuevoGrupo = administrador.crearGrupo(data)
            respuesta = {
                'mensaje': 'Grupo creado exitosamente',
                'profesional': nuevoGrupo.to_dict()
            }
            return jsonify(respuesta), 201
        
        except ValueError as error:
            respuesta = {'mensaje': str(error)}
            return jsonify(respuesta), 400
        
        except Exception as excepcion:
            respuesta = {'mensaje': 'Error al crear' + str(excepcion)}
            return jsonify(respuesta), 500


    def put(self, id):

        data = request.get_json()

        try:
            grupoModificado = administrador.modificarGrupo(data, id)
            respuesta = {
                'mensaje': 'Grupo modificado correctamente',
                'grupo': grupoModificado.to_dict()
            }
            return jsonify(respuesta), 201
        
        except ValueError as error:
            respuesta = {'mensaje': str(error)}
            return jsonify(respuesta), 400
        
        except Exception as excepcion:
            respuesta = {'mensaje': 'Error al crear' + str(excepcion)}
            return jsonify(respuesta), 500
        


grupos_view = ControladorGrupo.as_view('controlador_grupo')


grupos_bp.add_url_rule('/', view_func = grupos_view, methods=['GET'])
grupos_bp.add_url_rule('/<int:id>', view_func = grupos_view, methods=['GET'])
grupos_bp.add_url_rule('/', view_func = grupos_view, methods=['POST'])
grupos_bp.add_url_rule('/<int:id>', view_func = grupos_view, methods=['PUT'])
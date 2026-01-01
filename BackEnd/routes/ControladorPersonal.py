from datetime import date
from flask import Blueprint, request, jsonify
from flask.views import MethodView
from database import db
from models.personal import Personal, Investigador, Profesional, Becario, Soporte, Visitante
from models.actividadDocente import ActividadDocente
from models.gradoAcademico import GradoAcademico
from models.models_db import Institucion, LoginCredentials

from services.AdminPersonal import AdminPersonal

personal_bp = Blueprint('personal_bp', __name__)
administrador = AdminPersonal()

class ControladorPersonal(MethodView):

    def get(self, id = None):

        if id is None:
            lista_personal = administrador.obtenerTodoPersonal()
            respuesta = jsonify([personal.to_dict() for personal in lista_personal])
            return respuesta, 200
        
        else:
            personal = administrador.obtenerUnPersonal(id)

            if personal:
                respuesta = jsonify(personal.to_dict())
                return respuesta, 200
            
            else:
                respuesta = jsonify({"error" : "Personal no encontrado"}), 404


    def post(self, operacion):
        
        if operacion is not None and operacion not in {1, 2, 3, 4, 5}:
        
            respuesta = {'mensaje': "Operacion invalida: 1- Profesional, 2- Soporte, 3- Becario, 4- Visitante, 5-Investigador"}
            return jsonify(respuesta), 400
        
        data = request.get_json()

        try:
            nuevoPersonal = administrador.crearPersonal(data, operacion)
            respuesta = {
                'mensaje': 'Personal creado exitosamente',
                'profesional': nuevoPersonal.to_dict()
            }
            return jsonify(respuesta), 201
        
        except ValueError as error:
            respuesta = {'mensaje': str(error)}
            return jsonify(respuesta), 400
        
        except Exception as excepcion:
            respuesta = {'mensaje': 'Error al crear' + str(excepcion)}
            return jsonify(respuesta), 500
    


personal_view = ControladorPersonal.as_view('controlador_personal')


personal_bp.add_url_rule('/', view_func=personal_view, methods=['GET'])
personal_bp.add_url_rule('/<int:id>', view_func=personal_view, methods=['GET'])
personal_bp.add_url_rule('/<int:operacion>', view_func=personal_view, methods=['POST'])
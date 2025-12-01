from flask import Blueprint, request, jsonify
from flask.views import MethodView
from database import db
from models.personal import Soporte
from models.gradoAcademico import GradoAcademico
from models.enums import RolesSoporte

soporte_bp = Blueprint('soporte_bp', __name__)

class ControladorSoporte(MethodView):
    def crearSoporte(self, data):
        grado = data.get('gradoAcademicoId')
        gradoObj = GradoAcademico.query.filter_by(id=grado).first()
        if not gradoObj:
            raise ValueError("Grado Académico no encontrado")
        
        rolData = data.get('rol')
        if rolData not in [rol.value for rol in RolesSoporte]:
            raise ValueError("Rol de soporte inválido")
        
        try:
            nuevoSoporte = Soporte(
                nombre=data.get('nombre'),
                apellido=data.get('apellido'),
                horas=data.get('horas'),
                gradoAcademicoId=data.get('gradoAcademicoId'),
                institucionId=data.get('institucionId'),

                rol=rolData
            )

            db.session.add(nuevoSoporte)
            db.session.commit()
            return nuevoSoporte
        except Exception as e:
            db.session.rollback()
            raise e
        
    def modificarSoporte(self, id, data):
        soporte = Soporte.query.filter_by(id=id).first()
        if not soporte:
            return None
        try:
            if 'gradoAcademicoId' in data:
                grado = data.get('gradoAcademicoId')
                gradoObj = GradoAcademico.query.filter_by(id=grado).first()
                if not gradoObj:
                    raise ValueError("Grado Académico no encontrado")
                
                soporte.gradoAcademicoId = gradoObj.id

            if 'rol' in data:
                rolData = data.get('rol')
                if rolData not in [rol.value for rol in RolesSoporte]:
                    raise ValueError("Rol de soporte inválido")
                soporte.rol = rolData

            soporte.nombre = data.get('nombre', soporte.nombre)
            soporte.apellido = data.get('apellido', soporte.apellido)
            soporte.horas = data.get('horas', soporte.horas)
            soporte.institucionId = data.get('institucionId', soporte.institucionId)

            db.session.commit()
            return soporte
        except Exception as e:
            db.session.rollback()
            raise e
        
    def eliminarSoporte(self, id):
        soporte = Soporte.query.filter_by(id=id).first()
        if not soporte:
            return False
        try:
            db.session.delete(soporte)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e

    def get(self, id=None):
        if id is None:
            soportes = Soporte.query.all()
            return jsonify([soporte.to_dict() for soporte in soportes]), 200
        else:
            soporte = Soporte.query.filter_by(id=id).first()
            if soporte:
                return jsonify(soporte.to_dict()), 200
            else:
                return jsonify({"error": "Personal de soporte no encontrado"}), 404
    
    
    def post(self):
        data = request.get_json()
        try:
            nuevoSoporte = self.crearSoporte(data)
            return jsonify({
                "mensaje" : "Personal de soporte creado exitosamente",
                "soporte": nuevoSoporte.to_dict()
            }), 201
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
        except Exception as e:
            return jsonify({"error al crear": str(e)}), 500

    def put(self, id):
        data = request.get_json()
        try:
            soporte = self.modificarSoporte(id, data)
            if not soporte:
                return jsonify({"error": "Personal de soporte no encontrado"}), 404
            return jsonify({
                "mensaje" : "Personal de soporte actualizado exitosamente",
                "soporte": soporte.to_dict()
            }), 200
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
        except Exception as e:
            return jsonify({"error al modificar": str(e)}), 500

    def delete(self, id):
        try:
            exito = self.eliminarSoporte(id)
            if not exito:
                return jsonify({"error": "Personal de soporte no encontrado"}), 404
            return jsonify({"mensaje": "Personal de soporte eliminado exitosamente"}), 200
            
        except Exception as e:
            return jsonify({"error al eliminar": str(e)}), 500

soporte_view = ControladorSoporte.as_view('controlador_soporte')

#API
soporte_bp.add_url_rule('/', defaults={'id': None}, view_func=soporte_view, methods=['GET',])
soporte_bp.add_url_rule('/', view_func=soporte_view, methods=['POST',])
soporte_bp.add_url_rule('/<int:id>', view_func=soporte_view, methods=['GET', 'PUT', 'DELETE'])
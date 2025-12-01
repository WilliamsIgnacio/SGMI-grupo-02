from flask import Blueprint, request, jsonify
from flask.views import MethodView
from database import db
from models.personal import Becario
from models.gradoAcademico import GradoAcademico
from models.enums import TipoFormacion

becario_bp = Blueprint('becario_bp', __name__)

class ControladorBecario(MethodView):
    def crearBecario(self, data):
        grado = data.get('gradoAcademicoId')
        gradoObj = GradoAcademico.query.filter_by(id=grado).first()
        if not gradoObj:
            raise ValueError("Grado Académico no encontrado")
        
        rolData = data.get('rol')
        if rolData not in [tipo.value for tipo in TipoFormacion]:
            raise ValueError("Rol de becario inválido")
        
        try:
            nuevoBecario = Becario(
                nombre=data.get('nombre'),
                apellido=data.get('apellido'),
                horas=data.get('horas'),
                correo_electronico=data.get('correoElectronico'),
                gradoAcademicoId=data.get('gradoAcademicoId'),
                institucionId=data.get('institucionId'),

                rol=rolData
            )

            db.session.add(nuevoBecario)
            db.session.commit()
            return nuevoBecario
        except Exception as e:
            db.session.rollback()
            raise e

    def modificarBecario(self, id, data):
        becario = Becario.query.filter_by(id=id).first()
        if not becario:
            return None
        try:
            if 'gradoAcademicoId' in data:
                grado = data.get('gradoAcademicoId')
                gradoObj = GradoAcademico.query.filter_by(id=grado).first()
                if not gradoObj:
                    raise ValueError("Grado Académico no encontrado")
                
                becario.gradoAcademicoId = gradoObj.id

            if 'rol' in data:
                rolData = data.get('rol')
                if rolData not in [tipo.value for tipo in TipoFormacion]:
                    raise ValueError("Rol de becario inválido")
                becario.rol = rolData

            becario.nombre = data.get('nombre', becario.nombre)
            becario.apellido = data.get('apellido', becario.apellido)
            becario.horas = data.get('horas', becario.horas)
            becario.correo_electronico = data.get('correoElectronico', becario.correo_electronico)
            becario.institucionId = data.get('institucionId', becario.institucionId)

            db.session.commit()
            return becario
        except Exception as e:
            db.session.rollback()
            raise e
    
    def eliminarBecario(self, id):
        becario = Becario.query.filter_by(id=id).first()
        if not becario:
            return False
        try:
            db.session.delete(becario)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e

    def get(self, id=None):
        if id is None:
            becarios = Becario.query.all()
            return jsonify([becario.to_dict() for becario in becarios]), 200
        else:
            becario = Becario.query.filter_by(id=id).first()
            if becario:
                return jsonify(becario.to_dict()), 200
            else:
                return jsonify({"error": "Becario no encontrado"}), 404
            
    def post(self):
        data = request.get_json()
        try:
            nuevoBecario = self.crearBecario(data)
            return jsonify({
                "mensaje" : "Becario creado exitosamente",
                "becario": nuevoBecario.to_dict()
            }), 201
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
        except Exception as e:
            return jsonify({"error": "Error al crear" + str(e)}), 500
    
    def put(self, id):
        data = request.get_json()
        try:
            becario = self.modificarBecario(id, data)
            if not becario:
                return jsonify({"error": "Becario no encontrado"}), 404
            return jsonify({
                "mensaje" : "Becario actualizado exitosamente",
                "becario": becario.to_dict()
            }), 200
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
        except Exception as e:
            return jsonify({"error al modificar": str(e)}), 500
    
    def delete(self, id):
        try:
            exito = self.eliminarBecario(id)
            if not exito:
                return jsonify({"error": "Becario no encontrado"}), 404
            return jsonify({"mensaje": "Becario eliminado exitosamente"}), 200
        except Exception as e:
            return jsonify({"error al eliminar": str(e)}), 500

becario_view = ControladorBecario.as_view('controlador_becario')

#API
becario_bp.add_url_rule('/', defaults={'id': None}, view_func=becario_view, methods=['GET',])
becario_bp.add_url_rule('/', view_func=becario_view, methods=['POST',])
becario_bp.add_url_rule('/<int:id>', view_func=becario_view, methods=['GET', 'PUT', 'DELETE'])
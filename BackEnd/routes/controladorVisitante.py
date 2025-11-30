from flask import Blueprint, request, jsonify
from flask.views import MethodView
from database import db
from models.personal import Visitante
from models.gradoAcademico import GradoAcademico
from models.enums import RolesVisitante

visitante_bp = Blueprint('visitante_bp', __name__)

class ControladorVisitante(MethodView):
    def crearVisitante(self, data):
        grado = data.get('gradoAcademicoId')
        gradoObj = GradoAcademico.query.filter_by(id=grado).first()
        if not gradoObj:
            raise ValueError("Grado Académico no encontrado")
        
        rolData = data.get('rol')
        if rolData not in [rol.value for rol in RolesVisitante]:
            raise ValueError("Rol de visitante inválido")

        try:
            nuevoVisitante = Visitante(
                nombre=data.get('nombre'),
                apellido=data.get('apellido'),
                horas=data.get('horas'),
                gradoAcademicoId=data.get('gradoAcademicoId'),
                institucionId=data.get('institucionId'),

                rol=rolData
            )

            db.session.add(nuevoVisitante)
            db.session.commit()
            return nuevoVisitante
        except Exception as e:
            db.session.rollback()
            raise e

    def modificarVisitante(self, id, data):
        visitante = Visitante.query.filter_by(id=id).first()
        if not visitante:
            return None
        try:
            if 'gradoAcademicoId' in data:
                grado = data.get('gradoAcademicoId')
                gradoObj = GradoAcademico.query.filter_by(id=grado).first()
                if not gradoObj:
                    raise ValueError("Grado Académico no encontrado")
                
                visitante.gradoAcademicoId = gradoObj.id

            if 'rol' in data:
                rolData = data.get('rol')
                if rolData not in [rol.value for rol in RolesVisitante]:
                    raise ValueError("Rol de visitante inválido")
                visitante.rol = rolData
            
            visitante.nombre = data.get('nombre', visitante.nombre)
            visitante.apellido = data.get('apellido', visitante.apellido)
            visitante.horas = data.get('horas', visitante.horas)
            visitante.institucionId = data.get('institucionId', visitante.institucionId)

            db.session.commit()
            return visitante
        except Exception as e:
            db.session.rollback()
            raise e
        
    def eliminarVisitante(self, id):
        visitante = Visitante.query.filter_by(id=id).first()
        if not visitante:
            return False
        try:
            db.session.delete(visitante)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e

    def get(self, id=None):
        if id is None:
            visitantes = Visitante.query.all()
            visitantes_list = [visitante.to_dict() for visitante in visitantes]
            return jsonify(visitantes_list), 200
        else:
            visitante = Visitante.query.filter_by(id=id).first()
            if visitante:
                return jsonify(visitante.to_dict()), 200
            else:
                return jsonify({"error": "Visitante no encontrado"}), 404
        
    
    def post(self):
        data = request.get_json()
        try:
            nuevoVisitante = self.crearVisitante(data)

            return jsonify({
                "mensaje" : "Visitante creado exitosamente",
                "visitante": nuevoVisitante.to_dict()
            }), 201
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
        except Exception as e:
            return jsonify({"error a crear": str(e)}), 500

    def put(self, id):
        data = request.get_json()
        try:
            visitante = self.modificarVisitante(id, data)
            if not visitante:   
                return jsonify({"error": "Visitante no encontrado"}), 404

            return jsonify({
                "mensaje": "Visitante actualizado exitosamente",
                "visitante": visitante.to_dict()
            }), 200
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
        except Exception as e:
            return jsonify({"error a modificar": str(e)}), 500
    
    def delete(self, id):
        try:
            eliminado = self.eliminarVisitante(id)
            if not eliminado:
                return jsonify({"error": "Visitante no encontrado"}), 404
            return jsonify({"mensaje": "Visitante eliminado exitosamente"}), 200
        except Exception as e:
            return jsonify({"error al eliminar": str(e)}), 400

visitante_view = ControladorVisitante.as_view('controlador_visitante')

#API
visitante_bp.add_url_rule('/', defaults={'id': None}, view_func=visitante_view, methods=['GET'])
visitante_bp.add_url_rule('/', view_func=visitante_view, methods=['POST'])
visitante_bp.add_url_rule('/<int:id>', view_func=visitante_view, methods=['GET', 'PUT', 'DELETE'])
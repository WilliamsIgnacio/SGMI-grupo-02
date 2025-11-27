from flask import Blueprint, request, jsonify
from flask.views import MethodView
from app import db
from models.personal import Visitante

visitante_bp = Blueprint('visitante_bp', __name__)

class ControladorVisitante(MethodView):
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
            nuevoVisitante = Visitante(
                nombre=data.get('nombre'),
                apellido=data.get('apellido'),
                horas=data.get('horas'),
                gradoAcademicoId=data.get('gradoAcademicoId'),
                institucionId=data.get('institucionId'),

                rol=data.get('rol'),
            )

            db.session.add(nuevoVisitante)
            db.session.commit()

            return jsonify({
                "mensaje:" : "Visitante creado exitosamente",
                "becario": nuevoVisitante.to_dict()
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400

    def put(self, id):
        visitante = Visitante.query.filter_by(id=id).first()
        if not visitante:
            return jsonify({"error": "Visitante no encontrado"}), 404

        data = request.get_json()
        try:
            visitante.nombre = data.get('nombre', visitante.nombre)
            visitante.apellido = data.get('apellido', visitante.apellido)
            visitante.horas = data.get('horas', visitante.horas)
            visitante.gradoAcademicoId = data.get('gradoAcademicoId', visitante.gradoAcademicoId)
            visitante.institucionId = data.get('institucionId', visitante.institucionId)

            visitante.rol = data.get('rol', visitante.rol)

            db.session.commit()

            return jsonify({
                "mensaje": "Visitante actualizado exitosamente",
                "visitante": visitante.to_dict()
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400
    
    def delete(self, id):
        visitante = Visitante.query.filter_by(id=id).first()
        if not visitante:
            return jsonify({"error": "Visitante no encontrado"}), 404

        try:
            db.session.delete(visitante)
            db.session.commit()
            return jsonify({"mensaje": "Visitante eliminado exitosamente"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400

visitante_view = ControladorVisitante.as_view('controlador_visitante')

#API
visitante_bp.add_url_rule('/', defaults={'id': None}, view_func=visitante_view, methods=['GET'])
visitante_bp.add_url_rule('/', view_func=visitante_view, methods=['POST'])
visitante_bp.add_url_rule('/<int:id>', view_func=visitante_view, methods=['GET', 'PUT', 'DELETE'])
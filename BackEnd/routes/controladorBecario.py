from flask import Blueprint, request, jsonify
from flask.views import MethodView
from app import db
from models.personal import Becario

becario_bp = Blueprint('becario_bp', __name__)

class ControladorBecario(MethodView):
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
            nuevoBecario = Becario(
                nombre=data.get('nombre'),
                apellido=data.get('apellido'),
                horas=data.get('horas'),
                gradoAcademicoId=data.get('gradoAcademicoId'),
                institucionId=data.get('institucionId'),

                rol=data.get('rol'),
            )

            db.session.add(nuevoBecario)
            db.session.commit()

            return jsonify({
                "mensaje:" : "Becario creado exitosamente",
                "becario": nuevoBecario.to_dict()
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400
    
    def put(self, id):
        becario = Becario.query.filter_by(id=id).first()
        if not becario:
            return jsonify({"error": "Becario no encontrado"}), 404
        data = request.get_json()
        try:
            becario.nombre = data.get('nombre', becario.nombre)
            becario.apellido = data.get('apellido', becario.apellido)
            becario.horas = data.get('horas', becario.horas)
            becario.gradoAcademicoId = data.get('gradoAcademicoId', becario.gradoAcademicoId)
            becario.institucionId = data.get('institucionId', becario.institucionId)

            becario.rol = data.get('rol', becario.rol)

            db.session.commit()

            return jsonify({
                "mensaje:" : "Becario actualizado exitosamente",
                "becario": becario.to_dict()
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400
    
    def delete(self, id):
        becario = Becario.query.filter_by(id=id).first()
        if not becario:
            return jsonify({"error": "Becario no encontrado"}), 404
        try:
            db.session.delete(becario)
            db.session.commit()
            return jsonify({"mensaje": "Becario eliminado exitosamente"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400

becario_view = ControladorBecario.as_view('controlador_becario')

#API
becario_bp.add_url_rule('/', defaults={'id': None}, view_func=becario_view, methods=['GET',])
becario_bp.add_url_rule('/', view_func=becario_view, methods=['POST',])
becario_bp.add_url_rule('/<int:id>', view_func=becario_view, methods=['GET', 'PUT', 'DELETE'])
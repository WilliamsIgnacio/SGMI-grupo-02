from flask import Blueprint, request, jsonify
from flask.views import MethodView
from database import db
from models.personal import Soporte

soporte_bp = Blueprint('soporte_bp', __name__)

class ControladorSoporte(MethodView):
    def get(self, id=None):
        if id is None:
            soportes = Soporte.query.all()
            return jsonify([soporte.to_dict() for soporte in soportes]), 200
        else:
            soporte = Soporte.query.filter_by(id=id).first()
            if soporte:
                return jsonify(soporte.to_dict()), 200
            else:
                return jsonify({"error": "Soporte no encontrado"}), 404
    
    
    def post(self):
        data = request.get_json()
        try:
            nuevoSoporte = Soporte(
                nombre=data.get('nombre'),
                apellido=data.get('apellido'),
                horas=data.get('horas'),
                gradoAcademicoId=data.get('gradoAcademicoId'),
                institucionId=data.get('institucionId'),

                rol=data.get('rol'),
            )

            db.session.add(nuevoSoporte)
            db.session.commit()

            return jsonify({
                "mensaje:" : "Becario creado exitosamente",
                "becario": nuevoSoporte.to_dict()
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400

    def put(self, id):
        soporte = Soporte.query.filter_by(id=id).first()
        if not soporte:
            return jsonify({"error": "Becario no encontrado"}), 404
        data = request.get_json()
        try:
            soporte.nombre = data.get('nombre', soporte.nombre)
            soporte.apellido = data.get('apellido', soporte.apellido)
            soporte.horas = data.get('horas', soporte.horas)
            soporte.gradoAcademicoId = data.get('gradoAcademicoId', soporte.gradoAcademicoId)
            soporte.institucionId = data.get('institucionId', soporte.institucionId)

            soporte.rol = data.get('rol', soporte.rol)

            db.session.commit()

            return jsonify({
                "mensaje:" : "Becario actualizado exitosamente",
                "becario": soporte.to_dict()
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400

    def delete(self, id):
        soporte = Soporte.query.filter_by(id=id).first()
        if not soporte:
            return jsonify({"error": "Becario no encontrado"}), 404
        try:
            db.session.delete(soporte)
            db.session.commit()
            return jsonify({"mensaje": "Becario eliminado exitosamente"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400

soporte_view = ControladorSoporte.as_view('controlador_soporte')

#API
soporte_bp.add_url_rule('/', defaults={'id': None}, view_func=soporte_view, methods=['GET',])
soporte_bp.add_url_rule('/', view_func=soporte_view, methods=['POST',])
soporte_bp.add_url_rule('/<int:id>', view_func=soporte_view, methods=['GET', 'PUT', 'DELETE'])
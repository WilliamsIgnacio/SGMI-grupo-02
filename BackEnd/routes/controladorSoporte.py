from flask import Blueprint, request, jsonify
from flask.views import MethodView
from app import db
from models.personal import Personal

soporte_bp = Blueprint('becario_bp', __name__)

class ControladorSoporte(MethodView):
    def get(self):
        soportes = Personal.query.filter_by(object_type='soporte').all()
        return jsonify([soporte.to_dict() for soporte in soportes])
    
    def post(self):
        data = request.get_json()
        try:
            nuevoSoporte = Personal(
                nombre=data.get('nombre'),
                apellido=data.get('apellido'),
                horas=data.get('horas'),
                gradoAcademicoId=data.get('gradoAcademicoId'),
                institucionId=data.get('institucionId'),

                rol=data.get('rol'),

                objectType='becario',
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

soporte_view = ControladorSoporte.as_view('controlador_soporte')

#API
soporte_bp.add_url_rule('/soportes', view_func=soporte_view, methods=['GET', 'POST'])
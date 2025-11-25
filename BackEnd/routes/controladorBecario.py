from flask import Blueprint, request, jsonify
from flask.views import MethodView
from app import db
from models.personal import Personal

becario_bp = Blueprint('becario_bp', __name__)

class ControladorBecario(MethodView):
    def get(self):
        becarios = Personal.query.filter_by(object_type='becario').all()
        return jsonify([becario.to_dict() for becario in becarios])
    
    def post(self):
        data = request.get_json()
        try:
            nuevoBecario = Personal(
                nombre=data.get('nombre'),
                apellido=data.get('apellido'),
                horas=data.get('horas'),
                gradoAcademicoId=data.get('gradoAcademicoId'),
                institucionId=data.get('institucionId'),

                rol=data.get('rol'),

                objectType='becario',
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

becario_view = ControladorBecario.as_view('controlador_becario')

#API
becario_bp.add_url_rule('/becarios', view_func=becario_view, methods=['GET', 'POST'])
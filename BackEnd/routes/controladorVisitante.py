from flask import Blueprint, request, jsonify
from flask.views import MethodView
from app import db
from models.personal import Personal

visitante_bp = Blueprint('visitante_bp', __name__)

class ControladorVisitante(MethodView):
    def get(self):
        visitantes = Personal.query.filter_by(object_type='visitante').all()
        return jsonify([visitante.to_dict() for visitante in visitantes])
    
    def post(self):
        data = request.get_json()
        try:
            nuevoVisitante = Personal(
                nombre=data.get('nombre'),
                apellido=data.get('apellido'),
                horas=data.get('horas'),
                gradoAcademicoId=data.get('gradoAcademicoId'),
                institucionId=data.get('institucionId'),

                rol=data.get('rol'),

                objectType='visitante',
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

visitante_view = ControladorVisitante.as_view('controlador_visitante')

#API
visitante_bp.add_url_rule('/visitantes', view_func=visitante_view, methods=['GET', 'POST'])
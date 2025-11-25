from flask import Blueprint, request, jsonify
from flask.views import MethodView
from app import db
from models.personal import Personal

investigador_bp = Blueprint('investigador_bp', __name__)

class ControladorInvestigador(MethodView):
    def get(self):
        investigadores = Personal.query.filter_by(object_type='investigador').all()
        return jsonify([investigador.to_dict() for investigador in investigadores])
    
    def post(self):
        data = request.get_json()
        try:
            nuevoInvestigador = Personal(
                nombre=data.get['nombre'],
                apellido=data.get['apellido'],
                horas=data.get['horas'],
                gradoAcademicoId=data.get['gradoAcademicoId'],
                institucionId=data.get['institucionId'],

                categoria=data.get['categoria'],
                incentivo=data.get['incentivo'],
                dedicacion=data.get['dedicacion'],

                objectType='investigador',
            )

            db.session.add(nuevoInvestigador)
            db.session.commit()

            return jsonify({
                "mensaje:" : "Investigador creado exitosamente",
                "investigador": nuevoInvestigador.to_dict()
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400
        
investigador_view = ControladorInvestigador.as_view('controlador_investigador')

#API
investigador_bp.add_url_rule('/investigadores', view_func=investigador_view, methods=['GET', 'POST'])
  
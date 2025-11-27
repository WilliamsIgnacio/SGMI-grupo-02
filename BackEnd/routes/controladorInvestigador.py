from flask import Blueprint, request, jsonify
from flask.views import MethodView
from database import db
from models.personal import Investigador

investigador_bp = Blueprint('investigador_bp', __name__)

class ControladorInvestigador(MethodView):
    def get(self, id=None):
        if id is None:
            investigadores = Investigador.query.all()
            return jsonify([investigador.to_dict() for investigador in investigadores]), 200
        else:
            investigador = Investigador.query.filter_by(id=id).first()
            if investigador:
                return jsonify(investigador.to_dict()), 200
            else:
                return jsonify({"error": "Investigador no encontrado"}), 404
    
    def post(self):
        data = request.get_json()
        try:
            nuevoInvestigador = Investigador(
                nombre=data.get('nombre'),
                apellido=data.get('apellido'),
                horas=data.get('horas'),
                gradoAcademicoId=data.get('gradoAcademicoId'),
                institucion=data.get('institucionId'),

                categoria=data.get('categoria'),
                incentivo=data.get('incentivo'),
                dedicacion=data.get('dedicacion'),
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
        
    def put(self, id):
        investigador = Investigador.query.filter_by(id=id).first()
        if not investigador:
            return jsonify({"error": "Investigador no encontrado"}), 404
        data = request.get_json()
        try:
            investigador.nombre = data.get('nombre', investigador.nombre)
            investigador.apellido = data.get('apellido', investigador.apellido)
            investigador.horas = data.get('horas', investigador.horas)
            investigador.gradoAcademicoId = data.get('gradoAcademicoId', investigador.gradoAcademicoId)
            investigador.institucionId = data.get('institucionId', investigador.institucionId)

            investigador.categoria = data.get('categoria', investigador.categoria)
            investigador.incentivo = data.get('incentivo', investigador.incentivo)
            investigador.dedicacion = data.get('dedicacion', investigador.dedicacion)

            db.session.commit()

            return jsonify({
                "mensaje": "Investigador actualizado exitosamente",
                "investigador": investigador.to_dict()
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400
        
    def delete(self, id):
        investigador = Investigador.query.filter_by(id=id).first()
        if not investigador:
            return jsonify({"error": "Investigador no encontrado"}), 404
        try:
            db.session.delete(investigador)
            db.session.commit()
            return jsonify({"mensaje": "Investigador eliminado exitosamente"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400

investigador_view = ControladorInvestigador.as_view('controlador_investigador')

#API
investigador_bp.add_url_rule('/', defaults={'id': None}, view_func=investigador_view, methods=['GET',])
investigador_bp.add_url_rule('/', view_func=investigador_view, methods=['POST',])
investigador_bp.add_url_rule('/<int:id>', view_func=investigador_view, methods=['GET', 'PUT', 'DELETE'])
from flask import Blueprint, request, jsonify
from flask.views import MethodView
from database import db
from models.personal import Investigador
from models.gradoAcademico import GradoAcademico

investigador_bp = Blueprint('investigador_bp', __name__)

class ControladorInvestigador(MethodView):

    def crearInvestigador(self, data):
            
            grado = data.get('gradoAcademicoId')
            gradoObj = GradoAcademico.query.filter_by(id=grado).first()
            if not gradoObj:
                raise ValueError("Grado Académico no encontrado")
            try: 
                nuevoInvestigador = Investigador(
                    nombre=data.get('nombre'),
                    apellido=data.get('apellido'),
                    horas=data.get('horas'),
                    correo_electronico=data.get('correoElectronico'),
                    gradoAcademicoId=data.get('gradoAcademicoId'),
                    institucionId=data.get('institucionId'),

                    categoria=data.get('categoria'),
                    incentivo=data.get('incentivo'),
                    dedicacion=data.get('dedicacion'),
                )

                db.session.add(nuevoInvestigador)
                db.session.commit()
                return nuevoInvestigador
            except Exception as e:
                db.session.rollback()
                raise e
    
    def modificarInvestigador(self, id, data):
        investigador = Investigador.query.filter_by(id=id).first()
        if not investigador:
            return None
        try:
            if 'gradoAcademicoId' in data:
                grado = data.get('gradoAcademicoId')
                gradoObj = GradoAcademico.query.filter_by(id=grado).first()
                if not gradoObj:
                    raise ValueError("Grado Académico no encontrado")
                investigador.gradoAcademicoId = gradoObj.id
            investigador.nombre = data.get('nombre', investigador.nombre)
            investigador.apellido = data.get('apellido', investigador.apellido)
            investigador.horas = data.get('horas', investigador.horas)
            investigador.correo_electronico = data.get('correoElectronico', investigador.correo_electronico)
            investigador.institucionId = data.get('institucionId', investigador.institucionId)

            investigador.categoria = data.get('categoria', investigador.categoria)
            investigador.incentivo = data.get('incentivo', investigador.incentivo)
            investigador.dedicacion = data.get('dedicacion', investigador.dedicacion)

            db.session.commit()
            return investigador
        except Exception as e:
            db.session.rollback()
            raise e


    def eliminarInvestigador(self, id):
        investigador = Investigador.query.filter_by(id=id).first()
        if not investigador:
            return False
        try:
            db.session.delete(investigador)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e

    #HTTP
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
            nuevoInvestigador = self.crearInvestigador(data)
            return jsonify({
                "mensaje" : "Investigador creado exitosamente",
                "investigador": nuevoInvestigador.to_dict()
            }), 201
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
        except Exception as e:
            return jsonify({"error": "Error al crear" + str(e)}), 500
        
    def put(self, id):
        data = request.get_json()

        try:
            investigador = self.modificarInvestigador(id, data)
            if not investigador:
                return jsonify({"error": "Investigador no encontrado"}), 404
            return jsonify({
                "mensaje": "Investigador actualizado exitosamente",
                "investigador": investigador.to_dict()
            }), 200
        
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
    
        except Exception as e:
            return jsonify({"error al modificar": str(e)}), 500
        
    def delete(self, id):
        try:
            exito = self.eliminarInvestigador(id)
            if not exito:
                return jsonify({"error": "Investigador no encontrado"}), 404
            return jsonify({"mensaje": "Investigador eliminado exitosamente"}), 200
            
        except Exception as e:
            return jsonify({"error al eliminar": str(e)}), 500

investigador_view = ControladorInvestigador.as_view('controlador_investigador')

#API
investigador_bp.add_url_rule('/', defaults={'id': None}, view_func=investigador_view, methods=['GET',])
investigador_bp.add_url_rule('/', view_func=investigador_view, methods=['POST',])
investigador_bp.add_url_rule('/<int:id>', view_func=investigador_view, methods=['GET', 'PUT', 'DELETE'])
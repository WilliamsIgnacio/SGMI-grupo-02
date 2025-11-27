from flask import Blueprint, jsonify, request
from flask.views import MethodView
from models.gradoAcademico import GradoAcademico
from database import db

grado_academico_bp = Blueprint('grado_academico_bp', __name__)

class ControladorGradoAcademico(MethodView):
    def get(self, id=None):
        if id:
            grado = GradoAcademico.query.get(id)
            if grado:
                return jsonify(grado.to_dict()), 200
            return jsonify({'message': 'Grado Academico no encontrado'}), 404
        else:
            grados = GradoAcademico.query.all()
            return jsonify([grado.to_dict() for grado in grados]), 200
        
    def post(self):
        data = request.get_json()
        new_grado = GradoAcademico(
            nombre=data.get('nombre')
        )
        db.session.add(new_grado)
        db.session.commit()
        return jsonify(new_grado.to_dict()), 201
    
    def put(self, id):
        grado = GradoAcademico.query.get(id)
        if not grado:
            return jsonify({'message': 'Grado Academico no encontrado'}), 404
        
        data = request.get_json()
        grado.nombre = data.get('nombre', grado.nombre)
        
        db.session.commit()
        return jsonify(grado.to_dict()), 200
    
    def delete(self, id):
        grado = GradoAcademico.query.get(id)
        if not grado:
            return jsonify({'message': 'Grado Academico no encontrado'}), 404
        
        db.session.delete(grado)
        db.session.commit()
        return jsonify({'message': 'Grado Academico eliminado'}), 200 
    
grado_view = ControladorGradoAcademico.as_view('controlador_grado_academico')

# Rutas
grado_academico_bp.add_url_rule('/', defaults={'id': None}, view_func=grado_view, methods=['GET'])
grado_academico_bp.add_url_rule('/', view_func=grado_view, methods=['POST'])
grado_academico_bp.add_url_rule('/<int:id>', view_func=grado_view, methods=['GET', 'PUT', 'DELETE'])
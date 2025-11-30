from flask import Blueprint, jsonify
from flask.views import MethodView
from models.enums import RolesSoporte, RolesVisitante, TipoFormacion

enums_bp = Blueprint('enums_bp', __name__)

class ControladorEnums(MethodView):
    def get(self):
        return jsonify({
            "rolesSoporte": [e.value for e in RolesSoporte],
            "rolesVisitante": [e.value for e in RolesVisitante],
            "tipoFormacion": [e.value for e in TipoFormacion]
        }), 200

enums_view = ControladorEnums.as_view('controlador_enums')

# API
enums_bp.add_url_rule('/', view_func=enums_view, methods=['GET'])
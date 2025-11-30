"""
Controlador Blueprint para el módulo Experto de Información
Proporciona endpoints REST para acceder a datos usando el patrón Expert
"""

from flask import Blueprint, jsonify, request
from database import db
from routes.Experto import ExpertoInformacion
from models.grupo import Grupo
from models.proyecto import Proyecto
from models.equipamiento import Equipamiento
from models.bibliografia import Bibliografia

experto_bp = Blueprint('experto', __name__, url_prefix='/api/experto')


@experto_bp.route('/estadisticas', methods=['GET'])
def obtener_estadisticas():
    """
    GET /api/experto/estadisticas
    Obtiene estadísticas de todas las tablas (conteo de registros).
    """
    try:
        experto = ExpertoInformacion(db.session)
        estadisticas = experto.obtener_estadisticas()
        return jsonify(estadisticas), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@experto_bp.route('/todas-entidades', methods=['GET'])
def obtener_todas_entidades():
    """
    GET /api/experto/todas-entidades
    Obtiene todos los registros de todas las tablas.
    """
    try:
        experto = ExpertoInformacion(db.session)
        datos = experto.obtener_todas_entidades()
        return jsonify(datos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@experto_bp.route('/grupo/<int:id_grupo>', methods=['GET'])
def obtener_datos_grupo(id_grupo):
    """
    GET /api/experto/grupo/<id>
    Obtiene todos los datos relacionados con un grupo específico.
    """
    try:
        experto = ExpertoInformacion(db.session)
        datos = experto.obtener_datos_grupo(id_grupo)
        return jsonify(datos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@experto_bp.route('/grupo/<int:id_grupo>/por-fecha', methods=['GET'])
def obtener_datos_grupo_por_fecha(id_grupo):
    """
    GET /api/experto/grupo/<id>/por-fecha?fecha_inicio=YYYY-MM-DD&fecha_fin=YYYY-MM-DD&tabla_filtro=tabla
    Obtiene datos de un grupo filtrados por rango de fechas.
    
    Query params:
    - fecha_inicio: Fecha de inicio del filtro (formato YYYY-MM-DD)
    - fecha_fin: Fecha de fin del filtro (formato YYYY-MM-DD)
    - tabla_filtro: (Opcional) Tabla específica a filtrar ('proyecto', 'equipamiento', 'bibliografia')
    """
    try:
        fecha_inicio = request.args.get('fecha_inicio')
        fecha_fin = request.args.get('fecha_fin')
        tabla_filtro = request.args.get('tabla_filtro')
        
        experto = ExpertoInformacion(db.session)
        datos = experto.obtener_datos_grupo_por_fecha(
            id_grupo=id_grupo,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            tabla_filtro=tabla_filtro
        )
        return jsonify(datos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@experto_bp.route('/<tabla>/<id_valor>', methods=['GET'])
def obtener_por_id(tabla, id_valor):
    """
    GET /api/experto/<tabla>/<id>
    Obtiene un registro específico por su ID de cualquier tabla.
    
    Ejemplos:
    - /api/experto/grupo/1
    - /api/experto/proyecto/5
    """
    try:
        # Mapeo de nombres de tabla a clases de modelo
        modelos = {
            'grupo': Grupo,
            'proyecto': Proyecto,
            'equipamiento': Equipamiento,
            'bibliografia': Bibliografia,
            # Se pueden agregar más modelos según sea necesario
        }
        
        model_class = modelos.get(tabla.lower())
        if not model_class:
            return jsonify({"error": f"Tabla '{tabla}' no encontrada o no soportada"}), 404
        
        experto = ExpertoInformacion(db.session)
        datos = experto.obtener_por_id(model_class, id_valor)
        
        if datos is None:
            return jsonify({"error": f"Registro con ID {id_valor} no encontrado en tabla {tabla}"}), 404
        
        return jsonify(datos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

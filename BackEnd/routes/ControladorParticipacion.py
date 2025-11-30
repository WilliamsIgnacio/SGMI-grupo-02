"""Controlador de Participacion."""

from sqlalchemy.exc import IntegrityError
from flask import Blueprint, request, jsonify
from database import db

# Import ORM models
from models.models_db import Participacion, ParticipacionPersona, Institucion, RolParticipacion
from models.grupo import Grupo
from models.personal import Personal as Persona

participacion_bp = Blueprint('participacion', __name__, url_prefix='/api/participacion')

# ============ PARTICIPACION CRUD ENDPOINTS ============

@participacion_bp.route('', methods=['GET'])
def list_participaciones():
    try:
        grupo_id = request.args.get('grupo_id', type=int)
        query = db.session.query(Participacion)
        
        if grupo_id:
            query = query.filter(Participacion.grupo == grupo_id)
        
        result = []
        for p in query.all():
            result.append({
                'id': p.id,
                'grupo_id': p.grupo,
                'institucion_id': p.institucion,
                'rol_id': p.rol,
                'personal_id': p.personal
            })
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'success': False, 'message': f'Database error: {str(e)}'}), 500

@participacion_bp.route('', methods=['POST'])
def create_participacion():
    data = request.get_json(silent=True)
    if not data: return jsonify({'success': False, 'message': 'Invalid JSON'}), 400
    
    required = ['grupo', 'institucion', 'rol', 'persona']
    missing = [f for f in required if f not in data]
    if missing: return jsonify({'success': False, 'message': f'Missing fields: {missing}'}), 400
    
    try:
        # Validaciones de existencia
        if not db.session.query(Grupo).get(data['grupo']):
            return jsonify({'success': False, 'message': 'Grupo not found'}), 404
        if not db.session.query(Institucion).get(data['institucion']):
            return jsonify({'success': False, 'message': 'Institucion not found'}), 404
        if not db.session.query(RolParticipacion).get(data['rol']):
            return jsonify({'success': False, 'message': 'Rol not found'}), 404
        if not db.session.query(Persona).get(data['persona']):
            return jsonify({'success': False, 'message': 'Persona not found'}), 404
        
        participacion = Participacion(
            grupo=data['grupo'],
            institucion=data['institucion'],
            rol=data['rol'],
            personal=data['persona']
        )
        db.session.add(participacion)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Participacion created', 'id': participacion.id}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Integrity error'}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Database error: {str(e)}'}), 500

@participacion_bp.route('/<int:participacion_id>', methods=['GET'])
def get_participacion(participacion_id):
    try:
        p = db.session.query(Participacion).get(participacion_id)
        if not p: return jsonify({'success': False, 'message': 'Not found'}), 404
        
        return jsonify({
            'id': p.id,
            'grupo_id': p.grupo,
            'institucion_id': p.institucion,
            'rol_id': p.rol,
            'personal_id': p.personal
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@participacion_bp.route('/<int:participacion_id>', methods=['PUT'])
def update_participacion(participacion_id):
    data = request.get_json(silent=True)
    try:
        p = db.session.query(Participacion).get(participacion_id)
        if not p: return jsonify({'success': False, 'message': 'Not found'}), 404
        
        # Actualizar Grupo
        if 'grupo' in data: 
            grupo = db.session.query(Grupo).get(data['grupo'])
            if not grupo: return jsonify({'success': False, 'message': 'Grupo not found'}), 404
            p.grupo = data['grupo']

        # Actualizar Institución
        if 'institucion' in data: 
            instit = db.session.query(Institucion).get(data['institucion'])
            if not instit: return jsonify({'success': False, 'message': 'Institucion not found'}), 404
            p.institucion = data['institucion']

        # Actualizar Rol
        if 'rol' in data: 
            rol = db.session.query(RolParticipacion).get(data['rol'])
            if not rol: return jsonify({'success': False, 'message': 'Rol not found'}), 404
            p.rol = data['rol']
        
        # --- NUEVO: Actualizar Persona ---
        if 'persona' in data:
            persona = db.session.query(Persona).get(data['persona'])
            if not persona: return jsonify({'success': False, 'message': 'Persona not found'}), 404
            p.personal = data['persona']
        
        db.session.commit()
        return jsonify({'success': True, 'message': 'Updated'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@participacion_bp.route('/<int:participacion_id>', methods=['DELETE'])
def delete_participacion(participacion_id):
    try:
        p = db.session.query(Participacion).get(participacion_id)
        if not p: return jsonify({'success': False, 'message': 'Not found'}), 404
        db.session.delete(p)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Deleted'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

# ============ ROL PARTICIPACION ============

@participacion_bp.route('/roles', methods=['GET'])
def list_rol_participacion():
    try:
        roles = db.session.query(RolParticipacion).all()
        return jsonify([{'id': r.id, 'nombre': r.nombre} for r in roles]), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@participacion_bp.route('/roles', methods=['POST'])
def create_rol_participacion():
    data = request.get_json(silent=True)
    if not data or 'nombre' not in data:
        return jsonify({'success': False, 'message': 'Missing name'}), 400
    try:
        rol = RolParticipacion(nombre=data['nombre'])
        db.session.add(rol)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Rol created', 'id': rol.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
"""Controlador de Organizaciones - API endpoints for managing groups/organizations.

Uses SQLAlchemy ORM models from models to handle CRUD operations
on Grupo, PersonaGrupo, and related group management entities.
"""

from datetime import date
from sqlalchemy.exc import IntegrityError
from flask import Blueprint, request, jsonify

# Import ORM models
from database import db
from models.grupo import Grupo
from models.personaGrupo import PersonaGrupo
from models.personal import Personal as Persona

# Create blueprint for group management routes
org_bp = Blueprint('organizaciones', __name__, url_prefix='/api/organizaciones')

# ============ GRUPO CRUD ENDPOINTS ============

@org_bp.route('', methods=['GET'])
def list_grupos():
    try:
        grupos = db.session.query(Grupo).all()
        
        result = []
        for g in grupos:
            result.append({
                'id': g.id,
                'sigla': g.sigla,
                'nombre': g.nombre,
                'objetivos': g.objetivos,
                'organigrama': g.organigrama,
                'correoElectronico': g.correoElectronico,
                'director': g.director,
                'vicedirector': g.vicedirector,
                'consejo_ejecutivo': g.consejo_ejecutivo,
                'unidad_academica': g.unidad_academica
            })
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'success': False, 'message': f'Database error: {str(e)}'}), 500


@org_bp.route('', methods=['POST'])
def create_grupo():
    """Create a new grupo (group/organization)."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'success': False, 'message': 'Invalid JSON'}), 400
    
    required = ['sigla', 'nombre', 'objetivos']
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify({'success': False, 'message': f'Missing fields: {missing}'}), 400

    try:
        grupo = Grupo(
            sigla=data['sigla'],
            nombre=data['nombre'],
            objetivos=data['objetivos'],
            organigrama=data.get('organigrama'),
            correoElectronico=data.get('correoElectronico'),
            director=data.get('director'),
            vicedirector=data.get('vicedirector'),
            consejo_ejecutivo=data.get('consejo_ejecutivo'),
            unidad_academica=data.get('unidad_academica')
        )
        db.session.add(grupo)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Grupo created',
            'id': grupo.id
        }), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Integrity error'}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Database error: {str(e)}'}), 500


@org_bp.route('/<int:grupo_id>', methods=['GET'])
def get_grupo(grupo_id):
    """Get details of a specific grupo."""
    try:
        grupo = db.session.query(Grupo).filter(Grupo.id == grupo_id).first()
        if not grupo:
            return jsonify({'success': False, 'message': 'Grupo not found'}), 404
        
        return jsonify({
            'id': grupo.id,
            'sigla': grupo.sigla,
            'nombre': grupo.nombre,
            'objetivos': grupo.objetivos,
            'organigrama': grupo.organigrama,
            'correoElectronico': grupo.correoElectronico,
            'director': grupo.director,
            'vicedirector': grupo.vicedirector,
            'consejo_ejecutivo': grupo.consejo_ejecutivo,
            'unidad_academica': grupo.unidad_academica
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': f'Database error: {str(e)}'}), 500


@org_bp.route('/<int:grupo_id>', methods=['PUT'])
def update_grupo(grupo_id):
    """Update a grupo's fields."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'success': False, 'message': 'Invalid JSON'}), 400

    try:
        grupo = db.session.query(Grupo).filter(Grupo.id == grupo_id).first()
        if not grupo:
            return jsonify({'success': False, 'message': 'Grupo not found'}), 404
        
        # Update allowed fields
        allowed_fields = ['sigla', 'nombre', 'objetivos', 'organigrama',
                         'correoElectronico', 'director', 'vicedirector',
                         'consejo_ejecutivo', 'unidad_academica']
        for field in allowed_fields:
            if field in data:
                setattr(grupo, field, data[field])
        
        db.session.commit()
        return jsonify({'success': True, 'message': 'Grupo updated'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Database error: {str(e)}'}), 500

@org_bp.route('/<int:grupo_id>', methods=['DELETE'])
def delete_grupo(grupo_id):
    """Delete a grupo."""
    try:
        grupo = db.session.query(Grupo).filter(Grupo.id == grupo_id).first()
        if not grupo:
            return jsonify({'success': False, 'message': 'Grupo not found'}), 404
        
        db.session.delete(grupo)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Grupo deleted'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Database error: {str(e)}'}), 500


# ============ GRUPO MEMBERS ENDPOINTS ============

@org_bp.route('/<int:grupo_id>/miembros', methods=['GET'])
def get_grupo_miembros(grupo_id):
    """Get all members (personas) of a grupo."""
    try:
        grupo = db.session.query(Grupo).filter(Grupo.id == grupo_id).first()
        if not grupo:
            return jsonify({'success': False, 'message': 'Grupo not found'}), 404
        
        pg_list = db.session.query(PersonaGrupo).filter(PersonaGrupo.grupo == grupo_id).all()
        
        result = []
        for pg in pg_list:
            result.append({
                'id': pg.id,
                'persona_id': pg.persona,
                'fecha_inicio': pg.fecha_inicio.isoformat(),
                'fecha_fin': pg.fecha_fin.isoformat() if pg.fecha_fin else None
            })
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'success': False, 'message': f'Database error: {str(e)}'}), 500


@org_bp.route('/<int:grupo_id>/miembros', methods=['POST'])
def add_miembro_to_grupo(grupo_id):
    """Add a member (persona) to a grupo."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'success': False, 'message': 'Invalid JSON'}), 400
    
    required = ['persona', 'fecha_inicio']
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify({'success': False, 'message': f'Missing fields: {missing}'}), 400

    try:
        # Verify grupo exists
        grupo = db.session.query(Grupo).filter(Grupo.id == grupo_id).first()
        if not grupo:
            return jsonify({'success': False, 'message': 'Grupo not found'}), 404
        
        # Verify persona exists
        persona = db.session.query(Persona).filter(Persona.id == data['persona']).first()
        if not persona:
            return jsonify({'success': False, 'message': 'Persona not found'}), 404
        
        pg = PersonaGrupo(
            persona=data['persona'],
            grupo=grupo_id,
            fecha_inicio=date.fromisoformat(data['fecha_inicio']),
            fecha_fin=date.fromisoformat(data['fecha_fin']) if data.get('fecha_fin') else None
        )
        db.session.add(pg)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Member added to grupo',
            'id': pg.id
        }), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Integrity error'}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Database error: {str(e)}'}), 500

@org_bp.route('/<int:grupo_id>/miembros/<int:pg_id>', methods=['PUT'])
def update_miembro_grupo(grupo_id, pg_id):
    """Update a member's details in a grupo."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'success': False, 'message': 'Invalid JSON'}), 400

    try:
        pg = db.session.query(PersonaGrupo).filter(
            PersonaGrupo.id == pg_id,
            PersonaGrupo.grupo == grupo_id
        ).first()
        
        if not pg:
            return jsonify({'success': False, 'message': 'Member not found in grupo'}), 404
        
        # Update allowed fields
        allowed_fields = ['rol', 'institucion', 'fecha_inicio', 'fecha_fin']
        for field in allowed_fields:
            if field in data:
                if field in ['fecha_inicio', 'fecha_fin']:
                    setattr(pg, field, date.fromisoformat(data[field]) if data[field] else None)
                else:
                    setattr(pg, field, data[field])
        
        db.session.commit()
        return jsonify({'success': True, 'message': 'Member updated in grupo'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Database error: {str(e)}'}), 500


@org_bp.route('/<int:grupo_id>/miembros/<int:pg_id>', methods=['DELETE'])
def remove_miembro_from_grupo(grupo_id, pg_id):
    """Remove a member from a grupo."""
    try:
        pg = db.session.query(PersonaGrupo).filter(
            PersonaGrupo.id == pg_id,
            PersonaGrupo.grupo == grupo_id
        ).first()
        
        if not pg:
            return jsonify({'success': False, 'message': 'Member not found in grupo'}), 404
        
        db.session.delete(pg)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Member removed from grupo'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Database error: {str(e)}'}), 500

# ============ GRUPO DETALLE ============

@org_bp.route('/<int:grupo_id>/detalle', methods=['GET'])
def get_grupo_detalle(grupo_id):
    """
    Retorna la info del grupo y sus miembros.
    """
    try:
        grupo = db.session.query(Grupo).get(grupo_id)
        if not grupo: 
            return jsonify({'success': False, 'message': 'Grupo not found'}), 404

        # Datos básicos del grupo
        data = {
            'id': grupo.id,
            'sigla': grupo.sigla,
            'nombre': grupo.nombre,
            'objetivos': grupo.objetivos,
            'organigrama': grupo.organigrama,
            'correoElectronico': grupo.correoElectronico,
            'director': grupo.director,
            'vicedirector': grupo.vicedirector,
            'consejo_ejecutivo': grupo.consejo_ejecutivo,
            'unidad_academica': grupo.unidad_academica,
            'miembros': []
        }
        
        # Agregar miembros usando la relación existente
        for pg in grupo.persona_grupos:
            p = db.session.query(Persona).get(pg.persona)
            if p:
                data['miembros'].append({
                    'id': pg.id,
                    'persona': {
                        'id': p.id, 
                        'nombre': p.nombre, 
                        'apellido': p.apellido
                    },
                    'fecha_inicio': pg.fecha_inicio.isoformat(),
                    'fecha_fin': pg.fecha_fin.isoformat() if pg.fecha_fin else None
                })

        return jsonify(data), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

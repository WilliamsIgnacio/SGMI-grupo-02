"""Controlador de Organizaciones - API endpoints for managing groups/organizations.

Uses SQLAlchemy ORM models from models to handle CRUD operations
on Grupo, PersonaGrupo, and related group management entities.
"""

import os
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from flask import Blueprint, request, jsonify

# Import ORM models
from database import db
from models.grupo import Grupo
from models.personaGrupo import PersonaGrupo
from models.personal import Personal as Persona
from models.models_db import Institucion, Participacion, ParticipacionPersona
from models.proyecto import Proyecto
from models.equipamiento import Equipamiento
from models.bibliografia import Bibliografia

# Create blueprint for group management routes
org_bp = Blueprint('organizaciones', __name__, url_prefix='/api/organizaciones')

# Initialize database connection
def build_db_url():
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        return database_url
    user = os.getenv('PGUSER', '')
    password = os.getenv('PGPASSWORD', '')
    host = os.getenv('PGHOST', 'localhost')
    port = os.getenv('PGPORT', '5432')
    db = os.getenv('PGDATABASE', '')
    if user and password and db:
        return f'postgresql://{user}:{password}@{host}:{port}/{db}'
    return None


DB_URL = build_db_url() or "postgresql://postgres:Segundo_Francia_2025@db.hxrdfvfeiddvydvilrsa.supabase.co:5432/postgres"
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)


def get_session():
    """Return a new database session."""
    return SessionLocal()


# ============ GRUPO CRUD ENDPOINTS ============

@org_bp.route('', methods=['GET'])
def list_grupos():
    """List all grupos (groups/organizations)."""
    session = get_session()
    try:
        grupos = session.query(Grupo).all()
        
        result = []
        for g in grupos:
            result.append({
                'id': g.id,
                'sigla': g.sigla,
                'nombre': g.nombre,
                'objetivos': g.objetivos,
                'organigrama': g.organigrama,
                'consejo_ejecutivo': g.consejo_ejecutivo,
                'unidad_academica': g.unidad_academica
            })
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'success': False, 'message': f'Database error: {str(e)}'}), 500
    finally:
        session.close()


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
    
    session = get_session()
    try:
        grupo = Grupo(
            sigla=data['sigla'],
            nombre=data['nombre'],
            objetivos=data['objetivos'],
            organigrama=data.get('organigrama'),
            consejo_ejecutivo=data.get('consejo_ejecutivo'),
            unidad_academica=data.get('unidad_academica')
        )
        session.add(grupo)
        session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Grupo created',
            'id': grupo.id
        }), 201
    except IntegrityError:
        session.rollback()
        return jsonify({'success': False, 'message': 'Integrity error'}), 409
    except Exception as e:
        session.rollback()
        return jsonify({'success': False, 'message': f'Database error: {str(e)}'}), 500
    finally:
        session.close()


@org_bp.route('/<int:grupo_id>', methods=['GET'])
def get_grupo(grupo_id):
    """Get details of a specific grupo."""
    session = get_session()
    try:
        grupo = session.query(Grupo).filter(Grupo.id == grupo_id).first()
        if not grupo:
            return jsonify({'success': False, 'message': 'Grupo not found'}), 404
        
        return jsonify({
            'id': grupo.id,
            'sigla': grupo.sigla,
            'nombre': grupo.nombre,
            'objetivos': grupo.objetivos,
            'organigrama': grupo.organigrama,
            'consejo_ejecutivo': grupo.consejo_ejecutivo,
            'unidad_academica': grupo.unidad_academica
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': f'Database error: {str(e)}'}), 500
    finally:
        session.close()


@org_bp.route('/<int:grupo_id>', methods=['PUT'])
def update_grupo(grupo_id):
    """Update a grupo's fields."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'success': False, 'message': 'Invalid JSON'}), 400
    
    session = get_session()
    try:
        grupo = session.query(Grupo).filter(Grupo.id == grupo_id).first()
        if not grupo:
            return jsonify({'success': False, 'message': 'Grupo not found'}), 404
        
        # Update allowed fields
        allowed_fields = ['sigla', 'nombre', 'objetivos', 'organigrama',
                         'consejo_ejecutivo', 'unidad_academica']
        for field in allowed_fields:
            if field in data:
                setattr(grupo, field, data[field])
        
        session.commit()
        return jsonify({'success': True, 'message': 'Grupo updated'}), 200
    except Exception as e:
        session.rollback()
        return jsonify({'success': False, 'message': f'Database error: {str(e)}'}), 500
    finally:
        session.close()


@org_bp.route('/<int:grupo_id>', methods=['DELETE'])
def delete_grupo(grupo_id):
    """Delete a grupo."""
    session = get_session()
    try:
        grupo = session.query(Grupo).filter(Grupo.id == grupo_id).first()
        if not grupo:
            return jsonify({'success': False, 'message': 'Grupo not found'}), 404
        
        session.delete(grupo)
        session.commit()
        return jsonify({'success': True, 'message': 'Grupo deleted'}), 200
    except Exception as e:
        session.rollback()
        return jsonify({'success': False, 'message': f'Database error: {str(e)}'}), 500
    finally:
        session.close()


# ============ GRUPO MEMBERS ENDPOINTS ============

@org_bp.route('/<int:grupo_id>/miembros', methods=['GET'])
def get_grupo_miembros(grupo_id):
    """Get all members (personas) of a grupo."""
    session = get_session()
    try:
        grupo = session.query(Grupo).filter(Grupo.id == grupo_id).first()
        if not grupo:
            return jsonify({'success': False, 'message': 'Grupo not found'}), 404
        
        pg_list = session.query(PersonaGrupo).filter(PersonaGrupo.grupo == grupo_id).all()
        
        result = []
        for pg in pg_list:
            result.append({
                'id': pg.id,
                'persona_id': pg.persona,
                'rol_id': pg.rol,
                'institucion_id': pg.institucion,
                'fecha_inicio': pg.fecha_inicio.isoformat(),
                'fecha_fin': pg.fecha_fin.isoformat() if pg.fecha_fin else None
            })
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'success': False, 'message': f'Database error: {str(e)}'}), 500
    finally:
        session.close()


@org_bp.route('/<int:grupo_id>/miembros', methods=['POST'])
def add_miembro_to_grupo(grupo_id):
    """Add a member (persona) to a grupo."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'success': False, 'message': 'Invalid JSON'}), 400
    
    required = ['persona', 'rol', 'institucion', 'fecha_inicio']
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify({'success': False, 'message': f'Missing fields: {missing}'}), 400
    
    session = get_session()
    try:
        # Verify grupo exists
        grupo = session.query(Grupo).filter(Grupo.id == grupo_id).first()
        if not grupo:
            return jsonify({'success': False, 'message': 'Grupo not found'}), 404
        
        # Verify persona exists
        persona = session.query(Persona).filter(Persona.id == data['persona']).first()
        if not persona:
            return jsonify({'success': False, 'message': 'Persona not found'}), 404
        
        pg = PersonaGrupo(
            persona=data['persona'],
            grupo=grupo_id,
            rol=data['rol'],
            institucion=data['institucion'],
            fecha_inicio=date.fromisoformat(data['fecha_inicio']),
            fecha_fin=date.fromisoformat(data['fecha_fin']) if data.get('fecha_fin') else None
        )
        session.add(pg)
        session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Member added to grupo',
            'id': pg.id
        }), 201
    except IntegrityError:
        session.rollback()
        return jsonify({'success': False, 'message': 'Integrity error'}), 409
    except Exception as e:
        session.rollback()
        return jsonify({'success': False, 'message': f'Database error: {str(e)}'}), 500
    finally:
        session.close()


@org_bp.route('/<int:grupo_id>/miembros/<int:pg_id>', methods=['PUT'])
def update_miembro_grupo(grupo_id, pg_id):
    """Update a member's details in a grupo."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'success': False, 'message': 'Invalid JSON'}), 400
    
    session = get_session()
    try:
        pg = session.query(PersonaGrupo).filter(
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
        
        session.commit()
        return jsonify({'success': True, 'message': 'Member updated in grupo'}), 200
    except Exception as e:
        session.rollback()
        return jsonify({'success': False, 'message': f'Database error: {str(e)}'}), 500
    finally:
        session.close()


@org_bp.route('/<int:grupo_id>/miembros/<int:pg_id>', methods=['DELETE'])
def remove_miembro_from_grupo(grupo_id, pg_id):
    """Remove a member from a grupo."""
    session = get_session()
    try:
        pg = session.query(PersonaGrupo).filter(
            PersonaGrupo.id == pg_id,
            PersonaGrupo.grupo == grupo_id
        ).first()
        
        if not pg:
            return jsonify({'success': False, 'message': 'Member not found in grupo'}), 404
        
        session.delete(pg)
        session.commit()
        return jsonify({'success': True, 'message': 'Member removed from grupo'}), 200
    except Exception as e:
        session.rollback()
        return jsonify({'success': False, 'message': f'Database error: {str(e)}'}), 500
    finally:
        session.close()


# ============ GRUPO PROJECTS ENDPOINTS ============

@org_bp.route('/<int:grupo_id>/proyectos', methods=['GET'])
def get_grupo_proyectos(grupo_id):
    """Get all projects of a grupo."""
    session = get_session()
    try:
        grupo = session.query(Grupo).filter(Grupo.id == grupo_id).first()
        if not grupo:
            return jsonify({'success': False, 'message': 'Grupo not found'}), 404
        
        proyectos = session.query(Proyecto).filter(Proyecto.grupo == grupo_id).all()
        
        result = []
        for p in proyectos:
            result.append({
                'id': p.id,
                'tipo': p.tipo,
                'codigo': p.codigo,
                'nombre': p.nombre,
                'descripcion': p.descripcion,
                'fecha_inicio': p.fecha_inicio.isoformat(),
                'fecha_fin': p.fecha_fin.isoformat() if p.fecha_fin else None,
                'logros': p.logros,
                'dificultades': p.dificultades
            })
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'success': False, 'message': f'Database error: {str(e)}'}), 500
    finally:
        session.close()


@org_bp.route('/<int:grupo_id>/detalle', methods=['GET'])
def get_grupo_detalle(grupo_id):
    """Get all information about a specific grupo: basic fields, miembros,
    proyectos, equipamiento, bibliografia, participaciones."""
    session = get_session()
    try:
        grupo = session.query(Grupo).filter(Grupo.id == grupo_id).first()
        if not grupo:
            return jsonify({'success': False, 'message': 'Grupo not found'}), 404

        data = {
            'id': grupo.id,
            'sigla': grupo.sigla,
            'nombre': grupo.nombre,
            'objetivos': grupo.objetivos,
            'organigrama': grupo.organigrama,
            'consejo_ejecutivo': grupo.consejo_ejecutivo,
            'unidad_academica': grupo.unidad_academica
        }

        # Miembros con detalles de persona, rol e institucion
        miembros = []
        pg_list = session.query(PersonaGrupo).filter(PersonaGrupo.grupo == grupo_id).all()
        for pg in pg_list:
            persona = session.query(Persona).filter(Persona.id == pg.persona).first()
            rol = session.query(RolGrupo).filter(RolGrupo.id == pg.rol).first()
            instit = session.query(Institucion).filter(Institucion.id == pg.institucion).first()

            miembros.append({
                'id': pg.id,
                'persona': {
                    'id': persona.id if persona else None,
                    'nombre': persona.nombre if persona else None,
                    'apellido': persona.apellido if persona else None,
                    'horas': persona.horas if persona else None,
                    'institucion_id': persona.institucion if persona else None
                },
                'rol': {'id': rol.id, 'nombre': rol.nombre} if rol else None,
                'institucion': {'id': instit.id, 'descripcion': instit.descripcion} if instit else None,
                'fecha_inicio': pg.fecha_inicio.isoformat(),
                'fecha_fin': pg.fecha_fin.isoformat() if pg.fecha_fin else None
            })

        data['miembros'] = miembros

        # Proyectos
        proyectos = []
        for p in session.query(Proyecto).filter(Proyecto.grupo == grupo_id).all():
            proyectos.append({
                'id': p.id,
                'tipo': p.tipo,
                'codigo': p.codigo,
                'nombre': p.nombre,
                'descripcion': p.descripcion,
                'fecha_inicio': p.fecha_inicio.isoformat() if p.fecha_inicio else None,
                'fecha_fin': p.fecha_fin.isoformat() if p.fecha_fin else None,
                'logros': p.logros,
                'dificultades': p.dificultades
            })
        data['proyectos'] = proyectos

        # Equipamiento
        equipamientos = []
        for e in session.query(Equipamiento).filter(Equipamiento.grupo == grupo_id).all():
            equipamientos.append({
                'id': e.id,
                'denominacion': e.denominacion,
                'fechaIngreso': e.fechaIngreso.isoformat() if e.fechaIngreso else None,
                'monto': str(e.monto) if e.monto is not None else None,
                'descripcion': getattr(e, 'descripción', None),
                'actividad': e.actividad,
                'proyecto': e.proyecto
            })
        data['equipamientos'] = equipamientos

        # Bibliografia
        bibliografias = []
        for b in session.query(Bibliografia).filter(Bibliografia.grupo == grupo_id).all():
            bibliografias.append({
                'id': b.id,
                'titulo': b.titulo,
                'autores': b.autores,
                'editorial': b.editorial,
                'fecha': b.fecha.isoformat() if b.fecha else None
            })
        data['bibliografias'] = bibliografias

        # Participaciones (con personas asociadas)
        participaciones_out = []
        parts = session.query(Participacion).filter(Participacion.grupo == grupo_id).all()
        for part in parts:
            rolp = session.query(RolParticipacion).filter(RolParticipacion.id == part.rol).first()
            institp = session.query(Institucion).filter(Institucion.id == part.institucion).first()

            # personas asociadas a esta participacion
            pp_entries = session.query(ParticipacionPersona).filter(ParticipacionPersona.participacion == part.id).all()
            pp_personas = []
            for pp in pp_entries:
                persona = session.query(Persona).filter(Persona.id == pp.persona).first()
                if persona:
                    pp_personas.append({'id': persona.id, 'nombre': persona.nombre, 'apellido': persona.apellido})

            participaciones_out.append({
                'id': part.id,
                'rol': {'id': rolp.id, 'nombre': rolp.nombre} if rolp else None,
                'institucion': {'id': institp.id, 'descripcion': institp.descripcion} if institp else None,
                'personas': pp_personas,
                'personal': part.personal
            })

        data['participaciones'] = participaciones_out

        return jsonify(data), 200
    except Exception as e:
        return jsonify({'success': False, 'message': f'Database error: {str(e)}'}), 500
    finally:
        session.close()


# ============ ROL GRUPO MANAGEMENT ============

@org_bp.route('/roles', methods=['GET'])
def list_rol_grupo():
    """List all available grupo roles."""
    session = get_session()
    try:
        roles = session.query(RolGrupo).all()
        
        result = []
        for r in roles:
            result.append({
                'id': r.id,
                'nombre': r.nombre
            })
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'success': False, 'message': f'Database error: {str(e)}'}), 500
    finally:
        session.close()


@org_bp.route('/roles', methods=['POST'])
def create_rol_grupo():
    """Create a new grupo role."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'success': False, 'message': 'Invalid JSON'}), 400
    
    if 'nombre' not in data:
        return jsonify({'success': False, 'message': 'Missing field: nombre'}), 400
    
    session = get_session()
    try:
        rol = RolGrupo(nombre=data['nombre'])
        session.add(rol)
        session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Rol created',
            'id': rol.id
        }), 201
    except IntegrityError:
        session.rollback()
        return jsonify({'success': False, 'message': 'Integrity error'}), 409
    except Exception as e:
        session.rollback()
        return jsonify({'success': False, 'message': f'Database error: {str(e)}'}), 500
    finally:
        session.close()

from flask import Blueprint, request, jsonify
from flask.views import MethodView
from database import db

from models.models_db import LoginCredentials
import hashlib
import hmac
login_bp = Blueprint('login_bp', __name__)
def get_session():
    return db.session

@login_bp.route('/login', methods=['POST'])
def login():
    """
    Authenticate a user using Persona table from models_db.
    
    Expects JSON: {"email": "nombre@apellido", "password": "..."}
    Uses email formed from Persona.nombre + Persona.apellido as username.
    Hashes password with MD5 and compares against a stored hash 
    (can be extended to use a dedicated auth field).
    
    Returns main page on success, 401 on failure.
    """
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form.to_dict()

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'success': False, 'message': 'Missing email or password'}), 400

    # Compute MD5 hex digest (128-bit)
    provided_hash = hashlib.md5(password.encode('utf-8')).hexdigest()

    session = get_session()
    try:
        # Look up login record by exact email in login_details
        login = session.query(LoginCredentials).filter(LoginCredentials.email == email).first()
        if not login:
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

        # Check if account is active
        if hasattr(login, 'activo') and login.activo is False:
            return jsonify({'success': False, 'message': 'Account is deactivated'}), 403

        # Stored hash expected in `clave` column (stored as bytes/bytea); convert to string if necessary
        stored_hash = login.clave
        if isinstance(stored_hash, bytes):
            stored_hash = stored_hash.decode('utf-8')
        elif stored_hash is None:
            stored_hash = ''
        else:
            stored_hash = str(stored_hash)

        # Constant-time compare
        if not hmac.compare_digest(provided_hash, stored_hash):
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401


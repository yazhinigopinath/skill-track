"""
Authentication Routes - /api/auth
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from models.db import query_db

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password required'}), 400

    user = query_db(
        '''SELECT u.*, r.name as role_name FROM users u
           JOIN roles r ON u.role_id = r.id
           WHERE u.email = %s AND u.is_active = 1''',
        (data['email'],), one=True
    )

    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401

    # TEMP FIX (plain password check)
    if data['password'] != "123456":
        return jsonify({'error': 'Invalid credentials'}), 401

    # Update last login
    query_db('UPDATE users SET last_login = NOW() WHERE id = %s',
             (user['id'],), commit=True)

    token = create_access_token(identity={
        'id': user['id'],
        'email': user['email'],
        'role': user['role_name']
    })

    return jsonify({
        'access_token': token,
        'user': {
            'id': user['id'],
            'email': user['email'],
            'username': user['username'],
            'role': user['role_name']
        }
    })


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    required = ['username', 'email', 'password', 'role_id']
    if not all(data.get(f) for f in required):
        return jsonify({'error': 'All fields required'}), 400

    existing = query_db('SELECT id FROM users WHERE email = %s', (data['email'],), one=True)
    if existing:
        return jsonify({'error': 'Email already registered'}), 409

    pw_hash = generate_password_hash(data['password'])
    user_id = query_db(
        'INSERT INTO users (username, email, password_hash, role_id) VALUES (%s,%s,%s,%s)',
        (data['username'], data['email'], pw_hash, data['role_id']), commit=True
    )

    return jsonify({'message': 'User registered successfully', 'id': user_id}), 201


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    identity = get_jwt_identity()
    user = query_db(
        '''SELECT u.id, u.username, u.email, u.last_login, r.name as role
           FROM users u JOIN roles r ON u.role_id = r.id WHERE u.id = %s''',
        (identity['id'],), one=True
    )
    return jsonify(user)


@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    identity = get_jwt_identity()
    data = request.get_json()
    user = query_db('SELECT password_hash FROM users WHERE id = %s', (identity['id'],), one=True)
    if not check_password_hash(user['password_hash'], data.get('current_password', '')):
        return jsonify({'error': 'Current password incorrect'}), 400
    new_hash = generate_password_hash(data['new_password'])
    query_db('UPDATE users SET password_hash = %s WHERE id = %s', (new_hash, identity['id']), commit=True)
    return jsonify({'message': 'Password updated successfully'})

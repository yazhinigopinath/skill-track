"""Trainer Routes"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models.db import query_db

trainer_bp = Blueprint('trainers', __name__)

@trainer_bp.route('/', methods=['GET'])
@jwt_required()
def get_trainers():
    return jsonify(query_db('SELECT * FROM trainers ORDER BY full_name'))

@trainer_bp.route('/<int:tid>', methods=['GET'])
@jwt_required()
def get_trainer(tid):
    t = query_db('SELECT * FROM trainers WHERE id = %s', (tid,), one=True)
    return jsonify(t) if t else (jsonify({'error': 'Not found'}), 404)

@trainer_bp.route('/', methods=['POST'])
@jwt_required()
def create_trainer():
    d = request.get_json()
    nid = query_db(
        'INSERT INTO trainers (full_name, email, phone, specialization, experience_years, joined_date) VALUES (%s,%s,%s,%s,%s,%s)',
        (d['full_name'], d['email'], d.get('phone'), d.get('specialization'), d.get('experience_years', 0), d.get('joined_date')),
        commit=True
    )
    return jsonify({'message': 'Trainer created', 'id': nid}), 201

@trainer_bp.route('/<int:tid>', methods=['PUT'])
@jwt_required()
def update_trainer(tid):
    d = request.get_json()
    query_db(
        'UPDATE trainers SET full_name=%s, phone=%s, specialization=%s, experience_years=%s, status=%s WHERE id=%s',
        (d.get('full_name'), d.get('phone'), d.get('specialization'),
         d.get('experience_years', 0), d.get('status', 'Active'), tid),
        commit=True
    )
    return jsonify({'message': 'Trainer updated'})

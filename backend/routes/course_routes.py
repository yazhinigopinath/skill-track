"""Course Routes"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models.db import query_db

course_bp = Blueprint('courses', __name__)

@course_bp.route('/', methods=['GET'])
@jwt_required()
def get_courses():
    return jsonify(query_db("SELECT * FROM courses WHERE status='Active' ORDER BY title"))

@course_bp.route('/<int:cid>', methods=['GET'])
@jwt_required()
def get_course(cid):
    c = query_db('SELECT * FROM courses WHERE id=%s', (cid,), one=True)
    return jsonify(c) if c else (jsonify({'error': 'Not found'}), 404)

@course_bp.route('/', methods=['POST'])
@jwt_required()
def create_course():
    d = request.get_json()
    nid = query_db(
        'INSERT INTO courses (course_code, title, description, duration_weeks, fee) VALUES (%s,%s,%s,%s,%s)',
        (d['course_code'], d['title'], d.get('description'), d.get('duration_weeks'), d.get('fee')),
        commit=True
    )
    return jsonify({'message': 'Course created', 'id': nid}), 201

@course_bp.route('/<int:cid>', methods=['PUT'])
@jwt_required()
def update_course(cid):
    d = request.get_json()
    query_db('UPDATE courses SET title=%s, description=%s, fee=%s, status=%s WHERE id=%s',
             (d.get('title'), d.get('description'), d.get('fee'), d.get('status'), cid), commit=True)
    return jsonify({'message': 'Course updated'})

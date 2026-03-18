"""Batch Routes"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models.db import query_db

batch_bp = Blueprint('batches', __name__)

@batch_bp.route('/', methods=['GET'])
@jwt_required()
def get_batches():
    return jsonify(query_db('''
        SELECT b.*, c.title as course_title, t.full_name as trainer_name,
               COUNT(bs.student_id) as student_count
        FROM batches b
        JOIN courses c ON b.course_id = c.id
        LEFT JOIN trainers t ON b.trainer_id = t.id
        LEFT JOIN batch_students bs ON b.id = bs.batch_id
        GROUP BY b.id ORDER BY b.start_date DESC
    '''))

@batch_bp.route('/<int:bid>', methods=['GET'])
@jwt_required()
def get_batch(bid):
    b = query_db('''
        SELECT b.*, c.title as course_title, t.full_name as trainer_name
        FROM batches b JOIN courses c ON b.course_id=c.id
        LEFT JOIN trainers t ON b.trainer_id=t.id WHERE b.id=%s
    ''', (bid,), one=True)
    if not b: return jsonify({'error': 'Not found'}), 404
    students = query_db('''
        SELECT s.* FROM students s
        JOIN batch_students bs ON s.id=bs.student_id WHERE bs.batch_id=%s
    ''', (bid,))
    b['students'] = students
    return jsonify(b)

@batch_bp.route('/', methods=['POST'])
@jwt_required()
def create_batch():
    d = request.get_json()
    nid = query_db(
        'INSERT INTO batches (batch_code,course_id,trainer_id,batch_name,start_date,end_date,meeting_link,status) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)',
        (d['batch_code'],d['course_id'],d.get('trainer_id'),d['batch_name'],d.get('start_date'),d.get('end_date'),d.get('meeting_link'),'Upcoming'),
        commit=True
    )
    return jsonify({'message': 'Batch created', 'id': nid}), 201

@batch_bp.route('/<int:bid>/students', methods=['POST'])
@jwt_required()
def add_student_to_batch(bid):
    d = request.get_json()
    query_db('INSERT IGNORE INTO batch_students (batch_id,student_id) VALUES(%s,%s)',
             (bid, d['student_id']), commit=True)
    return jsonify({'message': 'Student added to batch'})

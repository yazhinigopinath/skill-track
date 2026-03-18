"""Student Routes - /api/students"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.db import query_db
import datetime

student_bp = Blueprint('students', __name__)

def gen_student_id():
    last = query_db("SELECT student_id FROM students ORDER BY id DESC LIMIT 1", one=True)
    if not last:
        return 'ST001'
    num = int(last['student_id'][2:]) + 1
    return f"ST{num:03d}"

@student_bp.route('/', methods=['GET'])
@jwt_required()
def get_students():
    students = query_db('''
        SELECT s.*, b.batch_name FROM students s
        LEFT JOIN batch_students bs ON s.id = bs.student_id
        LEFT JOIN batches b ON bs.batch_id = b.id
        ORDER BY s.created_at DESC
    ''')
    return jsonify(students)

@student_bp.route('/<int:sid>', methods=['GET'])
@jwt_required()
def get_student(sid):
    student = query_db('SELECT * FROM students WHERE id = %s', (sid,), one=True)
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    return jsonify(student)

@student_bp.route('/', methods=['POST'])
@jwt_required()
def create_student():
    data = request.get_json()
    sid = gen_student_id()
    new_id = query_db(
        '''INSERT INTO students (student_id, full_name, email, phone, address, dob, gender,
           qualification, enrolled_date, status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
        (sid, data['full_name'], data['email'], data.get('phone'), data.get('address'),
         data.get('dob'), data.get('gender'), data.get('qualification'),
         data.get('enrolled_date', str(datetime.date.today())), 'Active'),
        commit=True
    )
    return jsonify({'message': 'Student created', 'id': new_id, 'student_id': sid}), 201

@student_bp.route('/<int:sid>', methods=['PUT'])
@jwt_required()
def update_student(sid):
    data = request.get_json()
    query_db(
        '''UPDATE students SET full_name=%s, phone=%s, address=%s, qualification=%s, status=%s
           WHERE id=%s''',
        (data.get('full_name'), data.get('phone'), data.get('address'),
         data.get('qualification'), data.get('status'), sid), commit=True
    )
    return jsonify({'message': 'Student updated'})

@student_bp.route('/<int:sid>/attendance', methods=['GET'])
@jwt_required()
def student_attendance(sid):
    records = query_db('''
        SELECT a.*, b.batch_name FROM attendance a
        JOIN batches b ON a.batch_id = b.id
        WHERE a.student_id = %s ORDER BY a.date DESC
    ''', (sid,))
    return jsonify(records)

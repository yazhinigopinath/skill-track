"""Attendance Routes"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.db import query_db

attendance_bp = Blueprint('attendance', __name__)

@attendance_bp.route('/', methods=['GET'])
@jwt_required()
def get_attendance():
    batch_id = request.args.get('batch_id')
    date = request.args.get('date')
    sql = '''SELECT a.*, s.full_name, s.student_id FROM attendance a
             JOIN students s ON a.student_id=s.id WHERE 1=1'''
    params = []
    if batch_id:
        sql += ' AND a.batch_id=%s'; params.append(batch_id)
    if date:
        sql += ' AND a.date=%s'; params.append(date)
    sql += ' ORDER BY a.date DESC'
    return jsonify(query_db(sql, params))

@attendance_bp.route('/', methods=['POST'])
@jwt_required()
def mark_attendance():
    identity = get_jwt_identity()
    data = request.get_json()
    records = data.get('records', [])
    for rec in records:
        query_db('''
            INSERT INTO attendance (batch_id,student_id,date,status,in_time,out_time,marked_by)
            VALUES(%s,%s,%s,%s,%s,%s,%s)
            ON DUPLICATE KEY UPDATE status=%s, in_time=%s, out_time=%s
        ''', (rec['batch_id'], rec['student_id'], rec['date'], rec['status'],
              rec.get('in_time'), rec.get('out_time'), identity['id'],
              rec['status'], rec.get('in_time'), rec.get('out_time')), commit=True)
    return jsonify({'message': f'{len(records)} attendance records saved'})

@attendance_bp.route('/summary/<int:student_id>', methods=['GET'])
@jwt_required()
def attendance_summary(student_id):
    summary = query_db('''
        SELECT
            COUNT(*) as total,
            SUM(status='Present') as present,
            SUM(status='Absent') as absent,
            SUM(status='Leave') as on_leave,
            SUM(status='Late') as late,
            ROUND(SUM(status='Present')*100/COUNT(*),2) as percentage
        FROM attendance WHERE student_id=%s
    ''', (student_id,), one=True)
    return jsonify(summary)

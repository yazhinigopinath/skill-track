"""Assessment Routes"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.db import query_db

assessment_bp = Blueprint('assessments', __name__)

@assessment_bp.route('/', methods=['GET'])
@jwt_required()
def get_assessments():
    return jsonify(query_db('''SELECT a.*, b.batch_name FROM assessments a
        LEFT JOIN batches b ON a.batch_id=b.id ORDER BY a.scheduled_at DESC'''))

@assessment_bp.route('/', methods=['POST'])
@jwt_required()
def create_assessment():
    identity = get_jwt_identity()
    d = request.get_json()
    nid = query_db(
        'INSERT INTO assessments (title,assessment_type,batch_id,description,total_marks,pass_marks,duration_minutes,scheduled_at,created_by) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)',
        (d['title'],d.get('assessment_type','Aptitude'),d.get('batch_id'),d.get('description'),d.get('total_marks',100),d.get('pass_marks',40),d.get('duration_minutes',60),d.get('scheduled_at'),identity['id']),
        commit=True
    )
    return jsonify({'message': 'Assessment created', 'id': nid}), 201

@assessment_bp.route('/<int:aid>/results', methods=['POST'])
@jwt_required()
def submit_result(aid):
    d = request.get_json()
    assessment = query_db('SELECT pass_marks FROM assessments WHERE id=%s', (aid,), one=True)
    status = 'Pass' if d.get('score', 0) >= assessment['pass_marks'] else 'Fail'
    query_db(
        'INSERT INTO assessment_results (assessment_id,student_id,score,status,submitted_at) VALUES(%s,%s,%s,%s,NOW()) ON DUPLICATE KEY UPDATE score=%s,status=%s,submitted_at=NOW()',
        (aid,d['student_id'],d['score'],status,d['score'],status), commit=True
    )
    return jsonify({'message': 'Result submitted', 'status': status})

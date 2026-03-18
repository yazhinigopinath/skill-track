"""Job Routes"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.db import query_db

job_bp = Blueprint('jobs', __name__)

@job_bp.route('/', methods=['GET'])
@jwt_required()
def get_jobs():
    return jsonify(query_db("SELECT * FROM jobs WHERE status='Active' ORDER BY created_at DESC"))

@job_bp.route('/', methods=['POST'])
@jwt_required()
def create_job():
    identity = get_jwt_identity()
    d = request.get_json()
    nid = query_db(
        'INSERT INTO jobs (title,company,location,description,requirements,salary_range,job_type,posted_by,deadline) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)',
        (d['title'],d.get('company'),d.get('location'),d.get('description'),d.get('requirements'),d.get('salary_range'),d.get('job_type','Full-time'),identity['id'],d.get('deadline')),
        commit=True
    )
    return jsonify({'message': 'Job posted', 'id': nid}), 201

@job_bp.route('/<int:jid>/apply', methods=['POST'])
@jwt_required()
def apply_job(jid):
    d = request.get_json()
    query_db('INSERT IGNORE INTO job_applications (job_id,student_id) VALUES(%s,%s)',
             (jid, d['student_id']), commit=True)
    return jsonify({'message': 'Applied successfully'})

@job_bp.route('/<int:jid>/applications', methods=['GET'])
@jwt_required()
def job_applications(jid):
    return jsonify(query_db('''
        SELECT ja.*, s.full_name, s.student_id FROM job_applications ja
        JOIN students s ON ja.student_id=s.id WHERE ja.job_id=%s
    ''', (jid,)))

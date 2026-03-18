"""Project Routes"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.db import query_db

project_bp = Blueprint('projects', __name__)

@project_bp.route('/', methods=['GET'])
@jwt_required()
def get_projects():
    return jsonify(query_db('''
        SELECT p.*, b.batch_name, COUNT(t.id) as task_count FROM projects p
        LEFT JOIN batches b ON p.batch_id=b.id
        LEFT JOIN tasks t ON p.id=t.project_id
        GROUP BY p.id ORDER BY p.created_at DESC
    '''))

@project_bp.route('/', methods=['POST'])
@jwt_required()
def create_project():
    identity = get_jwt_identity()
    d = request.get_json()
    nid = query_db(
        'INSERT INTO projects (title,description,batch_id,assigned_by,deadline) VALUES(%s,%s,%s,%s,%s)',
        (d['title'], d.get('description'), d.get('batch_id'), identity['id'], d.get('deadline')),
        commit=True
    )
    return jsonify({'message': 'Project created', 'id': nid}), 201

@project_bp.route('/<int:pid>/tasks', methods=['GET'])
@jwt_required()
def get_tasks(pid):
    return jsonify(query_db('''
        SELECT t.*, s.full_name as student_name FROM tasks t
        JOIN students s ON t.student_id=s.id WHERE t.project_id=%s
    ''', (pid,)))

@project_bp.route('/<int:pid>/tasks', methods=['POST'])
@jwt_required()
def create_task(pid):
    d = request.get_json()
    nid = query_db(
        'INSERT INTO tasks (project_id,student_id,title,description,deadline,priority) VALUES(%s,%s,%s,%s,%s,%s)',
        (pid, d['student_id'], d['title'], d.get('description'), d.get('deadline'), d.get('priority','Medium')),
        commit=True
    )
    return jsonify({'message': 'Task created', 'id': nid}), 201

@project_bp.route('/tasks/<int:tid>', methods=['PUT'])
@jwt_required()
def update_task(tid):
    d = request.get_json()
    completed_at = 'NOW()' if d.get('status') == 'Completed' else None
    query_db('UPDATE tasks SET status=%s, completed_at=%s WHERE id=%s',
             (d.get('status'), completed_at, tid), commit=True)
    return jsonify({'message': 'Task updated'})

"""Lead Routes (Marketing)"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.db import query_db

lead_bp = Blueprint('leads', __name__)

@lead_bp.route('/', methods=['GET'])
@jwt_required()
def get_leads():
    status = request.args.get('status')
    sql = 'SELECT l.*, u.username as assigned_name FROM leads l LEFT JOIN users u ON l.assigned_to=u.id WHERE 1=1'
    params = []
    if status:
        sql += ' AND l.status=%s'; params.append(status)
    sql += ' ORDER BY l.created_at DESC'
    return jsonify(query_db(sql, params))

@lead_bp.route('/', methods=['POST'])
@jwt_required()
def create_lead():
    d = request.get_json()
    nid = query_db(
        'INSERT INTO leads (full_name,email,phone,source,interested_course,status,assigned_to) VALUES(%s,%s,%s,%s,%s,%s,%s)',
        (d['full_name'],d.get('email'),d.get('phone'),d.get('source','Website'),d.get('interested_course'),'New',d.get('assigned_to')),
        commit=True
    )
    return jsonify({'message': 'Lead created', 'id': nid}), 201

@lead_bp.route('/<int:lid>', methods=['PUT'])
@jwt_required()
def update_lead(lid):
    d = request.get_json()
    query_db('UPDATE leads SET status=%s,notes=%s,next_followup_date=%s WHERE id=%s',
             (d.get('status'),d.get('notes'),d.get('next_followup_date'),lid), commit=True)
    return jsonify({'message': 'Lead updated'})

@lead_bp.route('/<int:lid>/communicate', methods=['POST'])
@jwt_required()
def log_communication(lid):
    identity = get_jwt_identity()
    d = request.get_json()
    query_db('INSERT INTO lead_communications (lead_id,comm_type,message,sent_by) VALUES(%s,%s,%s,%s)',
             (lid,d.get('comm_type','Call'),d.get('message'),identity['id']), commit=True)
    return jsonify({'message': 'Communication logged'})

@lead_bp.route('/stats', methods=['GET'])
@jwt_required()
def lead_stats():
    return jsonify(query_db('''
        SELECT status, COUNT(*) as count FROM leads GROUP BY status ORDER BY count DESC
    '''))

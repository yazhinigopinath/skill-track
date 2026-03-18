"""Report Routes"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models.db import query_db

report_bp = Blueprint('reports', __name__)

@report_bp.route('/attendance-violations', methods=['GET'])
@jwt_required()
def attendance_violations():
    return jsonify(query_db('''
        SELECT s.student_id, s.full_name,
               COUNT(*) as total, SUM(a.status='Present') as present,
               ROUND(SUM(a.status='Present')*100/COUNT(*),1) as pct
        FROM attendance a JOIN students s ON a.student_id=s.id
        GROUP BY s.id HAVING pct < 75 ORDER BY pct ASC
    '''))

@report_bp.route('/project-violations', methods=['GET'])
@jwt_required()
def project_violations():
    return jsonify(query_db('''
        SELECT t.*, s.full_name, s.student_id, p.title as project_title
        FROM tasks t JOIN students s ON t.student_id=s.id
        JOIN projects p ON t.project_id=p.id
        WHERE t.deadline < NOW() AND t.status != 'Completed'
        ORDER BY t.deadline DESC
    '''))

@report_bp.route('/assessment-violations', methods=['GET'])
@jwt_required()
def assessment_violations():
    return jsonify(query_db('''
        SELECT ar.*, s.full_name, s.student_id, a.title as assessment_title, a.pass_marks
        FROM assessment_results ar
        JOIN students s ON ar.student_id=s.id
        JOIN assessments a ON ar.assessment_id=a.id
        WHERE ar.status='Fail' OR ar.status='Absent'
        ORDER BY ar.submitted_at DESC
    '''))

@report_bp.route('/dashboard-stats', methods=['GET'])
@jwt_required()
def dashboard_stats():
    return jsonify({
        'total_students': query_db("SELECT COUNT(*) as c FROM students WHERE status='Active'", one=True)['c'],
        'total_trainers': query_db("SELECT COUNT(*) as c FROM trainers WHERE status='Active'", one=True)['c'],
        'active_batches': query_db("SELECT COUNT(*) as c FROM batches WHERE status='Ongoing'", one=True)['c'],
        'total_courses': query_db("SELECT COUNT(*) as c FROM courses WHERE status='Active'", one=True)['c'],
        'open_jobs': query_db("SELECT COUNT(*) as c FROM jobs WHERE status='Active'", one=True)['c'],
        'new_leads': query_db("SELECT COUNT(*) as c FROM leads WHERE status='New'", one=True)['c'],
        'pending_fees': query_db("SELECT COALESCE(SUM(amount-paid_amount),0) as c FROM fees WHERE status IN ('Pending','Partial')", one=True)['c'],
    })

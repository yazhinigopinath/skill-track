"""
Skill Track - Training Institute Management System
Main Flask Application Entry Point
"""

from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta
import os

# Load .env if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from routes.auth_routes import auth_bp
from routes.student_routes import student_bp
from routes.trainer_routes import trainer_bp
from routes.course_routes import course_bp
from routes.batch_routes import batch_bp
from routes.attendance_routes import attendance_bp
from routes.project_routes import project_bp
from routes.job_routes import job_bp
from routes.assessment_routes import assessment_bp
from routes.report_routes import report_bp
from routes.lead_routes import lead_bp
from routes.fee_routes import fee_bp

app = Flask(__name__)

# ─── Configuration ───────────────────────────────────────────────────────────
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'skill-track-secret-key-2024')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-skill-track-2024')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=8)

# MySQL config
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'password')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'skill_track')

# Upload folder
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# ─── Extensions ──────────────────────────────────────────────────────────────
CORS(app, origins=['http://localhost:3000', 'http://127.0.0.1:5500', '*'])
jwt = JWTManager(app)

# ─── Register Blueprints ─────────────────────────────────────────────────────
app.register_blueprint(auth_bp,       url_prefix='/api/auth')
app.register_blueprint(student_bp,    url_prefix='/api/students')
app.register_blueprint(trainer_bp,    url_prefix='/api/trainers')
app.register_blueprint(course_bp,     url_prefix='/api/courses')
app.register_blueprint(batch_bp,      url_prefix='/api/batches')
app.register_blueprint(attendance_bp, url_prefix='/api/attendance')
app.register_blueprint(project_bp,    url_prefix='/api/projects')
app.register_blueprint(job_bp,        url_prefix='/api/jobs')
app.register_blueprint(assessment_bp, url_prefix='/api/assessments')
app.register_blueprint(report_bp,     url_prefix='/api/reports')
app.register_blueprint(lead_bp,       url_prefix='/api/leads')
app.register_blueprint(fee_bp,        url_prefix='/api/fees')

# ─── Health Check ────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return jsonify({
        'status': 'ok',
        'app': 'Skill Track API',
        'version': '1.0.0'
    })

@app.route('/api/health')
def health():
    return jsonify({'status': 'healthy', 'message': 'Skill Track backend running'})

# ─── JWT Error Handlers ──────────────────────────────────────────────────────
@jwt.unauthorized_loader
def unauthorized_response(callback):
    return jsonify({'error': 'Missing or invalid token'}), 401

@jwt.expired_token_loader
def expired_token_response(jwt_header, jwt_payload):
    return jsonify({'error': 'Token has expired'}), 401

# ─── Global Error Handlers ───────────────────────────────────────────────────
@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

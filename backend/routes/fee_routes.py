"""Fee Routes"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models.db import query_db
import datetime, random, string

fee_bp = Blueprint('fees', __name__)

def gen_receipt():
    return 'RCP-' + ''.join(random.choices(string.digits, k=8))

@fee_bp.route('/', methods=['GET'])
@jwt_required()
def get_fees():
    return jsonify(query_db('''
        SELECT f.*, s.full_name, s.student_id, b.batch_name FROM fees f
        JOIN students s ON f.student_id=s.id JOIN batches b ON f.batch_id=b.id
        ORDER BY f.created_at DESC
    '''))

@fee_bp.route('/', methods=['POST'])
@jwt_required()
def create_fee():
    d = request.get_json()
    nid = query_db(
        'INSERT INTO fees (student_id,batch_id,amount,due_date,receipt_number) VALUES(%s,%s,%s,%s,%s)',
        (d['student_id'],d['batch_id'],d['amount'],d.get('due_date'),gen_receipt()),
        commit=True
    )
    return jsonify({'message': 'Fee record created', 'id': nid}), 201

@fee_bp.route('/<int:fid>/pay', methods=['POST'])
@jwt_required()
def record_payment(fid):
    d = request.get_json()
    fee = query_db('SELECT * FROM fees WHERE id=%s', (fid,), one=True)
    new_paid = (fee['paid_amount'] or 0) + d['amount']
    status = 'Paid' if new_paid >= fee['amount'] else 'Partial'
    query_db('UPDATE fees SET paid_amount=%s, paid_date=%s, payment_mode=%s, status=%s WHERE id=%s',
             (new_paid, str(datetime.date.today()), d.get('payment_mode','Cash'), status, fid), commit=True)
    return jsonify({'message': 'Payment recorded', 'status': status, 'receipt': fee['receipt_number']})

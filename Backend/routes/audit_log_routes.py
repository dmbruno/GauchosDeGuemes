"""
CRUD endpoints for AuditLog entity.
"""
from flask import Blueprint, request, jsonify
from models.audit_log import AuditLog, AuditLogSchema
from extensions import db

audit_log_bp = Blueprint('audit_log_bp', __name__)
audit_log_schema = AuditLogSchema()
audit_logs_schema = AuditLogSchema(many=True)

@audit_log_bp.route('/audit-logs', methods=['POST'])
def create_audit_log():
    data = request.get_json()
    details = data.pop('details', None)  # Extract details if present
    audit_log = audit_log_schema.load(data, session=db.session)
    if details:  # If details were provided, update the log instance
        audit_log.details = details
    db.session.add(audit_log)
    db.session.commit()
    return jsonify(audit_log_schema.dump(audit_log)), 201

@audit_log_bp.route('/audit-logs', methods=['GET'])
def list_audit_logs():
    logs = db.session.query(AuditLog).all()
    return jsonify(audit_logs_schema.dump(logs))

@audit_log_bp.route('/audit-logs/<int:log_id>', methods=['GET'])
def get_audit_log(log_id):
    log = db.session.get(AuditLog, log_id)
    if not log:
        return jsonify({'error': 'AuditLog not found'}), 404
    return jsonify(audit_log_schema.dump(log))

@audit_log_bp.route('/audit-logs/<int:log_id>', methods=['PUT'])
def update_audit_log(log_id):
    log = db.session.get(AuditLog, log_id)
    if not log:
        return jsonify({'error': 'AuditLog not found'}), 404
    data = request.get_json()
    log = audit_log_schema.load(data, instance=log, session=db.session, partial=True)
    db.session.commit()
    return jsonify(audit_log_schema.dump(log))

@audit_log_bp.route('/audit-logs/<int:log_id>', methods=['DELETE'])
def delete_audit_log(log_id):
    log = db.session.get(AuditLog, log_id)
    if not log:
        return jsonify({'error': 'AuditLog not found'}), 404
    db.session.delete(log)
    db.session.commit()
    return '', 204

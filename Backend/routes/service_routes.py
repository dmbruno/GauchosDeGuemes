"""
CRUD endpoints for Service entity.
"""
from flask import Blueprint, request, jsonify
from models.service import Service, ServiceSchema
from extensions import db

service_bp = Blueprint('service_bp', __name__)
service_schema = ServiceSchema()
services_schema = ServiceSchema(many=True)

@service_bp.route('/services', methods=['POST'])
def create_service():
    data = request.get_json()
    service = service_schema.load(data, session=db.session)
    db.session.add(service)
    db.session.commit()
    return jsonify(service_schema.dump(service)), 201

@service_bp.route('/services', methods=['GET'])
def list_services():
    services = db.session.query(Service).all()
    return jsonify(services_schema.dump(services))

@service_bp.route('/services/<int:service_id>', methods=['GET'])
def get_service(service_id):
    service = db.session.get(Service, service_id)
    if not service:
        return jsonify({'error': 'Service not found'}), 404
    return jsonify(service_schema.dump(service))

@service_bp.route('/services/<int:service_id>', methods=['PUT'])
def update_service(service_id):
    service = db.session.get(Service, service_id)
    if not service:
        return jsonify({'error': 'Service not found'}), 404
    data = request.get_json()
    service = service_schema.load(data, instance=service, session=db.session, partial=True)
    db.session.commit()
    return jsonify(service_schema.dump(service))

@service_bp.route('/services/<int:service_id>', methods=['DELETE'])
def delete_service(service_id):
    service = db.session.get(Service, service_id)
    if not service:
        return jsonify({'error': 'Service not found'}), 404
    db.session.delete(service)
    db.session.commit()
    return '', 204

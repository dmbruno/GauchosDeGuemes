"""
CRUD endpoints for Client entity.
"""
from flask import Blueprint, request, jsonify
from models.client import Client, ClientSchema
from extensions import db

client_bp = Blueprint('client_bp', __name__)
client_schema = ClientSchema()
clients_schema = ClientSchema(many=True)

@client_bp.route('/clients', methods=['POST'])
def create_client():
    data = request.get_json()
    
    # Verificar si ya existe un cliente con ese DNI
    existing_client = db.session.query(Client).filter_by(dni=data.get('dni')).first()
    if existing_client:
        return jsonify({'error': 'Cliente con este DNI ya existe'}), 400
    
    # Validación para términos y condiciones (si viene del frontend)
    if 'accepted_terms' in data and not data.get('accepted_terms', False):
        return jsonify({
            'error': 'Debe aceptar los términos y condiciones para continuar'
        }), 400
    
    # Si no viene accepted_terms (desde la app), poner False por defecto
    if 'accepted_terms' not in data:
        data['accepted_terms'] = False
    
    client = client_schema.load(data, session=db.session)
    db.session.add(client)
    db.session.commit()
    return jsonify(client_schema.dump(client)), 201

@client_bp.route('/clients', methods=['GET'])
def list_clients():
    clients = db.session.query(Client).all()
    return jsonify(clients_schema.dump(clients))

@client_bp.route('/clients/<int:client_id>', methods=['GET'])
def get_client(client_id):
    client = db.session.get(Client, client_id)
    if not client:
        return jsonify({'error': 'Client not found'}), 404
    return jsonify(client_schema.dump(client))

@client_bp.route('/clients/<int:client_id>', methods=['PUT'])
def update_client(client_id):
    client = db.session.get(Client, client_id)
    if not client:
        return jsonify({'error': 'Client not found'}), 404
    
    data = request.get_json()
    
    # Si se actualiza el DNI, verificar que no exista en otro cliente
    if 'dni' in data and data['dni'] != client.dni:
        existing_client = db.session.query(Client).filter_by(dni=data['dni']).first()
        if existing_client:
            return jsonify({'error': 'Cliente con este DNI ya existe'}), 400
    
    client = client_schema.load(data, instance=client, session=db.session, partial=True)
    db.session.commit()
    return jsonify(client_schema.dump(client))

@client_bp.route('/clients/<int:client_id>', methods=['DELETE'])
def delete_client(client_id):
    client = db.session.get(Client, client_id)
    if not client:
        return jsonify({'error': 'Client not found'}), 404
    db.session.delete(client)
    db.session.commit()
    return '', 204

@client_bp.route('/clients', methods=['OPTIONS'])
def handle_options():
    return '', 200

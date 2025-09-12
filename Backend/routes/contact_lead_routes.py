"""
CRUD endpoints for ContactLead entity.
"""
from flask import Blueprint, request, jsonify
from models.contact_lead import ContactLead, ContactLeadSchema
from extensions import db

contact_lead_bp = Blueprint('contact_lead_bp', __name__)
contact_lead_schema = ContactLeadSchema()
contact_leads_schema = ContactLeadSchema(many=True)

@contact_lead_bp.route('/contact-leads', methods=['POST'])
def create_contact_lead():
    data = request.get_json()
    # Si se usa 'metadata', cambiar a 'lead_metadata'
    if 'metadata' in data:
        data['lead_metadata'] = data.pop('metadata')
    contact_lead = contact_lead_schema.load(data, session=db.session)
    db.session.add(contact_lead)
    db.session.commit()
    return jsonify(contact_lead_schema.dump(contact_lead)), 201

@contact_lead_bp.route('/contact-leads', methods=['GET'])
def list_contact_leads():
    leads = db.session.query(ContactLead).all()
    return jsonify(contact_leads_schema.dump(leads))

@contact_lead_bp.route('/contact-leads/<int:lead_id>', methods=['GET'])
def get_contact_lead(lead_id):
    lead = db.session.get(ContactLead, lead_id)
    if not lead:
        return jsonify({'error': 'ContactLead not found'}), 404
    return jsonify(contact_lead_schema.dump(lead))

@contact_lead_bp.route('/contact-leads/<int:lead_id>', methods=['PUT'])
def update_contact_lead(lead_id):
    lead = db.session.get(ContactLead, lead_id)
    if not lead:
        return jsonify({'error': 'ContactLead not found'}), 404
    data = request.get_json()
    lead = contact_lead_schema.load(data, instance=lead, session=db.session, partial=True)
    db.session.commit()
    return jsonify(contact_lead_schema.dump(lead))

@contact_lead_bp.route('/contact-leads/<int:lead_id>', methods=['DELETE'])
def delete_contact_lead(lead_id):
    lead = db.session.get(ContactLead, lead_id)
    if not lead:
        return jsonify({'error': 'ContactLead not found'}), 404
    db.session.delete(lead)
    db.session.commit()
    return '', 204

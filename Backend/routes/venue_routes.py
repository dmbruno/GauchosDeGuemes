"""
CRUD endpoints for Venue entity.
"""
from flask import Blueprint, request, jsonify
from models.venue import Venue, VenueSchema
from extensions import db

venue_bp = Blueprint('venue_bp', __name__)
venue_schema = VenueSchema()
venues_schema = VenueSchema(many=True)

@venue_bp.route('/venues', methods=['POST'])
def create_venue():
    data = request.get_json()
    venue = venue_schema.load(data, session=db.session)
    db.session.add(venue)
    db.session.commit()
    return jsonify(venue_schema.dump(venue)), 201

@venue_bp.route('/venues', methods=['GET'])
def list_venues():
    venues = db.session.query(Venue).all()
    return jsonify(venues_schema.dump(venues))

@venue_bp.route('/venues/<int:venue_id>', methods=['GET'])
def get_venue(venue_id):
    venue = db.session.get(Venue, venue_id)
    if not venue:
        return jsonify({'error': 'Venue not found'}), 404
    return jsonify(venue_schema.dump(venue))

@venue_bp.route('/venues/<int:venue_id>', methods=['PUT'])
def update_venue(venue_id):
    venue = db.session.get(Venue, venue_id)
    if not venue:
        return jsonify({'error': 'Venue not found'}), 404
    data = request.get_json()
    venue = venue_schema.load(data, instance=venue, session=db.session, partial=True)
    db.session.commit()
    return jsonify(venue_schema.dump(venue))

@venue_bp.route('/venues/<int:venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    venue = db.session.get(Venue, venue_id)
    if not venue:
        return jsonify({'error': 'Venue not found'}), 404
    db.session.delete(venue)
    db.session.commit()
    return '', 204

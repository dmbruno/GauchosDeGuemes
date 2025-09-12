"""
CRUD endpoints for Booking entity.
"""
from flask import Blueprint, request, jsonify
from models.booking import Booking, BookingSchema
from extensions import db

booking_bp = Blueprint('booking_bp', __name__)
booking_schema = BookingSchema()
bookings_schema = BookingSchema(many=True)

@booking_bp.route('/bookings', methods=['POST'])
def create_booking():
    data = request.get_json()
    booking = booking_schema.load(data, session=db.session)
    db.session.add(booking)
    db.session.commit()
    return jsonify(booking_schema.dump(booking)), 201

@booking_bp.route('/bookings', methods=['GET'])
def list_bookings():
    bookings = db.session.query(Booking).all()
    return jsonify(bookings_schema.dump(bookings))

@booking_bp.route('/bookings/<int:booking_id>', methods=['GET'])
def get_booking(booking_id):
    booking = db.session.get(Booking, booking_id)
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    return jsonify(booking_schema.dump(booking))

@booking_bp.route('/bookings/<int:booking_id>', methods=['PUT'])
def update_booking(booking_id):
    booking = db.session.get(Booking, booking_id)
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    data = request.get_json()
    booking = booking_schema.load(data, instance=booking, session=db.session, partial=True)
    db.session.commit()
    return jsonify(booking_schema.dump(booking))

@booking_bp.route('/bookings/<int:booking_id>', methods=['DELETE'])
def delete_booking(booking_id):
    booking = db.session.get(Booking, booking_id)
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    db.session.delete(booking)
    db.session.commit()
    return '', 204

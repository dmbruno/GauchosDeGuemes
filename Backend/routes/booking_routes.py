"""
CRUD endpoints for Booking entity.
"""
from flask import Blueprint, request, jsonify
from models.booking import Booking, BookingSchema, booking_services
from extensions import db

booking_bp = Blueprint('booking_bp', __name__)
booking_schema = BookingSchema()
bookings_schema = BookingSchema(many=True)

@booking_bp.route('/bookings', methods=['POST'])
def create_booking():
    data = request.get_json()
    
    # Extraer service_ids del JSON
    service_ids = data.pop('service_ids', [])
    
    # Crear booking
    booking = booking_schema.load(data, session=db.session)
    db.session.add(booking)
    db.session.flush()  # Para obtener el ID del booking
    
    # Agregar servicios a la tabla intermedia
    for service_id in service_ids:
        db.session.execute(booking_services.insert().values(
            booking_id=booking.id,
            service_id=service_id
        ))
    
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
    
    # Extraer service_ids del JSON
    service_ids = data.pop('service_ids', [])
    
    # Actualizar datos del booking
    booking = booking_schema.load(data, instance=booking, session=db.session, partial=True)
    
    # Actualizar servicios: eliminar los anteriores y agregar los nuevos
    # Eliminar todas las relaciones anteriores
    db.session.execute(
        booking_services.delete().where(booking_services.c.booking_id == booking_id)
    )
    
    # Agregar los nuevos servicios
    for service_id in service_ids:
        db.session.execute(booking_services.insert().values(
            booking_id=booking_id,
            service_id=service_id
        ))
    
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

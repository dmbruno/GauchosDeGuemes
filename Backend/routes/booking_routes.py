"""
CRUD endpoints for Booking entity.
"""
from flask import Blueprint, request, jsonify
from models.booking import Booking, BookingSchema, booking_services, BOOKING_STATUSES
from extensions import db
from datetime import date


booking_bp = Blueprint('booking_bp', __name__)
booking_schema = BookingSchema()
bookings_schema = BookingSchema(many=True)

@booking_bp.route('/bookings/statuses', methods=['GET'])
def get_booking_statuses():
    """Retorna la lista de estados permitidos para las reservas"""
    return jsonify({'statuses': BOOKING_STATUSES})

@booking_bp.route('/bookings', methods=['POST'])
def create_booking():
    data = request.get_json()
    
    # Validar el status si está presente (por defecto será "solicitada")
    status = data.get('status', 'solicitada')
    if status not in BOOKING_STATUSES:
        return jsonify({
            'error': f'Invalid status. Allowed values: {", ".join(BOOKING_STATUSES)}'
        }), 400
    data['status'] = status
    
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
    
    # Validar el status si está presente
    if 'status' in data and data['status'] not in BOOKING_STATUSES:
        return jsonify({
            'error': f'Invalid status. Allowed values: {", ".join(BOOKING_STATUSES)}'
        }), 400
    
    # Extraer service_ids del JSON si están presentes
    service_ids = data.pop('service_ids', None)
    
    # Actualizar campos del booking
    for key, value in data.items():
        if hasattr(booking, key):
            setattr(booking, key, value)
    
    # Si se enviaron service_ids, actualizar los servicios
    if service_ids is not None:
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
    
    # Refrescar el objeto para obtener todos los datos actualizados
    db.session.refresh(booking)
    
    return jsonify(booking_schema.dump(booking))

@booking_bp.route('/bookings/<int:booking_id>', methods=['DELETE'])
def delete_booking(booking_id):
    booking = db.session.get(Booking, booking_id)
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    db.session.delete(booking)
    db.session.commit()
    return '', 204



@booking_bp.route('/bookings/reserved-dates', methods=['GET'])
def get_reserved_dates():
    """
    Retorna una lista simple de fechas (YYYY-MM-DD) 
    que ya están confirmadas, a partir de hoy.
    """
    
    # ¡Importante! Filtramos solo las 'confirmadas'.
    # No querrás bloquear una fecha si alguien solo "solicitó" pero no pagó.
    query = (
        db.session.query(Booking.date)
        .filter(
            Booking.status == 'confirmada',
            Booking.date >= date.today()
        )
        .distinct() # Para que la fecha aparezca solo una vez
    )
    
    # La consulta devuelve objetos de fecha/hora.
    # Los convertimos a strings "YYYY-MM-DD" que tu frontend espera.
    fechas = [
        d[0].strftime('%Y-%m-%d') for d in query.all()
    ]
    
    return jsonify(fechas)
"""
BookingService model definition - Tabla intermedia para la relación Booking-Service.
"""
from extensions import db

class BookingService(db.Model):
    __tablename__ = "booking_services"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)

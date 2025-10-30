"""
Booking model definition.
"""
from extensions import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from datetime import datetime

class Booking(db.Model):
    __tablename__ = "bookings"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=True)  # Opcional según tu lógica
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    guests_count = db.Column(db.Integer, nullable=False)  # ← NUEVO CAMPO
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Opcional pero recomendado

class BookingSchema(SQLAlchemyAutoSchema):
    client_id = auto_field()
    service_id = auto_field()
    venue_id = auto_field()
    guests_count = auto_field()  # ← AGREGAR AQUÍ TAMBIÉN
    class Meta:
        model = Booking
        load_instance = True

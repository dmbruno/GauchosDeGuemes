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
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    guests_count = db.Column(db.Integer, nullable=False)
    contact_preference = db.Column(db.String(50), nullable=True)
    event_type = db.Column(db.String(100), nullable=True)
    other_services = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Tabla de asociación para la relación muchos a muchos
booking_services = db.Table('booking_services',
    db.Column('id', db.Integer, primary_key=True, autoincrement=True),
    db.Column('booking_id', db.Integer, db.ForeignKey('bookings.id'), nullable=False),
    db.Column('service_id', db.Integer, db.ForeignKey('services.id'), nullable=False)
)

# Agregar la relación después de definir la tabla
Booking.services = db.relationship('Service', secondary=booking_services, backref='bookings')

class BookingSchema(SQLAlchemyAutoSchema):
    client_id = auto_field()
    venue_id = auto_field()
    guests_count = auto_field()
    contact_preference = auto_field()
    event_type = auto_field()
    other_services = auto_field()
    
    class Meta:
        model = Booking
        load_instance = True
        include_relationships = True

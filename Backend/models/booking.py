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
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), nullable=False)

class BookingSchema(SQLAlchemyAutoSchema):
    client_id = auto_field()
    service_id = auto_field()
    venue_id = auto_field()
    class Meta:
        model = Booking
        load_instance = True

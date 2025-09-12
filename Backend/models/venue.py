"""
Venue model definition.
"""
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from extensions import db

class Venue(db.Model):
    __tablename__ = "venues"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime)

class VenueSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Venue
        load_instance = True

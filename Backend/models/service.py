"""
Service model definition.
"""
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from extensions import db

class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    details = db.Column(db.String(255))
    created_at = db.Column(db.DateTime)

class ServiceSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Service
        load_instance = True

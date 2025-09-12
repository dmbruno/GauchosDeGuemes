"""
ContactLead model definition.
"""
from sqlalchemy import Column, Integer, String, DateTime
import uuid
from models.base import Base
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from extensions import db

class ContactLead(db.Model):
    __tablename__ = "contact_leads"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.String(255))
    lead_metadata = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ContactLeadSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ContactLead
        load_instance = True

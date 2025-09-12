"""
GalleryImage model definition.
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from models.base import Base
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
import uuid
from extensions import db

class GalleryImage(db.Model):
    __tablename__ = "gallery_images"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'))
    url = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime)

class GalleryImageSchema(SQLAlchemyAutoSchema):
    venue_id = auto_field()
    class Meta:
        model = GalleryImage
        load_instance = True

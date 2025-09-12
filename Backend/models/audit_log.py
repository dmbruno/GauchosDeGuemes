"""
AuditLog model definition.

Este modelo registra acciones importantes realizadas en el sistema, por ejemplo:
- Creación, actualización o eliminación de usuarios, bookings, etc.
- Guarda el tipo de acción, el usuario que la realizó (user_id), detalles adicionales y la fecha/hora.
"""
from extensions import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from datetime import datetime

class AuditLog(db.Model):
    __tablename__ = "audit_logs"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    action = db.Column(db.String(120), nullable=False)  # Ej: 'create_user', 'delete_booking'
    user_id = db.Column(db.Integer)  # Usuario que realizó la acción
    details = db.Column(db.String(255))  # Información adicional (puede incluir entity, entity_id, etc)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class AuditLogSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = AuditLog
        load_instance = True

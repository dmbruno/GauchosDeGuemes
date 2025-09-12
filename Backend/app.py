"""
Main Flask application initialization.
"""
from flask import Flask
from extensions import db, ma
import os

# Importar todos los modelos para registrar las tablas
from models.user import User
from models.client import Client
from models.service import Service
from models.venue import Venue
from models.booking import Booking
from models.gallery_image import GalleryImage
from models.contact_lead import ContactLead
from models.audit_log import AuditLog

# Flask app initialization
app = Flask(__name__)

# SQLite database configuration usando ruta absoluta
instance_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')
db_path = os.path.join(instance_dir, 'gauchos.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
ma.init_app(app)

# Import and register blueprints
from routes.user_routes import user_bp
from routes.client_routes import client_bp
from routes.service_routes import service_bp
from routes.venue_routes import venue_bp
from routes.booking_routes import booking_bp
from routes.gallery_image_routes import gallery_image_bp
from routes.contact_lead_routes import contact_lead_bp
from routes.audit_log_routes import audit_log_bp

app.register_blueprint(user_bp)
app.register_blueprint(client_bp)
app.register_blueprint(service_bp)
app.register_blueprint(venue_bp)
app.register_blueprint(booking_bp)
app.register_blueprint(gallery_image_bp)
app.register_blueprint(contact_lead_bp)
app.register_blueprint(audit_log_bp)

# Crear tablas siempre que se inicialice la app
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)

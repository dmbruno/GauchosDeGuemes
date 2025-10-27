"""
Main Flask application initialization.
"""
from flask import Flask
from flask_cors import CORS
from extensions import db, ma
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde .env
load_dotenv()

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

CORS(app, 
     origins=["http://localhost:5173", "http://127.0.0.1:5173"], 
     supports_credentials=True)



# Configuración desde .env
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS') == 'True'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

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

# Crear carpeta instance si no existe
os.makedirs(os.path.join(app.root_path, 'instance'), exist_ok=True)

# Crear tablas siempre que se inicialice la app
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=5050)



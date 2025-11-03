"""
Main Flask application initialization.
"""
from flask import Flask, jsonify
from flask_cors import CORS
from extensions import db, ma, mail
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde .env
load_dotenv()

# Flask app initialization
app = Flask(__name__)

# Configurar CORS
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:5173", "http://localhost:5050", "http://127.0.0.1:5173"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})

# Configuración desde .env
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS') == 'True'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Configuración de email
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

db.init_app(app)
ma.init_app(app)
mail.init_app(app)

# Import and register blueprints
from routes.user_routes import user_bp
from routes.client_routes import client_bp
from routes.service_routes import service_bp
from routes.venue_routes import venue_bp
from routes.booking_routes import booking_bp
from routes.gallery_image_routes import gallery_image_bp
from routes.contact_lead_routes import contact_lead_bp
from routes.audit_log_routes import audit_log_bp
from routes.auth import auth_bp

app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(client_bp, url_prefix='/api')
app.register_blueprint(service_bp, url_prefix='/api')
app.register_blueprint(venue_bp, url_prefix='/api')
app.register_blueprint(booking_bp, url_prefix='/api')
app.register_blueprint(gallery_image_bp, url_prefix='/api')
app.register_blueprint(contact_lead_bp, url_prefix='/api')
app.register_blueprint(audit_log_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/api')

# Error handlers
@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Error interno del servidor'}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Recurso no encontrado'}), 404

# Importar todos los modelos para registrar las tablas
from models.user import User
from models.client import Client
from models.service import Service
from models.venue import Venue
from models.booking import Booking
from models.gallery_image import GalleryImage
from models.contact_lead import ContactLead
from models.audit_log import AuditLog

# Crear carpeta instance si no existe
os.makedirs(os.path.join(app.root_path, 'instance'), exist_ok=True)

# Crear tablas siempre que se inicialice la app
with app.app_context():
    db.create_all()

# Root endpoint
@app.route('/')
def index():
    return jsonify({
        'message': 'Gauchos De Güemes API',
        'version': '1.0',
        'endpoints': {
            'auth': '/api/auth/*',
            'users': '/api/users',
            'clients': '/api/clients',
            'services': '/api/services',
            'venues': '/api/venues',
            'bookings': '/api/bookings',
            'gallery': '/api/gallery-images',
            'leads': '/api/contact-leads',
            'audit': '/api/audit-logs'
        }
    })

if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=5050)



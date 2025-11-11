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
        "origins": [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost:5050",
            "http://127.0.0.1:5050",
            "https://gestionreservas-gauchosguemes.onrender.com",
            "https://ggeyc.netlify.app",
            "https://gauchosdeguemes.com.ar",  
            "https://www.gauchosdeguemes.com.ar"
            
        ],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True,
        "expose_headers": ["Content-Type", "Authorization"]
    }
})

# Configuración de base de datos (compatible con SQLite y PostgreSQL)
database_url = os.getenv('DATABASE_URL') or os.getenv('SQLALCHEMY_DATABASE_URI')

# Fix para Render: reemplazar postgres:// con postgresql://
if database_url and database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', 'False') == 'True'
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

# Crear tablas siempre que se inicialice la app
with app.app_context():
    db.create_all()
    
    # Migración segura para producción (solo si la variable está configurada)
    if os.getenv('RECREATE_TABLES', 'false').lower() == 'true':
        try:
            print("🔄 Starting table migration...")
            
            # Para PostgreSQL, verificar si la columna exists
            if database_url and 'postgresql://' in database_url:
                result = db.engine.execute("SELECT column_name FROM information_schema.columns WHERE table_name='clients' AND column_name='accepted_terms'")
                exists = result.fetchone()
                
                if not exists:
                    print("📝 Adding accepted_terms column...")
                    db.engine.execute("ALTER TABLE clients ADD COLUMN accepted_terms BOOLEAN NOT NULL DEFAULT FALSE")
                    print("✅ Column added successfully!")
                else:
                    print("✅ Column already exists")
            else:
                # Para SQLite, recrear todas las tablas es más fácil
                print("🔄 Recreating all tables for SQLite...")
                db.drop_all()
                db.create_all()
                print("✅ Tables recreated!")
                
        except Exception as e:
            print(f"⚠️ Migration error: {e}")
            # Si falla, recrear todas las tablas
            print("🔄 Recreating all tables as fallback...")
            db.drop_all()
            db.create_all()
            print("✅ Tables recreated!")

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



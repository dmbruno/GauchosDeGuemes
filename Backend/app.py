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

# Endpoint de test simple para verificar conexión a BD
@app.route('/api/test-db', methods=['GET'])
def test_db():
    """Endpoint simple para probar la conexión a la base de datos"""
    try:
        from models.user import User
        from models.venue import Venue
        
        # Probar conexión básica
        user_count = User.query.count()
        venue_count = Venue.query.count()
        
        return jsonify({
            "message": "Conexión a BD exitosa",
            "users_count": user_count,
            "venues_count": venue_count,
            "database_connected": True
        }), 200
        
    except Exception as e:
        return jsonify({
            "error": f"Error de BD: {str(e)}",
            "type": type(e).__name__,
            "database_connected": False
        }), 500

# Endpoint para inicializar datos semilla en producción
@app.route('/api/admin/init-database', methods=['POST'])
def init_database():
    """Endpoint para inicializar la base de datos con datos semilla"""
    from datetime import datetime
    
    print("🔥 DEBUG: Iniciando endpoint init_database")
    
    try:
        print("🔥 DEBUG: Buscando usuario admin existente")
        # Verificar si ya existe el usuario admin
        existing_admin = User.query.filter_by(email="admin@gauchosguemes.com").first()
        admin_created = False
        
        if not existing_admin:
            print("🔥 DEBUG: Creando usuario admin")
            # Crear usuario administrador
            admin = User(
                username="admin",
                email="admin@gauchosguemes.com",
                is_admin=True,
                created_at=datetime.utcnow()
            )
            admin.set_password("Admin123!")
            db.session.add(admin)
            admin_created = True
            print("🔥 DEBUG: Usuario admin agregado a sesión")
        else:
            print(f"🔥 DEBUG: Usuario admin ya existe: {existing_admin.email}")
        
        print("🔥 DEBUG: Buscando venue existente")
        # Verificar si ya existe el venue
        existing_venue = Venue.query.filter_by(name="Salon Gauchos de Guemes").first()
        venue_created = False
        
        if not existing_venue:
            print("🔥 DEBUG: Creando venue")
            # Crear venue inicial
            venue = Venue(
                name="Salon Gauchos de Guemes",
                address="Circunvalacion Oeste Salta Capital",
                created_at=datetime.utcnow()
            )
            db.session.add(venue)
            venue_created = True
            print("🔥 DEBUG: Venue agregado a sesión")
        else:
            print(f"🔥 DEBUG: Venue ya existe: {existing_venue.name}")
        
        print("🔥 DEBUG: Haciendo commit a la base de datos")
        db.session.commit()
        print("🔥 DEBUG: Commit exitoso")
        
        response_data = {
            "message": "Base de datos inicializada correctamente",
            "admin_created": admin_created,
            "venue_created": venue_created,
            "admin_email": "admin@gauchosguemes.com",
            "admin_password": "Admin123!",
            "venue_name": "Salon Gauchos de Guemes"
        }
        
        print(f"🔥 DEBUG: Respuesta preparada: {response_data}")
        return jsonify(response_data), 200
        
    except Exception as e:
        print(f"🔥 DEBUG: ERROR: {str(e)}")
        db.session.rollback()
        return jsonify({"error": str(e), "debug": "Error en init_database"}), 500

if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=5050)



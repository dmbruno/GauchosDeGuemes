"""
Script para poblar la base de datos con datos ficticios en todas las tablas principales.
Ejecuta este script después de crear las tablas para poder probar las rutas con Postman.
"""
from app import app, db
from models.user import User
from models.client import Client
from models.service import Service
from models.venue import Venue
from models.booking import Booking
from models.gallery_image import GalleryImage
from models.contact_lead import ContactLead
from models.audit_log import AuditLog
from datetime import datetime

with app.app_context():
    # Usuarios
    user1 = User(username="admin", email="admin@example.com", is_admin=True, created_at=datetime.utcnow())
    user2 = User(username="juan", email="juan@example.com", is_admin=False, created_at=datetime.utcnow())
    db.session.add_all([user1, user2])

    # Clientes
    client1 = Client(name="Cliente Uno", email="cliente1@example.com", created_at=datetime.utcnow())
    client2 = Client(name="Cliente Dos", email="cliente2@example.com", created_at=datetime.utcnow())
    db.session.add_all([client1, client2])

    # Servicios
    service1 = Service(name="Catering", type="Comida", details="Buffet libre", created_at=datetime.utcnow())
    service2 = Service(name="Fotografía", type="Foto", details="Cobertura profesional", created_at=datetime.utcnow())
    db.session.add_all([service1, service2])

    # Venues
    venue1 = Venue(name="Salon Fiesta", address="Av. Principal 123", created_at=datetime.utcnow())
    venue2 = Venue(name="Quinta Verde", address="Ruta 9 km 20", created_at=datetime.utcnow())
    db.session.add_all([venue1, venue2])

    # Bookings
    booking1 = Booking(client_id=client1.id, service_id=service1.id, venue_id=venue1.id, date=datetime(2025, 10, 1), status="confirmado", created_at=datetime.utcnow())
    booking2 = Booking(client_id=client2.id, service_id=service2.id, venue_id=venue2.id, date=datetime(2025, 11, 15), status="pendiente", created_at=datetime.utcnow())
    db.session.add_all([booking1, booking2])

    # Imágenes de galería
    img1 = GalleryImage(venue_id=venue1.id, url="https://picsum.photos/200", description="Foto del salón", created_at=datetime.utcnow())
    img2 = GalleryImage(venue_id=venue2.id, url="https://picsum.photos/201", description="Foto de la quinta", created_at=datetime.utcnow())
    db.session.add_all([img1, img2])

    # Leads de contacto
    lead1 = ContactLead(name="Pedro", email="pedro@mail.com", message="Quiero cotizar un evento", lead_metadata="web", created_at=datetime.utcnow())
    lead2 = ContactLead(name="Ana", email="ana@mail.com", message="Consulta por disponibilidad", lead_metadata="web", created_at=datetime.utcnow())
    db.session.add_all([lead1, lead2])

    # Logs de auditoría
    log1 = AuditLog(action="create_user", user_id=1, details="Usuario admin creado", timestamp=datetime.utcnow())
    log2 = AuditLog(action="create_booking", user_id=2, details="Reserva creada por Juan", timestamp=datetime.utcnow())
    db.session.add_all([log1, log2])

    db.session.commit()
    print("Datos ficticios insertados correctamente en todas las tablas.")

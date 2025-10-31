"""
Script para poblar la base de datos con datos ficticios en todas las tablas principales.
Ejecuta este script después de crear las tablas para poder probar las rutas con Postman.
"""
from app import app, db
from models.user import User
from models.client import Client
from models.service import Service
from models.venue import Venue
from models.booking import Booking, booking_services
from models.gallery_image import GalleryImage
from models.contact_lead import ContactLead
from models.audit_log import AuditLog
from datetime import datetime

with app.app_context():
    # Limpiar todas las tablas antes de insertar datos
    db.drop_all()
    db.create_all()
    
    # Usuarios
    user1 = User(username="admin", email="admin@example.com", is_admin=True, created_at=datetime.utcnow())
    user2 = User(username="juan", email="juan@example.com", is_admin=False, created_at=datetime.utcnow())
    db.session.add_all([user1, user2])

    # Clientes
    client1 = Client(
        dni="12345678",
        first_name="María",
        last_name="González",
        phone="+5493875051111",
        email="maria.gonzalez@example.com",
        created_at=datetime.utcnow()
    )
    client2 = Client(
        dni="87654321",
        first_name="Juan",
        last_name="Pérez",
        phone="+5493875051112",
        email="juan.perez@example.com",
        created_at=datetime.utcnow()
    )
    client3 = Client(
        dni="11223344",
        first_name="Ana",
        last_name="Rodríguez",
        phone="+5493875051113",
        email="ana.rodriguez@example.com",
        created_at=datetime.utcnow()
    )
    client4 = Client(
        dni="44332211",
        first_name="Carlos",
        last_name="López",
        phone="+5493875051114",
        email="carlos.lopez@example.com",
        created_at=datetime.utcnow()
    )
    db.session.add_all([client1, client2, client3, client4])

    # Servicios
    service1 = Service(name="Catering Premium", type="Comida", details="Buffet libre con carnes, ensaladas y postres", created_at=datetime.utcnow())
    service2 = Service(name="Fotografía Profesional", type="Foto", details="Cobertura completa del evento con álbum digital", created_at=datetime.utcnow())
    service3 = Service(name="Música y DJ", type="Entretenimiento", details="Equipo de sonido profesional con DJ", created_at=datetime.utcnow())
    service4 = Service(name="Decoración Floral", type="Decoración", details="Arreglos florales y centros de mesa", created_at=datetime.utcnow())
    service5 = Service(name="Video Institucional", type="Video", details="Grabación y edición de video del evento", created_at=datetime.utcnow())
    db.session.add_all([service1, service2, service3, service4, service5])

    # Venues
    venue1 = Venue(name="Gauchos De Güemes", address="Circunvalación Oeste S/N Salta - Argentina", created_at=datetime.utcnow())
    db.session.add(venue1)

    db.session.commit()  # Commit para asegurar que los IDs estén disponibles

    # Bookings (sin service_id)
    booking1 = Booking(
        client_id=client1.id,
        venue_id=venue1.id,
        date=datetime(2025, 12, 15),
        status="confirmado",
        guests_count=150,
        contact_preference="WhatsApp",
        event_type="Boda",
        other_services="Decoración adicional"
    )
    booking2 = Booking(
        client_id=client2.id,
        venue_id=venue1.id,
        date=datetime(2025, 11, 30),
        status="pendiente",
        guests_count=100,
        contact_preference="Email",
        event_type="Cumpleaños 50 años",
        other_services="Torta personalizada"
    )
    booking3 = Booking(
        client_id=client3.id,
        venue_id=venue1.id,
        date=datetime(2025, 12, 20),
        status="confirmado",
        guests_count=200,
        contact_preference="Llamada telefónica",
        event_type="Evento corporativo",
        other_services="Servicio de bar premium"
    )
    booking4 = Booking(
        client_id=client4.id,
        venue_id=venue1.id,
        date=datetime(2026, 1, 10),
        status="cotización",
        guests_count=80,
        contact_preference="No especificado",
        event_type="15 años",
        other_services="Ninguno"
    )
    db.session.add_all([booking1, booking2, booking3, booking4])
    db.session.commit()
    
    # Asignar múltiples servicios a cada booking mediante tabla intermedia
    db.session.execute(booking_services.insert().values(booking_id=booking1.id, service_id=service1.id))  # Catering
    db.session.execute(booking_services.insert().values(booking_id=booking1.id, service_id=service2.id))  # Fotografía
    db.session.execute(booking_services.insert().values(booking_id=booking1.id, service_id=service3.id))  # Música y DJ
    
    db.session.execute(booking_services.insert().values(booking_id=booking2.id, service_id=service1.id))  # Catering
    db.session.execute(booking_services.insert().values(booking_id=booking2.id, service_id=service4.id))  # Decoración
    
    db.session.execute(booking_services.insert().values(booking_id=booking3.id, service_id=service1.id))  # Catering
    db.session.execute(booking_services.insert().values(booking_id=booking3.id, service_id=service2.id))  # Fotografía
    db.session.execute(booking_services.insert().values(booking_id=booking3.id, service_id=service5.id))  # Video
    
    db.session.execute(booking_services.insert().values(booking_id=booking4.id, service_id=service3.id))  # Música
    db.session.execute(booking_services.insert().values(booking_id=booking4.id, service_id=service4.id))  # Decoración
    
    db.session.commit()

    # Imágenes de galería
    img1 = GalleryImage(venue_id=venue1.id, url="https://picsum.photos/800/600?random=1", description="Gauchos De Güemes - Vista principal", created_at=datetime.utcnow())
    img2 = GalleryImage(venue_id=venue1.id, url="https://picsum.photos/800/600?random=2", description="Gauchos De Güemes - Pista de baile", created_at=datetime.utcnow())
    img3 = GalleryImage(venue_id=venue1.id, url="https://picsum.photos/800/600?random=3", description="Gauchos De Güemes - Jardín exterior", created_at=datetime.utcnow())
    img4 = GalleryImage(venue_id=venue1.id, url="https://picsum.photos/800/600?random=4", description="Gauchos De Güemes - Salón de eventos", created_at=datetime.utcnow())
    img5 = GalleryImage(venue_id=venue1.id, url="https://picsum.photos/800/600?random=5", description="Gauchos De Güemes - Quincho", created_at=datetime.utcnow())
    img6 = GalleryImage(venue_id=venue1.id, url="https://picsum.photos/800/600?random=6", description="Gauchos De Güemes - Vista panorámica", created_at=datetime.utcnow())
    db.session.add_all([img1, img2, img3, img4, img5, img6])

    # Leads de contacto
    lead1 = ContactLead(name="Pedro Martínez", email="pedro.martinez@gmail.com", message="Hola, necesito cotizar un evento para 150 personas el 20 de diciembre. ¿Tienen disponibilidad?", lead_metadata="whatsapp", created_at=datetime.utcnow())
    lead2 = ContactLead(name="Ana Fernández", email="ana.fernandez@hotmail.com", message="Consulta por disponibilidad para boda en marzo 2026", lead_metadata="web", created_at=datetime.utcnow())
    lead3 = ContactLead(name="Roberto Silva", email="rsilva@empresa.com", message="Evento corporativo fin de año, necesito presupuesto urgente", lead_metadata="instagram", created_at=datetime.utcnow())
    lead4 = ContactLead(name="Laura Gutiérrez", email="laura.gut@yahoo.com", message="15 años para mi hija, quiero ver opciones de quintas", lead_metadata="facebook", created_at=datetime.utcnow())
    db.session.add_all([lead1, lead2, lead3, lead4])

    # Logs de auditoría
    log1 = AuditLog(action="create_user", user_id=user1.id, details="Usuario admin creado en el sistema", timestamp=datetime.utcnow())
    log2 = AuditLog(action="create_booking", user_id=user2.id, details="Reserva creada por Juan para cliente María González", timestamp=datetime.utcnow())
    log3 = AuditLog(action="update_client", user_id=user1.id, details="Actualización de datos de contacto de cliente Juan Pérez", timestamp=datetime.utcnow())
    log4 = AuditLog(action="create_lead", user_id=user1.id, details="Nuevo lead desde WhatsApp: Pedro Martínez", timestamp=datetime.utcnow())
    log5 = AuditLog(action="confirm_booking", user_id=user2.id, details="Reserva confirmada para María González en Salon Dorado", timestamp=datetime.utcnow())
    db.session.add_all([log1, log2, log3, log4, log5])

    db.session.commit()
    print("Datos ficticios insertados correctamente en todas las tablas.")
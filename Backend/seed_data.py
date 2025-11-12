"""
Script simplificado para crear el usuario administrador y un venue inicial 
en la base de datos de producción.
Ejecuta este script para inicializar la DB de Render con datos básicos.
"""
from app import app, db
from models.user import User
from models.venue import Venue
from datetime import datetime

with app.app_context():
    print("🚀 Iniciando carga de datos semilla...")
    
    # Verificar si ya existe el usuario admin
    existing_admin = User.query.filter_by(email="admin@gauchosguemes.com").first()
    
    if existing_admin:
        print("⚠️  El usuario admin ya existe en la base de datos.")
        print(f"Email: {existing_admin.email}")
    else:
        # Crear solo el usuario administrador
        admin = User(
            username="admin",
            email="admin@gauchosguemes.com",
            is_admin=True,
            created_at=datetime.utcnow()
        )
        admin.set_password("Admin123!")
        
        db.session.add(admin)
        print("✅ Usuario administrador creado exitosamente!")
    
    # Verificar si ya existe el venue
    existing_venue = Venue.query.filter_by(name="Salon Gauchos de Guemes").first()
    
    if existing_venue:
        print("⚠️  El venue 'Salon Gauchos de Guemes' ya existe en la base de datos.")
        print(f"Nombre: {existing_venue.name}")
    else:
        # Crear el venue inicial
        venue = Venue(
            name="Salon Gauchos de Guemes",
            address="Circunvalacion Oeste - Salta Capital",
            created_at=datetime.utcnow()
        )
        
        db.session.add(venue)
        print("✅ Venue inicial creado exitosamente!")
    
    # Guardar todos los cambios
    db.session.commit()
    
    print("\n" + "="*60)
    print("DATOS DE ACCESO PARA PRODUCCIÓN:")
    print("="*60)
    print(f"Email:    admin@gauchosguemes.com")
    print(f"Password: Admin123!")
    print("\nVenue disponible:")
    print(f"Nombre:   Salon Gauchos de Guemes")
    print(f"Dirección: Circunvalacion Oeste Salta Capital")
    print("="*60)
    print("\n⚠️  IMPORTANTE: Cambia la contraseña después del primer login.")
    print("🎉 Datos semilla cargados correctamente!")
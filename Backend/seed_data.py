"""
Script simplificado para crear solo un usuario administrador en la base de datos de producción.
Ejecuta este script para inicializar la DB de Render con el usuario admin.
"""
from app import app, db
from models.user import User
from datetime import datetime

with app.app_context():
    # Verificar si ya existe el usuario admin
    existing_admin = User.query.filter_by(email="admin@gauchosguemes.com").first()
    
    if existing_admin:
        print("⚠️  El usuario admin ya existe en la base de datos.")
        print(f"Email: {existing_admin.email}")
        print("No se crearon usuarios duplicados.")
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
        db.session.commit()
        
        print("✅ Usuario administrador creado exitosamente!")
        print("\n" + "="*50)
        print("CREDENCIALES DE ACCESO:")
        print("="*50)
        print(f"Email:    admin@gauchosguemes.com")
        print(f"Password: Admin123!")
        print("="*50)
        print("\n⚠️  IMPORTANTE: Cambia la contraseña después del primer login.")
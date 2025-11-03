# 🏛️ Gauchos De Güemes - Backend API

![Flask](https://img.shields.io/badge/Flask-3.1.2-000000?style=for-the-badge&logo=flask&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.9-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-Auth-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

> Sistema de gestión de reservas para eventos con autenticación JWT, recuperación de contraseñas por email y API RESTful completa.

---

## 📋 Tabla de Contenidos

- [🚀 Características](#-características)
- [🛠️ Tecnologías](#️-tecnologías)
- [📦 Instalación](#-instalación)
- [⚙️ Configuración](#️-configuración)
- [🔐 Autenticación JWT](#-autenticación-jwt)
- [📧 Sistema de Email](#-sistema-de-email)
- [🌐 API Endpoints](#-api-endpoints)
- [🧪 Testing](#-testing)
- [🔒 Seguridad](#-seguridad)
- [📝 Modelos de Datos](#-modelos-de-datos)
- [🚀 Deployment](#-deployment)

---

## 🚀 Características

✅ **Autenticación JWT** - Sistema completo de login/registro con tokens  
✅ **Recuperación de Contraseñas** - Envío de emails con links de reset  
✅ **CRUD Completo** - Usuarios, Clientes, Reservas, Servicios, Venues  
✅ **CORS Configurado** - Listo para trabajar con frontend React  
✅ **Validaciones** - Campos únicos, formatos de email, contraseñas seguras  
✅ **Relaciones Many-to-Many** - Reservas con múltiples servicios  
✅ **Estados de Reserva** - Solicitada, Confirmada, Cancelada  
✅ **Hash de Contraseñas** - PBKDF2-SHA256 con salt  
✅ **Error Handling** - Manejo de errores con rollback automático  

---

## 🛠️ Tecnologías

### Backend
- **Flask 3.1.2** - Framework web
- **SQLAlchemy 2.0** - ORM
- **Flask-Marshmallow** - Serialización
- **Flask-CORS** - Cross-Origin Resource Sharing
- **Flask-Mail** - Envío de emails
- **PyJWT 2.10** - JSON Web Tokens
- **Werkzeug** - Utilidades WSGI

### Base de Datos
- **SQLite** (desarrollo)
- **PostgreSQL** (producción - migración futura)

---

## 📦 Instalación

### 1. **Clonar el repositorio**

```bash
git clone https://github.com/dmbruno/GauchosDeGuemes.git
cd GauchosDeGuemes/Backend
```

### 2. **Crear entorno virtual**

```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. **Instalar dependencias**

```bash
pip install -r requirements.txt
```

### 4. **Configurar variables de entorno**

Crea un archivo `.env` en la raíz del Backend:

```env
FLASK_ENV=development
SECRET_KEY=tu-clave-secreta-super-segura
SQLALCHEMY_DATABASE_URI=sqlite:///instance/gauchos.db
SQLALCHEMY_TRACK_MODIFICATIONS=False

# Configuración de Email
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=tu-email@gmail.com
MAIL_PASSWORD=tu-contraseña-de-aplicacion
MAIL_DEFAULT_SENDER=tu-email@gmail.com
FRONTEND_URL=http://localhost:5173
```

### 5. **Crear base de datos con datos de prueba**

```bash
python3 seed_data.py
```

### 6. **Iniciar servidor**

```bash
python3 app.py
```

El servidor estará corriendo en: **http://localhost:5050**

---

## ⚙️ Configuración

### 📧 **Configuración de Email (Gmail)**

Para que funcione el sistema de recuperación de contraseñas:

#### **Paso 1: Crear Contraseña de Aplicación en Gmail**

1. Ve a: https://myaccount.google.com/security
2. Activa **"Verificación en 2 pasos"**
3. Ve a **"Contraseñas de aplicaciones"**
4. Selecciona:
   - Aplicación: **Correo**
   - Dispositivo: **Otro (personalizado)**
   - Nombre: **"Gauchos Backend"**
5. Copia la contraseña de 16 caracteres

#### **Paso 2: Actualizar `.env`**

```env
MAIL_USERNAME=tu-email@gmail.com
MAIL_PASSWORD=abcd efgh ijkl mnop  # Contraseña de 16 caracteres
MAIL_DEFAULT_SENDER=tu-email@gmail.com
```

#### **Paso 3: Reiniciar servidor**

```bash
python3 app.py
```

### 🔧 **Otros Proveedores de Email**

<details>
<summary><strong>Outlook/Hotmail</strong></summary>

```env
MAIL_SERVER=smtp-mail.outlook.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=tu-email@outlook.com
MAIL_PASSWORD=tu-contraseña
MAIL_DEFAULT_SENDER=tu-email@outlook.com
```
</details>

<details>
<summary><strong>Email Corporativo (cPanel)</strong></summary>

```env
MAIL_SERVER=mail.tudominio.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=noreply@tudominio.com
MAIL_PASSWORD=tu-contraseña-smtp
MAIL_DEFAULT_SENDER=noreply@tudominio.com
```
</details>

<details>
<summary><strong>Mailtrap (Solo Testing)</strong></summary>

```env
MAIL_SERVER=sandbox.smtp.mailtrap.io
MAIL_PORT=2525
MAIL_USE_TLS=True
MAIL_USERNAME=tu-username-mailtrap
MAIL_PASSWORD=tu-password-mailtrap
MAIL_DEFAULT_SENDER=noreply@gauchosguemes.com
```

Regístrate gratis en: https://mailtrap.io
</details>

---

## 🔐 Autenticación JWT

### **Endpoints de Autenticación**

| Método | Endpoint | Descripción | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/register` | Registrar nuevo usuario | ❌ |
| POST | `/api/auth/login` | Iniciar sesión | ❌ |
| GET | `/api/auth/verify` | Verificar token válido | ✅ |
| POST | `/api/auth/forgot-password` | Solicitar reset de contraseña | ❌ |
| POST | `/api/auth/reset-password` | Resetear contraseña con token | ❌ |

### **Ejemplos de Uso**

#### 📝 **Registro de Usuario**

```http
POST /api/auth/register
Content-Type: application/json

{
  "username": "maria",
  "email": "maria@example.com",
  "password": "securePassword123",
  "is_admin": false
}
```

**Respuesta (201):**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "maria",
    "email": "maria@example.com",
    "is_admin": false,
    "created_at": "2025-11-03T12:00:00"
  }
}
```

#### 🔑 **Login**

```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "admin@example.com",
  "password": "admin123"
}
```

**Respuesta (200):**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "is_admin": true
  }
}
```

#### ✅ **Verificar Token**

```http
GET /api/auth/verify
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Respuesta (200):**
```json
{
  "valid": true,
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "is_admin": true
  }
}
```

### **Protección de Rutas**

Para proteger endpoints, usa el decorador `@token_required`:

```python
from routes.auth import token_required

@booking_bp.route('/bookings', methods=['POST'])
@token_required
def create_booking(current_user):
    # current_user contiene los datos del usuario autenticado
    data = request.get_json()
    # ... código ...
```

### **Uso en Frontend (React)**

```javascript
// 1. Login y guardar token
const login = async (email, password) => {
  const response = await fetch('http://localhost:5050/api/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  
  const data = await response.json();
  localStorage.setItem('token', data.token);
  return data.user;
};

// 2. Hacer peticiones autenticadas
const fetchBookings = async () => {
  const token = localStorage.getItem('token');
  
  const response = await fetch('http://localhost:5050/api/bookings', {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  });
  
  return response.json();
};

// 3. Logout
const logout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('user');
};
```

---

## 📧 Sistema de Email

### **Flujo de Recuperación de Contraseñas**

```
1. Usuario hace clic en "Olvidé mi contraseña"
   ↓
2. Frontend envía POST /api/auth/forgot-password
   ↓
3. Backend genera token único y lo guarda en DB
   ↓
4. Backend envía email con enlace de reset
   ↓
5. Usuario hace clic en el enlace del email
   ↓
6. Frontend muestra formulario de nueva contraseña
   ↓
7. Frontend envía POST /api/auth/reset-password
   ↓
8. Backend valida token y actualiza contraseña
   ↓
9. Usuario puede iniciar sesión con nueva contraseña
```

### **Solicitar Reset de Contraseña**

```http
POST /api/auth/forgot-password
Content-Type: application/json

{
  "email": "usuario@example.com"
}
```

**Respuesta (200):**
```json
{
  "message": "Si el email existe, recibirás instrucciones para resetear tu contraseña"
}
```

### **Resetear Contraseña**

```http
POST /api/auth/reset-password
Content-Type: application/json

{
  "token": "token-recibido-por-email",
  "password": "nuevaContraseña123"
}
```

**Respuesta (200):**
```json
{
  "message": "Contraseña actualizada exitosamente"
}
```

### **Template del Email**

El sistema envía un email HTML profesional:

```html
Asunto: Recuperación de Contraseña - Gauchos De Güemes

Hola admin,

Recibimos una solicitud para restablecer la contraseña de tu cuenta.

[Botón: Restablecer Contraseña]

O copia este enlace:
http://localhost:5173/reset-password?token=abc123...

Este enlace expirará en 1 hora.

Si no solicitaste este cambio, ignora este email.

© 2025 Gauchos De Güemes
```

### **Características de Seguridad del Email**

✅ Tokens únicos y aleatorios (32 bytes)  
✅ Expiración automática (1 hora)  
✅ Un solo uso por token  
✅ Mensajes genéricos (no revela si email existe)  
✅ Contraseñas nunca enviadas por email  

---

## 🌐 API Endpoints

### **Base URL**
```
http://localhost:5050/api
```

### **Autenticación**

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/auth/register` | Registrar usuario |
| POST | `/auth/login` | Iniciar sesión |
| GET | `/auth/verify` | Verificar token |
| POST | `/auth/forgot-password` | Solicitar reset |
| POST | `/auth/reset-password` | Resetear contraseña |

### **Usuarios**

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/users` | Listar usuarios |
| POST | `/users` | Crear usuario |
| GET | `/users/<id>` | Obtener usuario |
| PUT | `/users/<id>` | Actualizar usuario |
| DELETE | `/users/<id>` | Eliminar usuario |

### **Clientes**

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/clients` | Listar clientes |
| POST | `/clients` | Crear cliente |
| GET | `/clients/<id>` | Obtener cliente |
| PUT | `/clients/<id>` | Actualizar cliente |
| DELETE | `/clients/<id>` | Eliminar cliente |

### **Reservas (Bookings)**

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/bookings` | Listar reservas |
| POST | `/bookings` | Crear reserva |
| GET | `/bookings/<id>` | Obtener reserva |
| PUT | `/bookings/<id>` | Actualizar reserva |
| DELETE | `/bookings/<id>` | Eliminar reserva |
| GET | `/bookings/statuses` | Estados permitidos |

**Estados de Reserva:**
- `solicitada` - Estado inicial
- `confirmada` - Reserva confirmada
- `cancelada` - Reserva cancelada

### **Servicios**

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/services` | Listar servicios |
| POST | `/services` | Crear servicio |
| GET | `/services/<id>` | Obtener servicio |
| PUT | `/services/<id>` | Actualizar servicio |
| DELETE | `/services/<id>` | Eliminar servicio |

**Servicios Disponibles:**
1. **Catering** - Comida para eventos
2. **Barra de Bebidas** - Servicio de bar

### **Venues**

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/venues` | Listar venues |
| POST | `/venues` | Crear venue |
| GET | `/venues/<id>` | Obtener venue |
| PUT | `/venues/<id>` | Actualizar venue |
| DELETE | `/venues/<id>` | Eliminar venue |

### **Galería**

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/gallery-images` | Listar imágenes |
| POST | `/gallery-images` | Crear imagen |
| GET | `/gallery-images/<id>` | Obtener imagen |
| PUT | `/gallery-images/<id>` | Actualizar imagen |
| DELETE | `/gallery-images/<id>` | Eliminar imagen |

### **Leads de Contacto**

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/contact-leads` | Listar leads |
| POST | `/contact-leads` | Crear lead |
| GET | `/contact-leads/<id>` | Obtener lead |
| PUT | `/contact-leads/<id>` | Actualizar lead |
| DELETE | `/contact-leads/<id>` | Eliminar lead |

### **Logs de Auditoría**

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/audit-logs` | Listar logs |
| POST | `/audit-logs` | Crear log |
| GET | `/audit-logs/<id>` | Obtener log |

---

## 🧪 Testing

### **Usuarios de Prueba**

Después de ejecutar `seed_data.py`:

| Username | Email | Password | Admin |
|----------|-------|----------|-------|
| admin | admin@example.com | admin123 | ✅ |
| juan | juan@example.com | juan123 | ❌ |

### **Testing con Postman/Thunder Client**

#### **1. Login**
```http
POST http://localhost:5050/api/auth/login
Content-Type: application/json

{
  "email": "admin@example.com",
  "password": "admin123"
}
```

#### **2. Crear Reserva (con token)**
```http
POST http://localhost:5050/api/bookings
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "client_id": 1,
  "venue_id": 1,
  "date": "2025-12-25T18:00:00",
  "status": "solicitada",
  "guests_count": 100,
  "service_ids": [1, 2]
}
```

#### **3. Recuperar Contraseña**
```http
POST http://localhost:5050/api/auth/forgot-password
Content-Type: application/json

{
  "email": "admin@example.com"
}
```

### **Testing Frontend (React)**

```javascript
// Ejemplo de integración
const API_URL = 'http://localhost:5050/api';

// Login
const loginUser = async (email, password) => {
  const response = await fetch(`${API_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  return response.json();
};

// Crear reserva
const createBooking = async (bookingData) => {
  const token = localStorage.getItem('token');
  
  const response = await fetch(`${API_URL}/bookings`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(bookingData)
  });
  return response.json();
};
```

---

## 🔒 Seguridad

### **Características Implementadas**

✅ **Contraseñas Hasheadas** - PBKDF2-SHA256 con salt automático  
✅ **JWT con Expiración** - Tokens válidos por 24 horas  
✅ **Reset Tokens** - Expiran en 1 hora, un solo uso  
✅ **CORS Configurado** - Solo orígenes permitidos  
✅ **Validación de Datos** - Campos requeridos, formatos de email  
✅ **SQL Injection Protection** - ORM SQLAlchemy  
✅ **XSS Protection** - Sanitización de inputs  
✅ **Campos Sensibles Excluidos** - password_hash no se expone en API  
✅ **Mensajes Genéricos** - No revelar información en forgot-password  
✅ **Rollback Automático** - Transacciones seguras  

### **Configuración de Seguridad**

```python
# JWT
SECRET_KEY = "clave-secreta-super-segura"  # Cambiar en producción
TOKEN_EXPIRATION = 24  # horas

# Hashing de contraseñas
method = 'pbkdf2:sha256'
salt_length = 8

# Reset tokens
RESET_TOKEN_LENGTH = 32  # bytes
RESET_TOKEN_EXPIRATION = 1  # hora
```

### **Mejores Prácticas**

🔐 **Producción:**
- Cambiar `SECRET_KEY` a un valor aleatorio y seguro
- Usar HTTPS (TLS/SSL)
- Implementar rate limiting
- Usar PostgreSQL en lugar de SQLite
- Configurar logs de auditoría
- Implementar CAPTCHA en forgot-password
- Usar variables de entorno para credenciales

⚠️ **No hacer:**
- Exponer el archivo `.env` en Git
- Usar contraseñas débiles en producción
- Retornar mensajes de error detallados al usuario
- Compartir tokens JWT
- Usar la misma SECRET_KEY en desarrollo y producción

---

## 📝 Modelos de Datos

### **User**
```python
{
  "id": Integer (PK),
  "username": String(80) UNIQUE,
  "email": String(120) UNIQUE,
  "password_hash": String(255),
  "is_admin": Boolean,
  "reset_token": String(255) NULLABLE,
  "reset_token_expires": DateTime NULLABLE,
  "created_at": DateTime
}
```

### **Client**
```python
{
  "id": Integer (PK),
  "dni": String(20) UNIQUE,
  "first_name": String(100),
  "last_name": String(100),
  "phone": String(20),
  "email": String(120),
  "created_at": DateTime
}
```

### **Booking**
```python
{
  "id": Integer (PK),
  "client_id": Integer (FK → clients.id),
  "venue_id": Integer (FK → venues.id),
  "date": DateTime,
  "status": String(50),  # solicitada, confirmada, cancelada
  "guests_count": Integer,
  "contact_preference": String(50),
  "event_type": String(100),
  "other_services": Text,
  "created_at": DateTime,
  "services": [Service]  # Many-to-Many
}
```

### **Service**
```python
{
  "id": Integer (PK),
  "name": String(120),  # Catering, Barra de Bebidas
  "type": String(20),
  "details": String(255),
  "created_at": DateTime
}
```

### **Venue**
```python
{
  "id": Integer (PK),
  "name": String(200),
  "address": String(255),
  "created_at": DateTime
}
```

### **Relaciones**

```
User (1) ───────── (N) AuditLog
Client (1) ──────── (N) Booking
Venue (1) ───────── (N) Booking
Venue (1) ───────── (N) GalleryImage
Booking (N) ─────── (N) Service  [Many-to-Many via booking_services]
```

---

## 🚀 Deployment

### **Preparación para Producción**

1. **Cambiar a PostgreSQL**

```python
# .env
SQLALCHEMY_DATABASE_URI=postgresql://user:password@localhost/gauchos_db
```

2. **Actualizar SECRET_KEY**

```python
# Generar clave segura
import secrets
print(secrets.token_hex(32))

# .env
SECRET_KEY=clave-generada-aleatoriamente
```

3. **Configurar Email de Producción**

```env
MAIL_SERVER=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USERNAME=apikey
MAIL_PASSWORD=tu-api-key-sendgrid
FRONTEND_URL=https://tudominio.com
```

4. **Agregar Gunicorn**

```bash
pip install gunicorn
```

```bash
# Iniciar con Gunicorn
gunicorn -w 4 -b 0.0.0.0:5050 app:app
```

5. **Variables de Entorno de Producción**

```env
FLASK_ENV=production
DEBUG=False
SECRET_KEY=clave-super-segura-aleatoria
SQLALCHEMY_DATABASE_URI=postgresql://...
```

### **Deployment en Heroku**

```bash
# Procfile
web: gunicorn app:app

# runtime.txt
python-3.9.18

# Desplegar
heroku create gauchos-backend
git push heroku main
heroku config:set SECRET_KEY=tu-secret-key
```

### **Deployment en Railway**

1. Conectar repositorio de GitHub
2. Configurar variables de entorno
3. Railway detectará automáticamente Flask
4. Deploy automático en cada push

---

## 📚 Documentación Adicional

### **Estructura del Proyecto**

```
Backend/
├── app.py                 # Aplicación principal
├── extensions.py          # Inicialización de extensiones
├── seed_data.py          # Datos de prueba
├── requirements.txt      # Dependencias
├── .env                  # Variables de entorno (no en Git)
├── models/               # Modelos SQLAlchemy
│   ├── user.py
│   ├── client.py
│   ├── booking.py
│   ├── service.py
│   ├── venue.py
│   ├── gallery_image.py
│   ├── contact_lead.py
│   └── audit_log.py
├── routes/               # Blueprints de rutas
│   ├── auth.py
│   ├── user_routes.py
│   ├── client_routes.py
│   ├── booking_routes.py
│   ├── service_routes.py
│   ├── venue_routes.py
│   ├── gallery_image_routes.py
│   ├── contact_lead_routes.py
│   └── audit_log_routes.py
└── instance/             # Base de datos SQLite
    └── gauchos.db
```

### **Dependencias Completas**

```txt
Flask==3.1.2
Flask-SQLAlchemy==3.1.1
Flask-Marshmallow==1.3.0
Flask-CORS==4.0.0
Flask-Mail==0.10.0
marshmallow-sqlalchemy==1.4.2
PyJWT==2.10.1
python-dotenv==1.1.1
Werkzeug==3.1.3
SQLAlchemy==2.0.43
```

---

## 🐛 Troubleshooting

### **Error: Token expirado**
```json
{"error": "Token expirado"}
```
**Solución:** Vuelve a hacer login para obtener un nuevo token.

### **Error: Email ya registrado**
```json
{"error": "El email ya está registrado"}
```
**Solución:** Usa otro email o actualiza el usuario existente.

### **Error: Error al enviar email**
```
Error al enviar email: SMTPAuthenticationError
```
**Solución:** 
- Verifica las credenciales en `.env`
- Asegúrate de usar contraseña de aplicación en Gmail
- Verifica que la verificación en 2 pasos esté activada

### **Error: CORS**
```
Access to fetch has been blocked by CORS policy
```
**Solución:** Verifica que el origen esté en la lista de CORS en `app.py`.

### **Error: Base de datos bloqueada**
```
sqlite3.OperationalError: database is locked
```
**Solución:** Cierra todas las conexiones o reinicia el servidor.

---

## 👥 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más información.

---

## 📞 Contacto

**Diego Bruno** - [@dmbruno](https://github.com/dmbruno)

**Link del Proyecto:** [https://github.com/dmbruno/GauchosDeGuemes](https://github.com/dmbruno/GauchosDeGuemes)

---

## 🙏 Agradecimientos

- Flask Documentation
- JWT.io
- SQLAlchemy
- Marshmallow

---

<div align="center">

**Hecho con ❤️ para Gauchos De Güemes**

![Status](https://img.shields.io/badge/Status-Production%20Ready-success?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-1.0.0-blue?style=for-the-badge)

</div>

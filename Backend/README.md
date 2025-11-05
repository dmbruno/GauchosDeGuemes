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

### **URLs Base**

- **Producción:** `https://gauchos-backend.onrender.com/api`
- **Desarrollo:** `http://localhost:5050/api`

### **Dominios CORS Permitidos**

✅ localhost (5050, 5173, 127.0.0.1)  
✅ https://gestionreservas-gauchosguemes.onrender.com  
✅ https://gauchosdeguemes.com.ar  
✅ https://ggeyc.netlify.app

### **Resumen de Endpoints**

| Recurso | GET | POST | PUT | DELETE | Auth |
|---------|-----|------|-----|--------|------|
| `/auth/login` | - | ✅ | - | - | ❌ |
| `/auth/register` | - | ✅ | - | - | ❌ |
| `/auth/verify` | ✅ | - | - | - | ✅ |
| `/users` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `/clients` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `/reservas` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `/services` | ✅ | ✅ | ✅ | ✅ | ❌/✅ |
| `/venues` | ✅ | ✅ | ✅ | ✅ | ❌/✅ |
| `/gallery-images` | ✅ | ✅ | ✅ | ✅ | ❌/✅ |
| `/contact-leads` | ✅ | ✅ | ✅ | ✅ | ❌/✅ |

**Nota:** ❌/✅ = GET es público, otros métodos requieren autenticación

### **Ejemplo Completo: Reservas**

#### **1. Obtener todas las reservas**
```http
GET https://gauchos-backend.onrender.com/api/reservas
Authorization: Bearer {token}
```

#### **2. Crear nueva reserva**
```http
POST https://gauchos-backend.onrender.com/api/reservas
Authorization: Bearer {token}
Content-Type: application/json

{
  "client_id": 1,
  "venue_id": 1,
  "date": "2025-12-20T19:00:00",
  "status": "solicitada",
  "guests_count": 150,
  "contact_preference": "WhatsApp",
  "event_type": "Boda",
  "other_services": "Decoración floral",
  "service_ids": [1, 2]
}
```

**Respuesta (201):**
```jsonn
{
  "id": 1,
  "client_id": 1,
  "venue_id": 1,
  "date": "2025-12-20T19:00:00",
  "status": "solicitada",
  "guests_count": 150,
  "services": [
    {"id": 1, "name": "Catering"},
    {"id": 2, "name": "Barra de Bebidas"}
  ],
  "created_at": "2025-11-05T15:30:00"
}
```

#### **3. Actualizar reserva**
```http
PUT https://gauchos-backend.onrender.com/api/reservas/1
Authorization: Bearer {token}
Content-Type: application/json

{
  "status": "confirmada",
  "guests_count": 180
}
```

#### **4. Eliminar reserva**
```http
DELETE https://gauchos-backend.onrender.com/api/reservas/1
Authorization: Bearer {token}
```

#### **5. Estados de reserva**
```http
GET https://gauchos-backend.onrender.com/api/reservas/statuses
```

**Respuesta:**
```json
{
  "statuses": ["solicitada", "confirmada", "cancelada"]
}
```

### **Integración en JavaScript**

```javascript
const API_URL = 'https://gauchos-backend.onrender.com/api';

// Login
async function login(email, password) {
  const response = await fetch(`${API_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  const data = await response.json();
  localStorage.setItem('token', data.token);
  return data;
}

// Obtener reservas
async function getReservas() {
  const token = localStorage.getItem('token');
  const response = await fetch(`${API_URL}/reservas`, {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  });
  return await response.json();
}

// Crear reserva
async function createReserva(data) {
  const token = localStorage.getItem('token');
  const response = await fetch(`${API_URL}/reservas`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  });
  return await response.json();
}
```

### **Códigos de Respuesta**

- `200` OK - Éxito
- `201` Created - Creado exitosamente
- `400` Bad Request - Datos inválidos
- `401` Unauthorized - Token inválido/expirado
- `404` Not Found - Recurso no encontrado
- `500` Server Error - Error del servidor

---

## 🧪 Testing

### **Credenciales de Prueba**

| Email | Password | Admin |
|-------|----------|-------|
| admin@gauchosguemes.com | Admin123! | ✅ |

### **URLs**

- **API Producción:** https://gauchos-backend.onrender.com/api
- **Panel Admin:** https://gestionreservas-gauchosguemes.onrender.com
- **API Desarrollo:** http://localhost:5050/api

### **Ejemplos con cURL**

```bash
# Login
curl -X POST https://gauchos-backend.onrender.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@gauchosguemes.com","password":"Admin123!"}'

# Listar reservas (reemplaza {token})
curl https://gauchos-backend.onrender.com/api/reservas \
  -H "Authorization: Bearer {token}"

# Crear reserva
curl -X POST https://gauchos-backend.onrender.com/api/reservas \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": 1,
    "venue_id": 1,
    "date": "2025-12-25T18:00:00",
    "status": "solicitada",
    "guests_count": 100,
    "service_ids": [1, 2]
  }'
```

---

## 🔒 Seguridad

✅ **Contraseñas Hasheadas** - PBKDF2-SHA256  
✅ **JWT con Expiración** - 24 horas  
✅ **Reset Tokens** - 1 hora, un solo uso  
✅ **CORS Configurado** - Solo orígenes permitidos  
✅ **SQL Injection Protection** - ORM SQLAlchemy  
✅ **Campos Sensibles Excluidos** - password_hash no se expone

### **Configuración**

```python
TOKEN_EXPIRATION = 24  # horas
RESET_TOKEN_EXPIRATION = 1  # hora
```

### **Mejores Prácticas**

🔐 Usar HTTPS en producción  
🔐 SECRET_KEY aleatorio y único  
🔐 PostgreSQL en lugar de SQLite  
🔐 Rate limiting para forgot-password  
🔐 Variables de entorno para credenciales

---

## 📝 Modelos de Datos

### **User**
- `id`, `username` (unique), `email` (unique)
- `password_hash`, `is_admin`, `created_at`
- `reset_token`, `reset_token_expires` (nullable)

### **Client**
- `id`, `dni` (unique), `first_name`, `last_name`
- `phone`, `email`, `created_at`

### **Booking**
- `id`, `client_id` (FK), `venue_id` (FK)
- `date`, `status` (solicitada/confirmada/cancelada)
- `guests_count`, `contact_preference`, `event_type`
- `other_services`, `created_at`
- `services` (Many-to-Many)

### **Service**
- `id`, `name`, `type`, `details`, `created_at`

### **Venue**
- `id`, `name`, `address`, `created_at`

### **Relaciones**
```
Client (1) → (N) Booking
Venue (1) → (N) Booking
Booking (N) ↔ (N) Service
User (1) → (N) AuditLog
Venue (1) → (N) GalleryImage
```

---

## 🚀 Deployment

### **Producción Actual**

✅ **Backend:** https://gauchos-backend.onrender.com  
✅ **Panel Admin:** https://gestionreservas-gauchosguemes.onrender.com  
✅ **Landing:** https://gauchosdeguemes.com.ar  
✅ **Database:** PostgreSQL en Render

### **Render - Backend Setup**

1. **Build Command:** `pip install -r requirements.txt`
2. **Start Command:** `gunicorn app:app`
3. **Environment Variables:**
```env
FLASK_ENV=production
SECRET_KEY=tu-secret-key-segura
DATABASE_URL=postgresql://...
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=salongauchosguemes@gmail.com
MAIL_PASSWORD=tu-app-password
FRONTEND_URL=https://gestionreservas-gauchosguemes.onrender.com
```

### **Seed Producción**

```bash
# Temporal: conectar a DB de producción
export DATABASE_URL="postgres://user:pass@host/db"
pip install psycopg2-binary
python3 seed_data.py
unset DATABASE_URL
```

### **Agregar Dominio a CORS**

Edita `app.py`:
```python
CORS(app, resources={
    r"/api/*": {
        "origins": [
            # ...existentes...
            "https://nuevo-dominio.com",
        ]
    }
})
```

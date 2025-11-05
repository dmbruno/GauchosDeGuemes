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

## 🌐 API Endpoints - Documentación Completa

### **URLs Base**

**Producción:**
```
https://gauchos-backend.onrender.com/api
```

**Desarrollo:**
```
http://localhost:5050/api
```

### 🔧 **Configuración del Frontend**

Crea un archivo `.env` en tu proyecto frontend:

```bash
# Para Vite (React + Vite)
VITE_API_URL=https://gauchos-backend.onrender.com/api

# Para Create React App
REACT_APP_API_URL=https://gauchos-backend.onrender.com/api

# Para Next.js
NEXT_PUBLIC_API_URL=https://gauchos-backend.onrender.com/api

# Para desarrollo local
VITE_API_URL=http://localhost:5050/api
```

### 🌐 **Dominios Permitidos (CORS)**

Los siguientes dominios están autorizados para hacer peticiones:

- ✅ `http://localhost:5173` (desarrollo local)
- ✅ `http://localhost:5050` (desarrollo local)
- ✅ `http://127.0.0.1:5173` (desarrollo local alternativo)
- ✅ `http://127.0.0.1:5050` (desarrollo local alternativo)
- ✅ `https://gestionreservas-gauchosguemes.onrender.com` (panel de gestión)
- ✅ `https://ggeyc.netlify.app` (landing temporal)
- ✅ `https://gauchosdeguemes.com.ar` (landing principal)
- ✅ `https://www.gauchosdeguemes.com.ar` (landing con www)

### 📚 **Endpoints Disponibles**

#### 🔐 **Autenticación**

| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| POST | `/auth/register` | Registrar usuario | ❌ |
| POST | `/auth/login` | Iniciar sesión | ❌ |
| GET | `/auth/verify` | Verificar token | ✅ |
| POST | `/auth/forgot-password` | Solicitar reset | ❌ |
| POST | `/auth/reset-password` | Resetear contraseña | ❌ |

**Ejemplo - Login:**
```json
POST /api/auth/login
{
  "email": "admin@gauchosguemes.com",
  "password": "Admin123!"
}

Response:
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@gauchosguemes.com",
    "is_admin": true
  }
}
```

**Ejemplo - Verificar Token:**
```http
GET /api/auth/verify
Authorization: Bearer {token}

Response:
{
  "valid": true,
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@gauchosguemes.com"
  }
}
```

#### 👥 **Usuarios**

| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| GET | `/users` | Listar usuarios | ✅ |
| POST | `/users` | Crear usuario | ✅ |
| GET | `/users/{id}` | Obtener usuario | ✅ |
| PUT | `/users/{id}` | Actualizar usuario | ✅ |
| DELETE | `/users/{id}` | Eliminar usuario | ✅ |

**Ejemplo - Crear Usuario:**
```json
POST /api/users
Authorization: Bearer {token}
{
  "username": "nuevo_usuario",
  "email": "nuevo@example.com",
  "password": "Password123!",
  "is_admin": false
}
```

#### 👤 **Clientes**

| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| GET | `/clients` | Listar clientes | ✅ |
| POST | `/clients` | Crear cliente | ✅ |
| GET | `/clients/{id}` | Obtener cliente | ✅ |
| PUT | `/clients/{id}` | Actualizar cliente | ✅ |
| DELETE | `/clients/{id}` | Eliminar cliente | ✅ |

**Ejemplo - Crear Cliente:**
```json
POST /api/clients
Authorization: Bearer {token}
{
  "dni": "12345678",
  "first_name": "Juan",
  "last_name": "Pérez",
  "phone": "+5493875051234",
  "email": "juan@example.com"
}
```

#### 📞 **Contacto / Leads**

| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| GET | `/contact-leads` | Listar consultas | ✅ |
| POST | `/contact-leads` | Enviar formulario | ❌ (público) |
| GET | `/contact-leads/{id}` | Obtener consulta | ✅ |
| PUT | `/contact-leads/{id}` | Actualizar consulta | ✅ |
| DELETE | `/contact-leads/{id}` | Eliminar consulta | ✅ |

**Ejemplo - Enviar Formulario (público):**
```json
POST /api/contact-leads
{
  "name": "Juan Pérez",
  "email": "juan@example.com",
  "phone": "+54 9 387 123-4567",
  "message": "Consulta sobre alquiler de salón",
  "lead_metadata": "landing-page"
}
```

#### 🎉 **Servicios**

| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| GET | `/services` | Listar servicios | ❌ (público) |
| POST | `/services` | Crear servicio | ✅ |
| GET | `/services/{id}` | Obtener servicio | ❌ (público) |
| PUT | `/services/{id}` | Actualizar servicio | ✅ |
| DELETE | `/services/{id}` | Eliminar servicio | ✅ |

**Ejemplo - Obtener Servicios (público):**
```json
GET /api/services

Response:
[
  {
    "id": 1,
    "name": "Catering",
    "type": "Comida",
    "details": "Disponemos de amplia variedad para que no falte nada en tu evento"
  },
  {
    "id": 2,
    "name": "Barra de Bebidas",
    "type": "Bebidas",
    "details": "Tenemos una barra super completa para que no te tengas que ocupar de esto durante tu evento"
  }
]
```

#### 🏛️ **Salones / Venues**

| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| GET | `/venues` | Listar venues | ❌ (público) |
| POST | `/venues` | Crear venue | ✅ |
| GET | `/venues/{id}` | Obtener venue | ❌ (público) |
| PUT | `/venues/{id}` | Actualizar venue | ✅ |
| DELETE | `/venues/{id}` | Eliminar venue | ✅ |

#### 📅 **Reservas**

| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| GET | `/reservas` | Listar reservas | ✅ |
| POST | `/reservas` | Crear reserva | ✅ |
| GET | `/reservas/{id}` | Obtener reserva | ✅ |
| PUT | `/reservas/{id}` | Actualizar reserva | ✅ |
| DELETE | `/reservas/{id}` | Eliminar reserva | ✅ |
| GET | `/reservas/statuses` | Estados permitidos | ✅ |

**Estados de Reserva:**
- `solicitada` - Estado inicial
- `confirmada` - Reserva confirmada
- `cancelada` - Reserva cancelada

**Ejemplo - Crear Reserva:**
```json
POST /api/reservas
Authorization: Bearer {token}
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

Response:
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

#### 🖼️ **Galería**

| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| GET | `/gallery-images` | Listar imágenes | ❌ (público) |
| POST | `/gallery-images` | Crear imagen | ✅ |
| GET | `/gallery-images/{id}` | Obtener imagen | ❌ (público) |
| PUT | `/gallery-images/{id}` | Actualizar imagen | ✅ |
| DELETE | `/gallery-images/{id}` | Eliminar imagen | ✅ |

#### 📝 **Logs de Auditoría**

| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| GET | `/audit-logs` | Listar logs | ✅ |
| POST | `/audit-logs` | Crear log | ✅ |
| GET | `/audit-logs/{id}` | Obtener log | ✅ |

### 💻 **Ejemplos de Integración**

#### **JavaScript Vanilla / Fetch API**

```javascript
// Configuración base
const API_URL = 'https://gauchos-backend.onrender.com/api';

// 1. Enviar formulario de contacto (público)
async function sendContactForm(data) {
  try {
    const response = await fetch(`${API_URL}/contact-leads`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });
    
    if (!response.ok) throw new Error('Error al enviar formulario');
    return await response.json();
  } catch (error) {
    console.error('Error:', error);
    throw error;
  }
}

// Uso:
const formData = {
  name: 'Juan Pérez',
  email: 'juan@example.com',
  phone: '+54 9 387 123-4567',
  message: 'Consulta sobre eventos',
  lead_metadata: 'landing-page'
};

sendContactForm(formData)
  .then(result => console.log('Consulta enviada:', result))
  .catch(error => console.error('Error:', error));

// 2. Obtener servicios (público)
async function getServices() {
  const response = await fetch(`${API_URL}/services`);
  return await response.json();
}

// 3. Login y obtener token
async function login(email, password) {
  const response = await fetch(`${API_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  
  const data = await response.json();
  
  // Guardar token
  localStorage.setItem('token', data.token);
  localStorage.setItem('user', JSON.stringify(data.user));
  
  return data;
}

// 4. Peticiones protegidas con token
async function getBookings() {
  const token = localStorage.getItem('token');
  
  const response = await fetch(`${API_URL}/reservas`, {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  });
  
  if (response.status === 401) {
    localStorage.removeItem('token');
    throw new Error('Sesión expirada');
  }
  
  return await response.json();
}

// 5. Logout
function logout() {
  localStorage.removeItem('token');
  localStorage.removeItem('user');
}
```

#### **React / Axios**

```javascript
import axios from 'axios';

// Crear instancia de axios
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'https://gauchos-backend.onrender.com/api',
  headers: { 'Content-Type': 'application/json' }
});

// Interceptor para agregar token automáticamente
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Interceptor para manejar errores de autenticación
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Servicios organizados
export const contactAPI = {
  send: (data) => api.post('/contact-leads', data),
  getAll: () => api.get('/contact-leads'),
  getById: (id) => api.get(`/contact-leads/${id}`),
  update: (id, data) => api.put(`/contact-leads/${id}`, data),
  delete: (id) => api.delete(`/contact-leads/${id}`)
};

export const servicesAPI = {
  getAll: () => api.get('/services'),
  getById: (id) => api.get(`/services/${id}`),
  create: (data) => api.post('/services', data),
  update: (id, data) => api.put(`/services/${id}`, data),
  delete: (id) => api.delete(`/services/${id}`)
};

export const authAPI = {
  login: (credentials) => api.post('/auth/login', credentials),
  register: (userData) => api.post('/auth/register', userData),
  verify: () => api.get('/auth/verify'),
  forgotPassword: (email) => api.post('/auth/forgot-password', { email }),
  resetPassword: (token, password) => api.post('/auth/reset-password', { token, password })
};

export const bookingsAPI = {
  getAll: () => api.get('/reservas'),
  getById: (id) => api.get(`/reservas/${id}`),
  create: (data) => api.post('/reservas', data),
  update: (id, data) => api.put(`/reservas/${id}`, data),
  delete: (id) => api.delete(`/reservas/${id}`),
  getStatuses: () => api.get('/reservas/statuses')
};

// Ejemplo de uso en componente
import { useState, useEffect } from 'react';
import { servicesAPI } from './api';

function ServicesPage() {
  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    servicesAPI.getAll()
      .then(response => setServices(response.data))
      .catch(error => console.error('Error:', error))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div>Cargando...</div>;

  return (
    <div>
      {services.map(service => (
        <div key={service.id}>
          <h3>{service.name}</h3>
          <p>{service.details}</p>
        </div>
      ))}
    </div>
  );
}
```

### 🔒 **Autenticación y Seguridad**

#### **Uso del Token JWT**

Todos los endpoints protegidos requieren un token JWT en el header:

```http
Authorization: Bearer {tu_token_aqui}
```

#### **Flujo de Autenticación**

1. **Login:** `POST /api/auth/login` → Obtienes token y datos de usuario
2. **Guardar token:** En `localStorage` o `sessionStorage`
3. **Usar token:** En cada petición protegida mediante header `Authorization`
4. **Verificar token:** `GET /api/auth/verify` para validar que sigue activo
5. **Logout:** Eliminar token del storage local

#### **Tiempo de Expiración**

- **Token JWT:** 24 horas
- **Token de reset de contraseña:** 1 hora

### ⚠️ **Manejo de Errores**

#### **Códigos de Respuesta HTTP**

- `200` - OK (éxito)
- `201` - Created (creado exitosamente)
- `400` - Bad Request (datos inválidos o faltantes)
- `401` - Unauthorized (no autenticado o token inválido)
- `403` - Forbidden (no tienes permisos)
- `404` - Not Found (recurso no encontrado)
- `500` - Internal Server Error (error del servidor)

#### **Formato de Errores**

```json
{
  "error": "Descripción del error"
}
```

#### **Ejemplo de Manejo de Errores**

```javascript
try {
  const response = await fetch(`${API_URL}/services`);
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error || 'Error en la petición');
  }
  
  const data = await response.json();
  console.log(data);
  
} catch (error) {
  console.error('Error:', error.message);
  alert(`Error: ${error.message}`);
}
```

### 📝 **Notas Importantes**

1. ✅ Todos los endpoints usan JSON (`Content-Type: application/json`)
2. ✅ Las fechas están en formato ISO 8601: `YYYY-MM-DDTHH:MM:SS`
3. ✅ Los endpoints públicos NO requieren autenticación:
   - `GET /api/services`
   - `GET /api/venues`
   - `GET /api/gallery-images`
   - `POST /api/contact-leads`
4. ✅ Los endpoints protegidos requieren token JWT en el header
5. ✅ Los tokens JWT expiran después de 24 horas
6. ✅ Las contraseñas nunca se devuelven en las respuestas
7. ✅ El backend usa PBKDF2-SHA256 para hashear contraseñas
8. ✅ Estados de reserva permitidos: `solicitada`, `confirmada`, `cancelada`

---

## 🧪 Testing

### **Credenciales de Prueba**

Después de ejecutar `seed_data.py`:

| Username | Email | Password | Admin |
|----------|-------|----------|-------|
| admin | admin@gauchosguemes.com | Admin123! | ✅ |

**Producción:**
- URL: `https://gauchos-backend.onrender.com/api`
- Panel: `https://gestionreservas-gauchosguemes.onrender.com`

**Desarrollo:**
- URL: `http://localhost:5050/api`
- Frontend: `http://localhost:5173`

### **Testing con Postman/Thunder Client**

#### **1. Login (Producción)**
```http
POST https://gauchos-backend.onrender.com/api/auth/login
Content-Type: application/json

{
  "email": "admin@gauchosguemes.com",
  "password": "Admin123!"
}
```

#### **2. Enviar Formulario de Contacto (público)**
```http
POST https://gauchos-backend.onrender.com/api/contact-leads
Content-Type: application/json

{
  "name": "Juan Pérez",
  "email": "juan@example.com",
  "phone": "+54 9 387 123-4567",
  "message": "Consulta sobre alquiler",
  "lead_metadata": "landing-page"
}
```

#### **3. Obtener Servicios (público)**
```http
GET https://gauchos-backend.onrender.com/api/services
```

#### **4. Crear Reserva (con token)**
```http
POST https://gauchos-backend.onrender.com/api/reservas
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

#### **5. Recuperar Contraseña**
```http
POST https://gauchos-backend.onrender.com/api/auth/forgot-password
Content-Type: application/json

{
  "email": "admin@gauchosguemes.com"
}
```

---

## 🔒 Seguridad

### **Características Implementadas**

✅ **Contraseñas Hasheadas** - PBKDF2-SHA256 con salt automático  
✅ **JWT con Expiración** - Tokens válidos por 24 horas  
✅ **Reset Tokens** - Expirán en 1 hora, un solo uso  
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

### **Entorno de Producción Actual**

✅ **Backend:** https://gauchos-backend.onrender.com  
✅ **Panel de Gestión:** https://gestionreservas-gauchosguemes.onrender.com  
✅ **Landing Page:** https://gauchosdeguemes.com.ar  
✅ **Re

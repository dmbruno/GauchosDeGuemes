# 🚀 Gauchos De Güemes - Documentación de API

## 📋 Información General

**URL Base de Producción:**
```
https://gauchos-backend.onrender.com
```

**URL Base de Desarrollo:**
```
http://localhost:5050
```

---

## 🔧 Configuración del Frontend

### Variables de Entorno

Crea un archivo `.env` en tu proyecto frontend con:

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

---

## 🌐 Dominios Permitidos (CORS)

Los siguientes dominios están autorizados para hacer peticiones:

- ✅ `http://localhost:5173` (desarrollo local)
- ✅ `http://localhost:5050` (desarrollo local)
- ✅ `https://gestionreservas-gauchosguemes.onrender.com` (panel de gestión)
- ✅ `https://ggeyc.netlify.app` (landing temporal)
- ✅ `https://gauchosdeguemes.com.ar` (landing principal)
- ✅ `https://www.gauchosdeguemes.com.ar` (landing con www)

---

## 📚 Endpoints Disponibles

### 🔐 Autenticación

#### **POST** `/api/auth/login`
Iniciar sesión y obtener token JWT.

**Request:**
```json
{
  "email": "admin@gauchosguemes.com",
  "password": "Admin123!"
}
```

**Response:**
```json
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

#### **POST** `/api/auth/register`
Registrar nuevo usuario.

**Request:**
```json
{
  "username": "usuario",
  "email": "usuario@example.com",
  "password": "Password123!",
  "is_admin": false
}
```

#### **GET** `/api/auth/verify`
Verificar si el token es válido (requiere autenticación).

**Headers:**
```
Authorization: Bearer {token}
```

**Response:**
```json
{
  "valid": true,
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@gauchosguemes.com"
  }
}
```

#### **POST** `/api/auth/forgot-password`
Solicitar recuperación de contraseña por email.

**Request:**
```json
{
  "email": "usuario@example.com"
}
```

#### **POST** `/api/auth/reset-password`
Resetear contraseña con token de email.

**Request:**
```json
{
  "token": "token-del-email",
  "password": "NuevaPassword123!"
}
```

---

### 👥 Usuarios

#### **GET** `/api/users`
Obtener lista de usuarios.

**Response:**
```json
[
  {
    "id": 1,
    "username": "admin",
    "email": "admin@gauchosguemes.com",
    "is_admin": true,
    "created_at": "2025-11-05T12:00:00"
  }
]
```

#### **POST** `/api/users`
Crear nuevo usuario.

**Request:**
```json
{
  "username": "nuevo_usuario",
  "email": "nuevo@example.com",
  "password": "Password123!",
  "is_admin": false
}
```

#### **GET** `/api/users/{id}`
Obtener usuario por ID.

#### **PUT** `/api/users/{id}`
Actualizar usuario.

**Request:**
```json
{
  "username": "usuario_actualizado",
  "email": "actualizado@example.com",
  "password": "NewPassword123!"
}
```

#### **DELETE** `/api/users/{id}`
Eliminar usuario.

---

### 👤 Clientes

#### **GET** `/api/clients`
Obtener lista de clientes.

**Response:**
```json
[
  {
    "id": 1,
    "dni": "12345678",
    "first_name": "María",
    "last_name": "González",
    "phone": "+5493875051111",
    "email": "maria@example.com",
    "created_at": "2025-11-05T12:00:00"
  }
]
```

#### **POST** `/api/clients`
Crear nuevo cliente.

**Request:**
```json
{
  "dni": "12345678",
  "first_name": "Juan",
  "last_name": "Pérez",
  "phone": "+5493875051234",
  "email": "juan@example.com"
}
```

#### **GET** `/api/clients/{id}`
Obtener cliente por ID.

#### **PUT** `/api/clients/{id}`
Actualizar cliente.

#### **DELETE** `/api/clients/{id}`
Eliminar cliente.

---

### 📞 Contacto / Leads

#### **POST** `/api/contact-leads`
Enviar formulario de contacto desde landing page (público).

**Request:**
```json
{
  "name": "Juan Pérez",
  "email": "juan@example.com",
  "phone": "+54 9 387 123-4567",
  "message": "Consulta sobre alquiler de salón para evento",
  "lead_metadata": "landing-page"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "Juan Pérez",
  "email": "juan@example.com",
  "phone": "+54 9 387 123-4567",
  "message": "Consulta sobre alquiler de salón para evento",
  "lead_metadata": "landing-page",
  "created_at": "2025-11-05T15:30:00"
}
```

#### **GET** `/api/contact-leads`
Obtener lista de consultas.

#### **GET** `/api/contact-leads/{id}`
Obtener consulta por ID.

#### **PUT** `/api/contact-leads/{id}`
Actualizar consulta.

#### **DELETE** `/api/contact-leads/{id}`
Eliminar consulta.

---

### 🎉 Servicios

#### **GET** `/api/services`
Obtener lista de servicios disponibles (público).

**Response:**
```json
[
  {
    "id": 1,
    "name": "Catering",
    "type": "Comida",
    "details": "Disponemos de amplia variedad para que no falte nada en tu evento",
    "created_at": "2025-11-05T12:00:00"
  },
  {
    "id": 2,
    "name": "Barra de Bebidas",
    "type": "Bebidas",
    "details": "Tenemos una barra super completa para que no te tengas que ocupar de esto durante tu evento",
    "created_at": "2025-11-05T12:00:00"
  }
]
```

#### **POST** `/api/services`
Crear nuevo servicio.

**Request:**
```json
{
  "name": "DJ y Sonido",
  "type": "Entretenimiento",
  "details": "Servicio de música y sonido profesional"
}
```

#### **GET** `/api/services/{id}`
Obtener servicio por ID.

#### **PUT** `/api/services/{id}`
Actualizar servicio.

#### **DELETE** `/api/services/{id}`
Eliminar servicio.

---

### 🏛️ Salones / Venues

#### **GET** `/api/venues`
Obtener lista de salones disponibles (público).

**Response:**
```json
[
  {
    "id": 1,
    "name": "Gauchos De Güemes",
    "address": "Circunvalación Oeste S/N Salta - Argentina",
    "created_at": "2025-11-05T12:00:00"
  }
]
```

#### **POST** `/api/venues`
Crear nuevo venue.

**Request:**
```json
{
  "name": "Salón Norte",
  "address": "Av. Principal 123, Salta"
}
```

#### **GET** `/api/venues/{id}`
Obtener venue por ID.

#### **PUT** `/api/venues/{id}`
Actualizar venue.

#### **DELETE** `/api/venues/{id}`
Eliminar venue.

---

### 📅 Reservas

#### **GET** `/api/reservas/statuses`
Obtener estados de reserva permitidos.

**Response:**
```json
{
  "statuses": ["solicitada", "confirmada", "cancelada"]
}
```

#### **POST** `/api/reservas`
Crear nueva reserva.

**Request:**
```json
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

**Response:**
```json
{
  "id": 1,
  "client_id": 1,
  "venue_id": 1,
  "date": "2025-12-20T19:00:00",
  "status": "solicitada",
  "guests_count": 150,
  "contact_preference": "WhatsApp",
  "event_type": "Boda",
  "other_services": "Decoración floral",
  "services": [
    {"id": 1, "name": "Catering"},
    {"id": 2, "name": "Barra de Bebidas"}
  ],
  "created_at": "2025-11-05T15:30:00"
}
```

#### **GET** `/api/reservas`
Obtener lista de reservas.

#### **GET** `/api/reservas/{id}`
Obtener reserva por ID.

#### **PUT** `/api/reservas/{id}`
Actualizar reserva.

**Request:**
```json
{
  "status": "confirmada",
  "guests_count": 180,
  "service_ids": [1, 2]
}
```

#### **DELETE** `/api/reservas/{id}`
Eliminar reserva.

---

### 🖼️ Galería

#### **GET** `/api/gallery-images`
Obtener imágenes de galería (público).

**Response:**
```json
[
  {
    "id": 1,
    "venue_id": 1,
    "url": "https://example.com/imagen1.jpg",
    "description": "Vista principal del salón",
    "created_at": "2025-11-05T12:00:00"
  }
]
```

#### **POST** `/api/gallery-images`
Crear nueva imagen.

**Request:**
```json
{
  "venue_id": 1,
  "url": "https://example.com/nueva-imagen.jpg",
  "description": "Nueva vista del jardín"
}
```

#### **GET** `/api/gallery-images/{id}`
Obtener imagen por ID.

#### **PUT** `/api/gallery-images/{id}`
Actualizar imagen.

#### **DELETE** `/api/gallery-images/{id}`
Eliminar imagen.

---

### 📝 Logs de Auditoría

#### **GET** `/api/audit-logs`
Obtener logs de auditoría.

**Response:**
```json
[
  {
    "id": 1,
    "action": "create_booking",
    "user_id": 1,
    "details": "Reserva creada para cliente María González",
    "timestamp": "2025-11-05T15:30:00"
  }
]
```

#### **POST** `/api/audit-logs`
Crear nuevo log.

#### **GET** `/api/audit-logs/{id}`
Obtener log por ID.

---

## 💻 Ejemplos de Código

### JavaScript / Fetch API

```javascript
// Configuración base
const API_URL = 'https://gauchos-backend.onrender.com/api';

// 1. Enviar formulario de contacto
async function sendContactForm(data) {
  try {
    const response = await fetch(`${API_URL}/contact-leads`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });
    
    if (!response.ok) {
      throw new Error('Error al enviar formulario');
    }
    
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
```

```javascript
// 2. Obtener servicios
async function getServices() {
  try {
    const response = await fetch(`${API_URL}/services`);
    
    if (!response.ok) {
      throw new Error('Error al obtener servicios');
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error:', error);
    throw error;
  }
}

// Uso:
getServices()
  .then(services => {
    console.log('Servicios disponibles:', services);
    // Renderizar servicios en la página
  })
  .catch(error => console.error('Error:', error));
```

```javascript
// 3. Login y obtener token
async function login(email, password) {
  try {
    const response = await fetch(`${API_URL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email, password })
    });
    
    if (!response.ok) {
      throw new Error('Credenciales inválidas');
    }
    
    const data = await response.json();
    
    // Guardar token
    localStorage.setItem('token', data.token);
    localStorage.setItem('user', JSON.stringify(data.user));
    
    return data;
  } catch (error) {
    console.error('Error en login:', error);
    throw error;
  }
}

// Uso:
login('admin@gauchosguemes.com', 'Admin123!')
  .then(data => {
    console.log('Login exitoso:', data.user);
    // Redirigir al dashboard
  })
  .catch(error => alert('Error al iniciar sesión'));
```

```javascript
// 4. Usar token en peticiones protegidas
async function getBookings() {
  const token = localStorage.getItem('token');
  
  if (!token) {
    throw new Error('No hay sesión activa');
  }
  
  try {
    const response = await fetch(`${API_URL}/reservas`, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (response.status === 401) {
      // Token expirado o inválido
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      throw new Error('Sesión expirada');
    }
    
    if (!response.ok) {
      throw new Error('Error al obtener reservas');
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error:', error);
    throw error;
  }
}

// 5. Logout
function logout() {
  localStorage.removeItem('token');
  localStorage.removeItem('user');
  // Redirigir a login
}
```

### React / Axios

```javascript
import axios from 'axios';

// Crear instancia de axios
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'https://gauchos-backend.onrender.com/api',
  headers: {
    'Content-Type': 'application/json'
  }
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
      localStorage.removeItem('user');
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
  resetPassword: (token, password) => api.post('/auth/reset-password', { token, password }),
  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  }
};

export const bookingsAPI = {
  getAll: () => api.get('/reservas'),
  getById: (id) => api.get(`/reservas/${id}`),
  create: (data) => api.post('/reservas', data),
  update: (id, data) => api.put(`/reservas/${id}`, data),
  delete: (id) => api.delete(`/reservas/${id}`),
  getStatuses: () => api.get('/reservas/statuses')
};

// Ejemplo de uso en componente React
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

---

## 🔒 Autenticación

### Token JWT

Todos los endpoints protegidos requieren un token JWT en el header:

```
Authorization: Bearer {tu_token_aqui}
```

### Flujo de autenticación

1. **Login:** `POST /api/auth/login` → Obtienes token y datos de usuario
2. **Guardar token:** En `localStorage` o `sessionStorage`
3. **Usar token:** En cada petición protegida mediante header `Authorization`
4. **Verificar token:** `GET /api/auth/verify` para validar que sigue activo
5. **Logout:** Eliminar token del storage local

### Tiempo de expiración

- **Token JWT:** 24 horas
- **Token de reset de contraseña:** 1 hora

---

## ⚠️ Manejo de Errores

### Códigos de respuesta HTTP

- `200` - OK (éxito)
- `201` - Created (creado exitosamente)
- `400` - Bad Request (datos inválidos o faltantes)
- `401` - Unauthorized (no autenticado o token inválido)
- `403` - Forbidden (no tienes permisos)
- `404` - Not Found (recurso no encontrado)
- `500` - Internal Server Error (error del servidor)

### Formato de errores

```json
{
  "error": "Descripción del error"
}
```

### Ejemplo de manejo de errores

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
  // Mostrar mensaje al usuario
  alert(`Error: ${error.message}`);
}
```

---

## 🚀 Deployment

### Frontend en Vercel

1. **Agregar variable de entorno:**
   ```
   VITE_API_URL=https://gauchos-backend.onrender.com/api
   ```

2. **Build y deploy:**
   ```bash
   npm run build
   vercel --prod
   ```

3. **Contactar al administrador** para agregar tu dominio al CORS

### Frontend en Netlify

1. **Site settings** → **Build & deploy** → **Environment**

2. **Agregar variable:**
   ```
   VITE_API_URL=https://gauchos-backend.onrender.com/api
   ```

3. **Deploy:**
   ```bash
   npm run build
   netlify deploy --prod
   ```

---

## 📞 Soporte

Para agregar nuevos dominios al CORS o consultas sobre la API:

- **Administrador:** Diego Bruno
- **Backend URL:** https://gauchos-backend.onrender.com
- **Panel de Gestión:** https://gestionreservas-gauchosguemes.onrender.com

---

## 📝 Notas Importantes

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
9. ✅ El backend está configurado con CORS para múltiples orígenes

---

## 🔄 Changelog

### Versión 1.0 - 5 de noviembre de 2025
- ✅ Sistema de autenticación JWT completo
- ✅ Recuperación de contraseñas por email
- ✅ CRUD completo para todas las entidades
- ✅ Relación many-to-many entre Bookings y Services
- ✅ Validación de estados de reserva
- ✅ Sistema de email con Flask-Mail
- ✅ Migración a PostgreSQL (compatible con SQLite)
- ✅ Desplegado en Render
- ✅ CORS configurado para múltiples dominios

---

**Versión:** 1.0  
**Última actualización:** 5 de noviembre de 2025  
**Base de datos:** PostgreSQL  
**Hosting:** Render

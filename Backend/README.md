# GauchosDeGuemes Backend API

Este proyecto es el backend en Flask para la gestión de usuarios, clientes, servicios, venues, bookings, imágenes de galería, leads de contacto y logs de auditoría.

## Endpoints principales

Todos los endpoints aceptan y devuelven datos en formato JSON.

### Usuarios
- `GET /users` — Listar usuarios
- `POST /users` — Crear usuario `{ "username": "Juan", "email": "juan@mail.com" }`
- `GET /users/<id>` — Obtener usuario
- `PUT /users/<id>` — Actualizar usuario
- `DELETE /users/<id>` — Eliminar usuario

### Clientes
- `GET /clients`
- `POST /clients` `{ "name": "Cliente", "email": "cliente@mail.com" }`
- `GET /clients/<id>`
- `PUT /clients/<id>`
- `DELETE /clients/<id>`

### Servicios
- `GET /services`
- `POST /services` `{ "name": "Servicio", "type": "TipoA", "details": "Detalles" }`
- `GET /services/<id>`
- `PUT /services/<id>`
- `DELETE /services/<id>`

### Venues
- `GET /venues`
- `POST /venues` `{ "name": "Salon", "address": "Calle 123" }`
- `GET /venues/<id>`
- `PUT /venues/<id>`
- `DELETE /venues/<id>`

### Bookings
- `GET /bookings`
- `POST /bookings` `{ "client_id": 1, "service_id": 1, "venue_id": 1, "date": "2025-12-01T00:00:00", "status": "pendiente" }`
- `GET /bookings/<id>`
- `PUT /bookings/<id>`
- `DELETE /bookings/<id>`

### Imágenes de galería
- `GET /gallery-images`
- `POST /gallery-images` `{ "venue_id": 1, "url": "https://picsum.photos/201", "description": "Foto" }`
- `GET /gallery-images/<id>`
- `PUT /gallery-images/<id>`
- `DELETE /gallery-images/<id>`

### Leads de contacto
- `GET /contact-leads`
- `POST /contact-leads` `{ "name": "Ana", "email": "ana@mail.com", "message": "Consulta", "lead_metadata": "web" }`
- `GET /contact-leads/<id>`
- `PUT /contact-leads/<id>`
- `DELETE /contact-leads/<id>`

### Logs de auditoría
- `GET /audit-logs`
- `POST /audit-logs` `{ "action": "create_user", "user_id": 1, "details": "Usuario creado", "timestamp": "2025-09-12T00:00:00" }`
- `GET /audit-logs/<id>`
- `PUT /audit-logs/<id>`
- `DELETE /audit-logs/<id>`

## Ejemplo de uso

Para crear un usuario desde el frontendd:
```js
fetch('http://localhost:5000/users', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ username: 'Juan', email: 'juan@mail.com' })
})
```

## Notas
- Todos los endpoints devuelven errores en formato `{ "error": "mensaje" }` y el código HTTP correspondiente.
- Los IDs son enteros.
- El backend corre en `http://localhost:5000` por defecto.

## Contacto
Para dudas técnicas, consulta con el equipo de backend.

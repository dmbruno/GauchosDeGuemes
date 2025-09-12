"""
Tests para la ruta /bookings
"""
import pytest
from app import app, db
from models.booking import Booking
from models.client import Client
from models.service import Service
from models.venue import Venue
from flask import json
from datetime import datetime

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.drop_all()
            db.create_all()
            c = Client(name="ClienteTest", email="ctest@example.com")
            s = Service(name="ServicioTest", type="TipoA", details="Detalles")
            v = Venue(name="SalonTest", address="Calle 123")
            db.session.add_all([c, s, v])
            db.session.commit()
            b = Booking(client_id=c.id, service_id=s.id, venue_id=v.id, date=datetime(2025, 10, 1), status="confirmado")
            db.session.add(b)
            db.session.commit()
        yield client

def test_list_bookings(client):
    response = client.get('/bookings')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert any(b['status'] == 'confirmado' for b in data)

def test_create_booking(client):
    # Se necesita crear entidades relacionadas primero
    with app.app_context():
        c = Client(name="ClienteNuevo", email="nuevo@cliente.com")
        s = Service(name="ServicioNuevo", type="TipoB", details="Detalles nuevos")
        v = Venue(name="SalonNuevo", address="Av. Siempre Viva 742")
        db.session.add_all([c, s, v])
        db.session.commit()
        payload = {"client_id": c.id, "service_id": s.id, "venue_id": v.id, "date": "2025-12-01T00:00:00", "status": "pendiente"}
    response = client.post('/bookings', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data['status'] == "pendiente"

def test_update_booking(client):
    with app.app_context():
        c = Client(name="ClienteNuevo", email="nuevo@cliente.com")
        s = Service(name="ServicioNuevo", type="TipoB", details="Detalles nuevos")
        v = Venue(name="SalonNuevo", address="Av. Siempre Viva 742")
        db.session.add_all([c, s, v])
        db.session.commit()
        payload = {"client_id": c.id, "service_id": s.id, "venue_id": v.id, "date": "2025-12-01T00:00:00", "status": "pendiente"}
    response = client.post('/bookings', json=payload)
    booking_id = response.get_json()["id"]
    response = client.put(f'/bookings/{booking_id}', json={"status": "confirmado"})
    assert response.status_code == 200
    assert response.get_json()["status"] == "confirmado"

def test_delete_booking(client):
    with app.app_context():
        c = Client(name="ClienteNuevo", email="nuevo@cliente.com")
        s = Service(name="ServicioNuevo", type="TipoB", details="Detalles nuevos")
        v = Venue(name="SalonNuevo", address="Av. Siempre Viva 742")
        db.session.add_all([c, s, v])
        db.session.commit()
        payload = {"client_id": c.id, "service_id": s.id, "venue_id": v.id, "date": "2025-12-01T00:00:00", "status": "pendiente"}
    response = client.post('/bookings', json=payload)
    booking_id = response.get_json()["id"]
    response = client.delete(f'/bookings/{booking_id}')
    assert response.status_code == 204

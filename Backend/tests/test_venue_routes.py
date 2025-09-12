"""
Tests para la ruta /venues
"""
import pytest
from app import app, db
from models.venue import Venue
from flask import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.drop_all()
            db.create_all()
            v = Venue(name="SalonTest", address="Calle 123")
            db.session.add(v)
            db.session.commit()
        yield client

def test_list_venues(client):
    response = client.get('/venues')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert any(v['name'] == 'SalonTest' for v in data)

def test_create_venue(client):
    payload = {"name": "NuevoSalon", "address": "Av. Siempre Viva 742"}
    response = client.post('/venues', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data['name'] == "NuevoSalon"
    assert data['address'] == "Av. Siempre Viva 742"

def test_update_venue(client):
    response = client.post('/venues', json={"name": "Salon", "address": "Calle 123"})
    venue_id = response.get_json()["id"]
    response = client.put(f'/venues/{venue_id}', json={"name": "Salon Actualizado"})
    assert response.status_code == 200
    assert response.get_json()["name"] == "Salon Actualizado"

def test_delete_venue(client):
    response = client.post('/venues', json={"name": "Salon", "address": "Calle 123"})
    venue_id = response.get_json()["id"]
    response = client.delete(f'/venues/{venue_id}')
    assert response.status_code == 204

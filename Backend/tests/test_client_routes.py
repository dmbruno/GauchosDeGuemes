"""
Tests para la ruta /clients
"""
import pytest
from app import app, db
from models.client import Client
from flask import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.drop_all()
            db.create_all()
            c = Client(name="ClienteTest", email="ctest@example.com")
            db.session.add(c)
            db.session.commit()
        yield client

def test_create_client(client):
    payload = {
        "name": "Cliente Test",
        "email": "test@mail.com",
        "phone": "+5491112345678"
    }
    response = client.post('/clients', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Cliente Test"
    assert data["email"] == "test@mail.com"
    assert data["phone"] == "+5491112345678"

def test_list_clients(client):
    client.post('/clients', json={
        "name": "Cliente Test",
        "email": "test@mail.com",
        "phone": "+5491112345678"
    })
    response = client.get('/clients')
    assert response.status_code == 200
    data = response.get_json()
    assert any(c["phone"] == "+5491112345678" for c in data)

def test_update_client(client):
    response = client.post('/clients', json={"name": "Cliente", "email": "cliente@mail.com"})
    client_id = response.get_json()["id"]
    response = client.put(f'/clients/{client_id}', json={"name": "Cliente Actualizado"})
    assert response.status_code == 200
    assert response.get_json()["name"] == "Cliente Actualizado"

def test_delete_client(client):
    response = client.post('/clients', json={"name": "Cliente", "email": "cliente@mail.com"})
    client_id = response.get_json()["id"]
    response = client.delete(f'/clients/{client_id}')
    assert response.status_code == 204

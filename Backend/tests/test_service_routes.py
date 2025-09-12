"""
Tests para la ruta /services
"""
import pytest
from app import app, db
from models.service import Service
from flask import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.drop_all()
            db.create_all()
            s = Service(name="ServicioTest", type="TipoA", details="Detalles")
            db.session.add(s)
            db.session.commit()
        yield client

def test_list_services(client):
    response = client.get('/services')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert any(s['name'] == 'ServicioTest' for s in data)

def test_create_service(client):
    payload = {"name": "NuevoServicio", "type": "TipoB", "details": "Detalles nuevos"}
    response = client.post('/services', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data['name'] == "NuevoServicio"
    assert data['type'] == "TipoB"

def test_update_service(client):
    response = client.post('/services', json={"name": "Servicio", "type": "TipoA", "details": "Detalles"})
    service_id = response.get_json()["id"]
    response = client.put(f'/services/{service_id}', json={"name": "Servicio Actualizado"})
    assert response.status_code == 200
    assert response.get_json()["name"] == "Servicio Actualizado"

def test_delete_service(client):
    response = client.post('/services', json={"name": "Servicio", "type": "TipoA", "details": "Detalles"})
    service_id = response.get_json()["id"]
    response = client.delete(f'/services/{service_id}')
    assert response.status_code == 204

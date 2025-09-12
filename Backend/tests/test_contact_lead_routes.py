"""
Tests para la ruta /contact_leads
"""
import pytest
from app import app, db
from models.contact_lead import ContactLead
from flask import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.drop_all()
            db.create_all()
            lead = ContactLead(name="Pedro", email="pedro@mail.com", message="Test", lead_metadata="web")
            db.session.add(lead)
            db.session.commit()
        yield client

def test_list_contact_leads(client):
    response = client.get('/contact-leads')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert any(l['name'] == 'Pedro' for l in data)

def test_create_contact_lead(client):
    payload = {"name": "Ana", "email": "ana@mail.com", "message": "Consulta", "lead_metadata": "web"}
    response = client.post('/contact-leads', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data['name'] == "Ana"
    assert data['email'] == "ana@mail.com"

def test_update_contact_lead(client):
    response = client.post('/contact-leads', json={"name": "Ana", "email": "ana@mail.com", "message": "Consulta", "lead_metadata": "web"})
    lead_id = response.get_json()["id"]
    response = client.put(f'/contact-leads/{lead_id}', json={"message": "Nueva consulta"})
    assert response.status_code == 200
    assert response.get_json()["message"] == "Nueva consulta"

def test_delete_contact_lead(client):
    response = client.post('/contact-leads', json={"name": "Ana", "email": "ana@mail.com", "message": "Consulta", "lead_metadata": "web"})
    lead_id = response.get_json()["id"]
    response = client.delete(f'/contact-leads/{lead_id}')
    assert response.status_code == 204

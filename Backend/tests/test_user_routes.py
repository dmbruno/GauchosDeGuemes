"""
Tests para la ruta /users
"""
import pytest
from app import app, db
from models.user import User
from flask import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.drop_all()
            db.create_all()
            user = User(username="testuser", email="test@example.com", is_admin=False)
            db.session.add(user)
            db.session.commit()
        yield client

def test_list_users(client):
    response = client.get('/users')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert any(u['username'] == 'testuser' for u in data)

def test_create_user(client):
    payload = {"username": "nuevo", "email": "nuevo@example.com", "is_admin": False}
    response = client.post('/users', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data['username'] == "nuevo"
    assert data['email'] == "nuevo@example.com"

def test_update_user(client):
    response = client.post('/users', json={"username": "Juan", "email": "juan@mail.com"})
    user_id = response.get_json()["id"]
    response = client.put(f'/users/{user_id}', json={"username": "JuanActualizado"})
    assert response.status_code == 200
    assert response.get_json()["username"] == "JuanActualizado"

def test_delete_user(client):
    response = client.post('/users', json={"username": "Juan", "email": "juan@mail.com"})
    user_id = response.get_json()["id"]
    response = client.delete(f'/users/{user_id}')
    assert response.status_code == 204

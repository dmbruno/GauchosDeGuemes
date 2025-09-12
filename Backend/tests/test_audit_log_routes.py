"""
Tests para la ruta /audit_logs
"""
import pytest
from app import app, db
from models.audit_log import AuditLog
from flask import json
from datetime import datetime

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.drop_all()
            db.create_all()
            log = AuditLog(action="create_user", user_id=1, details="Usuario creado", timestamp=datetime.utcnow())
            db.session.add(log)
            db.session.commit()
        yield client

def test_list_audit_logs(client):
    response = client.get('/audit-logs')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert any(l['action'] == 'create_user' for l in data)

def test_create_audit_log(client):
    payload = {"action": "create_booking", "user_id": 2, "details": "Reserva creada", "timestamp": "2025-09-12T00:00:00"}
    response = client.post('/audit-logs', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data['action'] == "create_booking"
    assert data['user_id'] == 2

def test_update_audit_log(client):
    with app.app_context():
        log = AuditLog(action="create_user", user_id=1, details="Usuario creado")
        db.session.add(log)
        db.session.commit()
    response = client.post('/audit-logs', json={"action": "create_user", "user_id": 1, "details": "Usuario creado", "timestamp": "2025-09-12T00:00:00"})
    log_id = response.get_json()["id"]
    response = client.put(f'/audit-logs/{log_id}', json={"details": "Usuario actualizado"})
    assert response.status_code == 200
    assert response.get_json()["details"] == "Usuario actualizado"

def test_delete_audit_log(client):
    with app.app_context():
        log = AuditLog(action="create_user", user_id=1, details="Usuario creado")
        db.session.add(log)
        db.session.commit()
    response = client.post('/audit-logs', json={"action": "create_user", "user_id": 1, "details": "Usuario creado", "timestamp": "2025-09-12T00:00:00"})
    log_id = response.get_json()["id"]
    response = client.delete(f'/audit-logs/{log_id}')
    assert response.status_code == 204

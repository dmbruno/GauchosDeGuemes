"""
Tests para la ruta /gallery_images
"""
import pytest
from app import app, db
from models.gallery_image import GalleryImage
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
            img = GalleryImage(venue_id=v.id, url="https://picsum.photos/200", description="Foto test")
            db.session.add(img)
            db.session.commit()
        yield client

def test_list_gallery_images(client):
    response = client.get('/gallery-images')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

def test_create_gallery_image(client):
    with app.app_context():
        v = Venue(name="SalonNuevo", address="Av. Siempre Viva 742")
        db.session.add(v)
        db.session.commit()
        payload = {"venue_id": v.id, "url": "https://picsum.photos/201", "description": "Foto nueva"}
    response = client.post('/gallery-images', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data['url'] == "https://picsum.photos/201"

def test_update_gallery_image(client):
    with app.app_context():
        v = Venue(name="SalonNuevo", address="Av. Siempre Viva 742")
        db.session.add(v)
        db.session.commit()
        payload = {"venue_id": v.id, "url": "https://picsum.photos/201", "description": "Foto original"}
    response = client.post('/gallery-images', json=payload)
    img_id = response.get_json()["id"]

    update_payload = {"description": "Foto actualizada"}
    response = client.put(f'/gallery-images/{img_id}', json=update_payload)
    assert response.status_code == 200
    assert response.get_json()["description"] == "Foto actualizada"

def test_delete_gallery_image(client):
    with app.app_context():
        v = Venue(name="SalonNuevo", address="Av. Siempre Viva 742")
        db.session.add(v)
        db.session.commit()
        payload = {"venue_id": v.id, "url": "https://picsum.photos/201", "description": "Foto a eliminar"}
    response = client.post('/gallery-images', json=payload)
    img_id = response.get_json()["id"]
    response = client.delete(f'/gallery-images/{img_id}')
    assert response.status_code == 204

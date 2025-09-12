"""
CRUD endpoints for GalleryImage entity.
"""
from flask import Blueprint, request, jsonify
from models.gallery_image import GalleryImage, GalleryImageSchema
from extensions import db

gallery_image_bp = Blueprint('gallery_image_bp', __name__)
gallery_image_schema = GalleryImageSchema()
gallery_images_schema = GalleryImageSchema(many=True)

@gallery_image_bp.route('/gallery-images', methods=['POST'])
def create_gallery_image():
    data = request.get_json()
    gallery_image = gallery_image_schema.load(data, session=db.session)
    db.session.add(gallery_image)
    db.session.commit()
    return jsonify(gallery_image_schema.dump(gallery_image)), 201

@gallery_image_bp.route('/gallery-images', methods=['GET'])
def list_gallery_images():
    images = db.session.query(GalleryImage).all()
    return jsonify(gallery_images_schema.dump(images))

@gallery_image_bp.route('/gallery-images/<int:image_id>', methods=['GET'])
def get_gallery_image(image_id):
    image = db.session.get(GalleryImage, image_id)
    if not image:
        return jsonify({'error': 'GalleryImage not found'}), 404
    return jsonify(gallery_image_schema.dump(image))

@gallery_image_bp.route('/gallery-images/<int:image_id>', methods=['PUT'])
def update_gallery_image(image_id):
    image = db.session.get(GalleryImage, image_id)
    if not image:
        return jsonify({'error': 'GalleryImage not found'}), 404
    data = request.get_json()
    image = gallery_image_schema.load(data, instance=image, session=db.session, partial=True)
    db.session.commit()
    return jsonify(gallery_image_schema.dump(image))

@gallery_image_bp.route('/gallery-images/<int:image_id>', methods=['DELETE'])
def delete_gallery_image(image_id):
    image = db.session.get(GalleryImage, image_id)
    if not image:
        return jsonify({'error': 'GalleryImage not found'}), 404
    db.session.delete(image)
    db.session.commit()
    return '', 204

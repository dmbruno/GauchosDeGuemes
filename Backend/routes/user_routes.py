"""
CRUD endpoints for User entity.
"""
from flask import Blueprint, request, jsonify
from models.user import User, UserSchema
from extensions import db

user_bp = Blueprint('user_bp', __name__)
user_schema = UserSchema()
users_schema = UserSchema(many=True)

@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = user_schema.load(data, session=db.session)
    db.session.add(user)
    db.session.commit()
    return jsonify(user_schema.dump(user)), 201

@user_bp.route('/users', methods=['GET'])
def list_users():
    users = db.session.query(User).all()
    return jsonify(users_schema.dump(users))

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user_schema.dump(user))

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    data = request.get_json()
    user = user_schema.load(data, instance=user, session=db.session, partial=True)
    db.session.commit()
    return jsonify(user_schema.dump(user))

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return '', 204

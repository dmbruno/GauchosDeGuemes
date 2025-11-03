"""
CRUD endpoints for User entity.
"""
from flask import Blueprint, request, jsonify
from models.user import User, UserSchema
from extensions import db
from datetime import datetime

user_bp = Blueprint('user_bp', __name__)
user_schema = UserSchema()
users_schema = UserSchema(many=True)

@user_bp.route('/users', methods=['POST'])
def create_user():
    """Crear nuevo usuario con validaciones"""
    data = request.get_json()
    
    # Validar campos requeridos
    required_fields = ['username', 'email', 'password']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field} es requerido'}), 400
    
    # Verificar username único
    if db.session.query(User).filter_by(username=data['username']).first():
        return jsonify({'error': 'El username ya está en uso'}), 400
    
    # Verificar email único
    if db.session.query(User).filter_by(email=data['email']).first():
        return jsonify({'error': 'El email ya está registrado'}), 400
    
    try:
        # Crear usuario
        user = User(
            username=data['username'],
            email=data['email'],
            is_admin=data.get('is_admin', False),
            created_at=datetime.utcnow()
        )
        
        # Hashear password
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify(user_schema.dump(user)), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al crear usuario: {str(e)}'}), 500

@user_bp.route('/users', methods=['GET'])
def list_users():
    """Listar todos los usuarios"""
    users = db.session.query(User).all()
    return jsonify(users_schema.dump(users))

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Obtener usuario por ID"""
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    return jsonify(user_schema.dump(user))

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Actualizar usuario existente"""
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    
    data = request.get_json()
    
    try:
        # Actualizar username si cambió
        if 'username' in data and data['username'] != user.username:
            if db.session.query(User).filter_by(username=data['username']).first():
                return jsonify({'error': 'El username ya está en uso'}), 400
            user.username = data['username']
        
        # Actualizar email si cambió
        if 'email' in data and data['email'] != user.email:
            if db.session.query(User).filter_by(email=data['email']).first():
                return jsonify({'error': 'El email ya está registrado'}), 400
            user.email = data['email']
        
        # Actualizar rol admin
        if 'is_admin' in data:
            user.is_admin = bool(data['is_admin'])
        
        # Actualizar password solo si se proporciona
        if 'password' in data and data['password']:
            user.set_password(data['password'])
        
        db.session.commit()
        return jsonify(user_schema.dump(user)), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al actualizar usuario: {str(e)}'}), 500

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Eliminar usuario"""
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'Usuario eliminado exitosamente'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al eliminar usuario: {str(e)}'}), 500

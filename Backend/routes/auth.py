"""
Authentication endpoints with JWT.
"""
from flask import Blueprint, request, jsonify
from models.user import User, UserSchema
from extensions import db, mail
from flask_mail import Message
import jwt
import os
from datetime import datetime, timedelta
from functools import wraps
import secrets

auth_bp = Blueprint('auth_bp', __name__)
user_schema = UserSchema()

SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')

# Decorador para proteger rutas
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'Token es requerido'}), 401
        
        try:
            # Remover 'Bearer ' si está presente
            if token.startswith('Bearer '):
                token = token[7:]
            
            # Decodificar token
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            current_user = db.session.get(User, data['user_id'])
            
            if not current_user:
                return jsonify({'error': 'Usuario no encontrado'}), 401
                
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token inválido'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated

@auth_bp.route('/auth/register', methods=['POST'])
def register():
    """Registrar nuevo usuario"""
    data = request.get_json()
    
    # Validar campos requeridos
    if not data.get('email') or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Email, username y password son requeridos'}), 400
    
    # Verificar si el usuario ya existe
    if db.session.query(User).filter_by(email=data['email']).first():
        return jsonify({'error': 'Email ya registrado'}), 400
    
    if db.session.query(User).filter_by(username=data['username']).first():
        return jsonify({'error': 'Username ya registrado'}), 400
    
    # Crear nuevo usuario
    user = User(
        username=data['username'],
        email=data['email'],
        is_admin=data.get('is_admin', False)
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    # Generar token JWT
    token = jwt.encode(
        {
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(hours=24)
        },
        SECRET_KEY,
        algorithm='HS256'
    )
    
    return jsonify({
        'token': token,
        'user': user_schema.dump(user)
    }), 201

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    """Iniciar sesión"""
    data = request.get_json()
    
    # Validar campos requeridos
    if not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email y password son requeridos'}), 400
    
    # Buscar usuario
    user = db.session.query(User).filter_by(email=data['email']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Credenciales inválidas'}), 401
    
    # Generar token JWT
    token = jwt.encode(
        {
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(hours=24)
        },
        SECRET_KEY,
        algorithm='HS256'
    )
    
    return jsonify({
        'token': token,
        'user': user_schema.dump(user)
    }), 200

@auth_bp.route('/auth/verify', methods=['GET'])
@token_required
def verify_token(current_user):
    """Verificar si el token es válido"""
    return jsonify({
        'valid': True,
        'user': user_schema.dump(current_user)
    }), 200

@auth_bp.route('/auth/forgot-password', methods=['POST'])
def forgot_password():
    """Solicitar recuperación de contraseña"""
    data = request.get_json()
    
    if not data.get('email'):
        return jsonify({'error': 'Email es requerido'}), 400
    
    user = db.session.query(User).filter_by(email=data['email']).first()
    
    # Mensaje genérico por seguridad (no revelar si el email existe)
    if user:
        # Generar token de recuperación
        reset_token = secrets.token_urlsafe(32)
        user.reset_token = reset_token
        user.reset_token_expires = datetime.utcnow() + timedelta(hours=1)
        db.session.commit()
        
        # Enviar email de recuperación
        try:
            frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:5173')
            reset_link = f"{frontend_url}/reset-password?token={reset_token}"
            
            msg = Message(
                subject='Recuperación de Contraseña - Gauchos De Güemes',
                recipients=[user.email],
                html=f"""
                <html>
                    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                            <h2 style="color: #2c3e50;">Recuperación de Contraseña</h2>
                            <p>Hola <strong>{user.username}</strong>,</p>
                            <p>Recibimos una solicitud para restablecer la contraseña de tu cuenta en Gauchos De Güemes.</p>
                            <p>Haz clic en el siguiente botón para crear una nueva contraseña:</p>
                            <div style="text-align: center; margin: 30px 0;">
                                <a href="{reset_link}" 
                                   style="background-color: #3498db; 
                                          color: white; 
                                          padding: 12px 30px; 
                                          text-decoration: none; 
                                          border-radius: 5px;
                                          display: inline-block;">
                                    Restablecer Contraseña
                                </a>
                            </div>
                            <p>O copia y pega este enlace en tu navegador:</p>
                            <p style="background-color: #f4f4f4; padding: 10px; word-break: break-all;">
                                {reset_link}
                            </p>
                            <p><strong>Este enlace expirará en 1 hora.</strong></p>
                            <p>Si no solicitaste este cambio, puedes ignorar este correo de forma segura.</p>
                            <hr style="margin-top: 30px; border: none; border-top: 1px solid #ddd;">
                            <p style="font-size: 12px; color: #777;">
                                © 2025 Gauchos De Güemes. Todos los derechos reservados.
                            </p>
                        </div>
                    </body>
                </html>
                """
            )
            
            mail.send(msg)
            
        except Exception as e:
            # Log del error (en producción usar un logger apropiado)
            print(f"Error al enviar email: {str(e)}")
            # No retornar error para no revelar si el email existe
    
    return jsonify({
        'message': 'Si el email existe, recibirás instrucciones para resetear tu contraseña'
    }), 200

@auth_bp.route('/auth/reset-password', methods=['POST'])
def reset_password():
    """Resetear contraseña con token"""
    data = request.get_json()
    
    if not data.get('token') or not data.get('password'):
        return jsonify({'error': 'Token y password son requeridos'}), 400
    
    # Buscar usuario con el token válido
    user = db.session.query(User).filter_by(reset_token=data['token']).first()
    
    if not user:
        return jsonify({'error': 'Token inválido'}), 400
    
    # Verificar si el token expiró
    if user.reset_token_expires < datetime.utcnow():
        return jsonify({'error': 'Token expirado'}), 400
    
    # Actualizar contraseña
    user.set_password(data['password'])
    user.reset_token = None
    user.reset_token_expires = None
    db.session.commit()
    
    return jsonify({'message': 'Contraseña actualizada exitosamente'}), 200

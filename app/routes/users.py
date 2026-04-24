from flask import Blueprint, request
from app.models import User
from app.utils.validators import validate_user_data
from app.utils.responses import success_response, error_response
from app.database import db

bp = Blueprint('users', __name__, url_prefix='/api/users')

# Constants
USER_NOT_FOUND = 'Usuario no encontrado'


@bp.route('', methods=['GET'])
def get_users():
    """Obtiene todos los usuarios"""
    users = User.get_all()
    return success_response(
        data=[user.to_dict() for user in users],
        count=len(users)
    )


@bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Obtiene un usuario específico por ID"""
    user = User.get_by_id(user_id)
    
    if not user:
        return error_response(USER_NOT_FOUND, 404)
    
    return success_response(data=user.to_dict())


@bp.route('', methods=['POST'])
def create_user():
    """Crea un nuevo usuario"""
    data = request.get_json()
    
    # Validar datos
    is_valid, error_message = validate_user_data(data)
    if not is_valid:
        return error_response(error_message, 400)
    
    # Verificar si el email ya existe
    if User.exists_email(data['email']):
        return error_response('El email ya está registrado', 400)
    
    # Crear y guardar usuario
    try:
        user = User(
            name=data['name'],
            email=data['email']
        )
        user.save()
        
        return success_response(
            data=user.to_dict(),
            message='Usuario creado exitosamente',
            status_code=201
        )
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error al crear usuario: {str(e)}', 500)


@bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Actualiza un usuario existente"""
    user = User.get_by_id(user_id)
    
    if not user:
        return error_response(USER_NOT_FOUND, 404)
    
    data = request.get_json()
    
    if not data:
        return error_response('No se proporcionaron datos para actualizar', 400)
    
    try:
        # Actualizar usuario
        user.update(**data)
        
        return success_response(
            data=user.to_dict(),
            message='Usuario actualizado exitosamente'
        )
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error al actualizar usuario: {str(e)}', 500)


@bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Elimina un usuario"""
    user = User.get_by_id(user_id)
    
    if not user:
        return error_response(USER_NOT_FOUND, 404)
    
    try:
        user_data = user.to_dict()
        user.delete()
        
        return success_response(
            data=user_data,
            message='Usuario eliminado exitosamente'
        )
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error al eliminar usuario: {str(e)}', 500)

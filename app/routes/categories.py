from flask import Blueprint, request
from app.models import Category
from app.utils.responses import success_response, error_response
from app.database import db

bp = Blueprint('categories', __name__, url_prefix='/api/categories')


@bp.route('', methods=['GET'])
def get_categories():
    """Obtiene todas las categorías"""
    categories = Category.get_all()
    return success_response(
        data=[category.to_dict() for category in categories],
        count=len(categories)
    )


@bp.route('/<int:category_id>', methods=['GET'])
def get_category(category_id):
    """Obtiene una categoría específica por ID"""
    category = Category.get_by_id(category_id)
    
    if not category:
        return error_response('Categoría no encontrada', 404)
    
    return success_response(data=category.to_dict())


@bp.route('', methods=['POST'])
def create_category():
    """Crea una nueva categoría"""
    data = request.get_json()
    
    if not data or 'name' not in data:
        return error_response('El campo name es requerido', 400)
    
    # Verificar si ya existe
    if Category.get_by_name(data['name']):
        return error_response('La categoría ya existe', 400)
    
    try:
        category = Category(
            name=data['name'],
            description=data.get('description', '')
        )
        category.save()
        
        return success_response(
            data=category.to_dict(),
            message='Categoría creada exitosamente',
            status_code=201
        )
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error al crear categoría: {str(e)}', 500)


@bp.route('/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    """Elimina una categoría"""
    category = Category.get_by_id(category_id)
    
    if not category:
        return error_response('Categoría no encontrada', 404)
    
    try:
        category_data = category.to_dict()
        category.delete()
        
        return success_response(
            data=category_data,
            message='Categoría eliminada exitosamente'
        )
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error al eliminar categoría: {str(e)}', 500)

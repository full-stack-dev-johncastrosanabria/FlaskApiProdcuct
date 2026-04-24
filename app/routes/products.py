from flask import Blueprint, request
from app.models import Product
from app.utils.validators import validate_product_data
from app.utils.responses import success_response, error_response
from app.database import db

bp = Blueprint('products', __name__, url_prefix='/api/products')

# Constants
PRODUCT_NOT_FOUND = 'Producto no encontrado'


@bp.route('', methods=['GET'])
def get_products():
    """Obtiene todos los productos con filtros opcionales"""
    # Obtener filtros de query params
    filters = {
        'min_price': request.args.get('min_price', type=float),
        'max_price': request.args.get('max_price', type=float),
        'category': request.args.get('category')
    }
    
    products = Product.get_all(filters=filters)
    
    return success_response(
        data=[product.to_dict() for product in products],
        count=len(products)
    )


@bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Obtiene un producto específico por ID"""
    product = Product.get_by_id(product_id)
    
    if not product:
        return error_response(PRODUCT_NOT_FOUND, 404)
    
    return success_response(data=product.to_dict())


@bp.route('', methods=['POST'])
def create_product():
    """Crea un nuevo producto"""
    data = request.get_json()
    
    # Validar datos
    is_valid, error_message = validate_product_data(data)
    if not is_valid:
        return error_response(error_message, 400)
    
    try:
        # Crear y guardar producto
        product = Product(
            name=data['name'],
            price=data['price'],
            category_id=data['category_id'],
            description=data.get('description', ''),
            stock=data.get('stock', 0)
        )
        product.save()
        
        return success_response(
            data=product.to_dict(),
            message='Producto creado exitosamente',
            status_code=201
        )
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error al crear producto: {str(e)}', 500)


@bp.route('/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """Actualiza un producto existente"""
    product = Product.get_by_id(product_id)
    
    if not product:
        return error_response(PRODUCT_NOT_FOUND, 404)
    
    data = request.get_json()
    
    if not data:
        return error_response('No se proporcionaron datos para actualizar', 400)
    
    try:
        # Actualizar producto
        product.update(**data)
        
        return success_response(
            data=product.to_dict(),
            message='Producto actualizado exitosamente'
        )
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error al actualizar producto: {str(e)}', 500)


@bp.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Elimina un producto"""
    product = Product.get_by_id(product_id)
    
    if not product:
        return error_response(PRODUCT_NOT_FOUND, 404)
    
    try:
        product_data = product.to_dict()
        product.delete()
        
        return success_response(
            data=product_data,
            message='Producto eliminado exitosamente'
        )
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error al eliminar producto: {str(e)}', 500)

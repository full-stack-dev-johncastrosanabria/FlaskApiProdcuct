from flask import Blueprint, request, jsonify
from app.models import Product
from app.utils.validators import validate_product_data
from app.utils.responses import success_response, error_response

bp = Blueprint('products', __name__, url_prefix='/api/products')


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


@bp.route('/<product_id>', methods=['GET'])
def get_product(product_id):
    """Obtiene un producto específico por ID"""
    product = Product.get_by_id(product_id)
    
    if not product:
        return error_response('Producto no encontrado', 404)
    
    return success_response(data=product.to_dict())


@bp.route('', methods=['POST'])
def create_product():
    """Crea un nuevo producto"""
    data = request.get_json()
    
    # Validar datos
    is_valid, error_message = validate_product_data(data)
    if not is_valid:
        return error_response(error_message, 400)
    
    # Crear y guardar producto
    product = Product(
        name=data['name'],
        price=data['price'],
        category=data['category'],
        description=data.get('description', ''),
        stock=data.get('stock', 0)
    )
    product.save()
    
    return success_response(
        data=product.to_dict(),
        message='Producto creado exitosamente',
        status_code=201
    )


@bp.route('/<product_id>', methods=['PUT'])
def update_product(product_id):
    """Actualiza un producto existente"""
    product = Product.get_by_id(product_id)
    
    if not product:
        return error_response('Producto no encontrado', 404)
    
    data = request.get_json()
    
    if not data:
        return error_response('No se proporcionaron datos para actualizar', 400)
    
    # Actualizar producto
    product.update(**data)
    
    return success_response(
        data=product.to_dict(),
        message='Producto actualizado exitosamente'
    )


@bp.route('/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Elimina un producto"""
    product = Product.get_by_id(product_id)
    
    if not product:
        return error_response('Producto no encontrado', 404)
    
    product_data = product.to_dict()
    product.delete()
    
    return success_response(
        data=product_data,
        message='Producto eliminado exitosamente'
    )

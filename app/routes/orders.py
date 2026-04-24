from flask import Blueprint, request
from app.models import Order, OrderItem, Product, User
from app.utils.responses import success_response, error_response
from app.database import db

bp = Blueprint('orders', __name__, url_prefix='/api/orders')


@bp.route('', methods=['GET'])
def get_orders():
    """Obtiene todas las órdenes con filtros opcionales"""
    filters = {
        'status': request.args.get('status'),
        'user_id': request.args.get('user_id', type=int)
    }
    
    orders = Order.get_all(filters=filters)
    
    return success_response(
        data=[order.to_dict() for order in orders],
        count=len(orders)
    )


@bp.route('/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Obtiene una orden específica por ID"""
    order = Order.get_by_id(order_id)
    
    if not order:
        return error_response('Orden no encontrada', 404)
    
    return success_response(data=order.to_dict())


@bp.route('', methods=['POST'])
def create_order():
    """Crea una nueva orden"""
    data = request.get_json()
    
    # Validar datos
    if not data or 'user_id' not in data or 'items' not in data:
        return error_response('Los campos user_id e items son requeridos', 400)
    
    # Verificar que el usuario existe
    user = User.get_by_id(data['user_id'])
    if not user:
        return error_response('Usuario no encontrado', 404)
    
    # Validar items
    if not data['items'] or len(data['items']) == 0:
        return error_response('La orden debe tener al menos un item', 400)
    
    try:
        # Calcular total
        total = 0
        order_items = []
        
        for item_data in data['items']:
            if 'product_id' not in item_data or 'quantity' not in item_data:
                return error_response('Cada item debe tener product_id y quantity', 400)
            
            product = Product.get_by_id(item_data['product_id'])
            if not product:
                return error_response(f'Producto {item_data["product_id"]} no encontrado', 404)
            
            if product.stock < item_data['quantity']:
                return error_response(f'Stock insuficiente para {product.name}', 400)
            
            subtotal = float(product.price) * item_data['quantity']
            total += subtotal
            
            order_items.append({
                'product': product,
                'quantity': item_data['quantity'],
                'price': product.price,
                'subtotal': subtotal
            })
        
        # Crear orden
        order = Order(
            user_id=data['user_id'],
            total=total,
            status='pending'
        )
        order.save()
        
        # Crear items de la orden y actualizar stock
        for item_info in order_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item_info['product'].id,
                quantity=item_info['quantity'],
                price=item_info['price'],
                subtotal=item_info['subtotal']
            )
            order_item.save()
            
            # Actualizar stock
            item_info['product'].update(stock=item_info['product'].stock - item_info['quantity'])
        
        return success_response(
            data=order.to_dict(),
            message='Orden creada exitosamente',
            status_code=201
        )
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error al crear orden: {str(e)}', 500)


@bp.route('/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    """Actualiza el estado de una orden"""
    order = Order.get_by_id(order_id)
    
    if not order:
        return error_response('Orden no encontrada', 404)
    
    data = request.get_json()
    
    if not data or 'status' not in data:
        return error_response('El campo status es requerido', 400)
    
    if data['status'] not in ['pending', 'completed', 'cancelled']:
        return error_response('Estado inválido', 400)
    
    try:
        order.update(status=data['status'])
        
        return success_response(
            data=order.to_dict(),
            message='Orden actualizada exitosamente'
        )
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error al actualizar orden: {str(e)}', 500)


@bp.route('/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    """Elimina una orden"""
    order = Order.get_by_id(order_id)
    
    if not order:
        return error_response('Orden no encontrada', 404)
    
    try:
        order_data = order.to_dict()
        order.delete()
        
        return success_response(
            data=order_data,
            message='Orden eliminada exitosamente'
        )
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error al eliminar orden: {str(e)}', 500)

"""
Base de conocimientos para la IA.
Contiene patrones de preguntas y respuestas basadas en datos reales.
"""
from typing import Dict, List
from datetime import datetime, timedelta, timezone
from sqlalchemy import func
from app.database import db
from app.models import Product, Order, User, Category, OrderItem


class KnowledgeBase:
    """Base de conocimientos con acceso a datos reales de la BD."""

    # Palabras clave para categorizar preguntas
    KEYWORDS = {
        'ventas': [
            'venta', 'ventas', 'ingresos', 'revenue',
            'ganancia', 'ganancias'
        ],
        'productos': [
            'producto', 'productos', 'item', 'items',
            'artículo', 'artículos'
        ],
        'clientes': [
            'cliente', 'clientes', 'usuario', 'usuarios',
            'comprador', 'compradores'
        ],
        'categorias': [
            'categoría', 'categorías', 'tipo', 'tipos',
            'clase', 'clases'
        ],
        'ordenes': [
            'orden', 'órdenes', 'pedido', 'pedidos',
            'compra', 'compras'
        ],
        'stock': [
            'stock', 'inventario', 'existencia',
            'existencias', 'disponible'
        ],
        'precio': [
            'precio', 'precios', 'costo', 'costos',
            'valor', 'valores'
        ],
        'estadisticas': [
            'estadística', 'estadísticas', 'promedio',
            'total', 'cantidad', 'cuántos'
        ],
        'tendencias': [
            'tendencia', 'tendencias', 'crecimiento',
            'aumento', 'disminución', 'cambio'
        ],
        'recomendaciones': [
            'recomendación', 'recomendaciones', 'sugerencia',
            'sugerencias', 'consejo', 'consejos'
        ]
    }

    @staticmethod
    def extract_keywords(question: str) -> List[str]:
        """Extrae palabras clave de la pregunta."""
        question_lower = question.lower()
        found_keywords = []

        for category, keywords in KnowledgeBase.KEYWORDS.items():
            for keyword in keywords:
                if keyword in question_lower:
                    found_keywords.append(category)
                    break

        return found_keywords if found_keywords else ['general']

    @staticmethod
    def get_sales_stats() -> Dict:
        """Obtiene estadísticas de ventas."""
        total_sales = db.session.query(
            func.sum(Order.total)
        ).filter(Order.status == 'completed').scalar() or 0

        total_orders = db.session.query(
            func.count(Order.id)
        ).filter(Order.status == 'completed').scalar() or 0

        avg_order = (
            float(total_sales) / total_orders
            if total_orders > 0
            else 0
        )

        today_sales = db.session.query(
            func.sum(Order.total)
        ).filter(
            Order.status == 'completed',
            func.date(Order.created_at) == datetime.now(timezone.utc).date()
        ).scalar() or 0

        return {
            'total_sales': float(total_sales),
            'total_orders': total_orders,
            'avg_order': avg_order,
            'today_sales': float(today_sales)
        }

    @staticmethod
    def get_product_stats() -> Dict:
        """Obtiene estadísticas de productos."""
        total_products = (
            db.session.query(func.count(Product.id)).scalar() or 0
        )
        total_stock = (
            db.session.query(func.sum(Product.stock)).scalar() or 0
        )

        low_stock = db.session.query(
            func.count(Product.id)
        ).filter(Product.stock <= 10).scalar() or 0

        out_of_stock = db.session.query(
            func.count(Product.id)
        ).filter(Product.stock == 0).scalar() or 0

        avg_price = db.session.query(
            func.avg(Product.price)
        ).scalar() or 0

        return {
            'total_products': total_products,
            'total_stock': total_stock,
            'low_stock': low_stock,
            'out_of_stock': out_of_stock,
            'avg_price': float(avg_price)
        }

    @staticmethod
    def get_customer_stats() -> Dict:
        """Obtiene estadísticas de clientes."""
        total_customers = (
            db.session.query(func.count(User.id)).scalar() or 0
        )

        customers_with_orders = db.session.query(
            func.count(func.distinct(Order.user_id))
        ).filter(Order.status == 'completed').scalar() or 0

        return {
            'total_customers': total_customers,
            'customers_with_orders': customers_with_orders,
            'inactive_customers': total_customers - customers_with_orders
        }

    @staticmethod
    def get_top_products(limit: int = 5) -> List[Dict]:
        """Obtiene los productos más vendidos."""
        products = db.session.query(
            Product.name,
            func.sum(OrderItem.quantity).label('total_quantity'),
            func.sum(OrderItem.subtotal).label('total_revenue')
        ).join(
            OrderItem, Product.id == OrderItem.product_id
        ).join(
            Order, OrderItem.order_id == Order.id
        ).filter(
            Order.status == 'completed'
        ).group_by(
            Product.id, Product.name
        ).order_by(
            func.sum(OrderItem.subtotal).desc()
        ).limit(limit).all()

        return [
            {
                'name': p.name,
                'quantity': p.total_quantity or 0,
                'revenue': (
                    float(p.total_revenue)
                    if p.total_revenue
                    else 0
                )
            }
            for p in products
        ]

    @staticmethod
    def get_category_stats() -> List[Dict]:
        """Obtiene estadísticas por categoría."""
        categories = db.session.query(
            Category.name,
            func.count(Product.id).label('product_count'),
            func.sum(Product.stock).label('total_stock'),
            func.sum(OrderItem.quantity).label('total_sold')
        ).outerjoin(
            Product, Category.id == Product.category_id
        ).outerjoin(
            OrderItem, Product.id == OrderItem.product_id
        ).group_by(
            Category.id, Category.name
        ).all()

        return [
            {
                'category': c.name,
                'products': c.product_count or 0,
                'stock': c.total_stock or 0,
                'sold': c.total_sold or 0
            }
            for c in categories
        ]

    @staticmethod
    def get_recommendations() -> Dict:
        """Genera recomendaciones basadas en datos."""
        recommendations = []

        # Verificar stock bajo
        low_stock_count = db.session.query(
            func.count(Product.id)
        ).filter(Product.stock <= 10).scalar() or 0

        if low_stock_count > 0:
            recommendations.append({
                'type': 'warning',
                'message': (
                    f'⚠️ Hay {low_stock_count} productos con stock bajo. '
                    f'Considera hacer un pedido.'
                )
            })

        # Verificar productos sin stock
        out_of_stock = db.session.query(
            func.count(Product.id)
        ).filter(Product.stock == 0).scalar() or 0

        if out_of_stock > 0:
            recommendations.append({
                'type': 'critical',
                'message': (
                    f'🔴 {out_of_stock} productos sin stock. '
                    f'Acción inmediata requerida.'
                )
            })

        # Productos más vendidos
        top_product = db.session.query(
            Product.name,
            func.sum(OrderItem.quantity).label('total_quantity')
        ).join(
            OrderItem, Product.id == OrderItem.product_id
        ).join(
            Order, OrderItem.order_id == Order.id
        ).filter(
            Order.status == 'completed'
        ).group_by(
            Product.id, Product.name
        ).order_by(
            func.sum(OrderItem.quantity).desc()
        ).first()

        if top_product:
            recommendations.append({
                'type': 'info',
                'message': (
                    f'📈 "{top_product.name}" es tu producto más vendido '
                    f'({top_product.total_quantity} unidades).'
                )
            })

        # Clientes inactivos
        inactive = db.session.query(
            func.count(User.id)
        ).filter(
            ~User.id.in_(
                db.session.query(func.distinct(Order.user_id)).filter(
                    Order.created_at >= (
                        datetime.now(timezone.utc) - timedelta(days=30)
                    )
                )
            )
        ).scalar() or 0

        if inactive > 0:
            recommendations.append({
                'type': 'info',
                'message': (
                    f'👥 {inactive} clientes no han comprado '
                    f'en los últimos 30 días.'
                )
            })

        return {
            'recommendations': recommendations,
            'count': len(recommendations)
        }

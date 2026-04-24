from sqlalchemy import func, desc
from app.database import db
from app.models import Order, OrderItem, Product, User, Category
from datetime import datetime, timedelta


class SalesAnalytics:
    """Clase para análisis de ventas"""
    
    @staticmethod
    def get_total_sales(start_date=None, end_date=None):
        """Obtiene el total de ventas en un período"""
        query = db.session.query(func.sum(Order.total)).filter(Order.status == 'completed')
        
        if start_date:
            query = query.filter(Order.created_at >= start_date)
        if end_date:
            query = query.filter(Order.created_at <= end_date)
        
        total = query.scalar()
        return float(total) if total else 0.0
    
    @staticmethod
    def get_sales_by_period(period='day', limit=30):
        """
        Obtiene ventas agrupadas por período
        period: 'day', 'week', 'month'
        """
        if period == 'day':
            date_format = func.date(Order.created_at)
        elif period == 'week':
            date_format = func.date_format(Order.created_at, '%Y-%U')
        else:  # month
            date_format = func.date_format(Order.created_at, '%Y-%m')
        
        results = db.session.query(
            date_format.label('period'),
            func.count(Order.id).label('order_count'),
            func.sum(Order.total).label('total_sales')
        ).filter(
            Order.status == 'completed'
        ).group_by('period').order_by(desc('period')).limit(limit).all()
        
        return [
            {
                'period': str(r.period),
                'order_count': r.order_count,
                'total_sales': float(r.total_sales) if r.total_sales else 0.0
            }
            for r in results
        ]
    
    @staticmethod
    def get_top_products(limit=10):
        """Obtiene los productos más vendidos"""
        results = db.session.query(
            Product.id,
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
            desc('total_revenue')
        ).limit(limit).all()
        
        return [
            {
                'product_id': r.id,
                'product_name': r.name,
                'total_quantity': r.total_quantity,
                'total_revenue': float(r.total_revenue) if r.total_revenue else 0.0
            }
            for r in results
        ]
    
    @staticmethod
    def get_top_customers(limit=10):
        """Obtiene los clientes con más compras"""
        results = db.session.query(
            User.id,
            User.name,
            User.email,
            func.count(Order.id).label('order_count'),
            func.sum(Order.total).label('total_spent')
        ).join(
            Order, User.id == Order.user_id
        ).filter(
            Order.status == 'completed'
        ).group_by(
            User.id, User.name, User.email
        ).order_by(
            desc('total_spent')
        ).limit(limit).all()
        
        return [
            {
                'user_id': r.id,
                'user_name': r.name,
                'user_email': r.email,
                'order_count': r.order_count,
                'total_spent': float(r.total_spent) if r.total_spent else 0.0
            }
            for r in results
        ]
    
    @staticmethod
    def get_sales_by_category():
        """Obtiene ventas por categoría"""
        results = db.session.query(
            Category.id,
            Category.name,
            func.sum(OrderItem.quantity).label('total_quantity'),
            func.sum(OrderItem.subtotal).label('total_revenue')
        ).join(
            Product, Category.id == Product.category_id
        ).join(
            OrderItem, Product.id == OrderItem.product_id
        ).join(
            Order, OrderItem.order_id == Order.id
        ).filter(
            Order.status == 'completed'
        ).group_by(
            Category.id, Category.name
        ).order_by(
            desc('total_revenue')
        ).all()
        
        return [
            {
                'category_id': r.id,
                'category_name': r.name,
                'total_quantity': r.total_quantity,
                'total_revenue': float(r.total_revenue) if r.total_revenue else 0.0
            }
            for r in results
        ]
    
    @staticmethod
    def get_dashboard_summary():
        """Obtiene un resumen para el dashboard"""
        # Total de ventas
        total_sales = SalesAnalytics.get_total_sales()
        
        # Total de órdenes
        total_orders = db.session.query(func.count(Order.id)).filter(
            Order.status == 'completed'
        ).scalar()
        
        # Total de clientes
        total_customers = db.session.query(func.count(User.id)).scalar()
        
        # Total de productos
        total_products = db.session.query(func.count(Product.id)).scalar()
        
        # Promedio de orden
        avg_order = total_sales / total_orders if total_orders > 0 else 0
        
        # Ventas del último mes
        last_month = datetime.utcnow() - timedelta(days=30)
        last_month_sales = SalesAnalytics.get_total_sales(start_date=last_month)
        
        # Órdenes pendientes
        pending_orders = db.session.query(func.count(Order.id)).filter(
            Order.status == 'pending'
        ).scalar()
        
        return {
            'total_sales': total_sales,
            'total_orders': total_orders or 0,
            'total_customers': total_customers or 0,
            'total_products': total_products or 0,
            'average_order_value': avg_order,
            'last_month_sales': last_month_sales,
            'pending_orders': pending_orders or 0
        }

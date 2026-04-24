from sqlalchemy import func
from app.database import db
from app.models import Product, Category


class InventoryAnalytics:
    """Clase para análisis de inventario"""
    
    @staticmethod
    def get_low_stock_products(threshold=10):
        """Obtiene productos con stock bajo"""
        products = Product.query.filter(Product.stock <= threshold).all()
        
        return [
            {
                'id': p.id,
                'name': p.name,
                'stock': p.stock,
                'category': p.category.name if p.category else None,
                'price': float(p.price)
            }
            for p in products
        ]
    
    @staticmethod
    def get_out_of_stock_products():
        """Obtiene productos sin stock"""
        products = Product.query.filter(Product.stock == 0).all()
        
        return [
            {
                'id': p.id,
                'name': p.name,
                'category': p.category.name if p.category else None,
                'price': float(p.price)
            }
            for p in products
        ]
    
    @staticmethod
    def get_inventory_value():
        """Calcula el valor total del inventario"""
        result = db.session.query(
            func.sum(Product.price * Product.stock)
        ).scalar()
        
        return float(result) if result else 0.0
    
    @staticmethod
    def get_inventory_by_category():
        """Obtiene inventario agrupado por categoría"""
        results = db.session.query(
            Category.id,
            Category.name,
            func.count(Product.id).label('product_count'),
            func.sum(Product.stock).label('total_stock'),
            func.sum(Product.price * Product.stock).label('total_value')
        ).join(
            Product, Category.id == Product.category_id
        ).group_by(
            Category.id, Category.name
        ).all()
        
        return [
            {
                'category_id': r.id,
                'category_name': r.name,
                'product_count': r.product_count,
                'total_stock': r.total_stock or 0,
                'total_value': float(r.total_value) if r.total_value else 0.0
            }
            for r in results
        ]
    
    @staticmethod
    def get_inventory_summary():
        """Obtiene un resumen del inventario"""
        total_products = db.session.query(func.count(Product.id)).scalar()
        total_stock = db.session.query(func.sum(Product.stock)).scalar()
        total_value = InventoryAnalytics.get_inventory_value()
        low_stock_count = db.session.query(func.count(Product.id)).filter(
            Product.stock <= 10
        ).scalar()
        out_of_stock_count = db.session.query(func.count(Product.id)).filter(
            Product.stock == 0
        ).scalar()
        
        return {
            'total_products': total_products or 0,
            'total_stock': total_stock or 0,
            'total_value': total_value,
            'low_stock_count': low_stock_count or 0,
            'out_of_stock_count': out_of_stock_count or 0
        }

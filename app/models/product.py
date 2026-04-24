from datetime import datetime
import uuid


class Product:
    """Modelo de Producto"""
    
    # Simulación de base de datos en memoria
    _products = {}
    
    def __init__(self, name, price, category, description='', stock=0, product_id=None):
        self.id = product_id or str(uuid.uuid4())
        self.name = name
        self.price = price
        self.category = category
        self.description = description
        self.stock = stock
        self.created_at = datetime.now().isoformat()
        self.updated_at = None
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'category': self.category,
            'description': self.description,
            'stock': self.stock,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    def save(self):
        """Guarda el producto en la base de datos"""
        Product._products[self.id] = self
        return self
    
    def update(self, **kwargs):
        """Actualiza los campos del producto"""
        for key, value in kwargs.items():
            if hasattr(self, key) and key not in ['id', 'created_at']:
                setattr(self, key, value)
        self.updated_at = datetime.now().isoformat()
        return self
    
    def delete(self):
        """Elimina el producto de la base de datos"""
        if self.id in Product._products:
            del Product._products[self.id]
            return True
        return False
    
    @classmethod
    def get_all(cls, filters=None):
        """
        Obtiene todos los productos con filtros opcionales
        filters: dict con min_price, max_price, category
        """
        products = list(cls._products.values())
        
        if filters:
            if 'min_price' in filters and filters['min_price'] is not None:
                products = [p for p in products if p.price >= filters['min_price']]
            
            if 'max_price' in filters and filters['max_price'] is not None:
                products = [p for p in products if p.price <= filters['max_price']]
            
            if 'category' in filters and filters['category']:
                products = [p for p in products if p.category.lower() == filters['category'].lower()]
        
        return products
    
    @classmethod
    def get_by_id(cls, product_id):
        """Obtiene un producto por ID"""
        return cls._products.get(product_id)

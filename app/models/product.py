from app.database import db
from datetime import datetime, timezone


class Product(db.Model):
    """Modelo de Producto con SQLAlchemy"""
    
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.now(timezone.utc))
    
    # Relación con categoría
    category = db.relationship('Category', backref='products')
    
    # Relación con items de orden
    order_items = db.relationship('OrderItem', backref='product', lazy=True)
    
    def __repr__(self):
        return f'<Product {self.name}>'
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': float(self.price),
            'stock': self.stock,
            'category': self.category.name if self.category else None,
            'category_id': self.category_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def get_all(cls, filters=None):
        """Obtiene todos los productos con filtros opcionales"""
        query = cls.query
        
        if filters:
            if 'min_price' in filters and filters['min_price'] is not None:
                query = query.filter(cls.price >= filters['min_price'])
            
            if 'max_price' in filters and filters['max_price'] is not None:
                query = query.filter(cls.price <= filters['max_price'])
            
            if 'category' in filters and filters['category']:
                query = query.join(cls.category).filter(
                    db.func.lower(Category.name) == filters['category'].lower()
                )
        
        return query.all()
    
    @classmethod
    def get_by_id(cls, product_id):
        """Obtiene un producto por ID"""
        return cls.query.get(product_id)
    
    def save(self):
        """Guarda el producto en la base de datos"""
        db.session.add(self)
        db.session.commit()
        return self
    
    def update(self, **kwargs):
        """Actualiza los campos del producto"""
        for key, value in kwargs.items():
            if hasattr(self, key) and key not in ['id', 'created_at']:
                setattr(self, key, value)
        self.updated_at = datetime.now(timezone.utc)
        db.session.commit()
        return self
    
    def delete(self):
        """Elimina el producto de la base de datos"""
        db.session.delete(self)
        db.session.commit()
        return True


# Importar Category para evitar errores de referencia circular
from app.models.category import Category

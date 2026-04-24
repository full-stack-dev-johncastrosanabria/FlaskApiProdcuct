from app.database import db
from datetime import datetime


class Order(db.Model):
    """Modelo de Orden de Compra"""
    
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='pending')  # pending, completed, cancelled
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    # Relación con items de la orden
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Order {self.id}>'
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_name': self.user.name if self.user else None,
            'total': float(self.total),
            'status': self.status,
            'items': [item.to_dict() for item in self.items] if self.items else [],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def get_all(cls, filters=None):
        """Obtiene todas las órdenes con filtros opcionales"""
        query = cls.query
        
        if filters:
            if 'status' in filters and filters['status']:
                query = query.filter_by(status=filters['status'])
            
            if 'user_id' in filters and filters['user_id']:
                query = query.filter_by(user_id=filters['user_id'])
        
        return query.order_by(cls.created_at.desc()).all()
    
    @classmethod
    def get_by_id(cls, order_id):
        """Obtiene una orden por ID"""
        return cls.query.get(order_id)
    
    def save(self):
        """Guarda la orden en la base de datos"""
        db.session.add(self)
        db.session.commit()
        return self
    
    def update(self, **kwargs):
        """Actualiza los campos de la orden"""
        for key, value in kwargs.items():
            if hasattr(self, key) and key not in ['id', 'created_at']:
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()
        db.session.commit()
        return self
    
    def delete(self):
        """Elimina la orden de la base de datos"""
        db.session.delete(self)
        db.session.commit()
        return True


class OrderItem(db.Model):
    """Modelo de Item de Orden"""
    
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)  # Precio al momento de la compra
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    
    def __repr__(self):
        return f'<OrderItem {self.id}>'
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'product_name': self.product.name if self.product else None,
            'quantity': self.quantity,
            'price': float(self.price),
            'subtotal': float(self.subtotal)
        }
    
    def save(self):
        """Guarda el item en la base de datos"""
        db.session.add(self)
        db.session.commit()
        return self

from app.database import db
from datetime import datetime


class Category(db.Model):
    """Modelo de Categoría"""
    
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Category {self.name}>'
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'product_count': len(self.products) if self.products else 0
        }
    
    @classmethod
    def get_all(cls):
        """Obtiene todas las categorías"""
        return cls.query.all()
    
    @classmethod
    def get_by_id(cls, category_id):
        """Obtiene una categoría por ID"""
        return cls.query.get(category_id)
    
    @classmethod
    def get_by_name(cls, name):
        """Obtiene una categoría por nombre"""
        return cls.query.filter_by(name=name).first()
    
    def save(self):
        """Guarda la categoría en la base de datos"""
        db.session.add(self)
        db.session.commit()
        return self
    
    def delete(self):
        """Elimina la categoría de la base de datos"""
        db.session.delete(self)
        db.session.commit()
        return True

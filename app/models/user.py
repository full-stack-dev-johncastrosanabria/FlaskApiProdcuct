from app.database import db
from datetime import datetime, timezone


class User(db.Model):
    """Modelo de Usuario con SQLAlchemy"""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.now(timezone.utc))
    
    # Relación con órdenes
    orders = db.relationship('Order', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.name}>'
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'total_orders': len(self.orders) if self.orders else 0
        }
    
    @classmethod
    def get_all(cls):
        """Obtiene todos los usuarios"""
        return cls.query.all()
    
    @classmethod
    def get_by_id(cls, user_id):
        """Obtiene un usuario por ID"""
        return cls.query.get(user_id)
    
    @classmethod
    def get_by_email(cls, email):
        """Obtiene un usuario por email"""
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def exists_email(cls, email):
        """Verifica si un email ya existe"""
        return cls.query.filter_by(email=email).first() is not None
    
    def save(self):
        """Guarda el usuario en la base de datos"""
        db.session.add(self)
        db.session.commit()
        return self
    
    def update(self, **kwargs):
        """Actualiza los campos del usuario"""
        for key, value in kwargs.items():
            if hasattr(self, key) and key not in ['id', 'created_at']:
                setattr(self, key, value)
        self.updated_at = datetime.now(timezone.utc)
        db.session.commit()
        return self
    
    def delete(self):
        """Elimina el usuario de la base de datos"""
        db.session.delete(self)
        db.session.commit()
        return True

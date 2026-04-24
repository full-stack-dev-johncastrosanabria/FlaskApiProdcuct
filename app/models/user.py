from datetime import datetime
import uuid


class User:
    """Modelo de Usuario"""
    
    # Simulación de base de datos en memoria
    _users = {}
    
    def __init__(self, name, email, user_id=None):
        self.id = user_id or str(uuid.uuid4())
        self.name = name
        self.email = email
        self.created_at = datetime.now().isoformat()
        self.updated_at = None
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    def save(self):
        """Guarda el usuario en la base de datos"""
        User._users[self.id] = self
        return self
    
    def update(self, **kwargs):
        """Actualiza los campos del usuario"""
        for key, value in kwargs.items():
            if hasattr(self, key) and key not in ['id', 'created_at']:
                setattr(self, key, value)
        self.updated_at = datetime.now().isoformat()
        return self
    
    def delete(self):
        """Elimina el usuario de la base de datos"""
        if self.id in User._users:
            del User._users[self.id]
            return True
        return False
    
    @classmethod
    def get_all(cls):
        """Obtiene todos los usuarios"""
        return list(cls._users.values())
    
    @classmethod
    def get_by_id(cls, user_id):
        """Obtiene un usuario por ID"""
        return cls._users.get(user_id)
    
    @classmethod
    def get_by_email(cls, email):
        """Obtiene un usuario por email"""
        for user in cls._users.values():
            if user.email == email:
                return user
        return None
    
    @classmethod
    def exists_email(cls, email):
        """Verifica si un email ya existe"""
        return cls.get_by_email(email) is not None

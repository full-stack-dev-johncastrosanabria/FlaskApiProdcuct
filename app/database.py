from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Inicializar SQLAlchemy
db = SQLAlchemy()


def init_db(app):
    """Inicializa la base de datos con la aplicación"""
    db.init_app(app)
    
    with app.app_context():
        # Crear todas las tablas
        db.create_all()
        print("✅ Base de datos inicializada correctamente")

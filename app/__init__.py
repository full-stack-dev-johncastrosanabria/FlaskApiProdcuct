from flask import Flask
from flask_cors import CORS
from config import config
from app.database import db, init_db


def create_app(config_name='default'):
    """
    Application Factory Pattern
    Crea y configura la aplicación Flask
    """
    app = Flask(__name__)
    
    # Cargar configuración
    app.config.from_object(config[config_name])
    
    # Inicializar base de datos
    init_db(app)
    
    # Configurar CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Registrar blueprints
    from app.routes import users, products, categories, orders, analytics, main
    app.register_blueprint(main.bp)
    app.register_blueprint(users.bp)
    app.register_blueprint(products.bp)
    app.register_blueprint(categories.bp)
    app.register_blueprint(orders.bp)
    app.register_blueprint(analytics.bp)
    
    # Registrar manejadores de errores
    from app.routes import errors
    errors.register_error_handlers(app)
    
    # Logging en producción
    if not app.debug and not app.testing:
        import logging
        from logging.handlers import RotatingFileHandler
        import os
        
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        file_handler = RotatingFileHandler(
            'logs/flask_api.log',
            maxBytes=10240,
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Flask API startup')
    
    return app

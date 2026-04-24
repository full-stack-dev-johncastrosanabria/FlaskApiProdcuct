from flask import Flask
from config import config


def create_app(config_name='default'):
    """
    Application Factory Pattern
    Crea y configura la aplicación Flask
    """
    app = Flask(__name__)
    
    # Cargar configuración
    app.config.from_object(config[config_name])
    
    # Registrar blueprints
    from app.routes import users, products, main
    app.register_blueprint(main.bp)
    app.register_blueprint(users.bp)
    app.register_blueprint(products.bp)
    
    # Registrar manejadores de errores
    from app.routes import errors
    errors.register_error_handlers(app)
    
    return app

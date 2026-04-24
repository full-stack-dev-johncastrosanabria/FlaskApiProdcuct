import os
from dotenv import load_dotenv
from app import create_app

# Cargar variables de entorno
load_dotenv()

DEFAULT_PORT = 5001


def get_config_name():
    """Obtiene el entorno de ejecución de la aplicación."""
    return os.environ.get('FLASK_ENV', 'development')


def get_port():
    """Obtiene el puerto del servidor con un valor por defecto consistente."""
    return int(os.environ.get('PORT', DEFAULT_PORT))


# Crear la aplicación usando el Application Factory
app = create_app(get_config_name())

if __name__ == '__main__':
    # Obtener puerto de variable de entorno o usar 5001 por defecto
    port = get_port()

    # Ejecutar la aplicación
    # En producción, usar un servidor WSGI como Gunicorn
    app.run(host='0.0.0.0', port=port, debug=app.debug)

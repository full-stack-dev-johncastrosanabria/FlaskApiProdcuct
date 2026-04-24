import os
from app import create_app

# Obtener el entorno de la variable de entorno o usar 'development' por defecto
config_name = os.environ.get('FLASK_ENV', 'development')

# Crear la aplicación usando el Application Factory
app = create_app(config_name)

if __name__ == '__main__':
    # Obtener puerto de variable de entorno o usar 5000 por defecto
    port = int(os.environ.get('PORT', 5000))
    
    # Ejecutar la aplicación
    # En producción, usar un servidor WSGI como Gunicorn
    app.run(host='0.0.0.0', port=port)

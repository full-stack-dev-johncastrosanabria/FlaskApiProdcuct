from flask import Blueprint, jsonify
from datetime import datetime

bp = Blueprint('main', __name__)


@bp.route('/', methods=['GET'])
def home():
    """Ruta principal con información de la API"""
    return jsonify({
        'message': 'API REST con Flask',
        'version': '1.0.0',
        'endpoints': {
            'users': '/api/users',
            'products': '/api/products',
            'health': '/api/health'
        }
    }), 200


@bp.route('/api/health', methods=['GET'])
def health_check():
    """Endpoint para verificar el estado de la API"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    }), 200

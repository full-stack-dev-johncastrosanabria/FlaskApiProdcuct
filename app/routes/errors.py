from flask import jsonify


def register_error_handlers(app):
    """Registra los manejadores de errores globales"""
    
    @app.errorhandler(404)
    def not_found(error):
        """Maneja errores 404"""
        return jsonify({
            'success': False,
            'error': 'Recurso no encontrado'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Maneja errores 500"""
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500
    
    @app.errorhandler(400)
    def bad_request(error):
        """Maneja errores 400"""
        return jsonify({
            'success': False,
            'error': 'Solicitud incorrecta'
        }), 400
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        """Maneja errores 405"""
        return jsonify({
            'success': False,
            'error': 'Método no permitido'
        }), 405

from flask import jsonify


def success_response(data=None, message=None, count=None, status_code=200):
    """
    Genera una respuesta exitosa estandarizada
    """
    response = {'success': True}
    
    if data is not None:
        response['data'] = data
    
    if message:
        response['message'] = message
    
    if count is not None:
        response['count'] = count
    
    return jsonify(response), status_code


def error_response(error_message, status_code=400):
    """
    Genera una respuesta de error estandarizada
    """
    return jsonify({
        'success': False,
        'error': error_message
    }), status_code

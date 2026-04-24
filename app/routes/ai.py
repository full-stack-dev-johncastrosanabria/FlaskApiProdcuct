"""
Rutas para el chatbot de IA.
"""
from flask import Blueprint, request

from app.ai import AIBot
from app.utils.responses import success_response, error_response

ai_bp = Blueprint('ai', __name__, url_prefix='/api/ai')

# Instancia global del bot (mantiene historial de conversación)
bot = AIBot()


@ai_bp.route('/ask', methods=['POST'])
def ask_question():
    """
    Procesa una pregunta del usuario.

    Body:
        {
            "question": "¿Cuántas ventas tenemos?"
        }

    Returns:
        {
            "success": true,
            "data": {
                "answer": "Las ventas totales son...",
                "confidence": 0.95,
                "data": {...},
                "category": "ventas"
            }
        }
    """
    try:
        data = request.get_json()

        if not data or 'question' not in data:
            return error_response('La pregunta es requerida', 400)

        question = data['question'].strip()

        if not question:
            return error_response('La pregunta no puede estar vacía', 400)

        # Procesar pregunta
        response = bot.process_question(question)

        return success_response(response, 'Pregunta procesada exitosamente')

    except ValueError as e:
        return error_response(f'Error de validación: {str(e)}', 400)
    except Exception as e:
        return error_response(f'Error interno: {str(e)}', 500)


@ai_bp.route('/history', methods=['GET'])
def get_history():
    """
    Obtiene el historial de conversación.

    Returns:
        {
            "success": true,
            "data": [
                {"type": "user", "message": "..."},
                {"type": "bot", "message": "..."}
            ]
        }
    """
    try:
        history = bot.get_conversation_history()
        return success_response(history, 'Historial obtenido exitosamente')

    except Exception as e:
        return error_response(f'Error al obtener historial: {str(e)}', 500)


@ai_bp.route('/history', methods=['DELETE'])
def clear_history():
    """
    Limpia el historial de conversación.

    Returns:
        {
            "success": true,
            "message": "Historial limpiado exitosamente"
        }
    """
    try:
        bot.clear_history()
        return success_response(
            {'cleared': True},
            'Historial limpiado exitosamente'
        )

    except Exception as e:
        return error_response(f'Error al limpiar historial: {str(e)}', 500)


@ai_bp.route('/capabilities', methods=['GET'])
def get_capabilities():
    """
    Obtiene las capacidades del bot.

    Returns:
        {
            "success": true,
            "data": {
                "categories": [...],
                "examples": [...]
            }
        }
    """
    try:
        capabilities = {
            'categories': [
                {
                    'name': 'Ventas',
                    'icon': '📊',
                    'description': 'Estadísticas de ventas, ingresos y órdenes'
                },
                {
                    'name': 'Productos',
                    'icon': '📦',
                    'description': 'Información sobre productos y stock'
                },
                {
                    'name': 'Clientes',
                    'icon': '👥',
                    'description': 'Datos de clientes y comportamiento'
                },
                {
                    'name': 'Categorías',
                    'icon': '🏷️',
                    'description': 'Información de categorías de productos'
                },
                {
                    'name': 'Stock',
                    'icon': '📋',
                    'description': 'Estado del inventario y alertas'
                },
                {
                    'name': 'Recomendaciones',
                    'icon': '💡',
                    'description': 'Sugerencias basadas en datos'
                }
            ],
            'examples': [
                '¿Cuántas ventas tenemos en total?',
                '¿Cuál es el producto más vendido?',
                '¿Cuántos clientes tenemos?',
                '¿Hay productos con stock bajo?',
                'Dame recomendaciones',
                '¿Cuál es el precio promedio de los productos?'
            ]
        }

        return success_response(
            capabilities,
            'Capacidades obtenidas exitosamente'
        )

    except Exception as e:
        return error_response(
            f'Error al obtener capacidades: {str(e)}',
            500
        )

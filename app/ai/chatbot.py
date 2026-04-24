"""
Chatbot IA básico con base de conocimientos.
Responde preguntas sobre datos reales del sistema.
"""
from typing import Dict, List
from app.ai.knowledge_base import KnowledgeBase


class AIBot:
    """Bot de IA que responde preguntas sobre datos del negocio."""

    def __init__(self):
        self.knowledge_base = KnowledgeBase()
        self.conversation_history = []

    def process_question(self, question: str) -> Dict:
        """
        Procesa una pregunta y retorna una respuesta.

        Args:
            question: Pregunta del usuario

        Returns:
            Diccionario con respuesta, confianza y datos
        """
        # Limpiar pregunta
        question = question.strip()
        if not question:
            return self._error_response("Por favor, haz una pregunta válida.")

        # Agregar a historial
        self.conversation_history.append({
            'type': 'user',
            'message': question
        })

        # Extraer palabras clave
        keywords = KnowledgeBase.extract_keywords(question)

        # Procesar según categoría
        response = self._process_by_category(question, keywords)

        # Agregar respuesta al historial
        self.conversation_history.append({
            'type': 'bot',
            'message': response['answer']
        })

        return response

    def _process_by_category(self, question: str, keywords: List[str]) -> Dict:
        """Procesa la pregunta según su categoría."""
        question_lower = question.lower()

        # Preguntas sobre ventas
        if 'ventas' in keywords:
            return self._answer_sales_question(question_lower)

        # Preguntas sobre productos
        if 'productos' in keywords:
            return self._answer_products_question(question_lower)

        # Preguntas sobre clientes
        if 'clientes' in keywords:
            return self._answer_customers_question(question_lower)

        # Preguntas sobre categorías
        if 'categorias' in keywords:
            return self._answer_categories_question(question_lower)

        # Preguntas sobre stock
        if 'stock' in keywords:
            return self._answer_stock_question(question_lower)

        # Preguntas sobre recomendaciones
        if 'recomendaciones' in keywords:
            return self._answer_recommendations_question(question_lower)

        # Preguntas generales
        return self._answer_general_question(question_lower)

    def _answer_sales_question(self, question: str) -> Dict:
        """Responde preguntas sobre ventas."""
        stats = self.knowledge_base.get_sales_stats()

        if 'total' in question or 'cuánto' in question:
            answer = (
                f"Las ventas totales son ${stats['total_sales']:,.2f} "
                f"en {stats['total_orders']} órdenes."
            )
            confidence = 0.95
        elif 'promedio' in question or 'media' in question:
            answer = (
                f"El valor promedio por orden es "
                f"${stats['avg_order']:,.2f}."
            )
            confidence = 0.95
        elif 'hoy' in question or 'día' in question:
            answer = (
                f"Las ventas de hoy son ${stats['today_sales']:,.2f}."
            )
            confidence = 0.95
        else:
            answer = (
                f"Tenemos {stats['total_orders']} órdenes completadas "
                f"con un total de ${stats['total_sales']:,.2f}. "
                f"El promedio por orden es ${stats['avg_order']:,.2f}."
            )
            confidence = 0.90

        return {
            'answer': answer,
            'confidence': confidence,
            'data': stats,
            'category': 'ventas'
        }

    def _answer_products_question(self, question: str) -> Dict:
        """Responde preguntas sobre productos."""
        stats = self.knowledge_base.get_product_stats()
        top_products = self.knowledge_base.get_top_products(3)

        if 'cuántos' in question or 'total' in question:
            answer = (
                f"Tenemos {stats['total_products']} productos en total "
                f"con {stats['total_stock']} unidades en stock."
            )
            confidence = 0.95
        elif 'más vendido' in question or 'popular' in question:
            if top_products:
                top = top_products[0]
                answer = (
                    f"El producto más vendido es '{top['name']}' "
                    f"con {top['quantity']} unidades vendidas."
                )
                confidence = 0.95
            else:
                answer = "No hay datos de productos vendidos aún."
                confidence = 0.80
        elif 'precio' in question:
            answer = (
                f"El precio promedio de nuestros productos es "
                f"${stats['avg_price']:,.2f}."
            )
            confidence = 0.90
        else:
            answer = (
                f"Tenemos {stats['total_products']} productos con "
                f"{stats['total_stock']} unidades en stock. "
                f"El precio promedio es ${stats['avg_price']:,.2f}."
            )
            confidence = 0.85

        return {
            'answer': answer,
            'confidence': confidence,
            'data': {**stats, 'top_products': top_products},
            'category': 'productos'
        }

    def _answer_customers_question(self, question: str) -> Dict:
        """Responde preguntas sobre clientes."""
        stats = self.knowledge_base.get_customer_stats()

        if 'cuántos' in question or 'total' in question:
            answer = (
                f"Tenemos {stats['total_customers']} clientes "
                f"registrados, de los cuales "
                f"{stats['customers_with_orders']} han realizado compras."
            )
            confidence = 0.95
        elif 'activo' in question or 'compra' in question:
            answer = (
                f"{stats['customers_with_orders']} clientes han "
                f"realizado compras."
            )
            confidence = 0.95
        elif 'inactivo' in question:
            answer = (
                f"Hay {stats['inactive_customers']} clientes sin "
                f"compras registradas."
            )
            confidence = 0.95
        else:
            answer = (
                f"Tenemos {stats['total_customers']} clientes en total. "
                f"{stats['customers_with_orders']} han comprado y "
                f"{stats['inactive_customers']} aún no."
            )
            confidence = 0.90

        return {
            'answer': answer,
            'confidence': confidence,
            'data': stats,
            'category': 'clientes'
        }

    def _answer_categories_question(self, question: str) -> Dict:
        """Responde preguntas sobre categorías."""
        categories = self.knowledge_base.get_category_stats()

        if not categories:
            return self._error_response("No hay datos de categorías disponibles.")

        if 'cuántas' in question or 'total' in question:
            answer = f"Tenemos {len(categories)} categorías de productos."
            confidence = 0.95
        else:
            category_list = ", ".join([
                f"{c['category']} ({c['products']} productos)"
                for c in categories
            ])
            answer = f"Nuestras categorías son: {category_list}."
            confidence = 0.90

        return {
            'answer': answer,
            'confidence': confidence,
            'data': {'categories': categories},
            'category': 'categorias'
        }

    def _answer_stock_question(self, question: str) -> Dict:
        """Responde preguntas sobre stock."""
        stats = self.knowledge_base.get_product_stats()

        if 'bajo' in question or 'poco' in question:
            answer = (
                f"Hay {stats['low_stock']} productos con stock bajo "
                f"(≤10 unidades)."
            )
            confidence = 0.95
        elif 'sin stock' in question or 'agotado' in question:
            answer = f"Hay {stats['out_of_stock']} productos sin stock."
            confidence = 0.95
        elif 'total' in question:
            answer = f"El stock total es de {stats['total_stock']} unidades."
            confidence = 0.95
        else:
            answer = (
                f"Stock total: {stats['total_stock']} unidades. "
                f"{stats['low_stock']} con stock bajo y "
                f"{stats['out_of_stock']} sin stock."
            )
            confidence = 0.90

        return {
            'answer': answer,
            'confidence': confidence,
            'data': stats,
            'category': 'stock'
        }

    def _answer_recommendations_question(self, question: str) -> Dict:
        """Responde preguntas sobre recomendaciones."""
        recommendations = self.knowledge_base.get_recommendations()

        if recommendations['count'] == 0:
            answer = (
                "✅ Todo está en orden. "
                "No hay recomendaciones urgentes en este momento."
            )
            confidence = 0.90
        else:
            rec_list = "\n".join([
                f"• {r['message']}"
                for r in recommendations['recommendations']
            ])
            answer = f"Aquí están mis recomendaciones:\n{rec_list}"
            confidence = 0.85

        return {
            'answer': answer,
            'confidence': confidence,
            'data': recommendations,
            'category': 'recomendaciones'
        }

    def _answer_general_question(self, question: str) -> Dict:
        """Responde preguntas generales."""
        # Preguntas de saludo
        if any(word in question
               for word in ['hola', 'hi', 'buenos', 'buenas']):
            answer = (
                "¡Hola! Soy tu asistente de IA. "
                "Puedo responder preguntas sobre ventas, productos, "
                "clientes, stock y más. ¿Qué te gustaría saber?"
            )
            confidence = 0.95
            return {
                'answer': answer,
                'confidence': confidence,
                'data': {},
                'category': 'saludo'
            }

        # Preguntas sobre qué puedo hacer
        if any(word in question
               for word in ['puedes', 'puedo', 'qué haces', 'ayuda']):
            answer = (
                "Puedo ayudarte con:\n"
                "• 📊 Estadísticas de ventas\n"
                "• 📦 Información de productos\n"
                "• 👥 Datos de clientes\n"
                "• 📈 Recomendaciones\n"
                "• 🏷️ Información de categorías\n"
                "• 📋 Estado del inventario\n\n"
                "¿Qué te gustaría saber?"
            )
            confidence = 0.95
            return {
                'answer': answer,
                'confidence': confidence,
                'data': {},
                'category': 'ayuda'
            }

        # Respuesta por defecto
        answer = (
            "No estoy seguro de cómo responder esa pregunta. "
            "Intenta preguntar sobre ventas, productos, clientes, "
            "stock o recomendaciones."
        )
        confidence = 0.50

        return {
            'answer': answer,
            'confidence': confidence,
            'data': {},
            'category': 'general'
        }

    def _error_response(self, message: str) -> Dict:
        """Retorna una respuesta de error."""
        return {
            'answer': message,
            'confidence': 0.0,
            'data': {},
            'category': 'error'
        }

    def get_conversation_history(self) -> List[Dict]:
        """Retorna el historial de conversación."""
        return self.conversation_history

    def clear_history(self) -> None:
        """Limpia el historial de conversación."""
        self.conversation_history = []

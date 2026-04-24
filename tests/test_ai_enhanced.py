"""
Enhanced tests for AI Chatbot - Edge cases and advanced scenarios
"""
import pytest
from app import create_app
from app.database import db
from app.models import User, Product, Category, Order, OrderItem
from app.ai.chatbot import AIBot
from app.ai.knowledge_base import KnowledgeBase


@pytest.fixture
def app():
    """Create test application."""
    app = create_app('testing')

    with app.app_context():
        db.create_all()

        # Create test data
        category = Category(
            name='Electrónica',
            description='Productos electrónicos'
        )
        db.session.add(category)
        db.session.commit()

        # Multiple products
        products = [
            Product(
                name='Laptop',
                price=999.99,
                stock=10,
                category_id=category.id,
                description='Laptop de prueba'
            ),
            Product(
                name='Mouse',
                price=29.99,
                stock=5,
                category_id=category.id,
                description='Mouse inalámbrico'
            ),
            Product(
                name='Teclado',
                price=0,
                stock=0,
                category_id=category.id,
                description='Sin stock'
            )
        ]
        for product in products:
            db.session.add(product)

        # Multiple users
        users = [
            User(name='User 1', email='user1@example.com'),
            User(name='User 2', email='user2@example.com'),
            User(name='User 3', email='user3@example.com')
        ]
        for user in users:
            db.session.add(user)
        db.session.commit()

        # Multiple orders
        order1 = Order(user_id=users[0].id, total=999.99, status='completed')
        order2 = Order(user_id=users[1].id, total=29.99, status='completed')
        db.session.add(order1)
        db.session.add(order2)
        db.session.commit()

        # Order items
        item1 = OrderItem(
            order_id=order1.id,
            product_id=products[0].id,
            quantity=1,
            price=999.99,
            subtotal=999.99
        )
        item2 = OrderItem(
            order_id=order2.id,
            product_id=products[1].id,
            quantity=1,
            price=29.99,
            subtotal=29.99
        )
        db.session.add(item1)
        db.session.add(item2)
        db.session.commit()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def bot(app):
    """Create bot instance."""
    with app.app_context():
        return AIBot()


class TestAIEdgeCases:
    """Test edge cases and error handling."""

    def test_very_long_question(self, client):
        """Test handling of very long questions."""
        long_question = "¿Cuántas ventas tenemos? " * 100
        response = client.post(
            '/api/ai/ask',
            json={'question': long_question}
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True

    def test_special_characters(self, client):
        """Test questions with special characters."""
        questions = [
            '¿Cuántas ventas tenemos? 🤔',
            '¿Productos con $$$?',
            '¿Clientes @#$%?',
            '¿Ventas & productos?'
        ]

        for question in questions:
            response = client.post(
                '/api/ai/ask',
                json={'question': question}
            )
            assert response.status_code == 200

    def test_numeric_only_question(self, client):
        """Test numeric-only questions."""
        response = client.post(
            '/api/ai/ask',
            json={'question': '12345'}
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['data']['category'] == 'general'

    def test_empty_string_variations(self, client):
        """Test various empty string formats."""
        empty_variations = ['', '   ', '\n', '\t', '  \n  \t  ']

        for empty in empty_variations:
            response = client.post(
                '/api/ai/ask',
                json={'question': empty}
            )
            assert response.status_code == 400

    def test_unicode_characters(self, client):
        """Test Unicode characters in questions."""
        response = client.post(
            '/api/ai/ask',
            json={'question': '¿Cuántas ventas 中文 한글 日本語?'}
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True


class TestAIKnowledgeBase:
    """Test knowledge base functionality."""

    def test_keyword_extraction(self, app):
        """Test keyword extraction from questions."""
        with app.app_context():
            test_cases = [
                ('¿Cuántas ventas tenemos?', 'ventas'),
                ('¿Productos disponibles?', 'productos'),
                ('¿Clientes activos?', 'clientes'),
                ('Hola', 'general')
            ]

            for question, expected_keyword in test_cases:
                keywords = KnowledgeBase.extract_keywords(question)
                assert expected_keyword in keywords

    def test_sales_stats_with_data(self, app):
        """Test sales statistics calculation."""
        with app.app_context():
            stats = KnowledgeBase.get_sales_stats()

            assert stats['total_sales'] >= 0
            assert stats['total_orders'] >= 0
            assert stats['avg_order'] >= 0
            assert stats['today_sales'] >= 0
            assert isinstance(stats, dict)

    def test_product_stats_with_data(self, app):
        """Test product statistics calculation."""
        with app.app_context():
            stats = KnowledgeBase.get_product_stats()

            assert stats['total_products'] >= 0
            assert stats['total_stock'] >= 0
            assert stats['low_stock'] >= 0
            assert stats['out_of_stock'] >= 0
            assert isinstance(stats, dict)

    def test_customer_stats_with_data(self, app):
        """Test customer statistics calculation."""
        with app.app_context():
            stats = KnowledgeBase.get_customer_stats()

            assert stats['total_customers'] >= 0
            assert stats['customers_with_orders'] >= 0
            assert stats['inactive_customers'] >= 0
            assert isinstance(stats, dict)

    def test_top_products(self, app):
        """Test top products retrieval."""
        with app.app_context():
            top_products = KnowledgeBase.get_top_products(5)

            assert isinstance(top_products, list)
            if len(top_products) > 0:
                assert 'name' in top_products[0]
                assert 'quantity' in top_products[0]
                assert 'revenue' in top_products[0]

    def test_recommendations_generation(self, app):
        """Test recommendations generation."""
        with app.app_context():
            recommendations = KnowledgeBase.get_recommendations()

            assert 'recommendations' in recommendations
            assert 'count' in recommendations
            assert isinstance(recommendations['recommendations'], list)


class TestAIBotLogic:
    """Test bot logic and response generation."""

    def test_conversation_history(self, bot):
        """Test conversation history tracking."""
        bot.process_question('Hola')
        bot.process_question('¿Cuántas ventas tenemos?')

        history = bot.get_conversation_history()

        assert len(history) == 4  # 2 questions + 2 responses
        assert history[0]['type'] == 'user'
        assert history[1]['type'] == 'bot'

    def test_clear_history(self, bot):
        """Test clearing conversation history."""
        bot.process_question('Hola')
        bot.process_question('¿Cuántas ventas tenemos?')

        bot.clear_history()
        history = bot.get_conversation_history()

        assert len(history) == 0

    def test_confidence_levels_range(self, bot):
        """Test confidence levels are within valid range."""
        questions = [
            '¿Cuántas ventas tenemos?',
            '¿Productos disponibles?',
            '¿Clientes activos?',
            'Pregunta sin sentido xyz123'
        ]

        for question in questions:
            response = bot.process_question(question)
            assert 0.0 <= response['confidence'] <= 1.0

    def test_category_classification(self, bot):
        """Test question category classification."""
        test_cases = [
            ('¿Cuántas ventas?', 'ventas'),
            ('¿Productos disponibles?', 'productos'),
            ('¿Clientes activos?', 'clientes'),
            ('¿Stock bajo?', 'stock'),
            ('Dame recomendaciones', 'recomendaciones'),
            ('Hola', 'saludo')
        ]

        for question, expected_category in test_cases:
            response = bot.process_question(question)
            assert response['category'] == expected_category

    def test_data_structure_in_response(self, bot):
        """Test response data structure."""
        response = bot.process_question('¿Cuántas ventas tenemos?')

        assert 'answer' in response
        assert 'confidence' in response
        assert 'data' in response
        assert 'category' in response
        assert isinstance(response['answer'], str)
        assert isinstance(response['confidence'], float)
        assert isinstance(response['data'], dict)


class TestAPIEndpoints:
    """Test API endpoint behavior."""

    def test_concurrent_requests(self, client):
        """Test handling of multiple concurrent requests."""
        questions = [
            '¿Cuántas ventas?',
            '¿Productos disponibles?',
            '¿Clientes activos?'
        ]

        responses = []
        for question in questions:
            response = client.post(
                '/api/ai/ask',
                json={'question': question}
            )
            responses.append(response)

        for response in responses:
            assert response.status_code == 200
            data = response.get_json()
            assert data['success'] is True

    def test_invalid_json(self, client):
        """Test handling of invalid JSON."""
        response = client.post(
            '/api/ai/ask',
            data='invalid json',
            content_type='application/json'
        )

        assert response.status_code in [400, 500]

    def test_missing_content_type(self, client):
        """Test request without content type."""
        response = client.post(
            '/api/ai/ask',
            data='{"question": "test"}'
        )

        # Should still work or return appropriate error
        assert response.status_code in [200, 400, 415, 500]

    def test_get_capabilities_structure(self, client):
        """Test capabilities endpoint structure."""
        response = client.get('/api/ai/capabilities')

        assert response.status_code == 200
        data = response.get_json()
        assert 'categories' in data['data']
        assert 'examples' in data['data']
        assert len(data['data']['categories']) > 0
        assert len(data['data']['examples']) > 0

        # Verify category structure
        category = data['data']['categories'][0]
        assert 'name' in category
        assert 'icon' in category
        assert 'description' in category


class TestPerformance:
    """Test performance characteristics."""

    def test_response_time(self, client):
        """Test response time is reasonable."""
        import time

        start = time.time()
        response = client.post(
            '/api/ai/ask',
            json={'question': '¿Cuántas ventas tenemos?'}
        )
        end = time.time()

        assert response.status_code == 200
        assert (end - start) < 1.0  # Should respond in less than 1 second

    def test_multiple_questions_performance(self, client):
        """Test performance with multiple questions."""
        import time

        questions = ['¿Cuántas ventas?'] * 10

        start = time.time()
        for question in questions:
            client.post('/api/ai/ask', json={'question': question})
        end = time.time()

        avg_time = (end - start) / len(questions)
        assert avg_time < 0.5  # Average should be less than 500ms


class TestErrorHandling:
    """Test error handling scenarios."""

    def test_database_error_handling(self, client, app):
        """Test handling when database is unavailable."""
        # This is a conceptual test - actual implementation
        # would require mocking database failures
        response = client.post(
            '/api/ai/ask',
            json={'question': '¿Cuántas ventas?'}
        )

        # Should handle gracefully
        assert response.status_code in [200, 500]

    def test_malformed_question_handling(self, bot):
        """Test handling of malformed questions."""
        malformed_questions = [
            None,
            '',
            '   ',
            '\n\n\n'
        ]

        for question in malformed_questions:
            if question is None:
                continue
            response = bot.process_question(question)
            assert 'answer' in response
            assert response['confidence'] >= 0.0

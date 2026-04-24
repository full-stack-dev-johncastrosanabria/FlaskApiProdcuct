"""
Tests para el módulo de IA (Chatbot)
"""
import pytest
from app import create_app
from app.database import db
from app.models import User, Product, Category, Order, OrderItem


@pytest.fixture
def app():
    """Crea una aplicación de prueba."""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        
        # Crear datos de prueba
        category = Category(name='Electrónica', description='Productos electrónicos')
        db.session.add(category)
        db.session.commit()
        
        product = Product(
            name='Laptop',
            price=999.99,
            stock=10,
            category_id=category.id,
            description='Laptop de prueba'
        )
        db.session.add(product)
        
        user = User(name='Test User', email='test@example.com')
        db.session.add(user)
        db.session.commit()
        
        order = Order(user_id=user.id, total=999.99, status='completed')
        db.session.add(order)
        db.session.commit()
        
        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=1,
            price=999.99,
            subtotal=999.99
        )
        db.session.add(order_item)
        db.session.commit()
        
        yield app
        
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Crea un cliente de prueba."""
    return app.test_client()


class TestAI:
    """Tests para el chatbot de IA."""
    
    def test_ask_question_success(self, client):
        """Test: Enviar pregunta exitosamente."""
        response = client.post(
            '/api/ai/ask',
            json={'question': '¿Cuántas ventas tenemos?'}
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'data' in data
        assert 'answer' in data['data']
        assert 'confidence' in data['data']
        assert 'category' in data['data']
    
    def test_ask_question_missing_question(self, client):
        """Test: Error al enviar pregunta sin contenido."""
        response = client.post(
            '/api/ai/ask',
            json={}
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False
    
    def test_ask_question_empty_question(self, client):
        """Test: Error al enviar pregunta vacía."""
        response = client.post(
            '/api/ai/ask',
            json={'question': '   '}
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False
    
    def test_ask_sales_question(self, client):
        """Test: Pregunta sobre ventas."""
        response = client.post(
            '/api/ai/ask',
            json={'question': '¿Cuántas ventas tenemos?'}
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['data']['category'] == 'ventas'
        assert 'total_sales' in data['data']['data']
    
    def test_ask_products_question(self, client):
        """Test: Pregunta sobre productos."""
        response = client.post(
            '/api/ai/ask',
            json={'question': '¿Cuántos productos tenemos?'}
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['data']['category'] == 'productos'
    
    def test_ask_customers_question(self, client):
        """Test: Pregunta sobre clientes."""
        response = client.post(
            '/api/ai/ask',
            json={'question': '¿Cuántos clientes tenemos?'}
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['data']['category'] == 'clientes'
    
    def test_ask_greeting(self, client):
        """Test: Saludo al bot."""
        response = client.post(
            '/api/ai/ask',
            json={'question': 'Hola'}
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['data']['category'] == 'saludo'
    
    def test_get_history(self, client):
        """Test: Obtener historial de conversación."""
        # Primero hacer una pregunta
        client.post(
            '/api/ai/ask',
            json={'question': 'Hola'}
        )
        
        # Obtener historial
        response = client.get('/api/ai/history')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert isinstance(data['data'], list)
        assert len(data['data']) > 0
    
    def test_clear_history(self, client):
        """Test: Limpiar historial de conversación."""
        # Primero hacer una pregunta
        client.post(
            '/api/ai/ask',
            json={'question': 'Hola'}
        )
        
        # Limpiar historial
        response = client.delete('/api/ai/history')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['data']['cleared'] is True
    
    def test_get_capabilities(self, client):
        """Test: Obtener capacidades del bot."""
        response = client.get('/api/ai/capabilities')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'categories' in data['data']
        assert 'examples' in data['data']
        assert len(data['data']['categories']) > 0
        assert len(data['data']['examples']) > 0
    
    def test_confidence_levels(self, client):
        """Test: Verificar niveles de confianza."""
        response = client.post(
            '/api/ai/ask',
            json={'question': '¿Cuántas ventas tenemos?'}
        )
        
        assert response.status_code == 200
        data = response.get_json()
        confidence = data['data']['confidence']
        assert 0.0 <= confidence <= 1.0
    
    def test_multiple_questions(self, client):
        """Test: Hacer múltiples preguntas."""
        questions = [
            '¿Cuántas ventas tenemos?',
            '¿Cuántos productos tenemos?',
            '¿Cuántos clientes tenemos?'
        ]
        
        for question in questions:
            response = client.post(
                '/api/ai/ask',
                json={'question': question}
            )
            assert response.status_code == 200
            data = response.get_json()
            assert data['success'] is True

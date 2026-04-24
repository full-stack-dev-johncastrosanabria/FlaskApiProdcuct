import pytest
import json


class TestProducts:
    """Tests para endpoints de productos"""
    
    def test_get_products_empty(self, client):
        """Test obtener productos cuando no hay ninguno"""
        response = client.get('/api/products')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['count'] == 0
        assert data['data'] == []
    
    def test_create_product_success(self, client):
        """Test crear producto exitosamente"""
        product_data = {
            'name': 'Laptop',
            'price': 999.99,
            'category': 'electrónica',
            'description': 'Laptop de alta gama',
            'stock': 10
        }
        response = client.post(
            '/api/products',
            data=json.dumps(product_data),
            content_type='application/json'
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['name'] == 'Laptop'
        assert data['data']['price'] == 999.99
        assert 'id' in data['data']
    
    def test_create_product_missing_fields(self, client):
        """Test crear producto sin campos requeridos"""
        product_data = {'name': 'Laptop'}
        response = client.post(
            '/api/products',
            data=json.dumps(product_data),
            content_type='application/json'
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
    
    def test_create_product_invalid_price(self, client):
        """Test crear producto con precio inválido"""
        product_data = {
            'name': 'Laptop',
            'price': -10,
            'category': 'electrónica'
        }
        response = client.post(
            '/api/products',
            data=json.dumps(product_data),
            content_type='application/json'
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'precio' in data['error'].lower()
    
    def test_get_product_by_id(self, client):
        """Test obtener producto por ID"""
        # Crear producto
        product_data = {
            'name': 'Mouse',
            'price': 25.99,
            'category': 'accesorios'
        }
        create_response = client.post(
            '/api/products',
            data=json.dumps(product_data),
            content_type='application/json'
        )
        product_id = json.loads(create_response.data)['data']['id']
        
        # Obtener producto
        response = client.get(f'/api/products/{product_id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['id'] == product_id
    
    def test_update_product(self, client):
        """Test actualizar producto"""
        # Crear producto
        product_data = {
            'name': 'Mouse',
            'price': 25.99,
            'category': 'accesorios'
        }
        create_response = client.post(
            '/api/products',
            data=json.dumps(product_data),
            content_type='application/json'
        )
        product_id = json.loads(create_response.data)['data']['id']
        
        # Actualizar producto
        update_data = {'price': 29.99, 'stock': 50}
        response = client.put(
            f'/api/products/{product_id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['price'] == 29.99
        assert data['data']['stock'] == 50
    
    def test_delete_product(self, client):
        """Test eliminar producto"""
        # Crear producto
        product_data = {
            'name': 'Mouse',
            'price': 25.99,
            'category': 'accesorios'
        }
        create_response = client.post(
            '/api/products',
            data=json.dumps(product_data),
            content_type='application/json'
        )
        product_id = json.loads(create_response.data)['data']['id']
        
        # Eliminar producto
        response = client.delete(f'/api/products/{product_id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        
        # Verificar que ya no existe
        get_response = client.get(f'/api/products/{product_id}')
        assert get_response.status_code == 404
    
    def test_filter_products_by_price(self, client):
        """Test filtrar productos por precio"""
        # Crear productos con diferentes precios
        products = [
            {'name': 'Producto 1', 'price': 10.0, 'category': 'test'},
            {'name': 'Producto 2', 'price': 25.0, 'category': 'test'},
            {'name': 'Producto 3', 'price': 50.0, 'category': 'test'}
        ]
        for product in products:
            client.post(
                '/api/products',
                data=json.dumps(product),
                content_type='application/json'
            )
        
        # Filtrar por precio mínimo
        response = client.get('/api/products?min_price=20')
        data = json.loads(response.data)
        assert data['count'] == 2
        
        # Filtrar por precio máximo
        response = client.get('/api/products?max_price=30')
        data = json.loads(response.data)
        assert data['count'] == 2
        
        # Filtrar por rango
        response = client.get('/api/products?min_price=20&max_price=40')
        data = json.loads(response.data)
        assert data['count'] == 1
    
    def test_filter_products_by_category(self, client):
        """Test filtrar productos por categoría"""
        # Crear productos con diferentes categorías
        products = [
            {'name': 'Laptop', 'price': 999.99, 'category': 'electrónica'},
            {'name': 'Mouse', 'price': 25.99, 'category': 'accesorios'},
            {'name': 'Teclado', 'price': 49.99, 'category': 'accesorios'}
        ]
        for product in products:
            client.post(
                '/api/products',
                data=json.dumps(product),
                content_type='application/json'
            )
        
        # Filtrar por categoría
        response = client.get('/api/products?category=accesorios')
        data = json.loads(response.data)
        assert data['count'] == 2

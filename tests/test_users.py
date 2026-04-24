import pytest
import json


class TestUsers:
    """Tests para endpoints de usuarios"""
    
    def test_get_users_empty(self, client):
        """Test obtener usuarios cuando no hay ninguno"""
        response = client.get('/api/users')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['count'] == 0
        assert data['data'] == []
    
    def test_create_user_success(self, client):
        """Test crear usuario exitosamente"""
        user_data = {
            'name': 'Juan Pérez',
            'email': 'juan@example.com'
        }
        response = client.post(
            '/api/users',
            data=json.dumps(user_data),
            content_type='application/json'
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['name'] == 'Juan Pérez'
        assert data['data']['email'] == 'juan@example.com'
        assert 'id' in data['data']
        assert 'created_at' in data['data']
    
    def test_create_user_missing_name(self, client):
        """Test crear usuario sin nombre"""
        user_data = {'email': 'juan@example.com'}
        response = client.post(
            '/api/users',
            data=json.dumps(user_data),
            content_type='application/json'
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'name' in data['error'].lower()
    
    def test_create_user_missing_email(self, client):
        """Test crear usuario sin email"""
        user_data = {'name': 'Juan Pérez'}
        response = client.post(
            '/api/users',
            data=json.dumps(user_data),
            content_type='application/json'
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'email' in data['error'].lower()
    
    def test_create_user_invalid_email(self, client):
        """Test crear usuario con email inválido"""
        user_data = {
            'name': 'Juan Pérez',
            'email': 'invalid-email'
        }
        response = client.post(
            '/api/users',
            data=json.dumps(user_data),
            content_type='application/json'
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
    
    def test_create_user_duplicate_email(self, client):
        """Test crear usuario con email duplicado"""
        user_data = {
            'name': 'Juan Pérez',
            'email': 'juan@example.com'
        }
        # Crear primer usuario
        client.post(
            '/api/users',
            data=json.dumps(user_data),
            content_type='application/json'
        )
        # Intentar crear segundo usuario con mismo email
        response = client.post(
            '/api/users',
            data=json.dumps(user_data),
            content_type='application/json'
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'email' in data['error'].lower()
    
    def test_get_user_by_id(self, client):
        """Test obtener usuario por ID"""
        # Crear usuario
        user_data = {
            'name': 'Juan Pérez',
            'email': 'juan@example.com'
        }
        create_response = client.post(
            '/api/users',
            data=json.dumps(user_data),
            content_type='application/json'
        )
        user_id = json.loads(create_response.data)['data']['id']
        
        # Obtener usuario
        response = client.get(f'/api/users/{user_id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['id'] == user_id
    
    def test_get_user_not_found(self, client):
        """Test obtener usuario que no existe"""
        response = client.get('/api/users/nonexistent-id')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['success'] is False
    
    def test_update_user(self, client):
        """Test actualizar usuario"""
        # Crear usuario
        user_data = {
            'name': 'Juan Pérez',
            'email': 'juan@example.com'
        }
        create_response = client.post(
            '/api/users',
            data=json.dumps(user_data),
            content_type='application/json'
        )
        user_id = json.loads(create_response.data)['data']['id']
        
        # Actualizar usuario
        update_data = {'name': 'Juan Actualizado'}
        response = client.put(
            f'/api/users/{user_id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['name'] == 'Juan Actualizado'
        assert 'updated_at' in data['data']
    
    def test_delete_user(self, client):
        """Test eliminar usuario"""
        # Crear usuario
        user_data = {
            'name': 'Juan Pérez',
            'email': 'juan@example.com'
        }
        create_response = client.post(
            '/api/users',
            data=json.dumps(user_data),
            content_type='application/json'
        )
        user_id = json.loads(create_response.data)['data']['id']
        
        # Eliminar usuario
        response = client.delete(f'/api/users/{user_id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        
        # Verificar que ya no existe
        get_response = client.get(f'/api/users/{user_id}')
        assert get_response.status_code == 404
    
    def test_get_all_users(self, client):
        """Test obtener todos los usuarios"""
        # Crear varios usuarios
        users = [
            {'name': 'Usuario 1', 'email': 'user1@example.com'},
            {'name': 'Usuario 2', 'email': 'user2@example.com'},
            {'name': 'Usuario 3', 'email': 'user3@example.com'}
        ]
        for user in users:
            client.post(
                '/api/users',
                data=json.dumps(user),
                content_type='application/json'
            )
        
        # Obtener todos
        response = client.get('/api/users')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['count'] == 3
        assert len(data['data']) == 3

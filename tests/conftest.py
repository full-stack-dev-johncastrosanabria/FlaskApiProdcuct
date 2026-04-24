import pytest
from app import create_app
from app.models import User, Product


@pytest.fixture
def app():
    """Crea una instancia de la aplicación para testing"""
    app = create_app('testing')
    yield app


@pytest.fixture
def client(app):
    """Crea un cliente de prueba"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Crea un runner de CLI"""
    return app.test_cli_runner()


@pytest.fixture(autouse=True)
def clean_database():
    """Limpia la base de datos antes de cada test"""
    User._users.clear()
    Product._products.clear()
    yield
    User._users.clear()
    Product._products.clear()

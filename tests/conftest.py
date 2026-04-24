import pytest
from app import create_app
from app.database import db
from app.models import User, Product, Category, Order


@pytest.fixture
def app():
    """Crea una instancia de la aplicación para testing"""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Crea un cliente de prueba"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Crea un runner de CLI"""
    return app.test_cli_runner()


@pytest.fixture(autouse=True)
def clean_database(app):
    """Limpia la base de datos antes de cada test"""
    with app.app_context():
        # Limpiar todas las tablas
        db.session.query(Order).delete()
        db.session.query(Product).delete()
        db.session.query(Category).delete()
        db.session.query(User).delete()
        db.session.commit()
        yield
        db.session.query(Order).delete()
        db.session.query(Product).delete()
        db.session.query(Category).delete()
        db.session.query(User).delete()
        db.session.commit()

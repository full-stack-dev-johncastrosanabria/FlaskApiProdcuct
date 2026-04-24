#!/usr/bin/env python3
"""
Script para inicializar la base de datos con datos de ejemplo
"""
from app import create_app
from app.database import db
from app.models import User, Product, Category, Order, OrderItem
from datetime import datetime, timedelta
import random

def init_database():
    """Inicializa la base de datos con datos de ejemplo"""
    app = create_app('development')
    
    with app.app_context():
        # Eliminar todas las tablas y recrearlas
        print("🗑️  Eliminando tablas existentes...")
        db.drop_all()
        
        print("📦 Creando tablas...")
        db.create_all()
        
        # Crear categorías
        print("📁 Creando categorías...")
        categories = [
            Category(name='Electrónica', description='Dispositivos electrónicos y accesorios'),
            Category(name='Ropa', description='Prendas de vestir y accesorios'),
            Category(name='Hogar', description='Artículos para el hogar'),
            Category(name='Deportes', description='Equipamiento deportivo'),
            Category(name='Libros', description='Libros y material de lectura')
        ]
        
        for category in categories:
            category.save()
        
        # Crear usuarios
        print("👤 Creando usuarios...")
        users = [
            User(name='Juan Pérez', email='juan@example.com'),
            User(name='María García', email='maria@example.com'),
            User(name='Carlos López', email='carlos@example.com'),
            User(name='Ana Martínez', email='ana@example.com'),
            User(name='Luis Rodríguez', email='luis@example.com')
        ]
        
        for user in users:
            user.save()
        
        # Crear productos
        print("📦 Creando productos...")
        products = [
            # Electrónica
            Product(name='Laptop HP', description='Laptop de alta gama', price=999.99, stock=15, category_id=1),
            Product(name='Mouse Logitech', description='Mouse inalámbrico', price=25.99, stock=50, category_id=1),
            Product(name='Teclado Mecánico', description='Teclado gaming RGB', price=79.99, stock=30, category_id=1),
            Product(name='Monitor Samsung 27"', description='Monitor Full HD', price=299.99, stock=20, category_id=1),
            Product(name='Auriculares Sony', description='Auriculares con cancelación de ruido', price=149.99, stock=25, category_id=1),
            
            # Ropa
            Product(name='Camiseta Nike', description='Camiseta deportiva', price=29.99, stock=100, category_id=2),
            Product(name='Jeans Levis', description='Jeans clásicos', price=59.99, stock=75, category_id=2),
            Product(name='Zapatillas Adidas', description='Zapatillas running', price=89.99, stock=40, category_id=2),
            
            # Hogar
            Product(name='Cafetera Nespresso', description='Cafetera automática', price=199.99, stock=12, category_id=3),
            Product(name='Aspiradora Dyson', description='Aspiradora sin cable', price=399.99, stock=8, category_id=3),
            
            # Deportes
            Product(name='Bicicleta Trek', description='Bicicleta de montaña', price=599.99, stock=10, category_id=4),
            Product(name='Balón Nike', description='Balón de fútbol profesional', price=39.99, stock=60, category_id=4),
            
            # Libros
            Product(name='Clean Code', description='Libro de programación', price=45.99, stock=30, category_id=5),
            Product(name='El Quijote', description='Clásico de la literatura', price=19.99, stock=50, category_id=5)
        ]
        
        for product in products:
            product.save()
        
        # Crear órdenes de ejemplo
        print("🛒 Creando órdenes...")
        for i in range(20):
            # Seleccionar usuario aleatorio
            user = random.choice(users)
            
            # Crear orden
            order = Order(
                user_id=user.id,
                total=0,
                status=random.choice(['completed', 'completed', 'completed', 'pending'])
            )
            
            # Fecha aleatoria en los últimos 60 días
            days_ago = random.randint(0, 60)
            order.created_at = datetime.utcnow() - timedelta(days=days_ago)
            order.save()
            
            # Agregar items aleatorios
            num_items = random.randint(1, 4)
            total = 0
            
            for _ in range(num_items):
                product = random.choice(products)
                quantity = random.randint(1, 3)
                price = product.price
                subtotal = float(price) * quantity
                total += subtotal
                
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=quantity,
                    price=price,
                    subtotal=subtotal
                )
                order_item.save()
            
            # Actualizar total de la orden
            order.update(total=total)
        
        print("✅ Base de datos inicializada correctamente!")
        print(f"   - {len(categories)} categorías")
        print(f"   - {len(users)} usuarios")
        print(f"   - {len(products)} productos")
        print(f"   - 20 órdenes de ejemplo")


if __name__ == '__main__':
    init_database()

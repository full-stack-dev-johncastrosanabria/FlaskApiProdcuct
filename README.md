# 🚀 API REST con Flask + MySQL + Análisis de Datos

API REST profesional desarrollada con Flask, MySQL y módulo de análisis de datos, siguiendo las mejores prácticas de arquitectura y desarrollo.

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Arquitectura](#-arquitectura)
- [Tecnologías](#-tecnologías)
- [Instalación](#-instalación)
- [Configuración de MySQL](#-configuración-de-mysql)
- [Uso](#-uso)
- [API Endpoints](#-api-endpoints)
- [Módulo de Análisis](#-módulo-de-análisis)
- [Testing](#-testing)
- [Cliente Web](#-cliente-web)
- [Mejores Prácticas](#-mejores-prácticas)
- [Despliegue](#-despliegue)

---

## ✨ Características

### Backend
- ✅ **API REST completa** con Flask
- ✅ **Base de datos MySQL** con SQLAlchemy ORM
- ✅ **5 modelos de datos**: Users, Products, Categories, Orders, OrderItems
- ✅ **Módulo de análisis de datos** con pandas y numpy
- ✅ **Application Factory Pattern**
- ✅ **Blueprints** para modularización
- ✅ **CORS** configurado
- ✅ **Validación de datos**
- ✅ **Manejo de errores** global

### Análisis de Datos
- ✅ **Análisis de ventas**: Total, por período, top productos, top clientes
- ✅ **Análisis de inventario**: Stock bajo, valor total, por categoría
- ✅ **Dashboard**: Resumen completo de métricas
- ✅ **Reportes**: Ventas por categoría, productos más vendidos

### Frontend
- ✅ **Cliente web moderno** y responsive
- ✅ **Gestión completa** de usuarios, productos, categorías y órdenes
- ✅ **Dashboard de análisis** con métricas en tiempo real
- ✅ **Filtros** y búsquedas avanzadas

---

## 🏗️ Arquitectura

```
flask-api/
├── app/
│   ├── __init__.py              # Application Factory
│   ├── database.py              # Configuración de SQLAlchemy
│   ├── models/                  # Modelos de datos (ORM)
│   │   ├── user.py             # Usuario
│   │   ├── product.py          # Producto
│   │   ├── category.py         # Categoría
│   │   └── order.py            # Orden y OrderItem
│   ├── routes/                  # Blueprints (API endpoints)
│   │   ├── main.py             # Rutas principales
│   │   ├── users.py            # CRUD usuarios
│   │   ├── products.py         # CRUD productos
│   │   ├── categories.py       # CRUD categorías
│   │   ├── orders.py           # CRUD órdenes
│   │   ├── analytics.py        # Endpoints de análisis
│   │   └── errors.py           # Manejo de errores
│   ├── analytics/               # Módulo de análisis de datos
│   │   ├── sales_analytics.py  # Análisis de ventas
│   │   └── inventory_analytics.py # Análisis de inventario
│   └── utils/                   # Utilidades
│       ├── validators.py       # Validadores
│       └── responses.py        # Respuestas estandarizadas
├── client/                      # Cliente web
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── tests/                       # Suite de tests
├── config.py                    # Configuraciones
├── run.py                       # Punto de entrada
├── init_db.py                   # Script de inicialización
└── requirements.txt             # Dependencias
```

### Patrones Implementados
1. **Application Factory** - Instancias configurables
2. **Blueprints** - Modularización de rutas
3. **ORM (SQLAlchemy)** - Abstracción de base de datos
4. **Repository Pattern** - Métodos de acceso a datos
5. **Separation of Concerns** - Capas bien definidas

---

## 🛠️ Tecnologías

### Backend
- **Flask 3.0.0** - Framework web
- **Flask-SQLAlchemy 3.1.1** - ORM
- **PyMySQL 1.1.0** - Conector MySQL
- **Flask-CORS 4.0.0** - Manejo de CORS
- **Python-dotenv 1.0.0** - Variables de entorno

### Análisis de Datos
- **Pandas 2.1.4** - Manipulación de datos
- **NumPy 1.26.2** - Cálculos numéricos

### Testing
- **Pytest 7.4.3** - Framework de testing
- **Pytest-Flask 1.3.0** - Testing para Flask
- **Pytest-Cov 4.1.0** - Cobertura de código

### Base de Datos
- **MySQL 8.0+** - Base de datos relacional

---

## 📦 Instalación

### 1. Requisitos Previos
- Python 3.8+
- MySQL 8.0+
- pip3

### 2. Clonar el Proyecto
```bash
git clone <repository-url>
cd flask-api
```

### 3. Crear Entorno Virtual
```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 4. Instalar Dependencias
```bash
pip3 install -r requirements.txt
```

### 5. Configurar Variables de Entorno
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

---

## 🗄️ Configuración de MySQL

### 1. Instalar MySQL
```bash
# macOS
brew install mysql
brew services start mysql

# Ubuntu/Debian
sudo apt-get install mysql-server
sudo systemctl start mysql

# Windows
# Descargar desde https://dev.mysql.com/downloads/mysql/
```

### 2. Crear Base de Datos
```bash
mysql -u root -p
```

```sql
CREATE DATABASE flask_api_dev CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'flask_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON flask_api_dev.* TO 'flask_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 3. Configurar Conexión
Editar `.env`:
```bash
DATABASE_URL=mysql+pymysql://flask_user:your_password@localhost:3306/flask_api_dev
```

### 4. Inicializar Base de Datos
```bash
python3 init_db.py
```

Este script creará:
- ✅ 5 tablas (users, products, categories, orders, order_items)
- ✅ 5 categorías de ejemplo
- ✅ 5 usuarios de ejemplo
- ✅ 14 productos de ejemplo
- ✅ 20 órdenes de ejemplo con items

---

## 🚀 Uso

### Iniciar la Aplicación
```bash
python3 run.py
```

La API estará disponible en: `http://localhost:5001`

### Abrir Cliente Web
```bash
open client/index.html
```

### Verificar Funcionamiento
```bash
curl http://localhost:5001/api/health
```

---

## 📡 API Endpoints

### Generales
- `GET /` - Información de la API
- `GET /api/health` - Health check

### Usuarios
- `GET /api/users` - Listar todos los usuarios
- `GET /api/users/{id}` - Obtener usuario por ID
- `POST /api/users` - Crear usuario
- `PUT /api/users/{id}` - Actualizar usuario
- `DELETE /api/users/{id}` - Eliminar usuario

### Productos
- `GET /api/products` - Listar productos (con filtros)
- `GET /api/products/{id}` - Obtener producto por ID
- `POST /api/products` - Crear producto
- `PUT /api/products/{id}` - Actualizar producto
- `DELETE /api/products/{id}` - Eliminar producto

**Filtros disponibles:**
- `min_price` - Precio mínimo
- `max_price` - Precio máximo
- `category` - Nombre de categoría

### Categorías
- `GET /api/categories` - Listar todas las categorías
- `GET /api/categories/{id}` - Obtener categoría por ID
- `POST /api/categories` - Crear categoría
- `DELETE /api/categories/{id}` - Eliminar categoría

### Órdenes
- `GET /api/orders` - Listar órdenes (con filtros)
- `GET /api/orders/{id}` - Obtener orden por ID
- `POST /api/orders` - Crear orden
- `PUT /api/orders/{id}` - Actualizar estado de orden
- `DELETE /api/orders/{id}` - Eliminar orden

**Filtros disponibles:**
- `status` - Estado de la orden (pending, completed, cancelled)
- `user_id` - ID del usuario

### Análisis
- `GET /api/analytics/dashboard` - Dashboard completo
- `GET /api/analytics/sales/total` - Total de ventas
- `GET /api/analytics/sales/by-period` - Ventas por período
- `GET /api/analytics/sales/top-products` - Productos más vendidos
- `GET /api/analytics/sales/top-customers` - Mejores clientes
- `GET /api/analytics/sales/by-category` - Ventas por categoría
- `GET /api/analytics/inventory/low-stock` - Productos con stock bajo
- `GET /api/analytics/inventory/out-of-stock` - Productos sin stock
- `GET /api/analytics/inventory/value` - Valor total del inventario
- `GET /api/analytics/inventory/by-category` - Inventario por categoría

---

## 📊 Módulo de Análisis

### Análisis de Ventas (`SalesAnalytics`)

#### 1. Total de Ventas
```python
from app.analytics.sales_analytics import SalesAnalytics

# Total de ventas
total = SalesAnalytics.get_total_sales()

# Ventas en un período
from datetime import datetime, timedelta
start = datetime.now() - timedelta(days=30)
total_month = SalesAnalytics.get_total_sales(start_date=start)
```

#### 2. Ventas por Período
```python
# Ventas por día (últimos 30 días)
daily_sales = SalesAnalytics.get_sales_by_period(period='day', limit=30)

# Ventas por semana
weekly_sales = SalesAnalytics.get_sales_by_period(period='week', limit=12)

# Ventas por mes
monthly_sales = SalesAnalytics.get_sales_by_period(period='month', limit=12)
```

#### 3. Top Productos
```python
# Top 10 productos más vendidos
top_products = SalesAnalytics.get_top_products(limit=10)
```

#### 4. Top Clientes
```python
# Top 10 clientes con más compras
top_customers = SalesAnalytics.get_top_customers(limit=10)
```

#### 5. Ventas por Categoría
```python
# Ventas agrupadas por categoría
sales_by_category = SalesAnalytics.get_sales_by_category()
```

#### 6. Dashboard Summary
```python
# Resumen completo para dashboard
summary = SalesAnalytics.get_dashboard_summary()
# Retorna: total_sales, total_orders, total_customers, total_products,
#          average_order_value, last_month_sales, pending_orders
```

### Análisis de Inventario (`InventoryAnalytics`)

#### 1. Productos con Stock Bajo
```python
from app.analytics.inventory_analytics import InventoryAnalytics

# Productos con stock <= 10
low_stock = InventoryAnalytics.get_low_stock_products(threshold=10)
```

#### 2. Productos Sin Stock
```python
# Productos con stock = 0
out_of_stock = InventoryAnalytics.get_out_of_stock_products()
```

#### 3. Valor del Inventario
```python
# Valor total del inventario (precio * stock)
total_value = InventoryAnalytics.get_inventory_value()
```

#### 4. Inventario por Categoría
```python
# Inventario agrupado por categoría
inventory_by_category = InventoryAnalytics.get_inventory_by_category()
```

#### 5. Resumen de Inventario
```python
# Resumen completo
summary = InventoryAnalytics.get_inventory_summary()
# Retorna: total_products, total_stock, total_value,
#          low_stock_count, out_of_stock_count
```

---

## 📝 Ejemplos de Uso

### Crear un Usuario
```bash
curl -X POST http://localhost:5001/api/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Juan Pérez","email":"juan@example.com"}'
```

### Crear una Categoría
```bash
curl -X POST http://localhost:5001/api/categories \
  -H "Content-Type: application/json" \
  -d '{"name":"Electrónica","description":"Dispositivos electrónicos"}'
```

### Crear un Producto
```bash
curl -X POST http://localhost:5001/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "name":"Laptop HP",
    "price":999.99,
    "stock":10,
    "category_id":1,
    "description":"Laptop de alta gama"
  }'
```

### Crear una Orden
```bash
curl -X POST http://localhost:5001/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "user_id":1,
    "items":[
      {"product_id":1,"quantity":2},
      {"product_id":2,"quantity":1}
    ]
  }'
```

### Obtener Dashboard de Análisis
```bash
curl http://localhost:5001/api/analytics/dashboard
```

### Obtener Top 10 Productos
```bash
curl http://localhost:5001/api/analytics/sales/top-products?limit=10
```

### Obtener Productos con Stock Bajo
```bash
curl http://localhost:5001/api/analytics/inventory/low-stock?threshold=10
```

---

## 🧪 Testing

### Ejecutar Todos los Tests
```bash
python3 -m pytest tests/ -v
```

### Tests con Cobertura
```bash
python3 -m pytest tests/ --cov=app --cov-report=html
```

### Ver Reporte de Cobertura
```bash
open htmlcov/index.html
```

---

## 🎨 Cliente Web

### Características
- ✅ **Dashboard de análisis** con métricas en tiempo real
- ✅ **Gestión de usuarios** - CRUD completo
- ✅ **Gestión de productos** - CRUD completo con categorías
- ✅ **Gestión de categorías** - Crear y eliminar
- ✅ **Gestión de órdenes** - Crear y visualizar
- ✅ **Filtros avanzados** - Por precio, categoría, estado
- ✅ **Gráficos y estadísticas** - Ventas, inventario, top productos
- ✅ **Responsive design** - Funciona en móviles y tablets

### Uso del Cliente
1. Abrir `client/index.html` en el navegador
2. Verificar que el indicador muestre "API Conectada"
3. Navegar entre las diferentes secciones usando los tabs
4. Usar los formularios para crear nuevos registros
5. Ver el dashboard de análisis para métricas en tiempo real

---

## 🏆 Mejores Prácticas Implementadas

### Arquitectura
- ✅ **Application Factory Pattern** - Instancias configurables
- ✅ **Blueprints** - Modularización de rutas
- ✅ **ORM (SQLAlchemy)** - Abstracción de base de datos
- ✅ **Separation of Concerns** - Modelos, rutas, lógica separados
- ✅ **Configuration Management** - Configuración por entornos

### Base de Datos
- ✅ **Relaciones** - Foreign keys y relaciones definidas
- ✅ **Índices** - En campos de búsqueda frecuente
- ✅ **Timestamps** - created_at y updated_at automáticos
- ✅ **Cascadas** - Eliminación en cascada configurada
- ✅ **Transacciones** - Rollback en caso de error

### Código Limpio
- ✅ **Nombres descriptivos** - Variables y funciones claras
- ✅ **Funciones pequeñas** - Una responsabilidad por función
- ✅ **DRY** - No repetir código
- ✅ **Comentarios útiles** - Explicar el "por qué"
- ✅ **Validación** - Validación de datos centralizada

### Seguridad
- ✅ **Variables de entorno** - Secretos no en el código
- ✅ **Validación de entrada** - Todos los datos validados
- ✅ **CORS configurado** - Orígenes controlados
- ✅ **SQL Injection** - Protegido por ORM
- ✅ **Manejo de errores** - Sin exponer detalles internos

### Análisis de Datos
- ✅ **Queries optimizadas** - Uso de agregaciones SQL
- ✅ **Índices** - Para mejorar performance
- ✅ **Cálculos eficientes** - Usando funciones de base de datos
- ✅ **Caché** - Preparado para implementar caché

---

## 🗄️ Esquema de Base de Datos

### Tabla: users
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INT (PK) | ID auto-incremental |
| name | VARCHAR(255) | Nombre del usuario |
| email | VARCHAR(255) | Email único |
| created_at | DATETIME | Fecha de creación |
| updated_at | DATETIME | Fecha de actualización |

### Tabla: categories
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INT (PK) | ID auto-incremental |
| name | VARCHAR(100) | Nombre único |
| description | TEXT | Descripción |
| created_at | DATETIME | Fecha de creación |

### Tabla: products
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INT (PK) | ID auto-incremental |
| name | VARCHAR(255) | Nombre del producto |
| description | TEXT | Descripción |
| price | DECIMAL(10,2) | Precio |
| stock | INT | Stock disponible |
| category_id | INT (FK) | Referencia a categories |
| created_at | DATETIME | Fecha de creación |
| updated_at | DATETIME | Fecha de actualización |

### Tabla: orders
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INT (PK) | ID auto-incremental |
| user_id | INT (FK) | Referencia a users |
| total | DECIMAL(10,2) | Total de la orden |
| status | VARCHAR(50) | Estado (pending/completed/cancelled) |
| created_at | DATETIME | Fecha de creación |
| updated_at | DATETIME | Fecha de actualización |

### Tabla: order_items
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INT (PK) | ID auto-incremental |
| order_id | INT (FK) | Referencia a orders |
| product_id | INT (FK) | Referencia a products |
| quantity | INT | Cantidad |
| price | DECIMAL(10,2) | Precio al momento de compra |
| subtotal | DECIMAL(10,2) | Subtotal (price * quantity) |

### Relaciones
- **users** 1:N **orders** - Un usuario puede tener muchas órdenes
- **categories** 1:N **products** - Una categoría tiene muchos productos
- **orders** 1:N **order_items** - Una orden tiene muchos items
- **products** 1:N **order_items** - Un producto puede estar en muchos items

---

## 🚀 Despliegue

### Desarrollo
```bash
export FLASK_ENV=development
python3 run.py
```

### Producción con Gunicorn
```bash
# Instalar Gunicorn
pip3 install gunicorn

# Ejecutar
export FLASK_ENV=production
export DATABASE_URL=mysql+pymysql://user:pass@host:3306/db
gunicorn -w 4 -b 0.0.0.0:5001 "app:create_app('production')"
```

### Docker (Opcional)
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5001

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5001", "app:create_app('production')"]
```

### Variables de Entorno en Producción
```bash
FLASK_ENV=production
SECRET_KEY=your-very-secret-key
DATABASE_URL=mysql+pymysql://user:password@host:3306/database
PORT=5001
```

---

## 📊 Métricas del Proyecto

### Código
- **Líneas de código Python:** ~2,000
- **Líneas de código JavaScript:** ~450
- **Líneas de código CSS:** ~400
- **Total:** ~2,850 líneas

### Archivos
- **Modelos:** 5 (User, Product, Category, Order, OrderItem)
- **Rutas (Blueprints):** 6
- **Módulos de análisis:** 2
- **Tests:** 23 tests unitarios

### Base de Datos
- **Tablas:** 5
- **Relaciones:** 4
- **Índices:** Configurados en campos clave

---

## 🔧 Solución de Problemas

### Error: "Access denied for user"
```bash
# Verificar credenciales en .env
# Crear usuario con permisos correctos
mysql -u root -p
GRANT ALL PRIVILEGES ON flask_api_dev.* TO 'flask_user'@'localhost';
```

### Error: "No module named 'MySQLdb'"
```bash
pip3 install pymysql cryptography
```

### Error: "Table doesn't exist"
```bash
# Reinicializar base de datos
python3 init_db.py
```

### Puerto 5001 en uso
```bash
# Cambiar puerto en .env
PORT=5002
```

---

## 📚 Recursos Adicionales

### Documentación
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

### Tutoriales
- [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
- [SQLAlchemy Tutorial](https://docs.sqlalchemy.org/en/14/tutorial/)

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está bajo la licencia MIT.

---

## 👨‍💻 Autor

Desarrollado como ejemplo de API REST profesional con Flask, MySQL y análisis de datos.

---

## 🎯 Resumen Ejecutivo

Este proyecto demuestra una implementación profesional de:

✅ **API REST** con Flask y MySQL  
✅ **5 modelos de datos** con relaciones  
✅ **Módulo de análisis** con pandas y numpy  
✅ **30+ endpoints** documentados  
✅ **Cliente web** moderno y funcional  
✅ **Mejores prácticas** de arquitectura y código  
✅ **Listo para producción**

**El proyecto está completo, probado y listo para ser usado como base para aplicaciones reales.**

---

**Versión:** 2.0.0  
**Última actualización:** Abril 24, 2026  
**Estado:** ✅ Completado y Probado

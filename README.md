# API REST con Flask

API REST completa desarrollada con Flask siguiendo las mejores prácticas y patrones de arquitectura profesional.

## 📋 Características

- ✅ **Arquitectura modular** con Application Factory Pattern
- ✅ **Blueprints** para organización de rutas
- ✅ **Modelos** separados con lógica de negocio
- ✅ **Validadores** centralizados
- ✅ **Respuestas estandarizadas** con utilidades reutilizables
- ✅ **Configuración por entornos** (development, production, testing)
- ✅ CRUD completo para Usuarios y Productos
- ✅ Filtros de búsqueda para productos
- ✅ Manejo de errores global
- ✅ Health check endpoint

## 🏗️ Arquitectura del Proyecto

```
flask-api/
├── app/
│   ├── __init__.py              # Application Factory
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py              # Modelo de Usuario
│   │   └── product.py           # Modelo de Producto
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── main.py              # Rutas principales
│   │   ├── users.py             # Blueprint de usuarios
│   │   ├── products.py          # Blueprint de productos
│   │   └── errors.py            # Manejadores de errores
│   └── utils/
│       ├── __init__.py
│       ├── validators.py        # Validadores de datos
│       └── responses.py         # Utilidades de respuestas
├── config.py                    # Configuraciones por entorno
├── run.py                       # Punto de entrada
├── requirements.txt             # Dependencias
├── .gitignore
└── README.md
```

### Patrones de Diseño Implementados

1. **Application Factory Pattern**: Permite crear múltiples instancias de la app con diferentes configuraciones
2. **Blueprints**: Organiza las rutas en módulos independientes y reutilizables
3. **Separation of Concerns**: Separa modelos, rutas, validadores y utilidades
4. **DRY (Don't Repeat Yourself)**: Utilidades centralizadas para respuestas y validaciones

## 🚀 Instalación

### Requisitos previos
- Python 3.8 o superior
- pip

### Pasos de instalación

1. **Clonar o descargar el proyecto**

2. **Crear un entorno virtual (recomendado)**
```bash
python -m venv venv
```

3. **Activar el entorno virtual**
   - En Windows:
   ```bash
   venv\Scripts\activate
   ```
   - En macOS/Linux:
   ```bash
   source venv/bin/activate
   ```

4. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

5. **Ejecutar la aplicación**

   **Modo desarrollo:**
   ```bash
   python run.py
   ```
   
   **O con Flask CLI:**
   ```bash
   export FLASK_APP=run.py
   export FLASK_ENV=development
   flask run
   ```
   
   **Modo producción con Gunicorn:**
   ```bash
   pip install gunicorn
   export FLASK_ENV=production
   gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app('production')"
   ```

La API estará disponible en `http://localhost:5000`

## 📚 Documentación de Endpoints

### Endpoints Generales

#### GET /
Información general de la API
```bash
curl http://localhost:5000/
```

#### GET /api/health
Verificar estado de la API
```bash
curl http://localhost:5000/api/health
```

---

### 👤 Endpoints de Usuarios

#### GET /api/users
Obtener todos los usuarios

**Ejemplo:**
```bash
curl http://localhost:5000/api/users
```

**Respuesta:**
```json
{
  "success": true,
  "data": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "name": "Juan Pérez",
      "email": "juan@example.com",
      "created_at": "2026-04-24T10:30:00"
    }
  ],
  "count": 1
}
```

#### GET /api/users/{user_id}
Obtener un usuario específico

**Ejemplo:**
```bash
curl http://localhost:5000/api/users/123e4567-e89b-12d3-a456-426614174000
```

#### POST /api/users
Crear un nuevo usuario

**Body (JSON):**
```json
{
  "name": "Juan Pérez",
  "email": "juan@example.com"
}
```

**Ejemplo:**
```bash
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Juan Pérez","email":"juan@example.com"}'
```

**Respuesta:**
```json
{
  "success": true,
  "data": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "name": "Juan Pérez",
    "email": "juan@example.com",
    "created_at": "2026-04-24T10:30:00"
  },
  "message": "Usuario creado exitosamente"
}
```

#### PUT /api/users/{user_id}
Actualizar un usuario existente

**Body (JSON):**
```json
{
  "name": "Juan Pérez Actualizado",
  "email": "juan.nuevo@example.com"
}
```

**Ejemplo:**
```bash
curl -X PUT http://localhost:5000/api/users/123e4567-e89b-12d3-a456-426614174000 \
  -H "Content-Type: application/json" \
  -d '{"name":"Juan Pérez Actualizado"}'
```

#### DELETE /api/users/{user_id}
Eliminar un usuario

**Ejemplo:**
```bash
curl -X DELETE http://localhost:5000/api/users/123e4567-e89b-12d3-a456-426614174000
```

---

### 📦 Endpoints de Productos

#### GET /api/products
Obtener todos los productos (con filtros opcionales)

**Query Parameters:**
- `min_price` (opcional): Precio mínimo
- `max_price` (opcional): Precio máximo
- `category` (opcional): Categoría del producto

**Ejemplos:**
```bash
# Todos los productos
curl http://localhost:5000/api/products

# Productos con precio entre 10 y 50
curl "http://localhost:5000/api/products?min_price=10&max_price=50"

# Productos de categoría "electrónica"
curl "http://localhost:5000/api/products?category=electrónica"
```

**Respuesta:**
```json
{
  "success": true,
  "data": [
    {
      "id": "456e7890-e89b-12d3-a456-426614174000",
      "name": "Laptop",
      "price": 999.99,
      "category": "electrónica",
      "description": "Laptop de alta gama",
      "stock": 10,
      "created_at": "2026-04-24T10:30:00"
    }
  ],
  "count": 1
}
```

#### GET /api/products/{product_id}
Obtener un producto específico

**Ejemplo:**
```bash
curl http://localhost:5000/api/products/456e7890-e89b-12d3-a456-426614174000
```

#### POST /api/products
Crear un nuevo producto

**Body (JSON):**
```json
{
  "name": "Laptop",
  "price": 999.99,
  "category": "electrónica",
  "description": "Laptop de alta gama",
  "stock": 10
}
```

**Campos requeridos:** `name`, `price`, `category`  
**Campos opcionales:** `description`, `stock`

**Ejemplo:**
```bash
curl -X POST http://localhost:5000/api/products \
  -H "Content-Type: application/json" \
  -d '{"name":"Laptop","price":999.99,"category":"electrónica","description":"Laptop de alta gama","stock":10}'
```

#### PUT /api/products/{product_id}
Actualizar un producto existente

**Body (JSON):**
```json
{
  "name": "Laptop Pro",
  "price": 1299.99,
  "stock": 5
}
```

**Ejemplo:**
```bash
curl -X PUT http://localhost:5000/api/products/456e7890-e89b-12d3-a456-426614174000 \
  -H "Content-Type: application/json" \
  -d '{"price":1299.99,"stock":5}'
```

#### DELETE /api/products/{product_id}
Eliminar un producto

**Ejemplo:**
```bash
curl -X DELETE http://localhost:5000/api/products/456e7890-e89b-12d3-a456-426614174000
```

---

## 📊 Formato de Respuestas

Todas las respuestas siguen un formato JSON estandarizado:

### Respuesta Exitosa
```json
{
  "success": true,
  "data": { ... },
  "message": "Mensaje opcional"
}
```

### Respuesta de Error
```json
{
  "success": false,
  "error": "Descripción del error"
}
```

---

## 🔧 Códigos de Estado HTTP

- `200 OK` - Solicitud exitosa
- `201 Created` - Recurso creado exitosamente
- `400 Bad Request` - Datos inválidos o faltantes
- `404 Not Found` - Recurso no encontrado
- `500 Internal Server Error` - Error del servidor

---

## 🧪 Pruebas con cURL

### Flujo completo de ejemplo

```bash
# 1. Verificar que la API está funcionando
curl http://localhost:5000/api/health

# 2. Crear un usuario
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name":"María García","email":"maria@example.com"}'

# 3. Crear un producto
curl -X POST http://localhost:5000/api/products \
  -H "Content-Type: application/json" \
  -d '{"name":"Mouse","price":25.99,"category":"accesorios","stock":50}'

# 4. Listar todos los usuarios
curl http://localhost:5000/api/users

# 5. Listar todos los productos
curl http://localhost:5000/api/products

# 6. Filtrar productos por precio
curl "http://localhost:5000/api/products?min_price=20&max_price=30"
```

---

## 🛠️ Tecnologías y Patrones Utilizados

- **Flask 3.0.0** - Framework web minimalista para Python
- **Python 3.8+** - Lenguaje de programación
- **Application Factory Pattern** - Patrón de creación de aplicaciones
- **Blueprints** - Modularización de rutas
- **MVC Pattern** - Separación de modelos, vistas y controladores

---

## 📝 Notas Importantes

### Base de Datos
Esta API utiliza almacenamiento en memoria para demostración. Los datos se pierden al reiniciar la aplicación. Para producción, se recomienda integrar una base de datos real como:
- **PostgreSQL** con SQLAlchemy
- **MySQL** con SQLAlchemy
- **MongoDB** con PyMongo
- **SQLite** para desarrollo

### Configuración por Entornos
El proyecto soporta múltiples entornos configurables:

```bash
# Desarrollo (por defecto)
export FLASK_ENV=development
python run.py

# Producción
export FLASK_ENV=production
python run.py

# Testing
export FLASK_ENV=testing
python run.py
```

### Despliegue en Producción
Para producción, usar un servidor WSGI como Gunicorn:

```bash
# Instalar Gunicorn
pip install gunicorn

# Ejecutar con 4 workers
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app('production')"

# Con logs
gunicorn -w 4 -b 0.0.0.0:5000 --access-logfile - --error-logfile - "app:create_app('production')"
```

---

## 🔧 Extensiones Recomendadas

Para llevar esta API al siguiente nivel, considera agregar:

### Base de Datos con SQLAlchemy
```bash
pip install flask-sqlalchemy psycopg2-binary
```

### Autenticación JWT
```bash
pip install flask-jwt-extended
```

### Validación con Marshmallow
```bash
pip install flask-marshmallow marshmallow-sqlalchemy
```

### CORS
```bash
pip install flask-cors
```

### Migraciones de Base de Datos
```bash
pip install flask-migrate
```

### Rate Limiting
```bash
pip install flask-limiter
```

## 🚀 Próximas Mejoras

- [ ] Autenticación y autorización (JWT)
- [ ] Paginación de resultados
- [ ] Integración con SQLAlchemy
- [ ] Validación con Marshmallow schemas
- [ ] Rate limiting
- [ ] Logging estructurado
- [ ] Tests unitarios y de integración
- [ ] Documentación con Swagger/OpenAPI
- [ ] CORS configurado
- [ ] Migraciones de base de datos con Flask-Migrate

---

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

---

## 👨‍💻 Autor

Desarrollado como ejemplo de API REST con Flask.

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o pull request para sugerencias o mejoras.

# 🗄️ Guía de Configuración de MySQL

## Instalación de MySQL

### macOS
```bash
# Instalar con Homebrew
brew install mysql

# Iniciar servicio
brew services start mysql

# Configurar seguridad (opcional)
mysql_secure_installation
```

### Ubuntu/Debian
```bash
# Instalar
sudo apt-get update
sudo apt-get install mysql-server

# Iniciar servicio
sudo systemctl start mysql
sudo systemctl enable mysql

# Configurar seguridad
sudo mysql_secure_installation
```

### Windows
1. Descargar desde: https://dev.mysql.com/downloads/mysql/
2. Ejecutar el instalador
3. Seguir el asistente de instalación
4. Configurar contraseña de root

---

## Configuración de la Base de Datos

### 1. Acceder a MySQL
```bash
mysql -u root -p
# Ingresar contraseña cuando se solicite
```

### 2. Crear Base de Datos y Usuario

```sql
-- Crear base de datos para desarrollo
CREATE DATABASE flask_api_dev CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Crear base de datos para producción (opcional)
CREATE DATABASE flask_api_prod CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Crear usuario
CREATE USER 'flask_user'@'localhost' IDENTIFIED BY 'your_secure_password';

-- Otorgar permisos
GRANT ALL PRIVILEGES ON flask_api_dev.* TO 'flask_user'@'localhost';
GRANT ALL PRIVILEGES ON flask_api_prod.* TO 'flask_user'@'localhost';

-- Aplicar cambios
FLUSH PRIVILEGES;

-- Salir
EXIT;
```

### 3. Verificar Conexión
```bash
mysql -u flask_user -p flask_api_dev
# Ingresar contraseña
```

---

## Configuración de Variables de Entorno

### Archivo .env
```bash
# Copiar ejemplo
cp .env.example .env

# Editar .env
nano .env
```

### Contenido del .env
```bash
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
PORT=5001

# Base de datos MySQL
DATABASE_URL=mysql+pymysql://flask_user:your_secure_password@localhost:3306/flask_api_dev
```

---

## Inicializar Base de Datos

### Opción 1: Con Datos de Ejemplo
```bash
python3 init_db.py
```

Este script creará:
- ✅ 5 tablas (users, products, categories, orders, order_items)
- ✅ 5 categorías de ejemplo
- ✅ 5 usuarios de ejemplo
- ✅ 14 productos de ejemplo
- ✅ 20 órdenes de ejemplo

### Opción 2: Solo Tablas (Sin Datos)
```python
from app import create_app
from app.database import db

app = create_app('development')
with app.app_context():
    db.create_all()
    print("Tablas creadas exitosamente")
```

---

## Verificar Tablas Creadas

```bash
mysql -u flask_user -p flask_api_dev
```

```sql
-- Ver todas las tablas
SHOW TABLES;

-- Ver estructura de una tabla
DESCRIBE users;
DESCRIBE products;
DESCRIBE categories;
DESCRIBE orders;
DESCRIBE order_items;

-- Ver datos de ejemplo
SELECT * FROM users;
SELECT * FROM categories;
SELECT * FROM products LIMIT 5;
```

---

## Comandos Útiles de MySQL

### Ver Bases de Datos
```sql
SHOW DATABASES;
```

### Usar una Base de Datos
```sql
USE flask_api_dev;
```

### Ver Tablas
```sql
SHOW TABLES;
```

### Ver Estructura de Tabla
```sql
DESCRIBE table_name;
```

### Ver Datos
```sql
SELECT * FROM table_name LIMIT 10;
```

### Contar Registros
```sql
SELECT COUNT(*) FROM table_name;
```

### Eliminar Todos los Datos (Cuidado!)
```sql
TRUNCATE TABLE table_name;
```

### Eliminar Base de Datos (Cuidado!)
```sql
DROP DATABASE database_name;
```

---

## Solución de Problemas

### Error: "Access denied for user"
```bash
# Verificar usuario y contraseña
mysql -u flask_user -p

# Si no funciona, recrear usuario
mysql -u root -p
DROP USER 'flask_user'@'localhost';
CREATE USER 'flask_user'@'localhost' IDENTIFIED BY 'new_password';
GRANT ALL PRIVILEGES ON flask_api_dev.* TO 'flask_user'@'localhost';
FLUSH PRIVILEGES;
```

### Error: "Can't connect to MySQL server"
```bash
# Verificar que MySQL esté corriendo
# macOS
brew services list
brew services start mysql

# Linux
sudo systemctl status mysql
sudo systemctl start mysql
```

### Error: "Unknown database"
```bash
# Crear la base de datos
mysql -u root -p
CREATE DATABASE flask_api_dev;
```

### Error: "Table doesn't exist"
```bash
# Reinicializar base de datos
python3 init_db.py
```

---

## Backup y Restore

### Hacer Backup
```bash
# Backup completo
mysqldump -u flask_user -p flask_api_dev > backup.sql

# Backup solo estructura
mysqldump -u flask_user -p --no-data flask_api_dev > structure.sql

# Backup solo datos
mysqldump -u flask_user -p --no-create-info flask_api_dev > data.sql
```

### Restaurar Backup
```bash
mysql -u flask_user -p flask_api_dev < backup.sql
```

---

## Configuración para Producción

### 1. Crear Usuario con Permisos Limitados
```sql
CREATE USER 'flask_prod'@'%' IDENTIFIED BY 'very_secure_password';
GRANT SELECT, INSERT, UPDATE, DELETE ON flask_api_prod.* TO 'flask_prod'@'%';
FLUSH PRIVILEGES;
```

### 2. Configurar Conexión Remota (Si es necesario)
```bash
# Editar configuración de MySQL
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf

# Cambiar bind-address
bind-address = 0.0.0.0

# Reiniciar MySQL
sudo systemctl restart mysql
```

### 3. Variables de Entorno en Producción
```bash
DATABASE_URL=mysql+pymysql://flask_prod:password@host:3306/flask_api_prod
```

---

## Monitoreo y Mantenimiento

### Ver Procesos Activos
```sql
SHOW PROCESSLIST;
```

### Ver Tamaño de Bases de Datos
```sql
SELECT 
    table_schema AS 'Database',
    ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS 'Size (MB)'
FROM information_schema.tables
GROUP BY table_schema;
```

### Optimizar Tablas
```sql
OPTIMIZE TABLE users;
OPTIMIZE TABLE products;
OPTIMIZE TABLE orders;
```

---

## Recursos Adicionales

- [MySQL Documentation](https://dev.mysql.com/doc/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [PyMySQL Documentation](https://pymysql.readthedocs.io/)

---

**¡Listo! Tu base de datos MySQL está configurada y lista para usar.**

# 🚀 API REST con Flask + Cliente TypeScript + IA

API REST profesional desarrollada con Flask, SQLite, análisis de datos avanzado, dashboard interactivo y chatbot de IA con base de conocimientos.

**Estado:** ✅ 100% COMPLETADO Y PROBADO  
**Versión:** 4.0.0 (TypeScript + Análisis Avanzado + IA)  
**Última actualización:** Abril 24, 2026

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Arquitectura](#-arquitectura)
- [Tecnologías](#-tecnologías)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [API Endpoints](#-api-endpoints)
- [Cliente Web TypeScript](#-cliente-web-typescript)
- [Módulo de Análisis](#-módulo-de-análisis)
- [Dashboard Interactivo](#-dashboard-interactivo)
- [Chatbot de IA](#-chatbot-de-ia)
- [Testing](#-testing)
- [Solución de Problemas](#-solución-de-problemas)
- [Recursos Adicionales](#-recursos-adicionales)

---

## ✨ Características

### Backend (Flask)
- ✅ **API REST completa** con 40+ endpoints
- ✅ **Base de datos SQLite** con SQLAlchemy ORM
- ✅ **5 modelos de datos**: Users, Products, Categories, Orders, OrderItems
- ✅ **4 módulos de análisis de datos** con pandas y numpy
- ✅ **🤖 Chatbot de IA** con base de conocimientos
- ✅ **Dashboard interactivo** con 7 gráficos en tiempo real
- ✅ **Application Factory Pattern**
- ✅ **Blueprints** para modularización
- ✅ **CORS** configurado
- ✅ **Validación de datos** en todos los endpoints
- ✅ **Manejo de errores** global

### Frontend (TypeScript)
- ✅ **Cliente moderno** con TypeScript y Vite
- ✅ **Arquitectura modular** con 9 componentes especializados
- ✅ **🤖 Interfaz de chat con IA** interactiva
- ✅ **Dashboard interactivo** con gráficos en tiempo real
- ✅ **Sistema de tipos** completo (20+ interfaces)
- ✅ **Gestión de estado** reactiva
- ✅ **Notificaciones toast** elegantes
- ✅ **Diseño responsive** y moderno
- ✅ **Validación de formularios** tipada
- ✅ **Manejo de errores** robusto
- ✅ **7 tipos de gráficos** interactivos

### Análisis de Datos
- ✅ **Dashboard completo** con 6 métricas en tiempo real
- ✅ **Análisis de ventas**: Total, por período, top productos, top clientes, por categoría
- ✅ **Análisis de inventario**: Stock bajo, valor total, por categoría
- ✅ **Análisis Avanzado** (5 vistas):
  - Pronóstico de ventas (30 días con intervalos de confianza)
  - Análisis de cohortes (retención de clientes)
  - Análisis RFM (segmentación avanzada)
  - Matriz de rendimiento de productos
  - Análisis estacional
- ✅ **Inteligencia de Negocios** (5 vistas):
  - Dashboard KPI completo
  - Embudo de conversión
  - Segmentación de clientes (6 segmentos)
  - Análisis ABC
  - Análisis de rentabilidad

### Chatbot de IA
- ✅ **Procesamiento de lenguaje natural** básico
- ✅ **6 categorías de preguntas**: Ventas, Productos, Clientes, Stock, Categorías, Recomendaciones
- ✅ **Respuestas basadas en datos reales** de la base de datos
- ✅ **Niveles de confianza** (0-100%)
- ✅ **Historial de conversación**
- ✅ **Interfaz de chat moderna** con animaciones
- ✅ **Auto-scroll y auto-resize**

---

## 🏗️ Arquitectura

```
FlaskApiProduct/
├── app/                         # Backend Flask
│   ├── __init__.py             # Application Factory
│   ├── database.py             # SQLAlchemy setup
│   ├── models/                 # Modelos ORM (5)
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── category.py
│   │   └── order.py
│   ├── routes/                 # Blueprints (7)
│   │   ├── users.py
│   │   ├── products.py
│   │   ├── categories.py
│   │   ├── orders.py
│   │   ├── analytics.py
│   │   ├── dashboard.py
│   │   └── ai.py
│   ├── analytics/              # Módulos de análisis (5)
│   │   ├── sales_analytics.py
│   │   ├── inventory_analytics.py
│   │   ├── advanced_analytics.py
│   │   ├── business_intelligence.py
│   │   └── dashboard_analytics.py
│   ├── ai/                     # Módulo de IA
│   │   ├── knowledge_base.py
│   │   └── chatbot.py
│   └── utils/                  # Utilidades
│       ├── validators.py
│       └── responses.py
├── client/                     # Frontend TypeScript
│   ├── src/
│   │   ├── components/         # 9 componentes modulares
│   │   │   ├── TabManager.ts
│   │   │   ├── UserManager.ts
│   │   │   ├── ProductManager.ts
│   │   │   ├── DashboardManager.ts
│   │   │   ├── InteractiveDashboard.ts
│   │   │   ├── AdvancedAnalytics.ts
│   │   │   ├── BusinessIntelligence.ts
│   │   │   ├── AIChat.ts
│   │   │   ├── ChartManager.ts
│   │   │   └── HealthIndicator.ts
│   │   ├── services/           # Servicios API
│   │   │   └── api.ts
│   │   ├── types/              # Definiciones TypeScript
│   │   │   └── index.ts
│   │   ├── utils/              # Utilidades
│   │   │   ├── helpers.ts
│   │   │   ├── toast.ts
│   │   │   └── charts.ts
│   │   ├── styles/             # Estilos CSS
│   │   │   └── main.css
│   │   └── main.ts             # Punto de entrada
│   ├── dist/                   # Build compilado
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── index.html
├── tests/                      # Tests unitarios (38)
├── config.py                   # Configuraciones
├── run.py                      # Punto de entrada
├── init_db.py                  # Script de inicialización
└── requirements.txt            # Dependencias Python
```

---

## 🛠️ Tecnologías

### Backend
- **Flask 3.0.0** - Framework web
- **Flask-SQLAlchemy 3.1.1** - ORM
- **Flask-CORS 4.0.0** - Manejo de CORS
- **Pandas 2.1.4** - Análisis de datos
- **NumPy 1.26.2** - Cálculos numéricos

### Frontend
- **TypeScript 5.3.0** - Lenguaje tipado
- **Vite 5.0.0** - Build tool moderno
- **Axios 1.6.0** - Cliente HTTP
- **CSS Variables** - Diseño moderno

### Base de Datos
- **SQLite** - Base de datos embebida (desarrollo)
- **MySQL** - Soporte para producción (opcional)

---

## 📦 Instalación

### 1. Requisitos Previos
- Python 3.8+
- Node.js 18+
- npm o yarn

### 2. Clonar el Proyecto
```bash
git clone <repository-url>
cd FlaskApiProduct
```

### 3. Backend (Flask)
```bash
# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip3 install -r requirements.txt

# Inicializar base de datos
python3 init_db.py
```

### 4. Frontend (TypeScript)
```bash
cd client

# Instalar dependencias
npm install

# Modo desarrollo
npm run dev

# O construir para producción
npm run build
```

---

## 🚀 Uso

### Opción 1: Desarrollo Completo (Recomendado)

#### Terminal 1 - Backend:
```bash
python3 run.py
```
- Servidor en: http://localhost:5001
- API disponible en: http://localhost:5001/api

#### Terminal 2 - Frontend:
```bash
cd client
npm run dev
```
- Cliente en: http://localhost:3000
- Hot reload automático

### Opción 2: Producción

#### Backend
```bash
python3 run.py
```

#### Frontend (Usar archivos compilados)
```bash
# Los archivos están en client/dist/
# Servir con cualquier servidor web (nginx, Apache, etc.)
```

---

## 📡 API Endpoints

### Generales
- `GET /` - Información de la API
- `GET /api/health` - Health check

### Usuarios (5 endpoints)
- `GET /api/users` - Listar usuarios
- `POST /api/users` - Crear usuario
- `GET /api/users/{id}` - Obtener usuario
- `PUT /api/users/{id}` - Actualizar usuario
- `DELETE /api/users/{id}` - Eliminar usuario

### Productos (5 endpoints)
- `GET /api/products` - Listar productos (con filtros)
- `POST /api/products` - Crear producto
- `GET /api/products/{id}` - Obtener producto
- `PUT /api/products/{id}` - Actualizar producto
- `DELETE /api/products/{id}` - Eliminar producto

**Filtros disponibles:**
- `min_price` - Precio mínimo
- `max_price` - Precio máximo
- `category` - Nombre de categoría

### Categorías (4 endpoints)
- `GET /api/categories` - Listar categorías
- `POST /api/categories` - Crear categoría
- `GET /api/categories/{id}` - Obtener categoría
- `DELETE /api/categories/{id}` - Eliminar categoría

### Órdenes (5 endpoints)
- `GET /api/orders` - Listar órdenes
- `POST /api/orders` - Crear orden
- `GET /api/orders/{id}` - Obtener orden
- `PUT /api/orders/{id}` - Actualizar orden
- `DELETE /api/orders/{id}` - Eliminar orden

### Analytics (15+ endpoints)
- `GET /api/analytics/dashboard` - Dashboard completo
- `GET /api/analytics/kpi-dashboard` - Dashboard KPI
- `GET /api/analytics/sales/top-products` - Top productos
- `GET /api/analytics/sales/top-customers` - Mejores clientes
- `GET /api/analytics/sales/by-category` - Ventas por categoría
- `GET /api/analytics/sales/by-period` - Ventas por período
- `GET /api/analytics/sales/forecast` - Pronóstico de ventas
- `GET /api/analytics/customers/cohort-analysis` - Análisis de cohortes
- `GET /api/analytics/customers/rfm-analysis` - Análisis RFM
- `GET /api/analytics/customers/segmentation` - Segmentación de clientes
- `GET /api/analytics/customers/conversion-funnel` - Embudo de conversión
- `GET /api/analytics/products/performance-matrix` - Matriz de rendimiento
- `GET /api/analytics/products/abc-analysis` - Análisis ABC
- `GET /api/analytics/sales/seasonal-analysis` - Análisis estacional
- `GET /api/analytics/financial/profit-analysis` - Análisis de rentabilidad
- `GET /api/analytics/inventory/low-stock` - Stock bajo
- `GET /api/analytics/inventory/out-of-stock` - Sin stock
- `GET /api/analytics/inventory/value` - Valor inventario

### Dashboard Interactivo (9 endpoints)
- `GET /api/dashboard/summary` - Resumen general
- `GET /api/dashboard/daily-sales` - Ventas diarias
- `GET /api/dashboard/category-sales` - Ventas por categoría
- `GET /api/dashboard/top-products` - Productos más vendidos
- `GET /api/dashboard/payment-methods` - Métodos de pago
- `GET /api/dashboard/customer-growth` - Crecimiento de clientes
- `GET /api/dashboard/inventory-status` - Estado del inventario
- `GET /api/dashboard/revenue-by-hour` - Ingresos por hora
- `GET /api/dashboard/product-performance` - Desempeño de productos

### Chatbot IA (4 endpoints)
- `POST /api/ai/ask` - Enviar pregunta
- `GET /api/ai/history` - Obtener historial
- `DELETE /api/ai/history` - Limpiar historial
- `GET /api/ai/capabilities` - Obtener capacidades

---

## 💻 Cliente Web TypeScript

### Características Modernas

#### 🎯 Arquitectura Modular
```typescript
// Componentes especializados
- TabManager: Gestión de pestañas
- UserManager: CRUD de usuarios
- ProductManager: CRUD de productos
- DashboardManager: Analytics en tiempo real
- InteractiveDashboard: Dashboard con gráficos
- AdvancedAnalytics: Análisis avanzado (5 vistas)
- BusinessIntelligence: Inteligencia de negocios (5 vistas)
- AIChat: Chatbot de IA
- ChartManager: Gestión de gráficos
- HealthIndicator: Estado de la API
```

#### 🎨 Diseño Moderno
- **CSS Variables** para temas consistentes
- **Responsive design** para móviles y tablets
- **Animaciones suaves** y transiciones
- **Sistema de notificaciones** toast elegante
- **Indicadores visuales** de estado

### Comandos de Desarrollo

```bash
cd client

# Desarrollo con hot reload
npm run dev

# Verificar tipos
npm run type-check

# Construir para producción
npm run build

# Preview de producción
npm run preview
```

---

## 📊 Módulo de Análisis

### Dashboard Completo
El dashboard muestra métricas en tiempo real:

- **💰 Ventas Totales** - Ingresos acumulados
- **📦 Total de Órdenes** - Número de pedidos
- **👥 Clientes Únicos** - Base de clientes
- **📋 Productos** - Catálogo total
- **📊 Promedio por Orden** - Ticket promedio
- **🏪 Valor Inventario** - Capital en stock

### Análisis Avanzado (5 vistas)
1. **Pronóstico de Ventas** - Predicción 30 días con intervalos de confianza
2. **Análisis de Cohortes** - Retención de clientes por período
3. **Análisis RFM** - Segmentación de clientes (Champions, Loyal, etc.)
4. **Rendimiento de Productos** - Matriz de productos (Star, Cash Cow, etc.)
5. **Análisis Estacional** - Patrones de ventas por mes

### Inteligencia de Negocios (5 vistas)
1. **Dashboard KPI** - Métricas de negocio completas
2. **Embudo de Conversión** - Usuarios → Órdenes → Completadas → Recurrentes
3. **Segmentación de Clientes** - 6 segmentos diferentes
4. **Análisis ABC** - Clasificación de productos por ingresos
5. **Análisis de Rentabilidad** - Ganancias por producto y categoría

---

## 📈 Dashboard Interactivo

### Gráficos Disponibles

| Gráfico | Tipo | Descripción |
|---------|------|-------------|
| Ventas Diarias | Línea | Últimos 30 días |
| Categorías | Pastel | Distribución de ventas |
| Métodos de Pago | Pastel | Distribución de pagos |
| Top Productos | Barras | 10 más vendidos |
| Crecimiento Clientes | Línea | Últimos 12 meses |
| Stock por Categoría | Barras | Inventario disponible |
| Ingresos por Hora | Línea | Análisis horario |

### Características
- ✅ **Auto-refresh** cada 5 minutos
- ✅ **Actualización manual** con botón
- ✅ **Exportación de datos** a JSON
- ✅ **Diseño responsive**
- ✅ **Animaciones suaves**
- ✅ **Manejo de errores** con fallbacks

### Uso

1. Abrir http://localhost:3000
2. Hacer clic en la pestaña **"Dashboard Interactivo"**
3. Los gráficos se cargarán automáticamente
4. Usar botón "🔄 Actualizar Ahora" para refrescar
5. Usar botón "📥 Descargar Datos" para exportar

---

## 🤖 Chatbot de IA

### Descripción
Asistente inteligente que responde preguntas sobre datos reales del negocio usando procesamiento de lenguaje natural básico.

### Capacidades

#### 📊 Ventas
- Total de ventas e ingresos
- Número de órdenes
- Promedio por orden
- Ventas del día

#### 📦 Productos
- Total de productos y stock
- Productos más vendidos
- Precio promedio
- Stock bajo y sin stock

#### 👥 Clientes
- Total de clientes
- Clientes activos e inactivos
- Comportamiento de compra

#### 🏷️ Categorías
- Listado de categorías
- Productos por categoría

#### 📋 Stock
- Stock total
- Productos con stock bajo
- Productos sin stock

#### 💡 Recomendaciones
- Alertas de stock bajo
- Productos destacados
- Sugerencias de acción

### Ejemplos de Preguntas

```
¿Cuántas ventas tenemos?
¿Cuál es el producto más vendido?
¿Cuántos clientes tenemos?
¿Hay productos con stock bajo?
Dame recomendaciones
¿Cuál es el precio promedio?
¿Cuántos clientes están inactivos?
¿Cuál es el stock total?
```

### API Endpoints

#### Enviar Pregunta
```bash
curl -X POST http://localhost:5001/api/ai/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "¿Cuántas ventas tenemos?"}'
```

**Respuesta:**
```json
{
  "success": true,
  "data": {
    "answer": "Las ventas totales son $10,000 en 50 órdenes.",
    "confidence": 0.95,
    "category": "ventas",
    "data": {
      "total_sales": 10000.0,
      "total_orders": 50
    }
  }
}
```

### Interfaz Web

1. Abrir http://localhost:3000
2. Hacer clic en la pestaña **"🤖 Chat IA"**
3. Escribir preguntas en el campo de texto
4. Ver respuestas con niveles de confianza

### Características de la Interfaz

- ✅ Chat en tiempo real
- ✅ Indicador de escritura animado
- ✅ Niveles de confianza visuales (🟢🟡🔴)
  - 🟢 Verde (≥90%): Alta confianza
  - 🟡 Amarillo (70-89%): Confianza media
  - 🔴 Rojo (<70%): Baja confianza
- ✅ Categorización de respuestas
- ✅ Historial de conversación
- ✅ Diseño responsive
- ✅ Auto-scroll y auto-resize
- ✅ Botón para limpiar historial

---

## 🧪 Testing

### Backend (Python)
```bash
# Ejecutar todos los tests
python3 -m pytest tests/ -v

# Tests con cobertura
python3 -m pytest tests/ --cov=app --cov-report=html

# Ver reporte de cobertura
open htmlcov/index.html
```

### Resultado Esperado
```
38 passed, 47 warnings in 0.89s
```

### Tests Incluidos
- ✅ 11 tests de usuarios
- ✅ 9 tests de productos
- ✅ 12 tests de chatbot IA
- ✅ 3 tests de endpoints principales
- ✅ 3 tests de configuración

### Frontend (TypeScript)
```bash
cd client

# Verificar tipos
npm run type-check

# Construir (verifica errores)
npm run build
```

---

## 🔧 Solución de Problemas

### Puerto 5001 en uso
```bash
lsof -ti:5001 | xargs kill -9
```

### Limpiar caché de Node
```bash
cd client
rm -rf node_modules
npm install
```

### Reinicializar base de datos
```bash
rm -f instance/flask_api.db
python3 init_db.py
```

### El dashboard no carga
1. Verificar que el backend esté corriendo
2. Abrir la consola del navegador (F12)
3. Buscar errores de red
4. Verificar que hay datos en la BD

### El chatbot no responde
1. Verificar que el servidor Flask esté corriendo
2. Abrir la consola del navegador y buscar errores
3. Verificar que la base de datos tenga datos
4. Ejecutar `python3 init_db.py` para crear datos de ejemplo

### Error 500 en endpoints
1. Verificar que la base de datos esté inicializada
2. Ejecutar `python3 init_db.py`
3. Reiniciar el servidor Flask
4. Revisar logs del servidor

### Errores de TypeScript
```bash
cd client
rm -rf node_modules dist
npm install
npm run build
```

---

## 📚 Recursos Adicionales

### Documentación
- [Flask Documentation](https://flask.palletsprojects.com/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Vite Guide](https://vitejs.dev/guide/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)

### Comandos Útiles
```bash
# Backend
python3 run.py                    # Iniciar servidor
python3 -m pytest tests/ -v       # Ejecutar tests
python3 init_db.py                # Inicializar BD

# Frontend
cd client
npm run dev                       # Servidor de desarrollo
npm run build                     # Compilar para producción
npm run preview                   # Vista previa de producción

# Base de datos
rm -f instance/flask_api.db       # Eliminar BD
python3 init_db.py                # Recrear BD
```

---

## 🎉 ¡Listo!

El proyecto está completamente funcional. Puedes:

1. ✅ Crear, leer, actualizar y eliminar usuarios
2. ✅ Crear, leer, actualizar y eliminar productos
3. ✅ Crear, leer, actualizar y eliminar órdenes
4. ✅ Ver análisis de ventas e inventario
5. ✅ Ver dashboard interactivo con 7 gráficos
6. ✅ Chatear con IA sobre tus datos
7. ✅ Ver análisis avanzado (pronóstico, cohortes, RFM, etc.)
8. ✅ Ver inteligencia de negocios (KPIs, segmentación, rentabilidad, etc.)
9. ✅ Ejecutar tests unitarios
10. ✅ Compilar para producción

**¡API REST profesional con análisis avanzado, dashboard interactivo y chatbot de IA!** 🚀

---

**Versión:** 4.0.0 (TypeScript + Análisis Avanzado + Dashboard + IA)  
**Última actualización:** Abril 24, 2026  
**Estado:** ✅ Completado y Modernizado

**🎊 ¡API REST ahora tiene, análisis profesional, dashboard interactivo y chatbot de IA!**

"""
Rutas para el dashboard con gráficos interactivos.
"""
from flask import Blueprint, jsonify

from app.analytics.dashboard_analytics import DashboardAnalytics
from app.utils.responses import success_response, error_response

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')


@dashboard_bp.route('/summary', methods=['GET'])
def get_dashboard_summary():
    """Obtiene resumen general del dashboard."""
    try:
        data = DashboardAnalytics.get_dashboard_summary()
        return success_response(data, 'Dashboard summary retrieved successfully')
    except Exception as e:
        return error_response(str(e), 500)


@dashboard_bp.route('/daily-sales', methods=['GET'])
def get_daily_sales():
    """Obtiene datos de ventas diarias."""
    try:
        data = DashboardAnalytics.get_daily_sales_chart(days=30)
        return success_response(data, 'Daily sales data retrieved successfully')
    except Exception as e:
        return error_response(str(e), 500)


@dashboard_bp.route('/category-sales', methods=['GET'])
def get_category_sales():
    """Obtiene ventas por categoría."""
    try:
        data = DashboardAnalytics.get_category_sales_chart()
        return success_response(data, 'Category sales data retrieved successfully')
    except Exception as e:
        return error_response(str(e), 500)


@dashboard_bp.route('/top-products', methods=['GET'])
def get_top_products():
    """Obtiene productos más vendidos."""
    try:
        data = DashboardAnalytics.get_top_products_chart(limit=10)
        return success_response(data, 'Top products data retrieved successfully')
    except Exception as e:
        return error_response(str(e), 500)


@dashboard_bp.route('/payment-methods', methods=['GET'])
def get_payment_methods():
    """Obtiene distribución de métodos de pago."""
    try:
        data = DashboardAnalytics.get_payment_methods_chart()
        return success_response(data, 'Payment methods data retrieved successfully')
    except Exception as e:
        return error_response(str(e), 500)


@dashboard_bp.route('/customer-growth', methods=['GET'])
def get_customer_growth():
    """Obtiene crecimiento de clientes."""
    try:
        data = DashboardAnalytics.get_customer_growth_chart(months=12)
        return success_response(data, 'Customer growth data retrieved successfully')
    except Exception as e:
        return error_response(str(e), 500)


@dashboard_bp.route('/inventory-status', methods=['GET'])
def get_inventory_status():
    """Obtiene estado del inventario."""
    try:
        data = DashboardAnalytics.get_inventory_status_chart()
        return success_response(data, 'Inventory status data retrieved successfully')
    except Exception as e:
        return error_response(str(e), 500)


@dashboard_bp.route('/revenue-by-hour', methods=['GET'])
def get_revenue_by_hour():
    """Obtiene ingresos por hora."""
    try:
        data = DashboardAnalytics.get_revenue_by_hour_chart()
        return success_response(data, 'Revenue by hour data retrieved successfully')
    except Exception as e:
        return error_response(str(e), 500)


@dashboard_bp.route('/product-performance', methods=['GET'])
def get_product_performance():
    """Obtiene matriz de desempeño de productos."""
    try:
        data = DashboardAnalytics.get_product_performance_heatmap()
        return success_response(data, 'Product performance data retrieved successfully')
    except Exception as e:
        return error_response(str(e), 500)

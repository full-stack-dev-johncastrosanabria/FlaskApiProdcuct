from flask import Blueprint, request
from app.analytics.sales_analytics import SalesAnalytics
from app.analytics.inventory_analytics import InventoryAnalytics
from app.analytics.advanced_analytics import AdvancedAnalytics
from app.analytics.business_intelligence import BusinessIntelligence
from app.utils.responses import success_response, error_response
from datetime import datetime

bp = Blueprint('analytics', __name__, url_prefix='/api/analytics')


@bp.route('/dashboard', methods=['GET'])
def get_dashboard():
    """Obtiene resumen completo para el dashboard"""
    try:
        sales_summary = SalesAnalytics.get_dashboard_summary()
        inventory_summary = InventoryAnalytics.get_inventory_summary()
        
        return success_response(data={
            'sales': sales_summary,
            'inventory': inventory_summary
        })
    except Exception as e:
        return error_response(f'Error al obtener dashboard: {str(e)}', 500)


@bp.route('/kpi-dashboard', methods=['GET'])
def get_kpi_dashboard():
    """Obtiene dashboard completo de KPIs"""
    try:
        kpi_data = BusinessIntelligence.get_kpi_dashboard()
        return success_response(data=kpi_data)
    except Exception as e:
        return error_response(f'Error al obtener KPI dashboard: {str(e)}', 500)


@bp.route('/sales/total', methods=['GET'])
def get_total_sales():
    """Obtiene el total de ventas"""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    try:
        if start_date:
            start_date = datetime.fromisoformat(start_date)
        if end_date:
            end_date = datetime.fromisoformat(end_date)
        
        total = SalesAnalytics.get_total_sales(start_date, end_date)
        
        return success_response(data={'total_sales': total})
    except Exception as e:
        return error_response(f'Error al obtener ventas: {str(e)}', 500)


@bp.route('/sales/by-period', methods=['GET'])
def get_sales_by_period():
    """Obtiene ventas agrupadas por período"""
    period = request.args.get('period', 'day')
    limit = request.args.get('limit', 30, type=int)
    
    try:
        data = SalesAnalytics.get_sales_by_period(period, limit)
        return success_response(data=data, count=len(data))
    except Exception as e:
        return error_response(f'Error al obtener ventas por período: {str(e)}', 500)


@bp.route('/sales/top-products', methods=['GET'])
def get_top_products():
    """Obtiene los productos más vendidos"""
    limit = request.args.get('limit', 10, type=int)
    
    try:
        data = SalesAnalytics.get_top_products(limit)
        return success_response(data=data, count=len(data))
    except Exception as e:
        return error_response(f'Error al obtener top productos: {str(e)}', 500)


@bp.route('/sales/top-customers', methods=['GET'])
def get_top_customers():
    """Obtiene los clientes con más compras"""
    limit = request.args.get('limit', 10, type=int)
    
    try:
        data = SalesAnalytics.get_top_customers(limit)
        return success_response(data=data, count=len(data))
    except Exception as e:
        return error_response(f'Error al obtener top clientes: {str(e)}', 500)


@bp.route('/sales/by-category', methods=['GET'])
def get_sales_by_category():
    """Obtiene ventas por categoría"""
    try:
        data = SalesAnalytics.get_sales_by_category()
        return success_response(data=data, count=len(data))
    except Exception as e:
        return error_response(f'Error al obtener ventas por categoría: {str(e)}', 500)


@bp.route('/sales/forecast', methods=['GET'])
def get_sales_forecast():
    """Obtiene pronóstico de ventas"""
    days_ahead = request.args.get('days_ahead', 30, type=int)
    
    try:
        data = AdvancedAnalytics.get_sales_forecast(days_ahead)
        return success_response(data=data)
    except Exception as e:
        return error_response(f'Error al obtener pronóstico: {str(e)}', 500)


@bp.route('/customers/cohort-analysis', methods=['GET'])
def get_cohort_analysis():
    """Obtiene análisis de cohortes"""
    months_back = request.args.get('months_back', 12, type=int)
    
    try:
        data = AdvancedAnalytics.get_cohort_analysis(months_back)
        return success_response(data=data, count=len(data))
    except Exception as e:
        return error_response(f'Error al obtener análisis de cohortes: {str(e)}', 500)


@bp.route('/customers/rfm-analysis', methods=['GET'])
def get_rfm_analysis():
    """Obtiene análisis RFM"""
    try:
        data = AdvancedAnalytics.get_rfm_analysis()
        return success_response(data=data, count=len(data))
    except Exception as e:
        return error_response(f'Error al obtener análisis RFM: {str(e)}', 500)


@bp.route('/customers/segmentation', methods=['GET'])
def get_customer_segmentation():
    """Obtiene segmentación de clientes"""
    try:
        data = BusinessIntelligence.get_customer_segmentation()
        return success_response(data=data)
    except Exception as e:
        return error_response(f'Error al obtener segmentación: {str(e)}', 500)


@bp.route('/customers/conversion-funnel', methods=['GET'])
def get_conversion_funnel():
    """Obtiene embudo de conversión"""
    try:
        data = BusinessIntelligence.get_conversion_funnel()
        return success_response(data=data)
    except Exception as e:
        return error_response(f'Error al obtener embudo de conversión: {str(e)}', 500)


@bp.route('/products/performance-matrix', methods=['GET'])
def get_product_performance_matrix():
    """Obtiene matriz de rendimiento de productos"""
    try:
        data = AdvancedAnalytics.get_product_performance_matrix()
        return success_response(data=data, count=len(data))
    except Exception as e:
        return error_response(f'Error al obtener matriz de rendimiento: {str(e)}', 500)


@bp.route('/products/abc-analysis', methods=['GET'])
def get_abc_analysis():
    """Obtiene análisis ABC"""
    try:
        data = BusinessIntelligence.get_abc_analysis()
        return success_response(data=data)
    except Exception as e:
        return error_response(f'Error al obtener análisis ABC: {str(e)}', 500)


@bp.route('/sales/seasonal-analysis', methods=['GET'])
def get_seasonal_analysis():
    """Obtiene análisis estacional"""
    try:
        data = AdvancedAnalytics.get_seasonal_analysis()
        return success_response(data=data)
    except Exception as e:
        return error_response(f'Error al obtener análisis estacional: {str(e)}', 500)


@bp.route('/financial/profit-analysis', methods=['GET'])
def get_profit_analysis():
    """Obtiene análisis de rentabilidad"""
    try:
        data = BusinessIntelligence.get_profit_analysis()
        return success_response(data=data)
    except Exception as e:
        return error_response(f'Error al obtener análisis de rentabilidad: {str(e)}', 500)


@bp.route('/inventory/low-stock', methods=['GET'])
def get_low_stock():
    """Obtiene productos con stock bajo"""
    threshold = request.args.get('threshold', 10, type=int)
    
    try:
        data = InventoryAnalytics.get_low_stock_products(threshold)
        return success_response(data=data, count=len(data))
    except Exception as e:
        return error_response(f'Error al obtener productos con stock bajo: {str(e)}', 500)


@bp.route('/inventory/out-of-stock', methods=['GET'])
def get_out_of_stock():
    """Obtiene productos sin stock"""
    try:
        data = InventoryAnalytics.get_out_of_stock_products()
        return success_response(data=data, count=len(data))
    except Exception as e:
        return error_response(f'Error al obtener productos sin stock: {str(e)}', 500)


@bp.route('/inventory/value', methods=['GET'])
def get_inventory_value():
    """Obtiene el valor total del inventario"""
    try:
        value = InventoryAnalytics.get_inventory_value()
        return success_response(data={'total_value': value})
    except Exception as e:
        return error_response(f'Error al obtener valor del inventario: {str(e)}', 500)


@bp.route('/inventory/by-category', methods=['GET'])
def get_inventory_by_category():
    """Obtiene inventario por categoría"""
    try:
        data = InventoryAnalytics.get_inventory_by_category()
        return success_response(data=data, count=len(data))
    except Exception as e:
        return error_response(f'Error al obtener inventario por categoría: {str(e)}', 500)

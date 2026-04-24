"""
Módulo de análisis para dashboard con datos en tiempo real.

Proporciona funcionalidades para:
- Gráficos de ventas diarias
- Análisis de categorías
- Tendencias de productos
- Distribución de métodos de pago
- Análisis de clientes
"""
from datetime import datetime, timedelta, timezone
from typing import Dict, List

import numpy as np
import pandas as pd
from sqlalchemy import and_, extract, func

from app.database import db
from app.models import Category, Order, OrderItem, Product, User


class DashboardAnalytics:
    """Análisis avanzado para dashboard con datos en tiempo real."""

    @staticmethod
    def get_daily_sales_chart(days: int = 30) -> Dict:
        """
        Obtiene datos de ventas diarias para gráfico de línea.

        Args:
            days: Número de días a incluir

        Returns:
            Diccionario con datos para gráfico de línea
        """
        # Obtener ventas diarias
        daily_sales = db.session.query(
            func.date(Order.created_at).label('date'),
            func.count(Order.id).label('orders'),
            func.sum(Order.total).label('revenue')
        ).filter(
            Order.status == 'completed',
            Order.created_at >= datetime.now(timezone.utc) - timedelta(days=days)
        ).group_by(
            func.date(Order.created_at)
        ).order_by('date').all()

        if not daily_sales:
            return {
                'labels': [],
                'datasets': [
                    {'label': 'Ingresos', 'data': [], 'color': '#4CAF50'},
                    {'label': 'Órdenes', 'data': [], 'color': '#2196F3'}
                ]
            }

        dates = []
        revenues = []
        orders = []

        for sale in daily_sales:
            dates.append(sale.date.strftime('%d/%m'))
            revenues.append(float(sale.revenue) if sale.revenue else 0)
            orders.append(sale.orders)

        return {
            'labels': dates,
            'datasets': [
                {
                    'label': 'Ingresos ($)',
                    'data': revenues,
                    'color': '#4CAF50',
                    'type': 'line'
                },
                {
                    'label': 'Órdenes',
                    'data': orders,
                    'color': '#2196F3',
                    'type': 'bar'
                }
            ]
        }

    @staticmethod
    def get_category_sales_chart() -> Dict:
        """
        Obtiene ventas por categoría para gráfico de pastel.

        Returns:
            Diccionario con datos para gráfico de pastel
        """
        category_sales = db.session.query(
            Category.name,
            func.sum(Order.total).label('total_sales'),
            func.count(Order.id).label('order_count')
        ).join(
            Product, Category.id == Product.category_id
        ).join(
            OrderItem, Product.id == OrderItem.product_id
        ).join(
            Order, OrderItem.order_id == Order.id
        ).filter(
            Order.status == 'completed'
        ).group_by(
            Category.name
        ).all()

        if not category_sales:
            return {
                'labels': [],
                'data': [],
                'colors': []
            }

        labels = []
        data = []
        colors = [
            '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0',
            '#9966FF', '#FF9F40', '#FF6384', '#C9CBCF'
        ]

        for i, sale in enumerate(category_sales):
            labels.append(sale.name)
            data.append(float(sale.total_sales) if sale.total_sales else 0)

        return {
            'labels': labels,
            'data': data,
            'colors': colors[:len(labels)]
        }

    @staticmethod
    def get_top_products_chart(limit: int = 10) -> Dict:
        """
        Obtiene los productos más vendidos.

        Args:
            limit: Número de productos a incluir

        Returns:
            Diccionario con datos para gráfico de barras
        """
        top_products = db.session.query(
            Product.name,
            func.sum(OrderItem.quantity).label('total_quantity'),
            func.sum(OrderItem.subtotal).label('total_revenue')
        ).join(
            OrderItem, Product.id == OrderItem.product_id
        ).join(
            Order, OrderItem.order_id == Order.id
        ).filter(
            Order.status == 'completed'
        ).group_by(
            Product.id, Product.name
        ).order_by(
            func.sum(OrderItem.subtotal).desc()
        ).limit(limit).all()

        if not top_products:
            return {
                'labels': [],
                'datasets': [
                    {'label': 'Cantidad', 'data': [], 'color': '#2196F3'},
                    {'label': 'Ingresos', 'data': [], 'color': '#4CAF50'}
                ]
            }

        labels = []
        quantities = []
        revenues = []

        for product in top_products:
            labels.append(product.name[:20])  # Limitar nombre
            quantities.append(product.total_quantity or 0)
            revenues.append(float(product.total_revenue) if product.total_revenue else 0)

        return {
            'labels': labels,
            'datasets': [
                {
                    'label': 'Cantidad Vendida',
                    'data': quantities,
                    'color': '#2196F3'
                },
                {
                    'label': 'Ingresos ($)',
                    'data': revenues,
                    'color': '#4CAF50'
                }
            ]
        }

    @staticmethod
    def get_payment_methods_chart() -> Dict:
        """
        Obtiene distribución de métodos de pago.

        Returns:
            Diccionario con datos para gráfico de pastel
        """
        payment_methods = db.session.query(
            Order.payment_method,
            func.count(Order.id).label('count'),
            func.sum(Order.total).label('total')
        ).filter(
            Order.status == 'completed'
        ).group_by(
            Order.payment_method
        ).all()

        if not payment_methods:
            return {
                'labels': [],
                'data': [],
                'colors': []
            }

        labels = []
        data = []
        colors = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF']

        method_names = {
            'credit_card': 'Tarjeta de Crédito',
            'debit_card': 'Tarjeta de Débito',
            'paypal': 'PayPal',
            'bank_transfer': 'Transferencia Bancaria',
            'cash': 'Efectivo'
        }

        for i, method in enumerate(payment_methods):
            method_name = method_names.get(
                method.payment_method, method.payment_method or 'Desconocido'
            )
            labels.append(method_name)
            data.append(method.count)

        return {
            'labels': labels,
            'data': data,
            'colors': colors[:len(labels)]
        }

    @staticmethod
    def get_customer_growth_chart(months: int = 12) -> Dict:
        """
        Obtiene crecimiento de clientes por mes.

        Args:
            months: Número de meses a incluir

        Returns:
            Diccionario con datos para gráfico de línea
        """
        customer_growth = db.session.query(
            extract('year', User.created_at).label('year'),
            extract('month', User.created_at).label('month'),
            func.count(User.id).label('new_customers')
        ).group_by(
            extract('year', User.created_at),
            extract('month', User.created_at)
        ).order_by('year', 'month').all()

        if not customer_growth:
            return {
                'labels': [],
                'datasets': [
                    {'label': 'Nuevos Clientes', 'data': [], 'color': '#FF9F40'}
                ]
            }

        labels = []
        data = []
        month_names = [
            'Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
            'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'
        ]

        for growth in customer_growth:
            month_label = f"{month_names[int(growth.month) - 1]} {int(growth.year)}"
            labels.append(month_label)
            data.append(growth.new_customers)

        return {
            'labels': labels,
            'datasets': [
                {
                    'label': 'Nuevos Clientes',
                    'data': data,
                    'color': '#FF9F40'
                }
            ]
        }

    @staticmethod
    def get_inventory_status_chart() -> Dict:
        """
        Obtiene estado del inventario por categoría.

        Returns:
            Diccionario con datos para gráfico de barras apiladas
        """
        inventory_status = db.session.query(
            Category.name,
            func.sum(Product.stock).label('total_stock'),
            func.count(Product.id).label('product_count')
        ).join(
            Product, Category.id == Product.category_id
        ).group_by(
            Category.name
        ).all()

        if not inventory_status:
            return {
                'labels': [],
                'datasets': [
                    {'label': 'Stock', 'data': [], 'color': '#4CAF50'}
                ]
            }

        labels = []
        stock_data = []

        for status in inventory_status:
            labels.append(status.name)
            stock_data.append(status.total_stock or 0)

        return {
            'labels': labels,
            'datasets': [
                {
                    'label': 'Stock Total',
                    'data': stock_data,
                    'color': '#4CAF50'
                }
            ]
        }

    @staticmethod
    def get_revenue_by_hour_chart() -> Dict:
        """
        Obtiene ingresos por hora del día.

        Returns:
            Diccionario con datos para gráfico de área
        """
        revenue_by_hour = db.session.query(
            extract('hour', Order.created_at).label('hour'),
            func.sum(Order.total).label('revenue'),
            func.count(Order.id).label('orders')
        ).filter(
            Order.status == 'completed'
        ).group_by(
            extract('hour', Order.created_at)
        ).order_by('hour').all()

        if not revenue_by_hour:
            return {
                'labels': [],
                'datasets': [
                    {'label': 'Ingresos', 'data': [], 'color': '#4CAF50'}
                ]
            }

        labels = []
        data = []

        for hour_data in revenue_by_hour:
            hour = int(hour_data.hour) if hour_data.hour is not None else 0
            labels.append(f"{hour:02d}:00")
            data.append(float(hour_data.revenue) if hour_data.revenue else 0)

        return {
            'labels': labels,
            'datasets': [
                {
                    'label': 'Ingresos por Hora ($)',
                    'data': data,
                    'color': '#4CAF50'
                }
            ]
        }

    @staticmethod
    def get_product_performance_heatmap() -> Dict:
        """
        Obtiene matriz de desempeño de productos.

        Returns:
            Diccionario con datos para heatmap
        """
        products = db.session.query(
            Product.id,
            Product.name,
            Product.stock,
            Product.rating,
            Product.views,
            func.sum(OrderItem.quantity).label('sold'),
            func.sum(OrderItem.subtotal).label('revenue')
        ).outerjoin(
            OrderItem, Product.id == OrderItem.product_id
        ).group_by(
            Product.id, Product.name, Product.stock,
            Product.rating, Product.views
        ).limit(20).all()

        if not products:
            return {
                'labels': [],
                'data': []
            }

        labels = []
        data = []

        for product in products:
            labels.append(product.name[:15])
            data.append({
                'stock': product.stock,
                'rating': float(product.rating) if product.rating else 0,
                'views': product.views,
                'sold': product.sold or 0,
                'revenue': float(product.revenue) if product.revenue else 0
            })

        return {
            'labels': labels,
            'data': data
        }

    @staticmethod
    def get_dashboard_summary() -> Dict:
        """
        Obtiene resumen general del dashboard.

        Returns:
            Diccionario con métricas clave
        """
        # Ventas totales
        total_sales = db.session.query(
            func.sum(Order.total)
        ).filter(
            Order.status == 'completed'
        ).scalar() or 0

        # Órdenes totales
        total_orders = db.session.query(
            func.count(Order.id)
        ).filter(
            Order.status == 'completed'
        ).scalar() or 0

        # Clientes únicos
        total_customers = db.session.query(
            func.count(func.distinct(Order.user_id))
        ).filter(
            Order.status == 'completed'
        ).scalar() or 0

        # Productos totales
        total_products = db.session.query(
            func.count(Product.id)
        ).scalar() or 0

        # Stock total
        total_stock = db.session.query(
            func.sum(Product.stock)
        ).scalar() or 0

        # Valor del inventario
        inventory_value = db.session.query(
            func.sum(Product.price * Product.stock)
        ).scalar() or 0

        # Promedio por orden
        avg_order_value = float(total_sales) / total_orders if total_orders > 0 else 0

        # Ventas hoy
        today_sales = db.session.query(
            func.sum(Order.total)
        ).filter(
            Order.status == 'completed',
            func.date(Order.created_at) == datetime.now(timezone.utc).date()
        ).scalar() or 0

        # Órdenes hoy
        today_orders = db.session.query(
            func.count(Order.id)
        ).filter(
            Order.status == 'completed',
            func.date(Order.created_at) == datetime.now(timezone.utc).date()
        ).scalar() or 0

        return {
            'total_sales': float(total_sales),
            'total_orders': total_orders,
            'total_customers': total_customers,
            'total_products': total_products,
            'total_stock': total_stock,
            'inventory_value': float(inventory_value),
            'avg_order_value': avg_order_value,
            'today_sales': float(today_sales),
            'today_orders': today_orders
        }

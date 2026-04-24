"""
Módulo de análisis avanzado con análisis estadístico y pronósticos.

Proporciona funcionalidades para:
- Análisis de cohortes
- Análisis RFM (Recencia, Frecuencia, Monetario)
- Pronóstico de ventas
- Matriz de desempeño de productos
- Análisis estacional
"""
from datetime import datetime, timedelta, timezone
from typing import Dict, List

import numpy as np
import pandas as pd
from sqlalchemy import and_, extract, func

from app.database import db
from app.models import Category, Order, OrderItem, Product, User

# Helper for month names
MONTH_NAMES = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
]


class AdvancedAnalytics:
    """Advanced analytics with statistical analysis and forecasting"""

    @staticmethod
    def get_cohort_analysis() -> List[Dict]:
        """
        Análisis de cohortes para entender la retención de clientes.
        """
        # Get first purchase date for each customer
        first_purchase = db.session.query(
            Order.user_id,
            func.min(Order.created_at).label('first_purchase')
        ).filter(Order.status == 'completed').group_by(
            Order.user_id
        ).subquery()

        # Get all orders with cohort information
        orders_with_cohort = db.session.query(
            Order.user_id,
            Order.created_at,
            Order.total,
            first_purchase.c.first_purchase
        ).join(
            first_purchase, Order.user_id == first_purchase.c.user_id
        ).filter(Order.status == 'completed').all()

        if not orders_with_cohort:
            return []

        # Convert to DataFrame for easier analysis
        df = pd.DataFrame([
            {
                'user_id': o.user_id,
                'order_date': o.created_at,
                'total': float(o.total),
                'first_purchase': o.first_purchase
            }
            for o in orders_with_cohort
        ])

        # Calculate cohort periods
        df['order_period'] = df['order_date'].dt.to_period('M')
        df['cohort_group'] = df['first_purchase'].dt.to_period('M')
        df['period_number'] = (
            df['order_period'] - df['cohort_group']
        ).apply(lambda x: x.n)

        # Create cohort table
        cohort_data = df.groupby(
            ['cohort_group', 'period_number']
        )['user_id'].nunique().reset_index()
        cohort_sizes = df.groupby('cohort_group')['user_id'].nunique()

        cohort_table = cohort_data.pivot(
            index='cohort_group',
            columns='period_number',
            values='user_id'
        )

        # Calculate retention rates
        cohort_percentages = cohort_table.divide(cohort_sizes, axis=0)

        # Convert to list of dictionaries
        result = []
        for cohort in cohort_percentages.index:
            cohort_dict = {
                'cohort': str(cohort),
                'size': int(cohort_sizes[cohort]),
                'retention_rates': {}
            }
            for period in cohort_percentages.columns:
                if not pd.isna(cohort_percentages.loc[cohort, period]):
                    cohort_dict['retention_rates'][
                        f'period_{period}'
                    ] = round(
                        cohort_percentages.loc[cohort, period] * 100, 2
                    )
            result.append(cohort_dict)

        return result

    @staticmethod
    def get_rfm_analysis() -> List[Dict]:
        """
        Análisis RFM (Recencia, Frecuencia, Monetario)
        para segmentación de clientes.
        """
        # Calculate RFM metrics
        current_date = datetime.now(timezone.utc)

        rfm_data = db.session.query(
            Order.user_id,
            User.name,
            User.email,
            func.max(Order.created_at).label('last_order_date'),
            func.count(Order.id).label('frequency'),
            func.sum(Order.total).label('monetary')
        ).join(
            User, Order.user_id == User.id
        ).filter(
            Order.status == 'completed'
        ).group_by(
            Order.user_id, User.name, User.email
        ).all()

        if not rfm_data:
            return []

        # Convert to DataFrame
        df = pd.DataFrame([
            {
                'user_id': r.user_id,
                'name': r.name,
                'email': r.email,
                'last_order_date': r.last_order_date,
                'frequency': r.frequency,
                'monetary': float(r.monetary)
            }
            for r in rfm_data
        ])

        # Ensure datetime is timezone-aware
        df['last_order_date'] = pd.to_datetime(
            df['last_order_date'], utc=True
        )

        # Calculate recency (days since last order)
        df['recency'] = (
            current_date - df['last_order_date']
        ).dt.days

        # Calculate RFM scores (1-5 scale) - convert to int
        df['r_score'] = pd.qcut(
            df['recency'].rank(method='first'),
            5,
            labels=[5, 4, 3, 2, 1]
        ).astype(int)
        df['f_score'] = pd.qcut(
            df['frequency'].rank(method='first'),
            5,
            labels=[1, 2, 3, 4, 5]
        ).astype(int)
        df['m_score'] = pd.qcut(
            df['monetary'].rank(method='first'),
            5,
            labels=[1, 2, 3, 4, 5]
        ).astype(int)

        # Create RFM segments
        df['rfm_score'] = (
            df['r_score'].astype(str) +
            df['f_score'].astype(str) +
            df['m_score'].astype(str)
        )

        # Define customer segments
        def get_segment(rfm_score):
            """Mapea puntuaciones RFM a segmentos de clientes."""
            segment_mapping = {
                '555': 'Champions', '554': 'Champions', '544': 'Champions',
                '545': 'Champions', '454': 'Champions', '455': 'Champions',
                '445': 'Champions',
                '543': 'Loyal Customers', '444': 'Loyal Customers',
                '435': 'Loyal Customers', '355': 'Loyal Customers',
                '354': 'Loyal Customers', '345': 'Loyal Customers',
                '344': 'Loyal Customers', '335': 'Loyal Customers',
                '512': 'Potential Loyalists', '511': 'Potential Loyalists',
                '422': 'Potential Loyalists', '421': 'Potential Loyalists',
                '412': 'Potential Loyalists', '411': 'Potential Loyalists',
                '311': 'Potential Loyalists',
                '533': 'New Customers', '532': 'New Customers',
                '531': 'New Customers', '523': 'New Customers',
                '522': 'New Customers', '521': 'New Customers',
                '515': 'New Customers', '514': 'New Customers',
                '513': 'New Customers', '425': 'New Customers',
                '424': 'New Customers', '413': 'New Customers',
                '414': 'New Customers', '415': 'New Customers',
                '315': 'New Customers', '314': 'New Customers',
                '313': 'New Customers',
                '155': 'Promising', '154': 'Promising', '144': 'Promising',
                '214': 'Promising', '215': 'Promising', '115': 'Promising',
                '114': 'Promising',
                '254': 'Need Attention', '245': 'Need Attention',
                '331': 'About to Sleep', '321': 'About to Sleep',
                '231': 'About to Sleep', '241': 'About to Sleep',
                '251': 'About to Sleep',
                '125': 'Cannot Lose Them', '124': 'Cannot Lose Them',
                '332': 'Hibernating', '322': 'Hibernating',
                '233': 'Hibernating', '232': 'Hibernating',
                '223': 'Hibernating', '222': 'Hibernating',
                '132': 'Hibernating', '123': 'Hibernating',
            }
            return segment_mapping.get(rfm_score, 'Lost')

        df['segment'] = df['rfm_score'].apply(get_segment)

        # Convert back to list of dictionaries
        result = []
        for _, row in df.iterrows():
            result.append({
                'user_id': int(row['user_id']),
                'name': row['name'],
                'email': row['email'],
                'recency': int(row['recency']),
                'frequency': int(row['frequency']),
                'monetary': float(row['monetary']),
                'r_score': int(row['r_score']),
                'f_score': int(row['f_score']),
                'm_score': int(row['m_score']),
                'rfm_score': row['rfm_score'],
                'segment': row['segment']
            })

        return result

    @staticmethod
    def get_sales_forecast(days_ahead: int = 30) -> Dict:
        """
        Pronóstico simple de ventas usando regresión lineal.
        """
        # Get historical daily sales
        daily_sales = db.session.query(
            func.date(Order.created_at).label('date'),
            func.sum(Order.total).label('total_sales')
        ).filter(
            Order.status == 'completed'
        ).group_by(
            func.date(Order.created_at)
        ).order_by('date').all()

        if len(daily_sales) < 7:  # Need at least a week of data
            return {
                'error': 'Insufficient data for forecasting',
                'forecast': [],
                'model_metrics': {}
            }

        # Convert to DataFrame
        df = pd.DataFrame([
            {
                'date': pd.to_datetime(r.date),
                'total_sales': float(r.total_sales) if r.total_sales else 0.0
            }
            for r in daily_sales
        ])

        # Create date range and fill missing dates with 0
        date_range = pd.date_range(
            start=df['date'].min(),
            end=df['date'].max(),
            freq='D'
        )
        df_complete = pd.DataFrame({'date': date_range})
        df_complete['date'] = pd.to_datetime(df_complete['date'])
        df['date'] = pd.to_datetime(df['date'])
        df_complete = df_complete.merge(df, on='date', how='left')
        df_complete['total_sales'] = df_complete['total_sales'].fillna(0)

        # Prepare data for linear regression
        df_complete['day_number'] = range(len(df_complete))
        x_values = df_complete['day_number'].values.flatten()
        y_values = df_complete['total_sales'].values

        # Calculate linear regression coefficients
        slope, intercept = AdvancedAnalytics._calculate_regression(
            x_values, y_values
        )

        # Generate forecast
        last_day = len(df_complete) - 1
        forecast_days = np.array(
            range(last_day + 1, last_day + 1 + days_ahead)
        )
        forecast_values = slope * forecast_days + intercept

        # Calculate model metrics
        y_pred = slope * x_values + intercept
        residuals = y_values - y_pred
        mse = np.mean(residuals ** 2)
        rmse = np.sqrt(mse)

        # Calculate R-squared
        ss_res = np.sum(residuals ** 2)
        ss_tot = np.sum((y_values - np.mean(y_values)) ** 2)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0

        # Generate forecast dates and data
        last_date = df_complete['date'].max()
        forecast_dates = pd.date_range(
            start=last_date + timedelta(days=1),
            periods=days_ahead,
            freq='D'
        )

        forecast_data = [
            {
                'date': date.strftime('%Y-%m-%d'),
                'predicted_sales': float(max(0, forecast_values[i])),
                'confidence_interval_lower': float(
                    max(0, forecast_values[i] - 1.96 * rmse)
                ),
                'confidence_interval_upper': float(
                    forecast_values[i] + 1.96 * rmse
                )
            }
            for i, date in enumerate(forecast_dates)
        ]

        return {
            'forecast': forecast_data,
            'model_metrics': {
                'rmse': float(rmse),
                'r_squared': float(r_squared),
                'data_points_used': len(df_complete)
            }
        }

    @staticmethod
    def _calculate_regression(
        x_values: np.ndarray, y_values: np.ndarray
    ) -> tuple:
        """
        Calcula los coeficientes de regresión lineal.

        Args:
            x_values: Array de valores X
            y_values: Array de valores Y

        Returns:
            Tupla de (pendiente, intersección)
        """
        n = len(x_values)
        sum_x = np.sum(x_values)
        sum_y = np.sum(y_values)
        sum_xy = np.sum(x_values * y_values)
        sum_x2 = np.sum(x_values ** 2)

        denominator = n * sum_x2 - sum_x ** 2
        if denominator == 0:
            slope = 0
            intercept = np.mean(y_values)
        else:
            slope = (n * sum_xy - sum_x * sum_y) / denominator
            intercept = (sum_y - slope * sum_x) / n

        return slope, intercept
        return slope, intercept

    @staticmethod
    def get_product_performance_matrix() -> List[Dict]:
        """
        Matriz de desempeño de productos basada en volumen de ventas
        y margen de ganancia.
        """
        # Get product performance data
        product_data = db.session.query(
            Product.id,
            Product.name,
            Product.price,
            Category.name.label('category_name'),
            func.coalesce(
                func.sum(OrderItem.quantity), 0
            ).label('total_sold'),
            func.coalesce(
                func.sum(OrderItem.subtotal), 0
            ).label('total_revenue'),
            Product.stock
        ).outerjoin(
            OrderItem, Product.id == OrderItem.product_id
        ).outerjoin(
            Order, and_(
                OrderItem.order_id == Order.id,
                Order.status == 'completed'
            )
        ).outerjoin(
            Category, Product.category_id == Category.id
        ).group_by(
            Product.id, Product.name, Product.price,
            Category.name, Product.stock
        ).all()

        if not product_data:
            return []

        # Convert to DataFrame for analysis
        df = pd.DataFrame([
            {
                'product_id': p.id,
                'name': p.name,
                'price': float(p.price),
                'category': p.category_name or 'Uncategorized',
                'total_sold': p.total_sold,
                'total_revenue': float(p.total_revenue),
                'stock': p.stock
            }
            for p in product_data
        ])

        # Calculate performance metrics
        df['revenue_per_unit'] = (
            df['total_revenue'] / df['total_sold'].replace(0, 1)
        )
        df['stock_turnover'] = (
            df['total_sold'] / df['stock'].replace(0, 1)
        )

        # Classify products into performance quadrants
        median_revenue = df['total_revenue'].median()
        median_turnover = df['stock_turnover'].median()

        def classify_product(row):
            """Clasifica productos en cuadrantes de desempeño."""
            if (row['total_revenue'] >= median_revenue and
                    row['stock_turnover'] >= median_turnover):
                return 'Star Products'
            if (row['total_revenue'] >= median_revenue and
                    row['stock_turnover'] < median_turnover):
                return 'Cash Cows'
            if (row['total_revenue'] < median_revenue and
                    row['stock_turnover'] >= median_turnover):
                return 'Question Marks'
            return 'Dogs'

        df['performance_category'] = df.apply(
            classify_product, axis=1
        )

        # Add recommendations
        def get_recommendation(category):
            """Proporciona recomendaciones basadas en categoría."""
            recommendations = {
                'Star Products': (
                    'Invest more in marketing and ensure adequate stock'
                ),
                'Cash Cows': (
                    'Maintain current strategy, '
                    'consider price optimization'
                ),
                'Question Marks': (
                    'Analyze market potential, '
                    'consider promotion or discontinuation'
                ),
                'Dogs': (
                    'Consider discontinuation or clearance pricing'
                )
            }
            return recommendations.get(category, 'Monitor performance')

        df['recommendation'] = df['performance_category'].apply(
            get_recommendation
        )

        # Convert back to list
        result = []
        for _, row in df.iterrows():
            result.append({
                'product_id': int(row['product_id']),
                'name': row['name'],
                'price': float(row['price']),
                'category': row['category'],
                'total_sold': int(row['total_sold']),
                'total_revenue': float(row['total_revenue']),
                'stock': int(row['stock']),
                'revenue_per_unit': float(row['revenue_per_unit']),
                'stock_turnover': float(row['stock_turnover']),
                'performance_category': row['performance_category'],
                'recommendation': row['recommendation']
            })

        return result

    @staticmethod
    def get_seasonal_analysis() -> Dict:
        """
        Analiza patrones estacionales en las ventas.
        """
        # Get monthly sales data
        monthly_sales = db.session.query(
            extract('year', Order.created_at).label('year'),
            extract('month', Order.created_at).label('month'),
            func.sum(Order.total).label('total_sales'),
            func.count(Order.id).label('order_count')
        ).filter(
            Order.status == 'completed'
        ).group_by(
            extract('year', Order.created_at),
            extract('month', Order.created_at)
        ).order_by('year', 'month').all()

        if not monthly_sales:
            return {
                'error': 'No sales data available',
                'seasonal_indices': {},
                'peak_months': {},
                'low_months': {},
                'monthly_data': []
            }

        # Convert to DataFrame
        df = pd.DataFrame([
            {
                'year': int(r.year),
                'month': int(r.month),
                'total_sales': float(r.total_sales) if r.total_sales else 0.0,
                'order_count': r.order_count
            }
            for r in monthly_sales
        ])

        # Calculate seasonal indices
        df['month_name'] = df['month'].apply(
            lambda x: MONTH_NAMES[x - 1]
        )
        monthly_avg = df.groupby('month')['total_sales'].mean()
        overall_avg = df['total_sales'].mean()

        if overall_avg == 0:
            seasonal_indices = pd.Series(
                {m: 100.0 for m in monthly_avg.index}
            )
        else:
            seasonal_indices = (
                (monthly_avg / overall_avg * 100).round(2)
            )

        # Identify peak and low seasons
        peak_months = seasonal_indices.nlargest(3)
        low_months = seasonal_indices.nsmallest(3)

        return {
            'seasonal_indices': {
                MONTH_NAMES[int(month) - 1]: float(index)
                for month, index in seasonal_indices.items()
            },
            'peak_months': {
                MONTH_NAMES[int(month) - 1]: float(index)
                for month, index in peak_months.items()
            },
            'low_months': {
                MONTH_NAMES[int(month) - 1]: float(index)
                for month, index in low_months.items()
            },
            'monthly_data': df.to_dict('records')
        }

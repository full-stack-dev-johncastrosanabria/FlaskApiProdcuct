import pandas as pd
import numpy as np
from sqlalchemy import func, desc, and_, or_, extract
from app.database import db
from app.models import Order, OrderItem, Product, User, Category
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
import json


class AdvancedAnalytics:
    """Advanced analytics with statistical analysis and forecasting"""
    
    @staticmethod
    def get_cohort_analysis(months_back: int = 12) -> List[Dict]:
        """
        Cohort analysis to understand customer retention
        """
        # Get first purchase date for each customer
        first_purchase = db.session.query(
            Order.user_id,
            func.min(Order.created_at).label('first_purchase')
        ).filter(Order.status == 'completed').group_by(Order.user_id).subquery()
        
        # Get all orders with cohort information
        orders_with_cohort = db.session.query(
            Order.user_id,
            Order.created_at,
            Order.total,
            first_purchase.c.first_purchase
        ).join(
            first_purchase, Order.user_id == first_purchase.c.user_id
        ).filter(Order.status == 'completed').all()
        
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
        
        if df.empty:
            return []
        
        # Calculate cohort periods
        df['order_period'] = df['order_date'].dt.to_period('M')
        df['cohort_group'] = df['first_purchase'].dt.to_period('M')
        df['period_number'] = (df['order_period'] - df['cohort_group']).apply(attrgetter('n'))
        
        # Create cohort table
        cohort_data = df.groupby(['cohort_group', 'period_number'])['user_id'].nunique().reset_index()
        cohort_sizes = df.groupby('cohort_group')['user_id'].nunique()
        
        cohort_table = cohort_data.pivot(index='cohort_group', columns='period_number', values='user_id')
        
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
                    cohort_dict['retention_rates'][f'period_{period}'] = round(
                        cohort_percentages.loc[cohort, period] * 100, 2
                    )
            result.append(cohort_dict)
        
        return result
    
    @staticmethod
    def get_rfm_analysis() -> List[Dict]:
        """
        RFM (Recency, Frequency, Monetary) Analysis for customer segmentation
        """
        # Calculate RFM metrics
        current_date = datetime.utcnow()
        
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
        
        # Calculate recency (days since last order)
        df['recency'] = (current_date - df['last_order_date']).dt.days
        
        # Calculate RFM scores (1-5 scale)
        df['r_score'] = pd.qcut(df['recency'].rank(method='first'), 5, labels=[5,4,3,2,1])
        df['f_score'] = pd.qcut(df['frequency'].rank(method='first'), 5, labels=[1,2,3,4,5])
        df['m_score'] = pd.qcut(df['monetary'].rank(method='first'), 5, labels=[1,2,3,4,5])
        
        # Create RFM segments
        df['rfm_score'] = df['r_score'].astype(str) + df['f_score'].astype(str) + df['m_score'].astype(str)
        
        # Define customer segments
        def get_segment(rfm_score):
            if rfm_score in ['555', '554', '544', '545', '454', '455', '445']:
                return 'Champions'
            elif rfm_score in ['543', '444', '435', '355', '354', '345', '344', '335']:
                return 'Loyal Customers'
            elif rfm_score in ['512', '511', '422', '421', '412', '411', '311']:
                return 'Potential Loyalists'
            elif rfm_score in ['533', '532', '531', '523', '522', '521', '515', '514', '513', '425', '424', '413', '414', '415', '315', '314', '313']:
                return 'New Customers'
            elif rfm_score in ['155', '154', '144', '214', '215', '115', '114']:
                return 'Promising'
            elif rfm_score in ['155', '254', '245']:
                return 'Need Attention'
            elif rfm_score in ['331', '321', '231', '241', '251']:
                return 'About to Sleep'
            elif rfm_score in ['155', '144', '214', '215', '115', '114']:
                return 'At Risk'
            elif rfm_score in ['125', '124']:
                return 'Cannot Lose Them'
            elif rfm_score in ['332', '322', '231', '241', '251', '233', '232', '223', '222', '132', '123']:
                return 'Hibernating'
            else:
                return 'Lost'
        
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
        Simple sales forecasting using linear regression
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
            return {'error': 'Insufficient data for forecasting'}
        
        # Convert to DataFrame
        df = pd.DataFrame([
            {
                'date': r.date,
                'total_sales': float(r.total_sales)
            }
            for r in daily_sales
        ])
        
        # Create date range and fill missing dates with 0
        date_range = pd.date_range(start=df['date'].min(), end=df['date'].max(), freq='D')
        df_complete = pd.DataFrame({'date': date_range})
        df_complete = df_complete.merge(df, on='date', how='left')
        df_complete['total_sales'] = df_complete['total_sales'].fillna(0)
        
        # Simple linear regression
        df_complete['day_number'] = range(len(df_complete))
        X = df_complete['day_number'].values.reshape(-1, 1)
        y = df_complete['total_sales'].values
        
        # Calculate slope and intercept manually
        n = len(X)
        sum_x = np.sum(X)
        sum_y = np.sum(y)
        sum_xy = np.sum(X.flatten() * y)
        sum_x2 = np.sum(X ** 2)
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
        intercept = (sum_y - slope * sum_x) / n
        
        # Generate forecast
        last_day = len(df_complete) - 1
        forecast_days = range(last_day + 1, last_day + 1 + days_ahead)
        forecast_values = [slope * day + intercept for day in forecast_days]
        
        # Calculate confidence metrics
        y_pred = slope * X.flatten() + intercept
        mse = np.mean((y - y_pred) ** 2)
        rmse = np.sqrt(mse)
        
        # Generate forecast dates
        last_date = df_complete['date'].max()
        forecast_dates = pd.date_range(
            start=last_date + timedelta(days=1),
            periods=days_ahead,
            freq='D'
        )
        
        forecast_data = []
        for i, date in enumerate(forecast_dates):
            forecast_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'predicted_sales': max(0, forecast_values[i]),  # Ensure non-negative
                'confidence_interval_lower': max(0, forecast_values[i] - 1.96 * rmse),
                'confidence_interval_upper': forecast_values[i] + 1.96 * rmse
            })
        
        return {
            'forecast': forecast_data,
            'model_metrics': {
                'rmse': float(rmse),
                'r_squared': float(1 - (np.sum((y - y_pred) ** 2) / np.sum((y - np.mean(y)) ** 2))),
                'data_points_used': len(df_complete)
            }
        }
    
    @staticmethod
    def get_product_performance_matrix() -> List[Dict]:
        """
        Product performance matrix based on sales volume and profit margin
        """
        # Get product performance data
        product_data = db.session.query(
            Product.id,
            Product.name,
            Product.price,
            Category.name.label('category_name'),
            func.coalesce(func.sum(OrderItem.quantity), 0).label('total_sold'),
            func.coalesce(func.sum(OrderItem.subtotal), 0).label('total_revenue'),
            Product.stock
        ).outerjoin(
            OrderItem, Product.id == OrderItem.product_id
        ).outerjoin(
            Order, and_(OrderItem.order_id == Order.id, Order.status == 'completed')
        ).outerjoin(
            Category, Product.category_id == Category.id
        ).group_by(
            Product.id, Product.name, Product.price, Category.name, Product.stock
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
        df['revenue_per_unit'] = df['total_revenue'] / df['total_sold'].replace(0, 1)
        df['stock_turnover'] = df['total_sold'] / df['stock'].replace(0, 1)
        
        # Classify products into performance quadrants
        median_revenue = df['total_revenue'].median()
        median_turnover = df['stock_turnover'].median()
        
        def classify_product(row):
            if row['total_revenue'] >= median_revenue and row['stock_turnover'] >= median_turnover:
                return 'Star Products'
            elif row['total_revenue'] >= median_revenue and row['stock_turnover'] < median_turnover:
                return 'Cash Cows'
            elif row['total_revenue'] < median_revenue and row['stock_turnover'] >= median_turnover:
                return 'Question Marks'
            else:
                return 'Dogs'
        
        df['performance_category'] = df.apply(classify_product, axis=1)
        
        # Add recommendations
        def get_recommendation(category):
            recommendations = {
                'Star Products': 'Invest more in marketing and ensure adequate stock',
                'Cash Cows': 'Maintain current strategy, consider price optimization',
                'Question Marks': 'Analyze market potential, consider promotion or discontinuation',
                'Dogs': 'Consider discontinuation or clearance pricing'
            }
            return recommendations.get(category, 'Monitor performance')
        
        df['recommendation'] = df['performance_category'].apply(get_recommendation)
        
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
        Analyze seasonal patterns in sales
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
            return {'error': 'No sales data available'}
        
        # Convert to DataFrame
        df = pd.DataFrame([
            {
                'year': int(r.year),
                'month': int(r.month),
                'total_sales': float(r.total_sales),
                'order_count': r.order_count
            }
            for r in monthly_sales
        ])
        
        # Calculate seasonal indices
        df['month_name'] = df['month'].apply(lambda x: pd.Timestamp(2023, x, 1).strftime('%B'))
        monthly_avg = df.groupby('month')['total_sales'].mean()
        overall_avg = df['total_sales'].mean()
        seasonal_indices = (monthly_avg / overall_avg * 100).round(2)
        
        # Identify peak and low seasons
        peak_months = seasonal_indices.nlargest(3)
        low_months = seasonal_indices.nsmallest(3)
        
        return {
            'seasonal_indices': {
                month_names[month-1]: float(index) 
                for month, index in seasonal_indices.items()
            },
            'peak_months': {
                month_names[month-1]: float(index) 
                for month, index in peak_months.items()
            },
            'low_months': {
                month_names[month-1]: float(index) 
                for month, index in low_months.items()
            },
            'monthly_data': df.to_dict('records')
        }


# Helper for month names
month_names = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
]

# Helper for cohort analysis
from operator import attrgetter
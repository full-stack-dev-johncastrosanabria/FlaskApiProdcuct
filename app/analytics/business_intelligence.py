import pandas as pd
import numpy as np
from sqlalchemy import func, desc, and_, or_, extract, case
from app.database import db
from app.models import Order, OrderItem, Product, User, Category
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Tuple, Any
from collections import defaultdict


class BusinessIntelligence:
    """Business Intelligence and KPI calculations"""
    
    @staticmethod
    def get_kpi_dashboard() -> Dict:
        """
        Comprehensive KPI dashboard with business metrics
        """
        current_date = datetime.now(timezone.utc)
        
        # Get all metrics
        revenue_metrics = BusinessIntelligence._get_revenue_metrics(current_date)
        order_metrics = BusinessIntelligence._get_order_metrics(current_date)
        customer_metrics = BusinessIntelligence._get_customer_metrics()
        product_metrics = BusinessIntelligence._get_product_metrics()
        
        return {
            'revenue_metrics': revenue_metrics,
            'order_metrics': order_metrics,
            'customer_metrics': customer_metrics,
            'product_metrics': product_metrics
        }
    
    @staticmethod
    def _get_revenue_metrics(current_date: datetime) -> Dict:
        """Get revenue metrics for different periods"""
        last_month = current_date - timedelta(days=30)
        last_week = current_date - timedelta(days=7)
        yesterday = current_date - timedelta(days=1)
        
        total_revenue = BusinessIntelligence._get_revenue_for_period()
        monthly_revenue = BusinessIntelligence._get_revenue_for_period(start_date=last_month)
        weekly_revenue = BusinessIntelligence._get_revenue_for_period(start_date=last_week)
        daily_revenue = BusinessIntelligence._get_revenue_for_period(start_date=yesterday)
        
        prev_month_revenue = BusinessIntelligence._get_revenue_for_period(
            start_date=current_date - timedelta(days=60),
            end_date=last_month
        )
        revenue_growth = BusinessIntelligence._calculate_growth_rate(monthly_revenue, prev_month_revenue)
        
        return {
            'total_revenue': float(total_revenue),
            'monthly_revenue': float(monthly_revenue),
            'weekly_revenue': float(weekly_revenue),
            'daily_revenue': float(daily_revenue),
            'revenue_growth_rate': float(revenue_growth)
        }
    
    @staticmethod
    def _get_order_metrics(current_date: datetime) -> Dict:
        """Get order metrics for different periods"""
        last_month = current_date - timedelta(days=30)
        last_week = current_date - timedelta(days=7)
        
        total_orders = BusinessIntelligence._get_orders_for_period()
        monthly_orders = BusinessIntelligence._get_orders_for_period(start_date=last_month)
        weekly_orders = BusinessIntelligence._get_orders_for_period(start_date=last_week)
        
        prev_month_orders = BusinessIntelligence._get_orders_for_period(
            start_date=current_date - timedelta(days=60),
            end_date=last_month
        )
        order_growth = BusinessIntelligence._calculate_growth_rate(monthly_orders, prev_month_orders)
        
        monthly_revenue = BusinessIntelligence._get_revenue_for_period(
            start_date=last_month
        )
        avg_order_value = monthly_revenue / monthly_orders if monthly_orders > 0 else 0
        
        return {
            'total_orders': total_orders,
            'monthly_orders': monthly_orders,
            'weekly_orders': weekly_orders,
            'avg_order_value': float(avg_order_value),
            'order_growth_rate': float(order_growth)
        }
    
    @staticmethod
    def _get_customer_metrics() -> Dict:
        """Get customer metrics"""
        total_customers = db.session.query(func.count(User.id)).scalar() or 0
        active_customers = BusinessIntelligence._get_active_customers(days=30)
        new_customers = BusinessIntelligence._get_new_customers(days=30)
        customer_lifetime_value = BusinessIntelligence._calculate_clv()
        churn_rate = BusinessIntelligence._calculate_churn_rate()
        
        return {
            'total_customers': total_customers,
            'active_customers': active_customers,
            'new_customers': new_customers,
            'customer_lifetime_value': float(customer_lifetime_value),
            'churn_rate': float(churn_rate)
        }
    
    @staticmethod
    def _get_product_metrics() -> Dict:
        """Get product metrics"""
        total_products = db.session.query(func.count(Product.id)).scalar() or 0
        active_products = BusinessIntelligence._get_active_products(days=30)
        
        return {
            'total_products': total_products,
            'active_products': active_products
        }
    
    @staticmethod
    def get_conversion_funnel() -> Dict:
        """
        Analyze conversion funnel from users to orders
        """
        # Total registered users
        total_users = db.session.query(func.count(User.id)).scalar() or 0
        
        # Users who have placed at least one order
        users_with_orders = db.session.query(
            func.count(func.distinct(Order.user_id))
        ).filter(Order.status.in_(['completed', 'pending'])).scalar() or 0
        
        # Users with completed orders
        users_with_completed_orders = db.session.query(
            func.count(func.distinct(Order.user_id))
        ).filter(Order.status == 'completed').scalar() or 0
        
        # Users with multiple orders (repeat customers)
        repeat_customers = db.session.query(
            func.count(func.distinct(Order.user_id))
        ).filter(Order.status == 'completed').group_by(Order.user_id).having(
            func.count(Order.id) > 1
        ).count()
        
        # Calculate conversion rates
        order_conversion_rate = (users_with_orders / total_users * 100) if total_users > 0 else 0
        completion_rate = (users_with_completed_orders / users_with_orders * 100) if users_with_orders > 0 else 0
        repeat_rate = (repeat_customers / users_with_completed_orders * 100) if users_with_completed_orders > 0 else 0
        
        return {
            'funnel_stages': {
                'registered_users': total_users,
                'users_with_orders': users_with_orders,
                'users_with_completed_orders': users_with_completed_orders,
                'repeat_customers': repeat_customers
            },
            'conversion_rates': {
                'order_conversion_rate': float(order_conversion_rate),
                'completion_rate': float(completion_rate),
                'repeat_customer_rate': float(repeat_rate)
            }
        }
    
    @staticmethod
    def get_abc_analysis() -> Dict:
        """
        ABC Analysis for inventory management
        """
        # Get product revenue data
        product_revenue = db.session.query(
            Product.id,
            Product.name,
            Category.name.label('category_name'),
            func.coalesce(func.sum(OrderItem.subtotal), 0).label('total_revenue')
        ).outerjoin(
            OrderItem, Product.id == OrderItem.product_id
        ).outerjoin(
            Order, and_(OrderItem.order_id == Order.id, Order.status == 'completed')
        ).outerjoin(
            Category, Product.category_id == Category.id
        ).group_by(
            Product.id, Product.name, Category.name
        ).order_by(desc('total_revenue')).all()
        
        if not product_revenue:
            return {'error': 'No product data available'}
        
        # Convert to DataFrame
        df = pd.DataFrame([
            {
                'product_id': p.id,
                'name': p.name,
                'category': p.category_name or 'Uncategorized',
                'revenue': float(p.total_revenue)
            }
            for p in product_revenue
        ])
        
        # Calculate cumulative percentage
        df['cumulative_revenue'] = df['revenue'].cumsum()
        total_revenue = df['revenue'].sum()
        df['cumulative_percentage'] = (df['cumulative_revenue'] / total_revenue * 100) if total_revenue > 0 else 0
        
        # Classify into ABC categories
        def classify_abc(cumulative_percentage):
            if cumulative_percentage <= 80:
                return 'A'
            elif cumulative_percentage <= 95:
                return 'B'
            else:
                return 'C'
        
        df['abc_category'] = df['cumulative_percentage'].apply(classify_abc)
        
        # Calculate category statistics
        category_stats = df.groupby('abc_category').agg({
            'product_id': 'count',
            'revenue': 'sum'
        }).reset_index()
        
        category_stats['revenue_percentage'] = (category_stats['revenue'] / total_revenue * 100) if total_revenue > 0 else 0
        category_stats['product_percentage'] = (category_stats['product_id'] / len(df) * 100) if len(df) > 0 else 0
        
        return {
            'products': df.to_dict('records'),
            'category_summary': {
                row['abc_category']: {
                    'product_count': int(row['product_id']),
                    'revenue': float(row['revenue']),
                    'revenue_percentage': float(row['revenue_percentage']),
                    'product_percentage': float(row['product_percentage'])
                }
                for _, row in category_stats.iterrows()
            },
            'recommendations': {
                'A': 'High priority - Focus on stock availability and customer satisfaction',
                'B': 'Medium priority - Monitor regularly and optimize when possible',
                'C': 'Low priority - Consider discontinuation or minimal stock'
            }
        }
    
    @staticmethod
    def get_customer_segmentation() -> Dict:
        """
        Advanced customer segmentation based on behavior
        """
        # Get customer data
        customer_data = db.session.query(
            User.id,
            User.name,
            User.email,
            User.created_at,
            func.count(Order.id).label('order_count'),
            func.sum(Order.total).label('total_spent'),
            func.avg(Order.total).label('avg_order_value'),
            func.max(Order.created_at).label('last_order_date'),
            func.min(Order.created_at).label('first_order_date')
        ).outerjoin(
            Order, and_(User.id == Order.user_id, Order.status == 'completed')
        ).group_by(
            User.id, User.name, User.email, User.created_at
        ).all()
        
        if not customer_data:
            return {'error': 'No customer data available'}
        
        current_date = datetime.now(timezone.utc)
        
        # Convert to DataFrame
        df = pd.DataFrame([
            {
                'user_id': c.id,
                'name': c.name,
                'email': c.email,
                'registration_date': c.created_at,
                'order_count': c.order_count or 0,
                'total_spent': float(c.total_spent or 0),
                'avg_order_value': float(c.avg_order_value or 0),
                'last_order_date': c.last_order_date,
                'first_order_date': c.first_order_date,
                'days_since_registration': (current_date - c.created_at).days,
                'days_since_last_order': (current_date - c.last_order_date).days if c.last_order_date else None
            }
            for c in customer_data
        ])
        
        # Segment customers
        def segment_customer(row):
            order_count = row['order_count']
            days_since_last = row['days_since_last_order']
            
            if order_count == 0:
                return 'Prospects'
            
            if order_count == 1:
                return 'New Customers' if days_since_last <= 30 else 'One-time Buyers'
            
            if order_count >= 2:
                if days_since_last <= 30:
                    return 'Active Customers'
                elif days_since_last <= 90:
                    return 'At Risk'
                else:
                    return 'Inactive Customers'
            
            return 'Unknown'
        
        df['segment'] = df.apply(segment_customer, axis=1)
        
        # Calculate segment statistics
        segment_stats = df.groupby('segment').agg({
            'user_id': 'count',
            'total_spent': 'sum',
            'avg_order_value': 'mean',
            'order_count': 'mean'
        }).reset_index()
        
        segment_stats.columns = ['segment', 'customer_count', 'total_revenue', 'avg_order_value', 'avg_orders']
        
        # Add recommendations for each segment
        recommendations = {
            'Prospects': 'Send welcome emails and first-purchase incentives',
            'New Customers': 'Nurture with onboarding sequence and product recommendations',
            'One-time Buyers': 'Re-engagement campaigns with special offers',
            'Active Customers': 'Loyalty programs and cross-selling opportunities',
            'At Risk': 'Win-back campaigns and personalized offers',
            'Inactive Customers': 'Reactivation campaigns or surveys to understand issues'
        }
        
        return {
            'segments': {
                row['segment']: {
                    'customer_count': int(row['customer_count']),
                    'total_revenue': float(row['total_revenue']),
                    'avg_order_value': float(row['avg_order_value']),
                    'avg_orders': float(row['avg_orders']),
                    'recommendation': recommendations.get(row['segment'], 'Monitor segment')
                }
                for _, row in segment_stats.iterrows()
            },
            'customers': df.to_dict('records')
        }
    
    @staticmethod
    def get_profit_analysis() -> Dict:
        """
        Profit analysis by product and category
        """
        # Assuming cost is 60% of price (you can adjust this or add cost field to Product model)
        COST_RATIO = 0.6
        
        profit_data = db.session.query(
            Product.id,
            Product.name,
            Product.price,
            Category.name.label('category_name'),
            func.coalesce(func.sum(OrderItem.quantity), 0).label('units_sold'),
            func.coalesce(func.sum(OrderItem.subtotal), 0).label('revenue')
        ).outerjoin(
            OrderItem, Product.id == OrderItem.product_id
        ).outerjoin(
            Order, and_(OrderItem.order_id == Order.id, Order.status == 'completed')
        ).outerjoin(
            Category, Product.category_id == Category.id
        ).group_by(
            Product.id, Product.name, Product.price, Category.name
        ).all()
        
        if not profit_data:
            return {'error': 'No profit data available'}
        
        # Calculate profit metrics
        products = []
        category_profits = defaultdict(lambda: {'revenue': 0, 'profit': 0, 'units_sold': 0})
        
        for p in profit_data:
            cost_per_unit = float(p.price) * COST_RATIO
            total_cost = cost_per_unit * p.units_sold
            profit = float(p.revenue) - total_cost
            profit_margin = (profit / float(p.revenue) * 100) if p.revenue > 0 else 0
            
            product_data = {
                'product_id': p.id,
                'name': p.name,
                'price': float(p.price),
                'cost_per_unit': cost_per_unit,
                'category': p.category_name or 'Uncategorized',
                'units_sold': p.units_sold,
                'revenue': float(p.revenue),
                'total_cost': total_cost,
                'profit': profit,
                'profit_margin': profit_margin
            }
            products.append(product_data)
            
            # Aggregate by category
            category = p.category_name or 'Uncategorized'
            category_profits[category]['revenue'] += float(p.revenue)
            category_profits[category]['profit'] += profit
            category_profits[category]['units_sold'] += p.units_sold
        
        # Calculate category profit margins
        category_summary = {}
        for category, data in category_profits.items():
            profit_margin = (data['profit'] / data['revenue'] * 100) if data['revenue'] > 0 else 0
            category_summary[category] = {
                'revenue': data['revenue'],
                'profit': data['profit'],
                'units_sold': data['units_sold'],
                'profit_margin': profit_margin
            }
        
        # Sort products by profit
        products.sort(key=lambda x: x['profit'], reverse=True)
        
        return {
            'products': products,
            'category_summary': category_summary,
            'total_metrics': {
                'total_revenue': sum(p['revenue'] for p in products),
                'total_profit': sum(p['profit'] for p in products),
                'overall_margin': (sum(p['profit'] for p in products) / sum(p['revenue'] for p in products) * 100) if sum(p['revenue'] for p in products) > 0 else 0
            }
        }
    
    # Helper methods
    @staticmethod
    def _get_revenue_for_period(start_date=None, end_date=None):
        query = db.session.query(func.sum(Order.total)).filter(Order.status == 'completed')
        if start_date:
            query = query.filter(Order.created_at >= start_date)
        if end_date:
            query = query.filter(Order.created_at <= end_date)
        return float(query.scalar() or 0)
    
    @staticmethod
    def _get_orders_for_period(start_date=None, end_date=None):
        query = db.session.query(func.count(Order.id)).filter(Order.status == 'completed')
        if start_date:
            query = query.filter(Order.created_at >= start_date)
        if end_date:
            query = query.filter(Order.created_at <= end_date)
        return query.scalar() or 0
    
    @staticmethod
    def _get_active_customers(days=30):
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
        return db.session.query(func.count(func.distinct(Order.user_id))).filter(
            and_(Order.created_at >= cutoff_date, Order.status == 'completed')
        ).scalar() or 0
    
    @staticmethod
    def _get_new_customers(days=30):
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
        return db.session.query(func.count(User.id)).filter(
            User.created_at >= cutoff_date
        ).scalar() or 0
    
    @staticmethod
    def _get_active_products(days=30):
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
        return db.session.query(func.count(func.distinct(OrderItem.product_id))).join(
            Order, OrderItem.order_id == Order.id
        ).filter(
            and_(Order.created_at >= cutoff_date, Order.status == 'completed')
        ).scalar() or 0
    
    @staticmethod
    def _calculate_growth_rate(current, previous):
        if previous == 0:
            return 100 if current > 0 else 0
        return ((current - previous) / previous) * 100
    
    @staticmethod
    def _calculate_clv():
        # Simple CLV calculation: Average order value * Purchase frequency * Customer lifespan
        avg_order_value = db.session.query(func.avg(Order.total)).filter(
            Order.status == 'completed'
        ).scalar() or 0
        
        # Average orders per customer
        total_orders = db.session.query(func.count(Order.id)).filter(
            Order.status == 'completed'
        ).scalar() or 0
        
        total_customers = db.session.query(func.count(func.distinct(Order.user_id))).filter(
            Order.status == 'completed'
        ).scalar() or 1
        
        avg_orders_per_customer = total_orders / total_customers
        
        # Assume average customer lifespan of 2 years
        customer_lifespan_years = 2
        
        return float(avg_order_value) * avg_orders_per_customer * customer_lifespan_years
    
    @staticmethod
    def _calculate_churn_rate():
        # Customers who haven't ordered in the last 90 days
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=90)
        
        total_customers = db.session.query(func.count(func.distinct(Order.user_id))).filter(
            Order.status == 'completed'
        ).scalar() or 1
        
        active_customers = db.session.query(func.count(func.distinct(Order.user_id))).filter(
            and_(Order.created_at >= cutoff_date, Order.status == 'completed')
        ).scalar() or 0
        
        churned_customers = total_customers - active_customers
        return (churned_customers / total_customers) * 100
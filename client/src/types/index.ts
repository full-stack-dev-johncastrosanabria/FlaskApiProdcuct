// Tipos de datos de la API
export interface User {
  id: number;
  name: string;
  email: string;
  created_at: string;
  updated_at?: string;
}

export interface Category {
  id: number;
  name: string;
  description: string;
  created_at: string;
  product_count?: number;
}

export interface Product {
  id: number;
  name: string;
  description: string;
  price: number;
  stock: number;
  category_id: number;
  category?: string;
  created_at: string;
  updated_at?: string;
}

export interface OrderItem {
  id: number;
  product_id: number;
  product_name?: string;
  quantity: number;
  price: number;
  subtotal: number;
}

export interface Order {
  id: number;
  user_id: number;
  user_name?: string;
  total: number;
  status: 'pending' | 'completed' | 'cancelled';
  items: OrderItem[];
  created_at: string;
  updated_at?: string;
}

// Tipos para formularios
export interface CreateUserData {
  name: string;
  email: string;
}

export interface CreateProductData {
  name: string;
  price: number;
  stock: number;
  category_id: number;
  description: string;
}

export interface CreateCategoryData {
  name: string;
  description: string;
}

export interface CreateOrderData {
  user_id: number;
  items: {
    product_id: number;
    quantity: number;
  }[];
}

// Tipos para respuestas de la API
export interface ApiResponse<T> {
  success: boolean;
  data: T;
  message?: string;
  error?: string;
  count?: number;
}

// Tipos para análisis básicos
export interface SalesAnalytics {
  total_sales: number;
  total_orders: number;
  total_customers: number;
  total_products: number;
  average_order_value: number;
  last_month_sales: number;
  pending_orders: number;
}

export interface InventoryAnalytics {
  total_products: number;
  total_stock: number;
  total_value: number;
  low_stock_count: number;
  out_of_stock_count: number;
}

export interface DashboardData {
  sales: SalesAnalytics;
  inventory: InventoryAnalytics;
}

// Tipos para análisis avanzados
export interface KPIDashboard {
  revenue_metrics: {
    total_revenue: number;
    monthly_revenue: number;
    weekly_revenue: number;
    daily_revenue: number;
    revenue_growth_rate: number;
  };
  order_metrics: {
    total_orders: number;
    monthly_orders: number;
    weekly_orders: number;
    avg_order_value: number;
    order_growth_rate: number;
  };
  customer_metrics: {
    total_customers: number;
    active_customers: number;
    new_customers: number;
    customer_lifetime_value: number;
    churn_rate: number;
  };
  product_metrics: {
    total_products: number;
    active_products: number;
  };
}

export interface SalesByPeriod {
  period: string;
  order_count: number;
  total_sales: number;
}

export interface TopProduct {
  product_id: number;
  product_name: string;
  total_quantity: number;
  total_revenue: number;
}

export interface TopCustomer {
  user_id: number;
  user_name: string;
  user_email: string;
  order_count: number;
  total_spent: number;
}

export interface SalesByCategory {
  category_id: number;
  category_name: string;
  total_quantity: number;
  total_revenue: number;
}

export interface SalesForecast {
  forecast: {
    date: string;
    predicted_sales: number;
    confidence_interval_lower: number;
    confidence_interval_upper: number;
  }[];
  model_metrics: {
    rmse: number;
    r_squared: number;
    data_points_used: number;
  };
}

export interface CohortAnalysis {
  cohort: string;
  size: number;
  retention_rates: Record<string, number>;
}

export interface RFMAnalysis {
  user_id: number;
  name: string;
  email: string;
  recency: number;
  frequency: number;
  monetary: number;
  r_score: number;
  f_score: number;
  m_score: number;
  rfm_score: string;
  segment: string;
}

export interface CustomerSegmentation {
  segments: Record<string, {
    customer_count: number;
    total_revenue: number;
    avg_order_value: number;
    avg_orders: number;
    recommendation: string;
  }>;
  customers: Array<{
    user_id: number;
    name: string;
    email: string;
    order_count: number;
    total_spent: number;
    segment: string;
  }>;
}

export interface ConversionFunnel {
  funnel_stages: {
    registered_users: number;
    users_with_orders: number;
    users_with_completed_orders: number;
    repeat_customers: number;
  };
  conversion_rates: {
    order_conversion_rate: number;
    completion_rate: number;
    repeat_customer_rate: number;
  };
}

export interface ProductPerformance {
  product_id: number;
  name: string;
  price: number;
  category: string;
  total_sold: number;
  total_revenue: number;
  stock: number;
  revenue_per_unit: number;
  stock_turnover: number;
  performance_category: 'Star Products' | 'Cash Cows' | 'Question Marks' | 'Dogs';
  recommendation: string;
}

export interface ABCAnalysis {
  products: Array<{
    product_id: number;
    name: string;
    category: string;
    revenue: number;
    cumulative_percentage: number;
    abc_category: 'A' | 'B' | 'C';
  }>;
  category_summary: Record<string, {
    product_count: number;
    revenue: number;
    revenue_percentage: number;
    product_percentage: number;
  }>;
  recommendations: Record<string, string>;
}

export interface SeasonalAnalysis {
  seasonal_indices: Record<string, number>;
  peak_months: Record<string, number>;
  low_months: Record<string, number>;
  monthly_data: Array<{
    year: number;
    month: number;
    total_sales: number;
    order_count: number;
  }>;
}

export interface ProfitAnalysis {
  products: Array<{
    product_id: number;
    name: string;
    price: number;
    cost_per_unit: number;
    category: string;
    units_sold: number;
    revenue: number;
    total_cost: number;
    profit: number;
    profit_margin: number;
  }>;
  category_summary: Record<string, {
    revenue: number;
    profit: number;
    units_sold: number;
    profit_margin: number;
  }>;
  total_metrics: {
    total_revenue: number;
    total_profit: number;
    overall_margin: number;
  };
}

// Tipos para filtros
export interface ProductFilters {
  min_price?: number;
  max_price?: number;
  category?: number;
}

export interface OrderFilters {
  status?: string;
  user_id?: number;
}

export interface AnalyticsFilters {
  start_date?: string;
  end_date?: string;
  period?: 'day' | 'week' | 'month';
  limit?: number;
}

// Tipos para notificaciones
export type ToastType = 'success' | 'error' | 'info' | 'warning';

export interface ToastMessage {
  message: string;
  type: ToastType;
  duration?: number;
}

// Tipos para gráficos
export interface ChartDataPoint {
  label: string;
  value: number;
  color?: string;
}

export interface TimeSeriesDataPoint {
  date: string;
  value: number;
  forecast?: boolean;
  confidence_lower?: number;
  confidence_upper?: number;
}

export interface ChartConfig {
  type: 'line' | 'bar' | 'pie' | 'doughnut' | 'area';
  title: string;
  data: ChartDataPoint[] | TimeSeriesDataPoint[];
  options?: {
    responsive?: boolean;
    maintainAspectRatio?: boolean;
    showLegend?: boolean;
    showTooltips?: boolean;
  };
}
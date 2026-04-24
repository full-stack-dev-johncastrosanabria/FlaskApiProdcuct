import axios, { AxiosResponse } from 'axios';
import type {
  ApiResponse,
  User,
  Product,
  Category,
  Order,
  CreateUserData,
  CreateProductData,
  CreateCategoryData,
  CreateOrderData,
  ProductFilters,
  OrderFilters,
  DashboardData,
  KPIDashboard,
  SalesByPeriod,
  TopProduct,
  TopCustomer,
  SalesByCategory,
  SalesForecast,
  CohortAnalysis,
  RFMAnalysis,
  CustomerSegmentation,
  ConversionFunnel,
  ProductPerformance,
  ABCAnalysis,
  SeasonalAnalysis,
  ProfitAnalysis
} from '../types';

// Configuración de Axios
const api = axios.create({
  baseURL: 'http://localhost:5001/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Interceptor para manejo de errores
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

// Clase principal del servicio API
export class ApiService {
  // Health Check
  static async healthCheck(): Promise<{ status: string; timestamp: string }> {
    const response = await api.get('/health');
    return response.data;
  }

  // === USUARIOS ===
  static async getUsers(): Promise<ApiResponse<User[]>> {
    const response: AxiosResponse<ApiResponse<User[]>> = await api.get('/users');
    return response.data;
  }

  static async getUser(id: number): Promise<ApiResponse<User>> {
    const response: AxiosResponse<ApiResponse<User>> = await api.get(`/users/${id}`);
    return response.data;
  }

  static async createUser(data: CreateUserData): Promise<ApiResponse<User>> {
    const response: AxiosResponse<ApiResponse<User>> = await api.post('/users', data);
    return response.data;
  }

  static async updateUser(id: number, data: Partial<CreateUserData>): Promise<ApiResponse<User>> {
    const response: AxiosResponse<ApiResponse<User>> = await api.put(`/users/${id}`, data);
    return response.data;
  }

  static async deleteUser(id: number): Promise<ApiResponse<User>> {
    const response: AxiosResponse<ApiResponse<User>> = await api.delete(`/users/${id}`);
    return response.data;
  }

  // === CATEGORÍAS ===
  static async getCategories(): Promise<ApiResponse<Category[]>> {
    const response: AxiosResponse<ApiResponse<Category[]>> = await api.get('/categories');
    return response.data;
  }

  static async getCategory(id: number): Promise<ApiResponse<Category>> {
    const response: AxiosResponse<ApiResponse<Category>> = await api.get(`/categories/${id}`);
    return response.data;
  }

  static async createCategory(data: CreateCategoryData): Promise<ApiResponse<Category>> {
    const response: AxiosResponse<ApiResponse<Category>> = await api.post('/categories', data);
    return response.data;
  }

  static async deleteCategory(id: number): Promise<ApiResponse<Category>> {
    const response: AxiosResponse<ApiResponse<Category>> = await api.delete(`/categories/${id}`);
    return response.data;
  }

  // === PRODUCTOS ===
  static async getProducts(filters?: ProductFilters): Promise<ApiResponse<Product[]>> {
    const params = new URLSearchParams();
    if (filters?.min_price) params.append('min_price', filters.min_price.toString());
    if (filters?.max_price) params.append('max_price', filters.max_price.toString());
    if (filters?.category) params.append('category', filters.category.toString());

    const response: AxiosResponse<ApiResponse<Product[]>> = await api.get(`/products?${params}`);
    return response.data;
  }

  static async getProduct(id: number): Promise<ApiResponse<Product>> {
    const response: AxiosResponse<ApiResponse<Product>> = await api.get(`/products/${id}`);
    return response.data;
  }

  static async createProduct(data: CreateProductData): Promise<ApiResponse<Product>> {
    const response: AxiosResponse<ApiResponse<Product>> = await api.post('/products', data);
    return response.data;
  }

  static async updateProduct(id: number, data: Partial<CreateProductData>): Promise<ApiResponse<Product>> {
    const response: AxiosResponse<ApiResponse<Product>> = await api.put(`/products/${id}`, data);
    return response.data;
  }

  static async deleteProduct(id: number): Promise<ApiResponse<Product>> {
    const response: AxiosResponse<ApiResponse<Product>> = await api.delete(`/products/${id}`);
    return response.data;
  }

  // === ÓRDENES ===
  static async getOrders(filters?: OrderFilters): Promise<ApiResponse<Order[]>> {
    const params = new URLSearchParams();
    if (filters?.status) params.append('status', filters.status);
    if (filters?.user_id) params.append('user_id', filters.user_id.toString());

    const response: AxiosResponse<ApiResponse<Order[]>> = await api.get(`/orders?${params}`);
    return response.data;
  }

  static async getOrder(id: number): Promise<ApiResponse<Order>> {
    const response: AxiosResponse<ApiResponse<Order>> = await api.get(`/orders/${id}`);
    return response.data;
  }

  static async createOrder(data: CreateOrderData): Promise<ApiResponse<Order>> {
    const response: AxiosResponse<ApiResponse<Order>> = await api.post('/orders', data);
    return response.data;
  }

  static async updateOrder(id: number, data: { status: string }): Promise<ApiResponse<Order>> {
    const response: AxiosResponse<ApiResponse<Order>> = await api.put(`/orders/${id}`, data);
    return response.data;
  }

  static async deleteOrder(id: number): Promise<ApiResponse<Order>> {
    const response: AxiosResponse<ApiResponse<Order>> = await api.delete(`/orders/${id}`);
    return response.data;
  }

  // === ANALYTICS ===
  static async getDashboard(): Promise<ApiResponse<DashboardData>> {
    const response: AxiosResponse<ApiResponse<DashboardData>> = await api.get('/analytics/dashboard');
    return response.data;
  }

  static async getKPIDashboard(): Promise<ApiResponse<KPIDashboard>> {
    const response: AxiosResponse<ApiResponse<KPIDashboard>> = await api.get('/analytics/kpi-dashboard');
    return response.data;
  }

  static async getSalesByPeriod(period: string = 'day', limit: number = 30): Promise<ApiResponse<SalesByPeriod[]>> {
    const response: AxiosResponse<ApiResponse<SalesByPeriod[]>> = await api.get(`/analytics/sales/by-period?period=${period}&limit=${limit}`);
    return response.data;
  }

  static async getTopProducts(limit: number = 10): Promise<ApiResponse<TopProduct[]>> {
    const response: AxiosResponse<ApiResponse<TopProduct[]>> = await api.get(`/analytics/sales/top-products?limit=${limit}`);
    return response.data;
  }

  static async getTopCustomers(limit: number = 10): Promise<ApiResponse<TopCustomer[]>> {
    const response: AxiosResponse<ApiResponse<TopCustomer[]>> = await api.get(`/analytics/sales/top-customers?limit=${limit}`);
    return response.data;
  }

  static async getSalesByCategory(): Promise<ApiResponse<SalesByCategory[]>> {
    const response: AxiosResponse<ApiResponse<SalesByCategory[]>> = await api.get('/analytics/sales/by-category');
    return response.data;
  }

  static async getSalesForecast(daysAhead: number = 30): Promise<ApiResponse<SalesForecast>> {
    const response: AxiosResponse<ApiResponse<SalesForecast>> = await api.get(`/analytics/sales/forecast?days_ahead=${daysAhead}`);
    return response.data;
  }

  static async getCohortAnalysis(monthsBack: number = 12): Promise<ApiResponse<CohortAnalysis[]>> {
    const response: AxiosResponse<ApiResponse<CohortAnalysis[]>> = await api.get(`/analytics/customers/cohort-analysis?months_back=${monthsBack}`);
    return response.data;
  }

  static async getRFMAnalysis(): Promise<ApiResponse<RFMAnalysis[]>> {
    const response: AxiosResponse<ApiResponse<RFMAnalysis[]>> = await api.get('/analytics/customers/rfm-analysis');
    return response.data;
  }

  static async getCustomerSegmentation(): Promise<ApiResponse<CustomerSegmentation>> {
    const response: AxiosResponse<ApiResponse<CustomerSegmentation>> = await api.get('/analytics/customers/segmentation');
    return response.data;
  }

  static async getConversionFunnel(): Promise<ApiResponse<ConversionFunnel>> {
    const response: AxiosResponse<ApiResponse<ConversionFunnel>> = await api.get('/analytics/customers/conversion-funnel');
    return response.data;
  }

  static async getProductPerformanceMatrix(): Promise<ApiResponse<ProductPerformance[]>> {
    const response: AxiosResponse<ApiResponse<ProductPerformance[]>> = await api.get('/analytics/products/performance-matrix');
    return response.data;
  }

  static async getABCAnalysis(): Promise<ApiResponse<ABCAnalysis>> {
    const response: AxiosResponse<ApiResponse<ABCAnalysis>> = await api.get('/analytics/products/abc-analysis');
    return response.data;
  }

  static async getSeasonalAnalysis(): Promise<ApiResponse<SeasonalAnalysis>> {
    const response: AxiosResponse<ApiResponse<SeasonalAnalysis>> = await api.get('/analytics/sales/seasonal-analysis');
    return response.data;
  }

  static async getProfitAnalysis(): Promise<ApiResponse<ProfitAnalysis>> {
    const response: AxiosResponse<ApiResponse<ProfitAnalysis>> = await api.get('/analytics/financial/profit-analysis');
    return response.data;
  }

  static async getLowStockProducts(threshold: number = 10): Promise<ApiResponse<Product[]>> {
    const response: AxiosResponse<ApiResponse<Product[]>> = await api.get(`/analytics/inventory/low-stock?threshold=${threshold}`);
    return response.data;
  }

  static async getOutOfStockProducts(): Promise<ApiResponse<Product[]>> {
    const response: AxiosResponse<ApiResponse<Product[]>> = await api.get('/analytics/inventory/out-of-stock');
    return response.data;
  }

  static async getInventoryValue(): Promise<ApiResponse<{ total_value: number }>> {
    const response: AxiosResponse<ApiResponse<{ total_value: number }>> = await api.get('/analytics/inventory/value');
    return response.data;
  }
}

export default ApiService;
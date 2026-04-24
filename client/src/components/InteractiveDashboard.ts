/**
 * Dashboard interactivo con gráficos en tiempo real
 */
import { ApiService } from '../services/api';
import { ChartRenderer } from '../utils/charts';
import { toast } from '../utils/toast';
import { formatPrice, formatNumber } from '../utils/helpers';

export class InteractiveDashboard {
  private dashboardContainer: HTMLElement;
  private refreshInterval: NodeJS.Timeout | null = null;

  constructor() {
    this.dashboardContainer = document.getElementById('dashboard') as HTMLElement;

    if (!this.dashboardContainer) {
      console.error('Dashboard container not found');
      return;
    }
  }

  async init(): Promise<void> {
    await this.loadDashboard();
    // Auto-refresh cada 5 minutos
    this.refreshInterval = setInterval(() => this.loadDashboard(), 5 * 60 * 1000);
  }

  destroy(): void {
    if (this.refreshInterval) {
      clearInterval(this.refreshInterval);
    }
  }

  async loadDashboard(): Promise<void> {
    this.dashboardContainer.innerHTML = '<p class="loading">Cargando dashboard...</p>';

    try {
      const [summary, dailySales, categorySales, topProducts, paymentMethods, customerGrowth, inventoryStatus, revenueByHour] = await Promise.all([
        ApiService.get('/api/dashboard/summary'),
        ApiService.get('/api/dashboard/daily-sales'),
        ApiService.get('/api/dashboard/category-sales'),
        ApiService.get('/api/dashboard/top-products'),
        ApiService.get('/api/dashboard/payment-methods'),
        ApiService.get('/api/dashboard/customer-growth'),
        ApiService.get('/api/dashboard/inventory-status'),
        ApiService.get('/api/dashboard/revenue-by-hour')
      ]);

      if (summary.success) {
        this.renderDashboard(
          summary.data,
          dailySales.data,
          categorySales.data,
          topProducts.data,
          paymentMethods.data,
          customerGrowth.data,
          inventoryStatus.data,
          revenueByHour.data
        );
      }
    } catch (error) {
      this.dashboardContainer.innerHTML = '<p class="error">Error al cargar dashboard</p>';
      toast.error('Error al cargar dashboard');
    }
  }

  private renderDashboard(
    summary: any,
    dailySales: any,
    categorySales: any,
    topProducts: any,
    paymentMethods: any,
    customerGrowth: any,
    inventoryStatus: any,
    revenueByHour: any
  ): void {
    this.dashboardContainer.innerHTML = `
      <div class="dashboard-container">
        <!-- Header con métricas principales -->
        <div class="dashboard-header">
          <h1>📊 Dashboard Interactivo</h1>
          <div class="header-metrics">
            <div class="metric-card primary">
              <div class="metric-icon">💰</div>
              <div class="metric-info">
                <div class="metric-label">Ventas Totales</div>
                <div class="metric-value">${formatPrice(summary.total_sales)}</div>
              </div>
            </div>
            <div class="metric-card">
              <div class="metric-icon">📦</div>
              <div class="metric-info">
                <div class="metric-label">Órdenes</div>
                <div class="metric-value">${formatNumber(summary.total_orders)}</div>
              </div>
            </div>
            <div class="metric-card">
              <div class="metric-icon">👥</div>
              <div class="metric-info">
                <div class="metric-label">Clientes</div>
                <div class="metric-value">${formatNumber(summary.total_customers)}</div>
              </div>
            </div>
            <div class="metric-card">
              <div class="metric-icon">📈</div>
              <div class="metric-info">
                <div class="metric-label">Promedio/Orden</div>
                <div class="metric-value">${formatPrice(summary.avg_order_value)}</div>
              </div>
            </div>
            <div class="metric-card">
              <div class="metric-icon">📊</div>
              <div class="metric-info">
                <div class="metric-label">Hoy</div>
                <div class="metric-value">${formatPrice(summary.today_sales)}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Sección de gráficos -->
        <div class="charts-section">
          <!-- Fila 1: Ventas diarias y Categorías -->
          <div class="charts-row">
            <div class="chart-container full-width">
              <h3>📈 Ventas Diarias (Últimos 30 días)</h3>
              <div id="daily-sales-chart" class="chart"></div>
            </div>
          </div>

          <!-- Fila 2: Categorías y Métodos de Pago -->
          <div class="charts-row">
            <div class="chart-container half-width">
              <h3>🏷️ Ventas por Categoría</h3>
              <div id="category-sales-chart" class="chart"></div>
            </div>
            <div class="chart-container half-width">
              <h3>💳 Métodos de Pago</h3>
              <div id="payment-methods-chart" class="chart"></div>
            </div>
          </div>

          <!-- Fila 3: Productos Top y Crecimiento de Clientes -->
          <div class="charts-row">
            <div class="chart-container full-width">
              <h3>🏆 Top 10 Productos Más Vendidos</h3>
              <div id="top-products-chart" class="chart"></div>
            </div>
          </div>

          <!-- Fila 4: Crecimiento de Clientes e Inventario -->
          <div class="charts-row">
            <div class="chart-container half-width">
              <h3>📊 Crecimiento de Clientes</h3>
              <div id="customer-growth-chart" class="chart"></div>
            </div>
            <div class="chart-container half-width">
              <h3>🏪 Stock por Categoría</h3>
              <div id="inventory-status-chart" class="chart"></div>
            </div>
          </div>

          <!-- Fila 5: Ingresos por Hora -->
          <div class="charts-row">
            <div class="chart-container full-width">
              <h3>⏰ Ingresos por Hora del Día</h3>
              <div id="revenue-by-hour-chart" class="chart"></div>
            </div>
          </div>
        </div>

        <!-- Botones de acción -->
        <div class="dashboard-actions">
          <button class="btn btn-primary" onclick="interactiveDashboard.loadDashboard()">
            🔄 Actualizar Ahora
          </button>
          <button class="btn btn-secondary" onclick="interactiveDashboard.exportData()">
            📥 Descargar Datos
          </button>
        </div>
      </div>
    `;

    // Renderizar gráficos
    this.renderCharts(
      dailySales,
      categorySales,
      topProducts,
      paymentMethods,
      customerGrowth,
      inventoryStatus,
      revenueByHour
    );
  }

  private renderCharts(
    dailySales: any,
    categorySales: any,
    topProducts: any,
    paymentMethods: any,
    customerGrowth: any,
    inventoryStatus: any,
    revenueByHour: any
  ): void {
    // Gráfico de ventas diarias
    const dailySalesChart = document.getElementById('daily-sales-chart');
    if (dailySalesChart && dailySales.labels.length > 0) {
      const data = dailySales.labels.map((_: string, i: number) => ({
        date: new Date().toISOString(),
        value: dailySales.datasets[0].data[i] || 0
      }));
      ChartRenderer.createLineChart(dailySalesChart, data, 'Ventas Diarias');
    }

    // Gráfico de categorías
    const categorySalesChart = document.getElementById('category-sales-chart');
    if (categorySalesChart && categorySales.labels.length > 0) {
      const data = categorySales.labels.map((label: string, i: number) => ({
        label,
        value: categorySales.data[i] || 0
      }));
      ChartRenderer.createPieChart(categorySalesChart, data, 'Ventas por Categoría');
    }

    // Gráfico de métodos de pago
    const paymentMethodsChart = document.getElementById('payment-methods-chart');
    if (paymentMethodsChart && paymentMethods.labels.length > 0) {
      const data = paymentMethods.labels.map((label: string, i: number) => ({
        label,
        value: paymentMethods.data[i] || 0
      }));
      ChartRenderer.createPieChart(paymentMethodsChart, data, 'Métodos de Pago');
    }

    // Gráfico de productos top
    const topProductsChart = document.getElementById('top-products-chart');
    if (topProductsChart && topProducts.labels.length > 0) {
      const data = topProducts.labels.map((label: string, i: number) => ({
        label,
        value: topProducts.datasets[0].data[i] || 0
      }));
      ChartRenderer.createBarChart(topProductsChart, data, 'Top 10 Productos');
    }

    // Gráfico de crecimiento de clientes
    const customerGrowthChart = document.getElementById('customer-growth-chart');
    if (customerGrowthChart && customerGrowth.labels.length > 0) {
      const data = customerGrowth.labels.map((_: string, i: number) => ({
        date: new Date().toISOString(),
        value: customerGrowth.datasets[0].data[i] || 0
      }));
      ChartRenderer.createLineChart(customerGrowthChart, data, 'Crecimiento de Clientes');
    }

    // Gráfico de estado del inventario
    const inventoryStatusChart = document.getElementById('inventory-status-chart');
    if (inventoryStatusChart && inventoryStatus.labels.length > 0) {
      const data = inventoryStatus.labels.map((label: string, i: number) => ({
        label,
        value: inventoryStatus.datasets[0].data[i] || 0
      }));
      ChartRenderer.createBarChart(inventoryStatusChart, data, 'Stock por Categoría');
    }

    // Gráfico de ingresos por hora
    const revenueByHourChart = document.getElementById('revenue-by-hour-chart');
    if (revenueByHourChart && revenueByHour.labels.length > 0) {
      const data = revenueByHour.labels.map((_: string, i: number) => ({
        date: new Date().toISOString(),
        value: revenueByHour.datasets[0].data[i] || 0
      }));
      ChartRenderer.createLineChart(revenueByHourChart, data, 'Ingresos por Hora');
    }
  }

  async exportData(): Promise<void> {
    try {
      const summary = await ApiService.get('/api/dashboard/summary');
      const data = {
        timestamp: new Date().toISOString(),
        summary: summary.data
      };

      const dataStr = JSON.stringify(data, null, 2);
      const dataBlob = new Blob([dataStr], { type: 'application/json' });
      const url = URL.createObjectURL(dataBlob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `dashboard-export-${new Date().toISOString().split('T')[0]}.json`;
      link.click();
      URL.revokeObjectURL(url);

      toast.success('Datos exportados correctamente');
    } catch (error) {
      toast.error('Error al exportar datos');
    }
  }
}

// Instancia global
declare global {
  interface Window {
    interactiveDashboard: InteractiveDashboard;
  }
}

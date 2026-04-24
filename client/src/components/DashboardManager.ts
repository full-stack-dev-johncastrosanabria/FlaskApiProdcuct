import { ApiService } from '../services/api';
import { toast } from '../utils/toast';
import { formatPrice, formatNumber } from '../utils/helpers';
import type { DashboardData } from '../types';

/**
 * Gestor del dashboard de analytics
 */
export class DashboardManager {
  private dashboardContainer: HTMLElement;

  constructor() {
    this.dashboardContainer = document.getElementById('dashboard') as HTMLElement;

    if (!this.dashboardContainer) {
      console.error('Dashboard container not found');
      return;
    }
  }

  async init(): Promise<void> {
    await this.loadDashboard();
  }

  async loadDashboard(): Promise<void> {
    this.dashboardContainer.innerHTML = '<p class="loading">Cargando dashboard...</p>';
    
    try {
      const [dashboardResponse, topProductsResponse, lowStockResponse] = await Promise.all([
        ApiService.getDashboard(),
        ApiService.getTopProducts(5),
        ApiService.getLowStockProducts(10)
      ]);

      if (dashboardResponse.success) {
        this.renderDashboard(dashboardResponse.data, topProductsResponse.data, lowStockResponse.data);
      }
    } catch (error) {
      this.dashboardContainer.innerHTML = '<p class="loading">Error al cargar dashboard</p>';
      toast.error('Error al cargar dashboard');
    }
  }

  private renderDashboard(data: DashboardData, topProducts: any[], lowStock: any[]): void {
    this.dashboardContainer.innerHTML = `
      <div class="dashboard-grid">
        <!-- Métricas principales -->
        <div class="metrics-grid">
          <div class="metric-card sales">
            <div class="metric-icon">💰</div>
            <div class="metric-content">
              <div class="metric-value">${formatPrice(data.sales.total_sales)}</div>
              <div class="metric-label">Ventas Totales</div>
            </div>
          </div>
          
          <div class="metric-card orders">
            <div class="metric-icon">📦</div>
            <div class="metric-content">
              <div class="metric-value">${formatNumber(data.sales.total_orders)}</div>
              <div class="metric-label">Órdenes</div>
            </div>
          </div>
          
          <div class="metric-card customers">
            <div class="metric-icon">👥</div>
            <div class="metric-content">
              <div class="metric-value">${formatNumber(data.sales.total_customers)}</div>
              <div class="metric-label">Clientes</div>
            </div>
          </div>
          
          <div class="metric-card products">
            <div class="metric-icon">📋</div>
            <div class="metric-content">
              <div class="metric-value">${formatNumber(data.inventory.total_products)}</div>
              <div class="metric-label">Productos</div>
            </div>
          </div>
          
          <div class="metric-card average">
            <div class="metric-icon">📊</div>
            <div class="metric-content">
              <div class="metric-value">${formatPrice(data.sales.average_order_value)}</div>
              <div class="metric-label">Promedio por Orden</div>
            </div>
          </div>
          
          <div class="metric-card inventory">
            <div class="metric-icon">🏪</div>
            <div class="metric-content">
              <div class="metric-value">${formatPrice(data.inventory.total_value)}</div>
              <div class="metric-label">Valor Inventario</div>
            </div>
          </div>
        </div>

        <!-- Top productos -->
        <div class="dashboard-section">
          <h3>🏆 Top 5 Productos Más Vendidos</h3>
          <div class="top-products-list">
            ${topProducts.length > 0 ? topProducts.map((product, index) => `
              <div class="top-product-item">
                <div class="product-rank">#${index + 1}</div>
                <div class="product-info">
                  <div class="product-name">${product.product_name}</div>
                  <div class="product-stats">
                    ${formatNumber(product.total_quantity)} vendidos • ${formatPrice(product.total_revenue)}
                  </div>
                </div>
              </div>
            `).join('') : '<p class="no-data">No hay datos de ventas</p>'}
          </div>
        </div>

        <!-- Stock bajo -->
        <div class="dashboard-section">
          <h3>⚠️ Productos con Stock Bajo</h3>
          <div class="low-stock-list">
            ${lowStock.length > 0 ? lowStock.map(product => `
              <div class="low-stock-item">
                <div class="product-info">
                  <div class="product-name">${product.name}</div>
                  <div class="product-category">${product.category || 'Sin categoría'}</div>
                </div>
                <div class="stock-info">
                  <span class="stock-count ${product.stock === 0 ? 'out' : 'low'}">${product.stock}</span>
                </div>
              </div>
            `).join('') : '<p class="no-data">Todos los productos tienen stock suficiente</p>'}
          </div>
        </div>

        <!-- Resumen de inventario -->
        <div class="dashboard-section">
          <h3>📊 Resumen de Inventario</h3>
          <div class="inventory-summary">
            <div class="summary-item">
              <span class="summary-label">Total de productos:</span>
              <span class="summary-value">${formatNumber(data.inventory.total_products)}</span>
            </div>
            <div class="summary-item">
              <span class="summary-label">Stock total:</span>
              <span class="summary-value">${formatNumber(data.inventory.total_stock)} unidades</span>
            </div>
            <div class="summary-item">
              <span class="summary-label">Valor total:</span>
              <span class="summary-value">${formatPrice(data.inventory.total_value)}</span>
            </div>
            <div class="summary-item">
              <span class="summary-label">Productos con stock bajo:</span>
              <span class="summary-value warning">${formatNumber(data.inventory.low_stock_count)}</span>
            </div>
            <div class="summary-item">
              <span class="summary-label">Productos sin stock:</span>
              <span class="summary-value danger">${formatNumber(data.inventory.out_of_stock_count)}</span>
            </div>
          </div>
        </div>

        <!-- Resumen de ventas -->
        <div class="dashboard-section">
          <h3>💼 Resumen de Ventas</h3>
          <div class="sales-summary">
            <div class="summary-item">
              <span class="summary-label">Ventas totales:</span>
              <span class="summary-value">${formatPrice(data.sales.total_sales)}</span>
            </div>
            <div class="summary-item">
              <span class="summary-label">Órdenes totales:</span>
              <span class="summary-value">${formatNumber(data.sales.total_orders)}</span>
            </div>
            <div class="summary-item">
              <span class="summary-label">Clientes únicos:</span>
              <span class="summary-value">${formatNumber(data.sales.total_customers)}</span>
            </div>
            <div class="summary-item">
              <span class="summary-label">Promedio por orden:</span>
              <span class="summary-value">${formatPrice(data.sales.average_order_value)}</span>
            </div>
            <div class="summary-item">
              <span class="summary-label">Órdenes pendientes:</span>
              <span class="summary-value warning">${formatNumber(data.sales.pending_orders)}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Botón de actualizar -->
      <div class="dashboard-actions">
        <button class="btn btn-primary" onclick="dashboardManager.loadDashboard()">
          🔄 Actualizar Dashboard
        </button>
      </div>
    `;
  }
}
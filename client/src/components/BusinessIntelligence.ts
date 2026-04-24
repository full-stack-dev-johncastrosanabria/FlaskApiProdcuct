import { ApiService } from '../services/api';
import { toast } from '../utils/toast';
import { ChartRenderer } from '../utils/charts';
import { formatPrice, formatNumber } from '../utils/helpers';
import type { 
  KPIDashboard, 
  ConversionFunnel, 
  CustomerSegmentation, 
  ABCAnalysis, 
  ProfitAnalysis,
  ChartDataPoint
} from '../types';

/**
 * Gestor de inteligencia de negocios
 */
export class BusinessIntelligence {
  private container: HTMLElement;
  private currentView: string = 'kpi';

  constructor() {
    this.container = document.getElementById('business-intelligence') as HTMLElement;
    if (!this.container) {
      console.error('Business intelligence container not found');
      return;
    }
    this.init();
  }

  private init(): void {
    this.renderNavigation();
    this.loadCurrentView();
  }

  private renderNavigation(): void {
    const nav = document.createElement('div');
    nav.className = 'analytics-nav';
    nav.innerHTML = `
      <div class="nav-tabs">
        <button class="nav-tab ${this.currentView === 'kpi' ? 'active' : ''}" 
                onclick="businessIntelligence.switchView('kpi')">
          📊 Dashboard KPI
        </button>
        <button class="nav-tab ${this.currentView === 'funnel' ? 'active' : ''}" 
                onclick="businessIntelligence.switchView('funnel')">
          🔄 Embudo de Conversión
        </button>
        <button class="nav-tab ${this.currentView === 'segmentation' ? 'active' : ''}" 
                onclick="businessIntelligence.switchView('segmentation')">
          👥 Segmentación de Clientes
        </button>
        <button class="nav-tab ${this.currentView === 'abc' ? 'active' : ''}" 
                onclick="businessIntelligence.switchView('abc')">
          🔤 Análisis ABC
        </button>
        <button class="nav-tab ${this.currentView === 'profit' ? 'active' : ''}" 
                onclick="businessIntelligence.switchView('profit')">
          💰 Análisis de Rentabilidad
        </button>
      </div>
    `;
    
    this.container.innerHTML = '';
    this.container.appendChild(nav);
    
    const content = document.createElement('div');
    content.className = 'analytics-content';
    content.id = 'bi-content';
    this.container.appendChild(content);
  }

  switchView(view: string): void {
    this.currentView = view;
    this.renderNavigation();
    this.loadCurrentView();
  }

  private async loadCurrentView(): Promise<void> {
    const content = document.getElementById('bi-content') as HTMLElement;
    content.innerHTML = '<div class="loading">Cargando análisis...</div>';

    try {
      switch (this.currentView) {
        case 'kpi':
          await this.loadKPIDashboard();
          break;
        case 'funnel':
          await this.loadConversionFunnel();
          break;
        case 'segmentation':
          await this.loadCustomerSegmentation();
          break;
        case 'abc':
          await this.loadABCAnalysis();
          break;
        case 'profit':
          await this.loadProfitAnalysis();
          break;
      }
    } catch (error) {
      content.innerHTML = '<div class="error">Error al cargar análisis</div>';
      toast.error('Error al cargar inteligencia de negocios');
    }
  }

  private async loadKPIDashboard(): Promise<void> {
    const content = document.getElementById('bi-content') as HTMLElement;
    
    try {
      const response = await ApiService.getKPIDashboard();
      
      if (response.success) {
        this.renderKPIDashboard(response.data);
      } else {
        throw new Error(response.error || 'Error al obtener KPIs');
      }
    } catch (error) {
      content.innerHTML = '<div class="error">Error al cargar dashboard KPI</div>';
    }
  }

  private renderKPIDashboard(data: KPIDashboard): void {
    const content = document.getElementById('bi-content') as HTMLElement;
    
    content.innerHTML = `
      <div class="analytics-section">
        <h2>📊 Dashboard de KPIs</h2>
        
        <div class="kpi-grid">
          <!-- Métricas de Ingresos -->
          <div class="kpi-section">
            <h3>💰 Métricas de Ingresos</h3>
            <div class="metrics-row">
              <div class="metric-card">
                <div class="metric-value">${formatPrice(data.revenue_metrics.total_revenue)}</div>
                <div class="metric-label">Ingresos Totales</div>
              </div>
              <div class="metric-card">
                <div class="metric-value">${formatPrice(data.revenue_metrics.monthly_revenue)}</div>
                <div class="metric-label">Ingresos Mensuales</div>
                <div class="metric-change ${data.revenue_metrics.revenue_growth_rate >= 0 ? 'positive' : 'negative'}">
                  ${data.revenue_metrics.revenue_growth_rate >= 0 ? '↗️' : '↘️'} ${Math.abs(data.revenue_metrics.revenue_growth_rate).toFixed(1)}%
                </div>
              </div>
              <div class="metric-card">
                <div class="metric-value">${formatPrice(data.revenue_metrics.weekly_revenue)}</div>
                <div class="metric-label">Ingresos Semanales</div>
              </div>
              <div class="metric-card">
                <div class="metric-value">${formatPrice(data.revenue_metrics.daily_revenue)}</div>
                <div class="metric-label">Ingresos Diarios</div>
              </div>
            </div>
          </div>

          <!-- Métricas de Órdenes -->
          <div class="kpi-section">
            <h3>📦 Métricas de Órdenes</h3>
            <div class="metrics-row">
              <div class="metric-card">
                <div class="metric-value">${formatNumber(data.order_metrics.total_orders)}</div>
                <div class="metric-label">Órdenes Totales</div>
              </div>
              <div class="metric-card">
                <div class="metric-value">${formatNumber(data.order_metrics.monthly_orders)}</div>
                <div class="metric-label">Órdenes Mensuales</div>
                <div class="metric-change ${data.order_metrics.order_growth_rate >= 0 ? 'positive' : 'negative'}">
                  ${data.order_metrics.order_growth_rate >= 0 ? '↗️' : '↘️'} ${Math.abs(data.order_metrics.order_growth_rate).toFixed(1)}%
                </div>
              </div>
              <div class="metric-card">
                <div class="metric-value">${formatPrice(data.order_metrics.avg_order_value)}</div>
                <div class="metric-label">Valor Promedio por Orden</div>
              </div>
              <div class="metric-card">
                <div class="metric-value">${formatNumber(data.order_metrics.weekly_orders)}</div>
                <div class="metric-label">Órdenes Semanales</div>
              </div>
            </div>
          </div>

          <!-- Métricas de Clientes -->
          <div class="kpi-section">
            <h3>👥 Métricas de Clientes</h3>
            <div class="metrics-row">
              <div class="metric-card">
                <div class="metric-value">${formatNumber(data.customer_metrics.total_customers)}</div>
                <div class="metric-label">Clientes Totales</div>
              </div>
              <div class="metric-card">
                <div class="metric-value">${formatNumber(data.customer_metrics.active_customers)}</div>
                <div class="metric-label">Clientes Activos (30d)</div>
              </div>
              <div class="metric-card">
                <div class="metric-value">${formatNumber(data.customer_metrics.new_customers)}</div>
                <div class="metric-label">Nuevos Clientes (30d)</div>
              </div>
              <div class="metric-card">
                <div class="metric-value">${formatPrice(data.customer_metrics.customer_lifetime_value)}</div>
                <div class="metric-label">Valor de Vida del Cliente</div>
              </div>
            </div>
            <div class="metrics-row">
              <div class="metric-card warning">
                <div class="metric-value">${data.customer_metrics.churn_rate.toFixed(1)}%</div>
                <div class="metric-label">Tasa de Abandono</div>
              </div>
            </div>
          </div>

          <!-- Métricas de Productos -->
          <div class="kpi-section">
            <h3>📋 Métricas de Productos</h3>
            <div class="metrics-row">
              <div class="metric-card">
                <div class="metric-value">${formatNumber(data.product_metrics.total_products)}</div>
                <div class="metric-label">Productos Totales</div>
              </div>
              <div class="metric-card">
                <div class="metric-value">${formatNumber(data.product_metrics.active_products)}</div>
                <div class="metric-label">Productos Activos (30d)</div>
              </div>
            </div>
          </div>
        </div>

        <div class="kpi-insights">
          <h3>💡 Insights Clave</h3>
          <div class="insights-grid">
            <div class="insight-card ${data.revenue_metrics.revenue_growth_rate >= 0 ? 'positive' : 'negative'}">
              <h4>Crecimiento de Ingresos</h4>
              <p>Los ingresos han ${data.revenue_metrics.revenue_growth_rate >= 0 ? 'crecido' : 'disminuido'} un ${Math.abs(data.revenue_metrics.revenue_growth_rate).toFixed(1)}% este mes.</p>
            </div>
            <div class="insight-card ${data.customer_metrics.churn_rate <= 10 ? 'positive' : 'warning'}">
              <h4>Retención de Clientes</h4>
              <p>La tasa de abandono es del ${data.customer_metrics.churn_rate.toFixed(1)}%, ${data.customer_metrics.churn_rate <= 10 ? 'excelente' : 'necesita atención'}.</p>
            </div>
            <div class="insight-card">
              <h4>Eficiencia de Ventas</h4>
              <p>El valor promedio por orden es ${formatPrice(data.order_metrics.avg_order_value)}.</p>
            </div>
          </div>
        </div>
      </div>
    `;
  }

  private async loadConversionFunnel(): Promise<void> {
    const content = document.getElementById('bi-content') as HTMLElement;
    
    try {
      const response = await ApiService.getConversionFunnel();
      
      if (response.success) {
        this.renderConversionFunnel(response.data);
      } else {
        throw new Error(response.error || 'Error al obtener embudo de conversión');
      }
    } catch (error) {
      content.innerHTML = '<div class="error">Error al cargar embudo de conversión</div>';
    }
  }

  private renderConversionFunnel(data: ConversionFunnel): void {
    const content = document.getElementById('bi-content') as HTMLElement;
    
    const stages = [
      { name: 'Usuarios Registrados', value: data.funnel_stages.registered_users, rate: 100 },
      { name: 'Usuarios con Órdenes', value: data.funnel_stages.users_with_orders, rate: data.conversion_rates.order_conversion_rate },
      { name: 'Órdenes Completadas', value: data.funnel_stages.users_with_completed_orders, rate: data.conversion_rates.completion_rate },
      { name: 'Clientes Recurrentes', value: data.funnel_stages.repeat_customers, rate: data.conversion_rates.repeat_customer_rate }
    ];

    content.innerHTML = `
      <div class="analytics-section">
        <h2>🔄 Embudo de Conversión</h2>
        
        <div class="funnel-explanation">
          <p>El embudo de conversión muestra cómo los usuarios progresan desde el registro hasta convertirse en clientes recurrentes.</p>
        </div>

        <div class="conversion-funnel">
          ${stages.map((stage, index) => {
            const width = (stage.value / stages[0].value) * 100;
            return `
              <div class="funnel-stage">
                <div class="stage-bar" style="width: ${width}%">
                  <div class="stage-content">
                    <div class="stage-name">${stage.name}</div>
                    <div class="stage-metrics">
                      <span class="stage-count">${formatNumber(stage.value)}</span>
                      <span class="stage-rate">${stage.rate.toFixed(1)}%</span>
                    </div>
                  </div>
                </div>
                ${index < stages.length - 1 ? `
                  <div class="stage-arrow">
                    <div class="conversion-rate">${stages[index + 1].rate.toFixed(1)}%</div>
                  </div>
                ` : ''}
              </div>
            `;
          }).join('')}
        </div>

        <div class="funnel-metrics">
          <div class="metric-card">
            <div class="metric-value">${data.conversion_rates.order_conversion_rate.toFixed(1)}%</div>
            <div class="metric-label">Tasa de Conversión a Orden</div>
          </div>
          <div class="metric-card">
            <div class="metric-value">${data.conversion_rates.completion_rate.toFixed(1)}%</div>
            <div class="metric-label">Tasa de Completación</div>
          </div>
          <div class="metric-card">
            <div class="metric-value">${data.conversion_rates.repeat_customer_rate.toFixed(1)}%</div>
            <div class="metric-label">Tasa de Clientes Recurrentes</div>
          </div>
        </div>

        <div class="funnel-insights">
          <h3>💡 Oportunidades de Mejora</h3>
          <div class="insights-list">
            ${data.conversion_rates.order_conversion_rate < 20 ? 
              '<div class="insight-item warning">📈 La conversión a orden es baja. Considera mejorar la experiencia de usuario.</div>' : 
              '<div class="insight-item positive">✅ Buena conversión a orden.</div>'
            }
            ${data.conversion_rates.completion_rate < 80 ? 
              '<div class="insight-item warning">⚠️ Muchas órdenes no se completan. Revisa el proceso de checkout.</div>' : 
              '<div class="insight-item positive">✅ Excelente tasa de completación.</div>'
            }
            ${data.conversion_rates.repeat_customer_rate < 30 ? 
              '<div class="insight-item warning">🔄 Pocos clientes recurrentes. Implementa programas de fidelización.</div>' : 
              '<div class="insight-item positive">✅ Buena retención de clientes.</div>'
            }
          </div>
        </div>
      </div>
    `;
  }

  private async loadCustomerSegmentation(): Promise<void> {
    const content = document.getElementById('bi-content') as HTMLElement;
    
    try {
      const response = await ApiService.getCustomerSegmentation();
      
      if (response.success) {
        this.renderCustomerSegmentation(response.data);
      } else {
        throw new Error(response.error || 'Error al obtener segmentación');
      }
    } catch (error) {
      content.innerHTML = '<div class="error">Error al cargar segmentación de clientes</div>';
    }
  }

  private renderCustomerSegmentation(data: CustomerSegmentation): void {
    const content = document.getElementById('bi-content') as HTMLElement;
    
    if ('error' in data) {
      content.innerHTML = `
        <div class="analytics-section">
          <h2>👥 Segmentación de Clientes</h2>
          <div class="no-data">
            <p>No hay datos suficientes para la segmentación de clientes.</p>
          </div>
        </div>
      `;
      return;
    }

    // Preparar datos para gráfico
    const chartData: ChartDataPoint[] = Object.entries(data.segments).map(([segment, info]) => ({
      label: segment,
      value: info.customer_count
    }));

    content.innerHTML = `
      <div class="analytics-section">
        <h2>👥 Segmentación de Clientes</h2>
        
        <div class="segmentation-explanation">
          <p>Los clientes se segmentan según su comportamiento de compra y actividad reciente.</p>
        </div>

        <div class="chart-container" id="segmentation-chart"></div>

        <div class="segments-grid">
          ${Object.entries(data.segments).map(([segment, info]) => `
            <div class="segment-card">
              <h3>${this.getSegmentIcon(segment)} ${segment}</h3>
              <div class="segment-metrics">
                <div class="metric">
                  <span class="metric-value">${formatNumber(info.customer_count)}</span>
                  <span class="metric-label">Clientes</span>
                </div>
                <div class="metric">
                  <span class="metric-value">${formatPrice(info.total_revenue)}</span>
                  <span class="metric-label">Ingresos Totales</span>
                </div>
                <div class="metric">
                  <span class="metric-value">${formatPrice(info.avg_order_value)}</span>
                  <span class="metric-label">Valor Promedio</span>
                </div>
                <div class="metric">
                  <span class="metric-value">${info.avg_orders.toFixed(1)}</span>
                  <span class="metric-label">Órdenes Promedio</span>
                </div>
              </div>
              <div class="segment-recommendation">
                <strong>Estrategia:</strong> ${info.recommendation}
              </div>
            </div>
          `).join('')}
        </div>

        <div class="segmentation-table">
          <h3>Detalle de Clientes por Segmento</h3>
          <table>
            <thead>
              <tr>
                <th>Cliente</th>
                <th>Email</th>
                <th>Órdenes</th>
                <th>Total Gastado</th>
                <th>Segmento</th>
              </tr>
            </thead>
            <tbody>
              ${data.customers.slice(0, 20).map(customer => `
                <tr>
                  <td>${customer.name}</td>
                  <td>${customer.email}</td>
                  <td>${customer.order_count}</td>
                  <td>${formatPrice(customer.total_spent)}</td>
                  <td><span class="segment-badge ${customer.segment.toLowerCase().replace(' ', '-')}">${customer.segment}</span></td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      </div>
    `;

    // Renderizar gráfico
    const chartContainer = document.getElementById('segmentation-chart') as HTMLElement;
    ChartRenderer.createPieChart(chartContainer, chartData, 'Distribución de Segmentos de Clientes');
  }

  private async loadABCAnalysis(): Promise<void> {
    const content = document.getElementById('bi-content') as HTMLElement;
    
    try {
      const response = await ApiService.getABCAnalysis();
      
      if (response.success) {
        this.renderABCAnalysis(response.data);
      } else {
        throw new Error(response.error || 'Error al obtener análisis ABC');
      }
    } catch (error) {
      content.innerHTML = '<div class="error">Error al cargar análisis ABC</div>';
    }
  }

  private renderABCAnalysis(data: ABCAnalysis): void {
    const content = document.getElementById('bi-content') as HTMLElement;
    
    if ('error' in data) {
      content.innerHTML = `
        <div class="analytics-section">
          <h2>🔤 Análisis ABC</h2>
          <div class="no-data">
            <p>No hay datos de productos para el análisis ABC.</p>
          </div>
        </div>
      `;
      return;
    }

    content.innerHTML = `
      <div class="analytics-section">
        <h2>🔤 Análisis ABC de Productos</h2>
        
        <div class="abc-explanation">
          <p>El análisis ABC clasifica productos según su contribución a los ingresos:</p>
          <ul>
            <li><strong>Categoría A:</strong> 80% de los ingresos (productos críticos)</li>
            <li><strong>Categoría B:</strong> 15% de los ingresos (productos importantes)</li>
            <li><strong>Categoría C:</strong> 5% de los ingresos (productos de bajo impacto)</li>
          </ul>
        </div>

        <div class="abc-summary">
          ${Object.entries(data.category_summary).map(([category, info]) => `
            <div class="abc-category">
              <h3>Categoría ${category}</h3>
              <div class="category-metrics">
                <div class="metric">
                  <span class="metric-value">${info.product_count}</span>
                  <span class="metric-label">Productos (${info.product_percentage.toFixed(1)}%)</span>
                </div>
                <div class="metric">
                  <span class="metric-value">${formatPrice(info.revenue)}</span>
                  <span class="metric-label">Ingresos (${info.revenue_percentage.toFixed(1)}%)</span>
                </div>
              </div>
              <div class="category-recommendation">
                <strong>Estrategia:</strong> ${data.recommendations[category]}
              </div>
            </div>
          `).join('')}
        </div>

        <div class="abc-table">
          <h3>Clasificación Detallada de Productos</h3>
          <table>
            <thead>
              <tr>
                <th>Producto</th>
                <th>Categoría</th>
                <th>Ingresos</th>
                <th>% Acumulado</th>
                <th>Clasificación ABC</th>
              </tr>
            </thead>
            <tbody>
              ${data.products.slice(0, 30).map(product => `
                <tr>
                  <td>${product.name}</td>
                  <td>${product.category}</td>
                  <td>${formatPrice(product.revenue)}</td>
                  <td>${product.cumulative_percentage.toFixed(1)}%</td>
                  <td><span class="abc-badge abc-${product.abc_category.toLowerCase()}">${product.abc_category}</span></td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      </div>
    `;
  }

  private async loadProfitAnalysis(): Promise<void> {
    const content = document.getElementById('bi-content') as HTMLElement;
    
    try {
      const response = await ApiService.getProfitAnalysis();
      
      if (response.success) {
        this.renderProfitAnalysis(response.data);
      } else {
        throw new Error(response.error || 'Error al obtener análisis de rentabilidad');
      }
    } catch (error) {
      content.innerHTML = '<div class="error">Error al cargar análisis de rentabilidad</div>';
    }
  }

  private renderProfitAnalysis(data: ProfitAnalysis): void {
    const content = document.getElementById('bi-content') as HTMLElement;
    
    if ('error' in data) {
      content.innerHTML = `
        <div class="analytics-section">
          <h2>💰 Análisis de Rentabilidad</h2>
          <div class="no-data">
            <p>No hay datos de ventas para el análisis de rentabilidad.</p>
          </div>
        </div>
      `;
      return;
    }

    // Preparar datos para gráfico de categorías
    const categoryData: ChartDataPoint[] = Object.entries(data.category_summary).map(([category, info]) => ({
      label: category,
      value: info.profit
    }));

    content.innerHTML = `
      <div class="analytics-section">
        <h2>💰 Análisis de Rentabilidad</h2>
        
        <div class="profit-summary">
          <div class="summary-metrics">
            <div class="metric-card">
              <div class="metric-value">${formatPrice(data.total_metrics.total_revenue)}</div>
              <div class="metric-label">Ingresos Totales</div>
            </div>
            <div class="metric-card">
              <div class="metric-value">${formatPrice(data.total_metrics.total_profit)}</div>
              <div class="metric-label">Beneficio Total</div>
            </div>
            <div class="metric-card">
              <div class="metric-value">${data.total_metrics.overall_margin.toFixed(1)}%</div>
              <div class="metric-label">Margen General</div>
            </div>
          </div>
        </div>

        <div class="chart-container" id="profit-chart"></div>

        <div class="category-profits">
          <h3>Rentabilidad por Categoría</h3>
          <div class="categories-grid">
            ${Object.entries(data.category_summary).map(([category, info]) => `
              <div class="category-card">
                <h4>${category}</h4>
                <div class="category-metrics">
                  <div class="metric">
                    <span class="metric-value">${formatPrice(info.revenue)}</span>
                    <span class="metric-label">Ingresos</span>
                  </div>
                  <div class="metric">
                    <span class="metric-value">${formatPrice(info.profit)}</span>
                    <span class="metric-label">Beneficio</span>
                  </div>
                  <div class="metric">
                    <span class="metric-value">${info.profit_margin.toFixed(1)}%</span>
                    <span class="metric-label">Margen</span>
                  </div>
                  <div class="metric">
                    <span class="metric-value">${info.units_sold}</span>
                    <span class="metric-label">Unidades</span>
                  </div>
                </div>
              </div>
            `).join('')}
          </div>
        </div>

        <div class="profit-table">
          <h3>Rentabilidad por Producto</h3>
          <table>
            <thead>
              <tr>
                <th>Producto</th>
                <th>Categoría</th>
                <th>Precio</th>
                <th>Costo</th>
                <th>Unidades</th>
                <th>Ingresos</th>
                <th>Beneficio</th>
                <th>Margen</th>
              </tr>
            </thead>
            <tbody>
              ${data.products.slice(0, 20).map(product => `
                <tr>
                  <td>${product.name}</td>
                  <td>${product.category}</td>
                  <td>${formatPrice(product.price)}</td>
                  <td>${formatPrice(product.cost_per_unit)}</td>
                  <td>${product.units_sold}</td>
                  <td>${formatPrice(product.revenue)}</td>
                  <td class="${product.profit >= 0 ? 'positive' : 'negative'}">${formatPrice(product.profit)}</td>
                  <td class="${product.profit_margin >= 20 ? 'positive' : product.profit_margin >= 10 ? 'warning' : 'negative'}">${product.profit_margin.toFixed(1)}%</td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      </div>
    `;

    // Renderizar gráfico
    const chartContainer = document.getElementById('profit-chart') as HTMLElement;
    ChartRenderer.createBarChart(chartContainer, categoryData, 'Beneficio por Categoría');
  }

  private getSegmentIcon(segment: string): string {
    const icons: Record<string, string> = {
      'Prospects': '🎯',
      'New Customers': '🌟',
      'One-time Buyers': '🛒',
      'Active Customers': '💎',
      'At Risk': '⚠️',
      'Inactive Customers': '😴'
    };
    return icons[segment] || '👤';
  }
}
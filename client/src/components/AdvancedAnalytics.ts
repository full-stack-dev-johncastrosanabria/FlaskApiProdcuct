import { ApiService } from '../services/api';
import { toast } from '../utils/toast';
import { ChartRenderer, createSimpleChart } from '../utils/charts';
import { formatPrice, formatNumber } from '../utils/helpers';
import type { 
  SalesForecast, 
  CohortAnalysis, 
  RFMAnalysis, 
  ProductPerformance, 
  SeasonalAnalysis,
  TimeSeriesDataPoint,
  ChartDataPoint
} from '../types';

/**
 * Gestor de análisis avanzados
 */
export class AdvancedAnalytics {
  private container: HTMLElement;
  private currentView: string = 'forecast';

  constructor() {
    this.container = document.getElementById('advanced-analytics') as HTMLElement;
    if (!this.container) {
      console.error('Advanced analytics container not found');
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
        <button class="nav-tab ${this.currentView === 'forecast' ? 'active' : ''}" 
                onclick="advancedAnalytics.switchView('forecast')">
          📈 Pronóstico de Ventas
        </button>
        <button class="nav-tab ${this.currentView === 'cohort' ? 'active' : ''}" 
                onclick="advancedAnalytics.switchView('cohort')">
          👥 Análisis de Cohortes
        </button>
        <button class="nav-tab ${this.currentView === 'rfm' ? 'active' : ''}" 
                onclick="advancedAnalytics.switchView('rfm')">
          🎯 Análisis RFM
        </button>
        <button class="nav-tab ${this.currentView === 'performance' ? 'active' : ''}" 
                onclick="advancedAnalytics.switchView('performance')">
          ⭐ Rendimiento de Productos
        </button>
        <button class="nav-tab ${this.currentView === 'seasonal' ? 'active' : ''}" 
                onclick="advancedAnalytics.switchView('seasonal')">
          🌟 Análisis Estacional
        </button>
      </div>
    `;
    
    this.container.innerHTML = '';
    this.container.appendChild(nav);
    
    const content = document.createElement('div');
    content.className = 'analytics-content';
    content.id = 'analytics-content';
    this.container.appendChild(content);
  }

  switchView(view: string): void {
    this.currentView = view;
    this.renderNavigation();
    this.loadCurrentView();
  }

  private async loadCurrentView(): Promise<void> {
    const content = document.getElementById('analytics-content') as HTMLElement;
    content.innerHTML = '<div class="loading">Cargando análisis...</div>';

    try {
      switch (this.currentView) {
        case 'forecast':
          await this.loadSalesForecast();
          break;
        case 'cohort':
          await this.loadCohortAnalysis();
          break;
        case 'rfm':
          await this.loadRFMAnalysis();
          break;
        case 'performance':
          await this.loadProductPerformance();
          break;
        case 'seasonal':
          await this.loadSeasonalAnalysis();
          break;
      }
    } catch (error) {
      content.innerHTML = '<div class="error">Error al cargar análisis</div>';
      toast.error('Error al cargar análisis avanzados');
    }
  }

  private async loadSalesForecast(): Promise<void> {
    const content = document.getElementById('analytics-content') as HTMLElement;
    
    try {
      const response = await ApiService.getSalesForecast(30);
      
      if (response.success) {
        this.renderSalesForecast(response.data);
      } else {
        throw new Error(response.error || 'Error al obtener pronóstico');
      }
    } catch (error) {
      content.innerHTML = '<div class="error">Error al cargar pronóstico de ventas</div>';
    }
  }

  private renderSalesForecast(data: SalesForecast): void {
    const content = document.getElementById('analytics-content') as HTMLElement;
    
    if ('error' in data) {
      content.innerHTML = `
        <div class="analytics-section">
          <h2>📈 Pronóstico de Ventas</h2>
          <div class="no-data">
            <p>No hay suficientes datos para generar un pronóstico.</p>
            <p>Se necesitan al menos 7 días de datos de ventas.</p>
          </div>
        </div>
      `;
      return;
    }

    // Preparar datos para el gráfico
    const chartData: TimeSeriesDataPoint[] = data.forecast.map(item => ({
      date: item.date,
      value: item.predicted_sales,
      forecast: true,
      confidence_lower: item.confidence_interval_lower,
      confidence_upper: item.confidence_interval_upper
    }));

    content.innerHTML = `
      <div class="analytics-section">
        <h2>📈 Pronóstico de Ventas (30 días)</h2>
        
        <div class="forecast-metrics">
          <div class="metric-card">
            <div class="metric-value">${data.model_metrics.r_squared.toFixed(3)}</div>
            <div class="metric-label">R² (Precisión del Modelo)</div>
          </div>
          <div class="metric-card">
            <div class="metric-value">${formatPrice(data.model_metrics.rmse)}</div>
            <div class="metric-label">RMSE (Error Promedio)</div>
          </div>
          <div class="metric-card">
            <div class="metric-value">${data.model_metrics.data_points_used}</div>
            <div class="metric-label">Días de Datos Utilizados</div>
          </div>
        </div>

        <div class="chart-container" id="forecast-chart"></div>

        <div class="forecast-table">
          <h3>Predicciones Detalladas</h3>
          <table>
            <thead>
              <tr>
                <th>Fecha</th>
                <th>Ventas Predichas</th>
                <th>Rango de Confianza</th>
              </tr>
            </thead>
            <tbody>
              ${data.forecast.slice(0, 10).map(item => `
                <tr>
                  <td>${new Date(item.date).toLocaleDateString()}</td>
                  <td>${formatPrice(item.predicted_sales)}</td>
                  <td>${formatPrice(item.confidence_interval_lower)} - ${formatPrice(item.confidence_interval_upper)}</td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      </div>
    `;

    // Renderizar gráfico
    const chartContainer = document.getElementById('forecast-chart') as HTMLElement;
    ChartRenderer.createLineChart(
      chartContainer,
      chartData,
      'Pronóstico de Ventas',
      { showForecast: true, showConfidence: true }
    );
  }

  private async loadCohortAnalysis(): Promise<void> {
    const content = document.getElementById('analytics-content') as HTMLElement;
    
    try {
      const response = await ApiService.getCohortAnalysis(12);
      
      if (response.success) {
        this.renderCohortAnalysis(response.data);
      } else {
        throw new Error(response.error || 'Error al obtener análisis de cohortes');
      }
    } catch (error) {
      content.innerHTML = '<div class="error">Error al cargar análisis de cohortes</div>';
    }
  }

  private renderCohortAnalysis(data: CohortAnalysis[]): void {
    const content = document.getElementById('analytics-content') as HTMLElement;
    
    if (data.length === 0) {
      content.innerHTML = `
        <div class="analytics-section">
          <h2>👥 Análisis de Cohortes</h2>
          <div class="no-data">
            <p>No hay suficientes datos para el análisis de cohortes.</p>
            <p>Se necesitan clientes con múltiples compras en diferentes períodos.</p>
          </div>
        </div>
      `;
      return;
    }

    content.innerHTML = `
      <div class="analytics-section">
        <h2>👥 Análisis de Cohortes - Retención de Clientes</h2>
        
        <div class="cohort-explanation">
          <p>El análisis de cohortes muestra cómo se comportan los grupos de clientes a lo largo del tiempo. 
          Cada fila representa un grupo de clientes que hicieron su primera compra en el mismo mes.</p>
        </div>

        <div class="cohort-table">
          <table>
            <thead>
              <tr>
                <th>Cohorte</th>
                <th>Tamaño</th>
                <th>Período 0</th>
                <th>Período 1</th>
                <th>Período 2</th>
                <th>Período 3</th>
                <th>Período 4</th>
                <th>Período 5</th>
              </tr>
            </thead>
            <tbody>
              ${data.map(cohort => {
                const periods = Object.keys(cohort.retention_rates).sort();
                return `
                  <tr>
                    <td><strong>${cohort.cohort}</strong></td>
                    <td>${cohort.size}</td>
                    ${Array.from({length: 6}, (_, i) => {
                      const periodKey = `period_${i}`;
                      const rate = cohort.retention_rates[periodKey];
                      if (rate !== undefined) {
                        const intensity = rate / 100;
                        return `<td style="background-color: rgba(59, 130, 246, ${intensity})">${rate}%</td>`;
                      }
                      return '<td>-</td>';
                    }).join('')}
                  </tr>
                `;
              }).join('')}
            </tbody>
          </table>
        </div>

        <div class="cohort-insights">
          <h3>💡 Insights Clave</h3>
          <ul>
            <li><strong>Retención Inicial:</strong> Observa el período 1 para ver qué porcentaje de clientes regresa</li>
            <li><strong>Retención a Largo Plazo:</strong> Los períodos 3-5 muestran la lealtad del cliente</li>
            <li><strong>Tendencias:</strong> Compara cohortes recientes vs. antiguas para identificar mejoras</li>
          </ul>
        </div>
      </div>
    `;
  }

  private async loadRFMAnalysis(): Promise<void> {
    const content = document.getElementById('analytics-content') as HTMLElement;
    
    try {
      const response = await ApiService.getRFMAnalysis();
      
      if (response.success) {
        this.renderRFMAnalysis(response.data);
      } else {
        throw new Error(response.error || 'Error al obtener análisis RFM');
      }
    } catch (error) {
      content.innerHTML = '<div class="error">Error al cargar análisis RFM</div>';
    }
  }

  private renderRFMAnalysis(data: RFMAnalysis[]): void {
    const content = document.getElementById('analytics-content') as HTMLElement;
    
    if (data.length === 0) {
      content.innerHTML = `
        <div class="analytics-section">
          <h2>🎯 Análisis RFM</h2>
          <div class="no-data">
            <p>No hay datos de clientes para el análisis RFM.</p>
          </div>
        </div>
      `;
      return;
    }

    // Agrupar por segmentos
    const segments = data.reduce((acc, customer) => {
      if (!acc[customer.segment]) {
        acc[customer.segment] = [];
      }
      acc[customer.segment].push(customer);
      return acc;
    }, {} as Record<string, RFMAnalysis[]>);

    // Preparar datos para gráfico de segmentos
    const segmentData: ChartDataPoint[] = Object.entries(segments).map(([segment, customers]) => ({
      label: segment,
      value: customers.length
    }));

    content.innerHTML = `
      <div class="analytics-section">
        <h2>🎯 Análisis RFM - Segmentación de Clientes</h2>
        
        <div class="rfm-explanation">
          <p><strong>RFM</strong> analiza a los clientes basándose en:</p>
          <ul>
            <li><strong>Recency (R):</strong> ¿Qué tan reciente fue su última compra?</li>
            <li><strong>Frequency (F):</strong> ¿Con qué frecuencia compra?</li>
            <li><strong>Monetary (M):</strong> ¿Cuánto dinero gasta?</li>
          </ul>
        </div>

        <div class="chart-container" id="rfm-segments-chart"></div>

        <div class="rfm-segments">
          ${Object.entries(segments).map(([segment, customers]) => `
            <div class="segment-card">
              <h3>${segment}</h3>
              <div class="segment-stats">
                <div class="stat">
                  <span class="stat-value">${customers.length}</span>
                  <span class="stat-label">Clientes</span>
                </div>
                <div class="stat">
                  <span class="stat-value">${formatPrice(customers.reduce((sum, c) => sum + c.monetary, 0) / customers.length)}</span>
                  <span class="stat-label">Gasto Promedio</span>
                </div>
                <div class="stat">
                  <span class="stat-value">${(customers.reduce((sum, c) => sum + c.frequency, 0) / customers.length).toFixed(1)}</span>
                  <span class="stat-label">Frecuencia Promedio</span>
                </div>
              </div>
              <div class="segment-customers">
                ${customers.slice(0, 3).map(customer => `
                  <div class="customer-item">
                    <span class="customer-name">${customer.name}</span>
                    <span class="customer-score">RFM: ${customer.rfm_score}</span>
                  </div>
                `).join('')}
                ${customers.length > 3 ? `<div class="more-customers">+${customers.length - 3} más</div>` : ''}
              </div>
            </div>
          `).join('')}
        </div>

        <div class="rfm-table">
          <h3>Detalle de Clientes</h3>
          <table>
            <thead>
              <tr>
                <th>Cliente</th>
                <th>Email</th>
                <th>Recency</th>
                <th>Frequency</th>
                <th>Monetary</th>
                <th>Score RFM</th>
                <th>Segmento</th>
              </tr>
            </thead>
            <tbody>
              ${data.slice(0, 20).map(customer => `
                <tr>
                  <td>${customer.name}</td>
                  <td>${customer.email}</td>
                  <td>${customer.recency} días</td>
                  <td>${customer.frequency}</td>
                  <td>${formatPrice(customer.monetary)}</td>
                  <td><span class="rfm-score">${customer.rfm_score}</span></td>
                  <td><span class="segment-badge">${customer.segment}</span></td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      </div>
    `;

    // Renderizar gráfico de segmentos
    const chartContainer = document.getElementById('rfm-segments-chart') as HTMLElement;
    ChartRenderer.createPieChart(chartContainer, segmentData, 'Distribución de Segmentos RFM');
  }

  private async loadProductPerformance(): Promise<void> {
    const content = document.getElementById('analytics-content') as HTMLElement;
    
    try {
      const response = await ApiService.getProductPerformanceMatrix();
      
      if (response.success) {
        this.renderProductPerformance(response.data);
      } else {
        throw new Error(response.error || 'Error al obtener rendimiento de productos');
      }
    } catch (error) {
      content.innerHTML = '<div class="error">Error al cargar rendimiento de productos</div>';
    }
  }

  private renderProductPerformance(data: ProductPerformance[]): void {
    const content = document.getElementById('analytics-content') as HTMLElement;
    
    if (data.length === 0) {
      content.innerHTML = `
        <div class="analytics-section">
          <h2>⭐ Matriz de Rendimiento de Productos</h2>
          <div class="no-data">
            <p>No hay datos de ventas para analizar el rendimiento de productos.</p>
          </div>
        </div>
      `;
      return;
    }

    // Agrupar por categoría de rendimiento
    const categories = data.reduce((acc, product) => {
      if (!acc[product.performance_category]) {
        acc[product.performance_category] = [];
      }
      acc[product.performance_category].push(product);
      return acc;
    }, {} as Record<string, ProductPerformance[]>);

    content.innerHTML = `
      <div class="analytics-section">
        <h2>⭐ Matriz de Rendimiento de Productos</h2>
        
        <div class="performance-explanation">
          <p>Los productos se clasifican en una matriz 2x2 basada en ingresos y rotación de inventario:</p>
          <ul>
            <li><strong>⭐ Star Products:</strong> Alto ingreso, alta rotación - Invertir más</li>
            <li><strong>🐄 Cash Cows:</strong> Alto ingreso, baja rotación - Mantener estrategia</li>
            <li><strong>❓ Question Marks:</strong> Bajo ingreso, alta rotación - Analizar potencial</li>
            <li><strong>🐕 Dogs:</strong> Bajo ingreso, baja rotación - Considerar descontinuar</li>
          </ul>
        </div>

        <div class="performance-matrix">
          ${Object.entries(categories).map(([category, products]) => `
            <div class="performance-category">
              <h3>${this.getCategoryIcon(category)} ${category}</h3>
              <div class="category-stats">
                <span>${products.length} productos</span>
                <span>${formatPrice(products.reduce((sum, p) => sum + p.total_revenue, 0))} ingresos</span>
              </div>
              <div class="products-list">
                ${products.slice(0, 5).map(product => `
                  <div class="product-item">
                    <div class="product-info">
                      <span class="product-name">${product.name}</span>
                      <span class="product-category">${product.category}</span>
                    </div>
                    <div class="product-metrics">
                      <span class="revenue">${formatPrice(product.total_revenue)}</span>
                      <span class="turnover">${product.stock_turnover.toFixed(2)}x</span>
                    </div>
                  </div>
                `).join('')}
                ${products.length > 5 ? `<div class="more-products">+${products.length - 5} productos más</div>` : ''}
              </div>
              <div class="category-recommendation">
                <strong>Recomendación:</strong> ${products[0]?.recommendation}
              </div>
            </div>
          `).join('')}
        </div>

        <div class="performance-table">
          <h3>Detalle de Productos</h3>
          <table>
            <thead>
              <tr>
                <th>Producto</th>
                <th>Categoría</th>
                <th>Precio</th>
                <th>Vendidos</th>
                <th>Ingresos</th>
                <th>Rotación</th>
                <th>Clasificación</th>
              </tr>
            </thead>
            <tbody>
              ${data.slice(0, 20).map(product => `
                <tr>
                  <td>${product.name}</td>
                  <td>${product.category}</td>
                  <td>${formatPrice(product.price)}</td>
                  <td>${product.total_sold}</td>
                  <td>${formatPrice(product.total_revenue)}</td>
                  <td>${product.stock_turnover.toFixed(2)}x</td>
                  <td><span class="performance-badge ${product.performance_category.toLowerCase().replace(' ', '-')}">${product.performance_category}</span></td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      </div>
    `;
  }

  private async loadSeasonalAnalysis(): Promise<void> {
    const content = document.getElementById('analytics-content') as HTMLElement;
    
    try {
      const response = await ApiService.getSeasonalAnalysis();
      
      if (response.success) {
        this.renderSeasonalAnalysis(response.data);
      } else {
        throw new Error(response.error || 'Error al obtener análisis estacional');
      }
    } catch (error) {
      content.innerHTML = '<div class="error">Error al cargar análisis estacional</div>';
    }
  }

  private renderSeasonalAnalysis(data: SeasonalAnalysis): void {
    const content = document.getElementById('analytics-content') as HTMLElement;
    
    if ('error' in data) {
      content.innerHTML = `
        <div class="analytics-section">
          <h2>🌟 Análisis Estacional</h2>
          <div class="no-data">
            <p>No hay suficientes datos para el análisis estacional.</p>
          </div>
        </div>
      `;
      return;
    }

    // Preparar datos para gráfico
    const chartData: ChartDataPoint[] = Object.entries(data.seasonal_indices).map(([month, index]) => ({
      label: month.substring(0, 3),
      value: index
    }));

    content.innerHTML = `
      <div class="analytics-section">
        <h2>🌟 Análisis Estacional de Ventas</h2>
        
        <div class="seasonal-explanation">
          <p>El índice estacional muestra la variación de ventas por mes. Un índice de 100 representa el promedio anual.</p>
          <ul>
            <li><strong>Índice > 100:</strong> Ventas por encima del promedio</li>
            <li><strong>Índice < 100:</strong> Ventas por debajo del promedio</li>
          </ul>
        </div>

        <div class="chart-container" id="seasonal-chart"></div>

        <div class="seasonal-insights">
          <div class="insight-card peak">
            <h3>📈 Meses Pico</h3>
            ${Object.entries(data.peak_months).map(([month, index]) => `
              <div class="month-item">
                <span class="month">${month}</span>
                <span class="index">${index.toFixed(1)}</span>
              </div>
            `).join('')}
          </div>

          <div class="insight-card low">
            <h3>📉 Meses Bajos</h3>
            ${Object.entries(data.low_months).map(([month, index]) => `
              <div class="month-item">
                <span class="month">${month}</span>
                <span class="index">${index.toFixed(1)}</span>
              </div>
            `).join('')}
          </div>
        </div>

        <div class="seasonal-table">
          <h3>Datos Mensuales Detallados</h3>
          <table>
            <thead>
              <tr>
                <th>Año</th>
                <th>Mes</th>
                <th>Ventas Totales</th>
                <th>Número de Órdenes</th>
                <th>Promedio por Orden</th>
              </tr>
            </thead>
            <tbody>
              ${data.monthly_data.map(item => `
                <tr>
                  <td>${item.year}</td>
                  <td>${new Date(item.year, item.month - 1).toLocaleDateString('es-ES', { month: 'long' })}</td>
                  <td>${formatPrice(item.total_sales)}</td>
                  <td>${item.order_count}</td>
                  <td>${formatPrice(item.total_sales / item.order_count)}</td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      </div>
    `;

    // Renderizar gráfico
    const chartContainer = document.getElementById('seasonal-chart') as HTMLElement;
    ChartRenderer.createBarChart(chartContainer, chartData, 'Índices Estacionales por Mes');
  }

  private getCategoryIcon(category: string): string {
    const icons: Record<string, string> = {
      'Star Products': '⭐',
      'Cash Cows': '🐄',
      'Question Marks': '❓',
      'Dogs': '🐕'
    };
    return icons[category] || '📦';
  }
}
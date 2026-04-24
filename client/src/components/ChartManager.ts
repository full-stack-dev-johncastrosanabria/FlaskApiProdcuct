import { ChartRenderer } from '../utils/charts';
import type { ChartConfig, ChartDataPoint, TimeSeriesDataPoint } from '../types';

/**
 * Gestor de gráficos y visualizaciones
 */
export class ChartManager {
  private static instance: ChartManager;
  private charts: Map<string, any> = new Map();

  private constructor() {}

  static getInstance(): ChartManager {
    if (!ChartManager.instance) {
      ChartManager.instance = new ChartManager();
    }
    return ChartManager.instance;
  }

  /**
   * Crear un gráfico y registrarlo
   */
  createChart(
    containerId: string,
    config: ChartConfig
  ): void {
    const container = document.getElementById(containerId);
    if (!container) {
      console.error(`Container ${containerId} not found`);
      return;
    }

    try {
      switch (config.type) {
        case 'line':
          ChartRenderer.createLineChart(
            container,
            config.data as TimeSeriesDataPoint[],
            config.title
          );
          break;
        case 'bar':
          ChartRenderer.createBarChart(
            container,
            config.data as ChartDataPoint[],
            config.title
          );
          break;
        case 'pie':
        case 'doughnut':
          ChartRenderer.createPieChart(
            container,
            config.data as ChartDataPoint[],
            config.title,
            { 
              showLabels: true,
              innerRadius: config.type === 'doughnut' ? 40 : 0
            }
          );
          break;
        case 'area':
          // Para gráficos de área, usar line chart con relleno
          ChartRenderer.createLineChart(
            container,
            config.data as TimeSeriesDataPoint[],
            config.title
          );
          break;
        default:
          console.error(`Chart type ${config.type} not supported`);
      }

      // Registrar el gráfico
      this.charts.set(containerId, config);
    } catch (error) {
      console.error(`Error creating chart ${containerId}:`, error);
      container.innerHTML = '<div class="chart-error">Error al crear gráfico</div>';
    }
  }

  /**
   * Actualizar un gráfico existente
   */
  updateChart(containerId: string, newData: ChartDataPoint[] | TimeSeriesDataPoint[]): void {
    const config = this.charts.get(containerId);
    if (!config) {
      console.error(`Chart ${containerId} not found`);
      return;
    }

    config.data = newData;
    this.createChart(containerId, config);
  }

  /**
   * Eliminar un gráfico
   */
  removeChart(containerId: string): void {
    const container = document.getElementById(containerId);
    if (container) {
      container.innerHTML = '';
    }
    this.charts.delete(containerId);
  }

  /**
   * Redimensionar todos los gráficos
   */
  resizeCharts(): void {
    this.charts.forEach((config, containerId) => {
      this.createChart(containerId, config);
    });
  }

  /**
   * Crear múltiples métricas en un contenedor
   */
  createMetricsGrid(
    containerId: string,
    metrics: Array<{
      value: number;
      label: string;
      change?: number;
      format?: 'number' | 'currency' | 'percentage';
    }>
  ): void {
    const container = document.getElementById(containerId);
    if (!container) {
      console.error(`Container ${containerId} not found`);
      return;
    }

    container.innerHTML = `
      <div class="metrics-grid">
        ${metrics.map(metric => {
          const changeClass = metric.change && metric.change > 0 ? 'positive' : 
                             metric.change && metric.change < 0 ? 'negative' : 'neutral';
          const changeIcon = metric.change && metric.change > 0 ? '↗️' : 
                            metric.change && metric.change < 0 ? '↘️' : '';
          
          return `
            <div class="metric-card">
              <div class="metric-value">${this.formatValue(metric.value, metric.format || 'number')}</div>
              <div class="metric-label">${metric.label}</div>
              ${metric.change !== undefined ? `
                <div class="metric-change ${changeClass}">
                  ${changeIcon} ${Math.abs(metric.change).toFixed(1)}%
                </div>
              ` : ''}
            </div>
          `;
        }).join('')}
      </div>
    `;
  }

  /**
   * Crear un dashboard de gráficos
   */
  createDashboard(
    containerId: string,
    charts: Array<{
      id: string;
      config: ChartConfig;
      size?: 'small' | 'medium' | 'large' | 'full';
    }>
  ): void {
    const container = document.getElementById(containerId);
    if (!container) {
      console.error(`Container ${containerId} not found`);
      return;
    }

    container.innerHTML = `
      <div class="charts-dashboard">
        ${charts.map(chart => `
          <div class="chart-wrapper ${chart.size || 'medium'}">
            <div id="${chart.id}" class="chart-container"></div>
          </div>
        `).join('')}
      </div>
    `;

    // Crear cada gráfico
    charts.forEach(chart => {
      setTimeout(() => {
        this.createChart(chart.id, chart.config);
      }, 100);
    });
  }

  /**
   * Exportar gráfico como imagen (simulado)
   */
  exportChart(containerId: string, format: 'png' | 'svg' = 'png'): void {
    const container = document.getElementById(containerId);
    if (!container) {
      console.error(`Container ${containerId} not found`);
      return;
    }

    // En una implementación real, aquí se convertiría el SVG a imagen
    console.log(`Exporting chart ${containerId} as ${format}`);
    
    // Simular descarga
    const link = document.createElement('a');
    link.download = `chart-${containerId}.${format}`;
    link.href = '#'; // En implementación real, sería el blob de la imagen
    link.click();
  }

  /**
   * Crear gráfico de comparación
   */
  createComparisonChart(
    containerId: string,
    datasets: Array<{
      label: string;
      data: ChartDataPoint[] | TimeSeriesDataPoint[];
      color?: string;
    }>,
    title: string,
    type: 'line' | 'bar' = 'line'
  ): void {
    const container = document.getElementById(containerId);
    if (!container) {
      console.error(`Container ${containerId} not found`);
      return;
    }

    // Para múltiples datasets, crear gráfico combinado
    if (type === 'line') {
      // Combinar todos los datos en una serie temporal
      const allData: TimeSeriesDataPoint[] = [];
      datasets.forEach((dataset) => {
        (dataset.data as TimeSeriesDataPoint[]).forEach(point => {
          allData.push({
            ...point,
            value: point.value
          });
        });
      });

      ChartRenderer.createLineChart(container, allData, title);
    } else {
      // Para barras, mostrar lado a lado
      const combinedData: ChartDataPoint[] = [];
      const labels = new Set<string>();
      
      datasets.forEach(dataset => {
        (dataset.data as ChartDataPoint[]).forEach(point => {
          labels.add(point.label);
        });
      });

      Array.from(labels).forEach(label => {
        datasets.forEach((dataset, index) => {
          const point = (dataset.data as ChartDataPoint[]).find(p => p.label === label);
          if (point) {
            combinedData.push({
              label: `${label} (${dataset.label})`,
              value: point.value,
              color: dataset.color || ChartRenderer['colors'][index]
            });
          }
        });
      });

      ChartRenderer.createBarChart(container, combinedData, title);
    }
  }

  /**
   * Crear tabla de datos
   */
  createDataTable(
    containerId: string,
    data: Array<Record<string, any>>,
    columns: Array<{
      key: string;
      label: string;
      format?: 'number' | 'currency' | 'percentage' | 'date';
    }>,
    title?: string
  ): void {
    const container = document.getElementById(containerId);
    if (!container) {
      console.error(`Container ${containerId} not found`);
      return;
    }

    container.innerHTML = `
      <div class="data-table-container">
        ${title ? `<h3 class="table-title">${title}</h3>` : ''}
        <div class="table-wrapper">
          <table class="data-table">
            <thead>
              <tr>
                ${columns.map(col => `<th>${col.label}</th>`).join('')}
              </tr>
            </thead>
            <tbody>
              ${data.map(row => `
                <tr>
                  ${columns.map(col => `
                    <td>${this.formatValue(row[col.key], col.format || 'text')}</td>
                  `).join('')}
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      </div>
    `;
  }

  private formatValue(value: any, format: string): string {
    if (value === null || value === undefined) return '-';

    switch (format) {
      case 'currency':
        return new Intl.NumberFormat('es-ES', { 
          style: 'currency', 
          currency: 'EUR' 
        }).format(Number(value));
      case 'percentage':
        return `${Number(value).toFixed(1)}%`;
      case 'number':
        return Number(value).toLocaleString('es-ES');
      case 'date':
        return new Date(value).toLocaleDateString('es-ES');
      default:
        return String(value);
    }
  }
}

// Exportar instancia singleton
export const chartManager = ChartManager.getInstance();
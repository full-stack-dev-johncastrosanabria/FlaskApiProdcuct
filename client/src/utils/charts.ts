import type { ChartConfig, ChartDataPoint, TimeSeriesDataPoint } from '../types';

/**
 * Utilidades profesionales para visualización de datos
 */
export class ChartRenderer {
  private static colors = [
    '#3b82f6', '#ef4444', '#10b981', '#f59e0b', '#8b5cf6',
    '#06b6d4', '#f97316', '#84cc16', '#ec4899', '#6366f1'
  ];

  /**
   * Crear un gráfico de líneas simple con HTML/CSS
   */
  static createLineChart(
    container: HTMLElement,
    data: TimeSeriesDataPoint[],
    title: string,
    options: { showForecast?: boolean; showConfidence?: boolean } = {}
  ): void {
    const maxValue = Math.max(...data.map(d => Math.max(d.value, d.confidence_upper || d.value)));
    const minValue = Math.min(...data.map(d => Math.min(d.value, d.confidence_lower || d.value)));
    const range = maxValue - minValue || 1;

    container.innerHTML = `
      <div class="chart-container">
        <h3 class="chart-title">${title}</h3>
        <div class="line-chart">
          <div class="chart-y-axis">
            <div class="y-label">${this.formatNumber(maxValue)}</div>
            <div class="y-label">${this.formatNumber(maxValue * 0.75)}</div>
            <div class="y-label">${this.formatNumber(maxValue * 0.5)}</div>
            <div class="y-label">${this.formatNumber(maxValue * 0.25)}</div>
            <div class="y-label">0</div>
          </div>
          <div class="chart-area">
            <svg class="line-svg" viewBox="0 0 400 200" preserveAspectRatio="none">
              ${this.createLinePath(data.filter(d => !d.forecast), 400, 200, minValue, range, this.colors[0])}
              ${options.showForecast ? this.createLinePath(data.filter(d => d.forecast), 400, 200, minValue, range, this.colors[1], true) : ''}
              ${options.showConfidence ? this.createConfidenceArea(data.filter(d => d.forecast), 400, 200, minValue, range) : ''}
            </svg>
            <div class="chart-x-axis">
              ${data.filter((_, i) => i % Math.ceil(data.length / 5) === 0).map(d => 
                `<div class="x-label">${new Date(d.date).toLocaleDateString()}</div>`
              ).join('')}
            </div>
          </div>
        </div>
        ${options.showForecast ? '<div class="chart-legend"><span class="legend-actual">Actual</span><span class="legend-forecast">Pronóstico</span></div>' : ''}
      </div>
    `;
  }

  /**
   * Crear un gráfico de barras
   */
  static createBarChart(
    container: HTMLElement,
    data: ChartDataPoint[],
    title: string,
    options: { horizontal?: boolean } = {}
  ): void {
    const maxValue = Math.max(...data.map(d => d.value));
    
    container.innerHTML = `
      <div class="chart-container">
        <h3 class="chart-title">${title}</h3>
        <div class="bar-chart ${options.horizontal ? 'horizontal' : 'vertical'}">
          ${data.map((item, index) => `
            <div class="bar-item">
              <div class="bar-label">${item.label}</div>
              <div class="bar-container">
                <div class="bar" style="
                  ${options.horizontal ? 'width' : 'height'}: ${(item.value / maxValue) * 100}%;
                  background-color: ${item.color || this.colors[index % this.colors.length]};
                "></div>
                <span class="bar-value">${this.formatNumber(item.value)}</span>
              </div>
            </div>
          `).join('')}
        </div>
      </div>
    `;
  }

  /**
   * Crear un gráfico de pastel
   */
  static createPieChart(
    container: HTMLElement,
    data: ChartDataPoint[],
    title: string,
    options: { showLabels?: boolean; innerRadius?: number } = {}
  ): void {
    const total = data.reduce((sum, item) => sum + item.value, 0);
    let currentAngle = 0;
    
    const segments = data.map((item, index) => {
      const percentage = (item.value / total) * 100;
      const angle = (item.value / total) * 360;
      const startAngle = currentAngle;
      currentAngle += angle;
      
      return {
        ...item,
        percentage,
        angle,
        startAngle,
        color: item.color || this.colors[index % this.colors.length]
      };
    });

    container.innerHTML = `
      <div class="chart-container">
        <h3 class="chart-title">${title}</h3>
        <div class="pie-chart-container">
          <div class="pie-chart">
            <svg viewBox="0 0 200 200" class="pie-svg">
              <circle cx="100" cy="100" r="80" fill="none" stroke="#f1f5f9" stroke-width="2"/>
              ${segments.map(segment => this.createPieSegment(segment, options.innerRadius || 0)).join('')}
            </svg>
            ${options.showLabels ? `
              <div class="pie-labels">
                ${segments.map(segment => `
                  <div class="pie-label" style="color: ${segment.color}">
                    ${segment.label}: ${segment.percentage.toFixed(1)}%
                  </div>
                `).join('')}
              </div>
            ` : ''}
          </div>
          <div class="pie-legend">
            ${segments.map(segment => `
              <div class="legend-item">
                <div class="legend-color" style="background-color: ${segment.color}"></div>
                <span class="legend-text">${segment.label} (${this.formatNumber(segment.value)})</span>
              </div>
            `).join('')}
          </div>
        </div>
      </div>
    `;
  }

  /**
   * Crear un mapa de calor
   */
  static createHeatmap(
    container: HTMLElement,
    data: Array<{ x: string; y: string; value: number }>,
    title: string
  ): void {
    const maxValue = Math.max(...data.map(d => d.value));
    const xValues = Array.from(new Set(data.map(d => d.x)));
    const yValues = Array.from(new Set(data.map(d => d.y)));

    container.innerHTML = `
      <div class="chart-container">
        <h3 class="chart-title">${title}</h3>
        <div class="heatmap">
          <div class="heatmap-y-labels">
            ${yValues.map(y => `<div class="heatmap-label">${y}</div>`).join('')}
          </div>
          <div class="heatmap-grid">
            ${yValues.map(y => `
              <div class="heatmap-row">
                ${xValues.map(x => {
                  const point = data.find(d => d.x === x && d.y === y);
                  const intensity = point ? (point.value / maxValue) : 0;
                  return `
                    <div class="heatmap-cell" 
                         style="background-color: rgba(59, 130, 246, ${intensity})"
                         title="${x}, ${y}: ${point?.value || 0}">
                    </div>
                  `;
                }).join('')}
              </div>
            `).join('')}
            <div class="heatmap-x-labels">
              ${xValues.map(x => `<div class="heatmap-label">${x}</div>`).join('')}
            </div>
          </div>
        </div>
      </div>
    `;
  }

  /**
   * Crear una tarjeta de métrica
   */
  static createMetricCard(
    container: HTMLElement,
    value: number,
    label: string,
    change?: number,
    format: 'number' | 'currency' | 'percentage' = 'number'
  ): void {
    const formattedValue = this.formatValue(value, format);
    const changeClass = change && change > 0 ? 'positive' : change && change < 0 ? 'negative' : 'neutral';
    const changeIcon = change && change > 0 ? '↗️' : change && change < 0 ? '↘️' : '';
    
    container.innerHTML = `
      <div class="metric-card">
        <div class="metric-value">${formattedValue}</div>
        <div class="metric-label">${label}</div>
        ${change !== undefined ? `
          <div class="metric-change ${changeClass}">
            ${changeIcon} ${Math.abs(change).toFixed(1)}%
          </div>
        ` : ''}
      </div>
    `;
  }

  // Métodos auxiliares
  private static createLinePath(
    data: TimeSeriesDataPoint[],
    width: number,
    height: number,
    minValue: number,
    range: number,
    color: string,
    dashed: boolean = false
  ): string {
    if (data.length === 0) return '';
    
    const points = data.map((d, i) => {
      const x = (i / (data.length - 1)) * width;
      const y = height - ((d.value - minValue) / range) * height;
      return `${x},${y}`;
    }).join(' ');
    
    return `
      <polyline 
        points="${points}" 
        fill="none" 
        stroke="${color}" 
        stroke-width="2"
        ${dashed ? 'stroke-dasharray="5,5"' : ''}
      />
    `;
  }

  private static createConfidenceArea(
    data: TimeSeriesDataPoint[],
    width: number,
    height: number,
    minValue: number,
    range: number
  ): string {
    if (data.length === 0) return '';
    
    const upperPoints = data.map((d, i) => {
      const x = (i / (data.length - 1)) * width;
      const y = height - ((d.confidence_upper || d.value) - minValue) / range * height;
      return `${x},${y}`;
    });
    
    const lowerPoints = data.map((d, i) => {
      const x = (i / (data.length - 1)) * width;
      const y = height - ((d.confidence_lower || d.value) - minValue) / range * height;
      return `${x},${y}`;
    }).reverse();
    
    const pathData = `M ${upperPoints.join(' L ')} L ${lowerPoints.join(' L ')} Z`;
    
    return `<path d="${pathData}" fill="rgba(59, 130, 246, 0.2)" />`;
  }

  private static createPieSegment(
    segment: any,
    innerRadius: number
  ): string {
    const { startAngle, angle, color } = segment;
    const outerRadius = 80;
    const inner = innerRadius;
    
    const startAngleRad = (startAngle - 90) * Math.PI / 180;
    const endAngleRad = (startAngle + angle - 90) * Math.PI / 180;
    
    const x1 = 100 + outerRadius * Math.cos(startAngleRad);
    const y1 = 100 + outerRadius * Math.sin(startAngleRad);
    const x2 = 100 + outerRadius * Math.cos(endAngleRad);
    const y2 = 100 + outerRadius * Math.sin(endAngleRad);
    
    const largeArcFlag = angle > 180 ? 1 : 0;
    
    let pathData;
    if (inner > 0) {
      const x3 = 100 + inner * Math.cos(endAngleRad);
      const y3 = 100 + inner * Math.sin(endAngleRad);
      const x4 = 100 + inner * Math.cos(startAngleRad);
      const y4 = 100 + inner * Math.sin(startAngleRad);
      
      pathData = `M ${x1} ${y1} A ${outerRadius} ${outerRadius} 0 ${largeArcFlag} 1 ${x2} ${y2} L ${x3} ${y3} A ${inner} ${inner} 0 ${largeArcFlag} 0 ${x4} ${y4} Z`;
    } else {
      pathData = `M 100 100 L ${x1} ${y1} A ${outerRadius} ${outerRadius} 0 ${largeArcFlag} 1 ${x2} ${y2} Z`;
    }
    
    return `<path d="${pathData}" fill="${color}" stroke="#fff" stroke-width="1"/>`;
  }

  private static formatNumber(value: number): string {
    if (value >= 1000000) {
      return (value / 1000000).toFixed(1) + 'M';
    } else if (value >= 1000) {
      return (value / 1000).toFixed(1) + 'K';
    }
    return value.toFixed(0);
  }

  private static formatValue(value: number, format: 'number' | 'currency' | 'percentage'): string {
    switch (format) {
      case 'currency':
        return new Intl.NumberFormat('es-ES', { 
          style: 'currency', 
          currency: 'EUR' 
        }).format(value);
      case 'percentage':
        return `${value.toFixed(1)}%`;
      default:
        return this.formatNumber(value);
    }
  }
}

// Exportar creador de gráficos simplificado para uso básico
export const createSimpleChart = {
  /**
   * Crear un gráfico de barras simple usando HTML/CSS
   */
  bar(container: HTMLElement, data: ChartDataPoint[], title: string) {
    ChartRenderer.createBarChart(container, data, title);
  },

  /**
   * Crear una tarjeta de métrica simple
   */
  metric(container: HTMLElement, value: number, label: string, change?: number) {
    ChartRenderer.createMetricCard(container, value, label, change);
  },

  /**
   * Crear un gráfico de líneas simple
   */
  line(container: HTMLElement, data: TimeSeriesDataPoint[], title: string) {
    ChartRenderer.createLineChart(container, data, title);
  },

  /**
   * Crear un gráfico de pastel simple
   */
  pie(container: HTMLElement, data: ChartDataPoint[], title: string) {
    ChartRenderer.createPieChart(container, data, title, { showLabels: true });
  }
};
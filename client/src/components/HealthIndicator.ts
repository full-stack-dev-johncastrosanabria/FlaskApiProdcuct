import { ApiService } from '../services/api';

/**
 * Indicador de salud de la API
 */
export class HealthIndicator {
  private indicator: HTMLElement;
  private statusText: HTMLElement;
  private checkInterval: NodeJS.Timeout | null = null;

  constructor() {
    this.indicator = document.querySelector('.status-indicator') as HTMLElement;
    this.statusText = document.querySelector('.status-text') as HTMLElement;
    
    if (!this.indicator || !this.statusText) {
      console.error('Health indicator elements not found');
      return;
    }

    this.startHealthCheck();
  }

  private async checkHealth(): Promise<void> {
    try {
      const health = await ApiService.healthCheck();
      
      if (health.status === 'healthy') {
        this.setHealthy();
      } else {
        this.setUnhealthy('API no saludable');
      }
    } catch (error) {
      this.setUnhealthy('API Desconectada');
    }
  }

  private setHealthy(): void {
    this.indicator.className = 'status-indicator healthy';
    this.statusText.textContent = 'API Conectada';
  }

  private setUnhealthy(message: string): void {
    this.indicator.className = 'status-indicator error';
    this.statusText.textContent = message;
  }

  private startHealthCheck(): void {
    // Check inicial
    this.checkHealth();
    
    // Check cada 30 segundos
    this.checkInterval = setInterval(() => {
      this.checkHealth();
    }, 30000);
  }

  destroy(): void {
    if (this.checkInterval) {
      clearInterval(this.checkInterval);
    }
  }
}
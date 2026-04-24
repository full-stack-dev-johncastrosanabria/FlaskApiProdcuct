import { TabManager } from './components/TabManager';
import { HealthIndicator } from './components/HealthIndicator';
import { UserManager } from './components/UserManager';
import { ProductManager } from './components/ProductManager';
import { DashboardManager } from './components/DashboardManager';
import { AdvancedAnalytics } from './components/AdvancedAnalytics';
import { BusinessIntelligence } from './components/BusinessIntelligence';
import { chartManager } from './components/ChartManager';
import './styles/main.css';

/**
 * Aplicación principal
 */
class App {
  private userManager!: UserManager;
  private productManager!: ProductManager;
  private dashboardManager!: DashboardManager;
  private advancedAnalytics!: AdvancedAnalytics;
  private businessIntelligence!: BusinessIntelligence;

  constructor() {
    this.init();
  }

  private init(): void {
    // Esperar a que el DOM esté listo
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => this.initializeComponents());
    } else {
      this.initializeComponents();
    }
  }

  private initializeComponents(): void {
    try {
      // Inicializar componentes
      new TabManager();
      new HealthIndicator();
      this.userManager = new UserManager();
      this.productManager = new ProductManager();
      this.dashboardManager = new DashboardManager();
      this.advancedAnalytics = new AdvancedAnalytics();
      this.businessIntelligence = new BusinessIntelligence();

      // Exponer managers globalmente para compatibilidad con HTML
      (window as any).userManager = this.userManager;
      (window as any).productManager = this.productManager;
      (window as any).dashboardManager = this.dashboardManager;
      (window as any).advancedAnalytics = this.advancedAnalytics;
      (window as any).businessIntelligence = this.businessIntelligence;
      (window as any).chartManager = chartManager;

      // Setup modal
      this.setupModal();

      // Setup event listeners
      this.setupEventListeners();

      // Setup window resize handler for charts
      this.setupResizeHandler();

      console.log('✅ Aplicación inicializada correctamente');
    } catch (error) {
      console.error('❌ Error al inicializar la aplicación:', error);
    }
  }

  private setupModal(): void {
    const modal = document.getElementById('editModal');
    const closeBtn = document.querySelector('.close');
    
    if (!modal || !closeBtn) return;

    closeBtn.addEventListener('click', () => {
      modal.classList.remove('active');
    });
    
    window.addEventListener('click', (event) => {
      if (event.target === modal) {
        modal.classList.remove('active');
      }
    });
  }

  private setupEventListeners(): void {
    // Escuchar cambios de tab
    window.addEventListener('tabChanged', (event) => {
      const customEvent = event as CustomEvent;
      const { tabName } = customEvent.detail;
      this.handleTabChange(tabName);
    });

    // Escuchar tecla Escape para cerrar modales
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape') {
        const modal = document.getElementById('editModal');
        if (modal && modal.classList.contains('active')) {
          modal.classList.remove('active');
        }
      }
    });
  }

  private handleTabChange(tabName: string): void {
    // Cargar datos específicos del tab si es necesario
    switch (tabName) {
      case 'dashboard':
        // El dashboard se carga automáticamente
        break;
      case 'users':
        // Los usuarios se cargan automáticamente
        break;
      case 'products':
        // Los productos se cargan automáticamente
        break;
      case 'advanced-analytics':
        // Los análisis avanzados se cargan automáticamente
        break;
      case 'business-intelligence':
        // La inteligencia de negocios se carga automáticamente
        break;
    }
  }

  private setupResizeHandler(): void {
    let resizeTimeout: number;
    window.addEventListener('resize', () => {
      clearTimeout(resizeTimeout);
      resizeTimeout = window.setTimeout(() => {
        chartManager.resizeCharts();
      }, 250);
    });
  }
}

// Inicializar la aplicación
new App();
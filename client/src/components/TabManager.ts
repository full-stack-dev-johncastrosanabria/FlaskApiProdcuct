/**
 * Gestor de pestañas (tabs) de la aplicación
 */
export class TabManager {
  private activeTab: string = 'dashboard';

  constructor() {
    this.initializeTabs();
  }

  private initializeTabs(): void {
    const tabButtons = document.querySelectorAll('.tab-button');
    
    tabButtons.forEach(button => {
      button.addEventListener('click', (e) => {
        const target = e.target as HTMLElement;
        const tabName = target.dataset.tab;
        if (tabName) {
          this.switchTab(tabName);
        }
      });
    });

    // Activar tab inicial
    this.switchTab(this.activeTab);
  }

  switchTab(tabName: string): void {
    // Actualizar botones
    document.querySelectorAll('.tab-button').forEach(btn => {
      btn.classList.remove('active');
    });
    
    const activeButton = document.querySelector(`[data-tab="${tabName}"]`);
    if (activeButton) {
      activeButton.classList.add('active');
    }
    
    // Actualizar contenido
    document.querySelectorAll('.tab-content').forEach(content => {
      content.classList.remove('active');
    });
    
    const activeContent = document.getElementById(tabName);
    if (activeContent) {
      activeContent.classList.add('active');
    }

    this.activeTab = tabName;

    // Disparar evento personalizado
    window.dispatchEvent(new CustomEvent('tabChanged', { 
      detail: { tabName } 
    }));
  }

  getActiveTab(): string {
    return this.activeTab;
  }
}
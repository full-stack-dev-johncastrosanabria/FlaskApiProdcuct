import type { ToastType } from '../types';

export class ToastManager {
  private static instance: ToastManager;
  private toastContainer!: HTMLElement;

  private constructor() {
    this.createToastContainer();
  }

  static getInstance(): ToastManager {
    if (!ToastManager.instance) {
      ToastManager.instance = new ToastManager();
    }
    return ToastManager.instance;
  }

  private createToastContainer(): void {
    this.toastContainer = document.createElement('div');
    this.toastContainer.id = 'toast-container';
    this.toastContainer.className = 'toast-container';
    document.body.appendChild(this.toastContainer);
  }

  show(message: string, type: ToastType = 'info', duration: number = 3000): void {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type} show`;
    toast.textContent = message;

    // Agregar icono según el tipo
    const icon = this.getIcon(type);
    toast.innerHTML = `${icon} ${message}`;

    this.toastContainer.appendChild(toast);

    // Auto-remover después del tiempo especificado
    setTimeout(() => {
      toast.classList.remove('show');
      setTimeout(() => {
        if (toast.parentNode) {
          toast.parentNode.removeChild(toast);
        }
      }, 300);
    }, duration);
  }

  private getIcon(type: ToastType): string {
    const icons = {
      success: '✅',
      error: '❌',
      warning: '⚠️',
      info: 'ℹ️'
    };
    return icons[type] || icons.info;
  }

  success(message: string, duration?: number): void {
    this.show(message, 'success', duration);
  }

  error(message: string, duration?: number): void {
    this.show(message, 'error', duration);
  }

  warning(message: string, duration?: number): void {
    this.show(message, 'warning', duration);
  }

  info(message: string, duration?: number): void {
    this.show(message, 'info', duration);
  }
}

// Instancia global
export const toast = ToastManager.getInstance();
/**
 * Utilidades generales para el cliente
 */

// Formatear fecha
export function formatDate(dateString: string): string {
  const date = new Date(dateString);
  return date.toLocaleString('es-ES', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
}

// Escapar HTML para prevenir XSS
export function escapeHtml(text: string): string {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

// Formatear precio
export function formatPrice(price: number): string {
  return `$${price.toFixed(2)}`;
}

// Formatear número con separadores de miles
export function formatNumber(num: number): string {
  return num.toLocaleString('es-ES');
}

// Validar email
export function isValidEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

// Debounce para búsquedas
export function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout;
  return (...args: Parameters<T>) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait);
  };
}

// Obtener clase CSS para stock
export function getStockClass(stock: number): string {
  if (stock === 0) return 'out';
  if (stock < 10) return 'low';
  return '';
}

// Obtener clase CSS para estado de orden
export function getOrderStatusClass(status: string): string {
  switch (status) {
    case 'completed':
      return 'status-completed';
    case 'pending':
      return 'status-pending';
    case 'cancelled':
      return 'status-cancelled';
    default:
      return '';
  }
}

// Capitalizar primera letra
export function capitalize(str: string): string {
  return str.charAt(0).toUpperCase() + str.slice(1);
}

// Truncar texto
export function truncate(text: string, maxLength: number): string {
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + '...';
}

// Generar ID único
export function generateId(): string {
  return Math.random().toString(36).substr(2, 9);
}

// Helper function to validate a single field
function validateField(value: any, rule: any, fieldLabel: string): string[] {
  const errors: string[] = [];

  // Check required
  if (rule.required && (!value || value.toString().trim() === '')) {
    errors.push(`El campo ${fieldLabel} es requerido`);
    return errors;
  }

  if (!value) return errors; // Skip other validations if no value

  // Validate email
  if (rule.type === 'email' && !isValidEmail(value)) {
    errors.push(`El campo ${fieldLabel} debe ser un email válido`);
  }

  // Validate number
  if (rule.type === 'number' && isNaN(Number(value))) {
    errors.push(`El campo ${fieldLabel} debe ser un número`);
  }

  // Validate min/max
  const numValue = Number(value);
  if (rule.min !== undefined && numValue < rule.min) {
    errors.push(`El campo ${fieldLabel} debe ser mayor a ${rule.min}`);
  }

  if (rule.max !== undefined && numValue > rule.max) {
    errors.push(`El campo ${fieldLabel} debe ser menor a ${rule.max}`);
  }

  // Validate minLength
  if (rule.minLength && value.toString().length < rule.minLength) {
    errors.push(`El campo ${fieldLabel} debe tener al menos ${rule.minLength} caracteres`);
  }

  return errors;
}

// Validar formulario
export function validateForm(formData: Record<string, any>, rules: Record<string, any>): { isValid: boolean; errors: string[] } {
  const errors: string[] = [];

  for (const [field, rule] of Object.entries(rules)) {
    const value = formData[field];
    const fieldLabel = rule.label || field;
    const fieldErrors = validateField(value, rule, fieldLabel);
    errors.push(...fieldErrors);
  }

  return {
    isValid: errors.length === 0,
    errors
  };
}
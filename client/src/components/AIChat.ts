/**
 * Componente de Chat con IA
 * Interfaz de conversación con el chatbot
 */
import { ApiService } from '../services/api';
import { toast } from '../utils/toast';

interface Message {
  type: 'user' | 'bot';
  message: string;
  confidence?: number;
  category?: string;
  timestamp?: Date;
}

interface AIResponse {
  answer: string;
  confidence: number;
  data: any;
  category: string;
}

export class AIChat {
  private container: HTMLElement | null;
  private messagesContainer: HTMLElement | null;
  private inputField: HTMLInputElement | null;
  private sendButton: HTMLElement | null;
  private clearButton: HTMLElement | null;
  private messages: Message[] = [];
  private isLoading: boolean = false;

  constructor() {
    this.container = document.getElementById('ai-chat-container');
    this.messagesContainer = document.getElementById('ai-messages');
    this.inputField = document.getElementById('ai-input') as HTMLInputElement;
    this.sendButton = document.getElementById('ai-send-btn');
    this.clearButton = document.getElementById('ai-clear-btn');

    this.init();
  }

  private init(): void {
    if (!this.container) {
      console.error('AI Chat container not found');
      return;
    }

    this.setupEventListeners();
    this.loadHistory();
    this.showWelcomeMessage();
  }

  private setupEventListeners(): void {
    // Botón enviar
    this.sendButton?.addEventListener('click', () => this.sendMessage());

    // Enter en el input
    this.inputField?.addEventListener('keypress', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        this.sendMessage();
      }
    });

    // Botón limpiar historial
    this.clearButton?.addEventListener('click', () => this.clearHistory());

    // Auto-resize del textarea
    this.inputField?.addEventListener('input', () => {
      if (this.inputField) {
        this.inputField.style.height = 'auto';
        this.inputField.style.height = this.inputField.scrollHeight + 'px';
      }
    });
  }

  private showWelcomeMessage(): void {
    if (this.messages.length === 0) {
      const welcomeMessage: Message = {
        type: 'bot',
        message: '¡Hola! 👋 Soy tu asistente de IA. Puedo ayudarte con información sobre:\n\n' +
                 '📊 Ventas y estadísticas\n' +
                 '📦 Productos e inventario\n' +
                 '👥 Clientes y comportamiento\n' +
                 '💡 Recomendaciones\n\n' +
                 '¿Qué te gustaría saber?',
        category: 'welcome',
        timestamp: new Date()
      };
      this.addMessage(welcomeMessage);
    }
  }

  private async loadHistory(): Promise<void> {
    try {
      const response = await ApiService.getAIHistory();
      
      if (response.success && response.data && response.data.length > 0) {
        this.messages = response.data.map((msg: any) => ({
          ...msg,
          timestamp: new Date()
        }));
        this.renderMessages();
      }
    } catch (error) {
      console.error('Error loading history:', error);
    }
  }

  private async sendMessage(): Promise<void> {
    if (!this.inputField || this.isLoading) return;

    const question = this.inputField.value.trim();
    
    if (!question) {
      toast.warning('Por favor escribe una pregunta');
      return;
    }

    // Agregar mensaje del usuario
    const userMessage: Message = {
      type: 'user',
      message: question,
      timestamp: new Date()
    };
    this.addMessage(userMessage);

    // Limpiar input
    this.inputField.value = '';
    this.inputField.style.height = 'auto';

    // Mostrar indicador de carga
    this.showTypingIndicator();
    this.isLoading = true;

    try {
      // Enviar pregunta a la API
      const response = await ApiService.askAI(question);

      this.hideTypingIndicator();

      if (response.success && response.data) {
        const aiResponse: AIResponse = response.data;
        
        const botMessage: Message = {
          type: 'bot',
          message: aiResponse.answer,
          confidence: aiResponse.confidence,
          category: aiResponse.category,
          timestamp: new Date()
        };
        
        this.addMessage(botMessage);
      } else {
        throw new Error(response.message || 'Error al procesar la pregunta');
      }
    } catch (error) {
      this.hideTypingIndicator();
      console.error('Error sending message:', error);
      
      const errorMessage: Message = {
        type: 'bot',
        message: '❌ Lo siento, hubo un error al procesar tu pregunta. Por favor intenta de nuevo.',
        category: 'error',
        timestamp: new Date()
      };
      this.addMessage(errorMessage);
      
      toast.error('Error al enviar mensaje');
    } finally {
      this.isLoading = false;
    }
  }

  private addMessage(message: Message): void {
    this.messages.push(message);
    this.renderMessage(message);
    this.scrollToBottom();
  }

  private renderMessages(): void {
    if (!this.messagesContainer) return;
    
    this.messagesContainer.innerHTML = '';
    this.messages.forEach(msg => this.renderMessage(msg));
    this.scrollToBottom();
  }

  private renderMessage(message: Message): void {
    if (!this.messagesContainer) return;

    const messageDiv = document.createElement('div');
    messageDiv.className = `ai-message ai-message-${message.type}`;

    // Avatar
    const avatar = document.createElement('div');
    avatar.className = 'ai-message-avatar';
    avatar.textContent = message.type === 'user' ? '👤' : '🤖';

    // Contenido
    const content = document.createElement('div');
    content.className = 'ai-message-content';

    // Texto del mensaje
    const text = document.createElement('div');
    text.className = 'ai-message-text';
    text.textContent = message.message;

    // Formatear texto con saltos de línea
    text.innerHTML = message.message.replace(/\n/g, '<br>');

    content.appendChild(text);

    // Metadata (solo para mensajes del bot)
    if (message.type === 'bot' && message.confidence !== undefined) {
      const meta = document.createElement('div');
      meta.className = 'ai-message-meta';
      
      const confidencePercent = Math.round(message.confidence * 100);
      const confidenceClass = confidencePercent >= 90 ? 'high' : 
                             confidencePercent >= 70 ? 'medium' : 'low';
      
      meta.innerHTML = `
        <span class="ai-confidence ai-confidence-${confidenceClass}">
          Confianza: ${confidencePercent}%
        </span>
        ${message.category ? `<span class="ai-category">${this.getCategoryIcon(message.category)} ${message.category}</span>` : ''}
      `;
      
      content.appendChild(meta);
    }

    messageDiv.appendChild(avatar);
    messageDiv.appendChild(content);

    this.messagesContainer.appendChild(messageDiv);
  }

  private getCategoryIcon(category: string): string {
    const icons: { [key: string]: string } = {
      'ventas': '📊',
      'productos': '📦',
      'clientes': '👥',
      'categorias': '🏷️',
      'stock': '📋',
      'recomendaciones': '💡',
      'saludo': '👋',
      'ayuda': '❓',
      'error': '❌',
      'welcome': '🤖'
    };
    return icons[category] || '💬';
  }

  private showTypingIndicator(): void {
    if (!this.messagesContainer) return;

    const indicator = document.createElement('div');
    indicator.className = 'ai-typing-indicator';
    indicator.id = 'ai-typing';
    indicator.innerHTML = `
      <div class="ai-message-avatar">🤖</div>
      <div class="ai-typing-dots">
        <span></span>
        <span></span>
        <span></span>
      </div>
    `;

    this.messagesContainer.appendChild(indicator);
    this.scrollToBottom();
  }

  private hideTypingIndicator(): void {
    const indicator = document.getElementById('ai-typing');
    if (indicator) {
      indicator.remove();
    }
  }

  private scrollToBottom(): void {
    if (this.messagesContainer) {
      this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }
  }

  private async clearHistory(): Promise<void> {
    if (!confirm('¿Estás seguro de que quieres limpiar el historial de conversación?')) {
      return;
    }

    try {
      const response = await ApiService.clearAIHistory();

      if (response.success) {
        this.messages = [];
        if (this.messagesContainer) {
          this.messagesContainer.innerHTML = '';
        }
        this.showWelcomeMessage();
        toast.success('Historial limpiado');
      } else {
        throw new Error(response.message || 'Error al limpiar historial');
      }
    } catch (error) {
      console.error('Error clearing history:', error);
      toast.error('Error al limpiar historial');
    }
  }

  public async loadCapabilities(): Promise<void> {
    try {
      const response = await ApiService.getAICapabilities();
      
      if (response.success && response.data) {
        console.log('AI Capabilities:', response.data);
      }
    } catch (error) {
      console.error('Error loading capabilities:', error);
    }
  }
}

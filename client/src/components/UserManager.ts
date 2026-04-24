import { ApiService } from '../services/api';
import { toast } from '../utils/toast';
import { formatDate, escapeHtml, validateForm } from '../utils/helpers';
import type { User, CreateUserData } from '../types';

/**
 * Gestor de usuarios
 */
export class UserManager {
  private usersList: HTMLElement;
  private createForm: HTMLFormElement;
  private editModal: HTMLElement;
  private currentEditUser: User | null = null;

  constructor() {
    this.usersList = document.getElementById('usersList') as HTMLElement;
    this.createForm = document.getElementById('createUserForm') as HTMLFormElement;
    this.editModal = document.getElementById('editModal') as HTMLElement;

    if (!this.usersList || !this.createForm || !this.editModal) {
      console.error('User manager elements not found');
      return;
    }

    this.setupEventListeners();
    this.loadUsers();
  }

  private setupEventListeners(): void {
    // Formulario de crear usuario
    this.createForm.addEventListener('submit', (e) => {
      e.preventDefault();
      this.handleCreateUser();
    });

    // Botón de actualizar lista
    const refreshButton = document.querySelector('[onclick="loadUsers()"]') as HTMLElement;
    if (refreshButton) {
      refreshButton.onclick = () => this.loadUsers();
    }
  }

  async loadUsers(): Promise<void> {
    this.usersList.innerHTML = '<p class="loading">Cargando usuarios...</p>';
    
    try {
      const response = await ApiService.getUsers();
      
      if (response.success) {
        if (response.data.length === 0) {
          this.usersList.innerHTML = `
            <div class="empty-state">
              <div class="empty-state-icon">👤</div>
              <p>No hay usuarios registrados</p>
            </div>
          `;
        } else {
          this.usersList.innerHTML = response.data.map(user => this.createUserCard(user)).join('');
        }
      }
    } catch (error) {
      this.usersList.innerHTML = '<p class="loading">Error al cargar usuarios</p>';
      toast.error('Error al cargar usuarios');
    }
  }

  private createUserCard(user: User): string {
    return `
      <div class="item-card">
        <div class="item-header">
          <div>
            <div class="item-title">${escapeHtml(user.name)}</div>
          </div>
          <div class="item-actions">
            <button class="btn btn-edit" onclick="userManager.editUser(${user.id})">✏️ Editar</button>
            <button class="btn btn-danger" onclick="userManager.deleteUser(${user.id})">🗑️ Eliminar</button>
          </div>
        </div>
        <div class="item-details">
          <div class="item-detail">
            <strong>Email:</strong> ${escapeHtml(user.email)}
          </div>
          <div class="item-detail">
            <strong>ID:</strong> ${user.id}
          </div>
          <div class="item-detail">
            <strong>Creado:</strong> ${formatDate(user.created_at)}
          </div>
        </div>
      </div>
    `;
  }

  private async handleCreateUser(): Promise<void> {
    const formData = new FormData(this.createForm);
    const userData: CreateUserData = {
      name: formData.get('name') as string,
      email: formData.get('email') as string
    };

    // Validar datos
    const validation = validateForm(userData, {
      name: { required: true, label: 'Nombre', minLength: 2 },
      email: { required: true, label: 'Email', type: 'email' }
    });

    if (!validation.isValid) {
      toast.error(validation.errors[0]);
      return;
    }

    try {
      const response = await ApiService.createUser(userData);
      
      if (response.success) {
        toast.success('Usuario creado exitosamente');
        this.loadUsers();
        this.createForm.reset();
      } else {
        toast.error(response.error || 'Error al crear usuario');
      }
    } catch (error) {
      toast.error('Error al crear usuario');
    }
  }

  async editUser(userId: number): Promise<void> {
    try {
      const response = await ApiService.getUser(userId);
      
      if (response.success) {
        this.currentEditUser = response.data;
        this.showEditModal(response.data);
      }
    } catch (error) {
      toast.error('Error al cargar usuario');
    }
  }

  private showEditModal(user: User): void {
    const modalTitle = document.getElementById('modalTitle') as HTMLElement;
    const formFields = document.getElementById('editFormFields') as HTMLElement;
    
    modalTitle.textContent = 'Editar Usuario';
    
    formFields.innerHTML = `
      <div class="form-group">
        <label for="editName">Nombre:</label>
        <input type="text" id="editName" value="${escapeHtml(user.name)}" required>
      </div>
      <div class="form-group">
        <label for="editEmail">Email:</label>
        <input type="email" id="editEmail" value="${escapeHtml(user.email)}" required>
      </div>
    `;
    
    this.editModal.classList.add('active');

    // Setup form submit
    const editForm = document.getElementById('editForm') as HTMLFormElement;
    editForm.onsubmit = (e) => {
      e.preventDefault();
      this.handleEditSubmit();
    };
  }

  private async handleEditSubmit(): Promise<void> {
    if (!this.currentEditUser) return;

    const nameInput = document.getElementById('editName') as HTMLInputElement;
    const emailInput = document.getElementById('editEmail') as HTMLInputElement;

    const userData: Partial<CreateUserData> = {
      name: nameInput.value,
      email: emailInput.value
    };

    // Validar datos
    const validation = validateForm(userData, {
      name: { required: true, label: 'Nombre', minLength: 2 },
      email: { required: true, label: 'Email', type: 'email' }
    });

    if (!validation.isValid) {
      toast.error(validation.errors[0]);
      return;
    }

    try {
      const response = await ApiService.updateUser(this.currentEditUser.id, userData);
      
      if (response.success) {
        toast.success('Usuario actualizado exitosamente');
        this.loadUsers();
        this.closeModal();
      } else {
        toast.error(response.error || 'Error al actualizar usuario');
      }
    } catch (error) {
      toast.error('Error al actualizar usuario');
    }
  }

  async deleteUser(userId: number): Promise<void> {
    if (!confirm('¿Estás seguro de eliminar este usuario?')) return;
    
    try {
      const response = await ApiService.deleteUser(userId);
      
      if (response.success) {
        toast.success('Usuario eliminado exitosamente');
        this.loadUsers();
      } else {
        toast.error(response.error || 'Error al eliminar usuario');
      }
    } catch (error) {
      toast.error('Error al eliminar usuario');
    }
  }

  private closeModal(): void {
    this.editModal.classList.remove('active');
    this.currentEditUser = null;
  }
}
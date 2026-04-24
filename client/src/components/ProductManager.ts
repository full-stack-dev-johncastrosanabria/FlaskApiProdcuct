import { ApiService } from '../services/api';
import { toast } from '../utils/toast';
import { formatDate, escapeHtml, formatPrice, getStockClass, validateForm } from '../utils/helpers';
import type { Product, Category, CreateProductData, ProductFilters } from '../types';

/**
 * Gestor de productos
 */
export class ProductManager {
  private productsList: HTMLElement;
  private createForm: HTMLFormElement;
  private editModal: HTMLElement;
  private currentEditProduct: Product | null = null;
  private categoriesCache: Category[] = [];

  constructor() {
    this.productsList = document.getElementById('productsList') as HTMLElement;
    this.createForm = document.getElementById('createProductForm') as HTMLFormElement;
    this.editModal = document.getElementById('editModal') as HTMLElement;

    if (!this.productsList || !this.createForm || !this.editModal) {
      console.error('Product manager elements not found');
      return;
    }

    this.setupEventListeners();
    this.loadCategories();
    this.loadProducts();
  }

  private setupEventListeners(): void {
    // Formulario de crear producto
    this.createForm.addEventListener('submit', (e) => {
      e.preventDefault();
      this.handleCreateProduct();
    });

    // Botón de actualizar lista
    const refreshButton = document.querySelector('[onclick="loadProducts()"]') as HTMLElement;
    if (refreshButton) {
      refreshButton.onclick = () => this.loadProducts();
    }

    // Filtros
    const filterButton = document.querySelector('[onclick="loadProducts()"]') as HTMLElement;
    if (filterButton) {
      filterButton.onclick = () => this.loadProducts();
    }
  }

  async loadCategories(): Promise<void> {
    try {
      const response = await ApiService.getCategories();
      
      if (response.success) {
        this.categoriesCache = response.data;
        this.populateCategorySelects();
      }
    } catch (error) {
      console.error('Error al cargar categorías:', error);
    }
  }

  private populateCategorySelects(): void {
    // Llenar el select de crear producto
    const createSelect = document.getElementById('productCategory') as HTMLSelectElement;
    if (createSelect) {
      createSelect.innerHTML = '<option value="">Selecciona una categoría</option>' +
        this.categoriesCache.map(cat => 
          `<option value="${cat.id}">${escapeHtml(cat.name)}</option>`
        ).join('');
    }
    
    // Llenar el select de filtro
    const filterSelect = document.getElementById('categoryFilter') as HTMLSelectElement;
    if (filterSelect) {
      filterSelect.innerHTML = '<option value="">Todas las categorías</option>' +
        this.categoriesCache.map(cat => 
          `<option value="${cat.id}">${escapeHtml(cat.name)}</option>`
        ).join('');
    }
  }

  async loadProducts(): Promise<void> {
    this.productsList.innerHTML = '<p class="loading">Cargando productos...</p>';
    
    // Obtener filtros
    const minPriceInput = document.getElementById('minPrice') as HTMLInputElement;
    const maxPriceInput = document.getElementById('maxPrice') as HTMLInputElement;
    const categoryInput = document.getElementById('categoryFilter') as HTMLSelectElement;
    
    const filters: ProductFilters = {};
    if (minPriceInput?.value) filters.min_price = parseFloat(minPriceInput.value);
    if (maxPriceInput?.value) filters.max_price = parseFloat(maxPriceInput.value);
    if (categoryInput?.value) filters.category = parseInt(categoryInput.value);
    
    try {
      const response = await ApiService.getProducts(filters);
      
      if (response.success) {
        if (response.data.length === 0) {
          this.productsList.innerHTML = `
            <div class="empty-state">
              <div class="empty-state-icon">📦</div>
              <p>No hay productos registrados</p>
            </div>
          `;
        } else {
          this.productsList.innerHTML = response.data.map(product => this.createProductCard(product)).join('');
        }
      }
    } catch (error) {
      this.productsList.innerHTML = '<p class="loading">Error al cargar productos</p>';
      toast.error('Error al cargar productos');
    }
  }

  private createProductCard(product: Product): string {
    const stockClass = getStockClass(product.stock);
    const categoryName = product.category || 'Sin categoría';
    
    return `
      <div class="item-card">
        <div class="item-header">
          <div>
            <div class="item-title">${escapeHtml(product.name)}</div>
            <div class="item-price">${formatPrice(product.price)}</div>
          </div>
          <div class="item-actions">
            <button class="btn btn-edit" onclick="productManager.editProduct(${product.id})">✏️ Editar</button>
            <button class="btn btn-danger" onclick="productManager.deleteProduct(${product.id})">🗑️ Eliminar</button>
          </div>
        </div>
        <div class="item-details">
          <div class="item-detail">
            <strong>Categoría:</strong> ${escapeHtml(categoryName)}
          </div>
          <div class="item-detail">
            <strong>Stock:</strong> <span class="item-stock ${stockClass}">${product.stock} unidades</span>
          </div>
          ${product.description ? `
          <div class="item-detail">
            <strong>Descripción:</strong> ${escapeHtml(product.description)}
          </div>
          ` : ''}
          <div class="item-detail">
            <strong>Creado:</strong> ${formatDate(product.created_at)}
          </div>
        </div>
      </div>
    `;
  }

  private async handleCreateProduct(): Promise<void> {
    const formData = new FormData(this.createForm);
    const productData: CreateProductData = {
      name: formData.get('name') as string,
      price: parseFloat(formData.get('price') as string),
      stock: parseInt(formData.get('stock') as string) || 0,
      category_id: parseInt(formData.get('category') as string),
      description: formData.get('description') as string || ''
    };

    // Validar datos
    const validation = validateForm(productData, {
      name: { required: true, label: 'Nombre', minLength: 2 },
      price: { required: true, label: 'Precio', type: 'number', min: 0 },
      category_id: { required: true, label: 'Categoría' },
      stock: { type: 'number', min: 0 }
    });

    if (!validation.isValid) {
      toast.error(validation.errors[0]);
      return;
    }

    try {
      const response = await ApiService.createProduct(productData);
      
      if (response.success) {
        toast.success('Producto creado exitosamente');
        this.loadProducts();
        this.createForm.reset();
      } else {
        toast.error(response.error || 'Error al crear producto');
      }
    } catch (error) {
      toast.error('Error al crear producto');
    }
  }

  async editProduct(productId: number): Promise<void> {
    try {
      const response = await ApiService.getProduct(productId);
      
      if (response.success) {
        this.currentEditProduct = response.data;
        this.showEditModal(response.data);
      }
    } catch (error) {
      toast.error('Error al cargar producto');
    }
  }

  private showEditModal(product: Product): void {
    const modalTitle = document.getElementById('modalTitle') as HTMLElement;
    const formFields = document.getElementById('editFormFields') as HTMLElement;
    
    modalTitle.textContent = 'Editar Producto';
    
    const categoryOptions = this.categoriesCache.map(cat => 
      `<option value="${cat.id}" ${cat.id === product.category_id ? 'selected' : ''}>${escapeHtml(cat.name)}</option>`
    ).join('');
    
    formFields.innerHTML = `
      <div class="form-group">
        <label for="editName">Nombre:</label>
        <input type="text" id="editName" value="${escapeHtml(product.name)}" required>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label for="editPrice">Precio:</label>
          <input type="number" id="editPrice" step="0.01" value="${product.price}" required>
        </div>
        <div class="form-group">
          <label for="editStock">Stock:</label>
          <input type="number" id="editStock" value="${product.stock}">
        </div>
      </div>
      <div class="form-group">
        <label for="editCategory">Categoría:</label>
        <select id="editCategory" required>
          <option value="">Selecciona una categoría</option>
          ${categoryOptions}
        </select>
      </div>
      <div class="form-group">
        <label for="editDescription">Descripción:</label>
        <textarea id="editDescription" rows="3">${escapeHtml(product.description || '')}</textarea>
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
    if (!this.currentEditProduct) return;

    const nameInput = document.getElementById('editName') as HTMLInputElement;
    const priceInput = document.getElementById('editPrice') as HTMLInputElement;
    const stockInput = document.getElementById('editStock') as HTMLInputElement;
    const categoryInput = document.getElementById('editCategory') as HTMLSelectElement;
    const descriptionInput = document.getElementById('editDescription') as HTMLTextAreaElement;

    const productData: Partial<CreateProductData> = {
      name: nameInput.value,
      price: parseFloat(priceInput.value),
      stock: parseInt(stockInput.value) || 0,
      category_id: parseInt(categoryInput.value),
      description: descriptionInput.value
    };

    // Validar datos
    const validation = validateForm(productData, {
      name: { required: true, label: 'Nombre', minLength: 2 },
      price: { required: true, label: 'Precio', type: 'number', min: 0 },
      category_id: { required: true, label: 'Categoría' },
      stock: { type: 'number', min: 0 }
    });

    if (!validation.isValid) {
      toast.error(validation.errors[0]);
      return;
    }

    try {
      const response = await ApiService.updateProduct(this.currentEditProduct.id, productData);
      
      if (response.success) {
        toast.success('Producto actualizado exitosamente');
        this.loadProducts();
        this.closeModal();
      } else {
        toast.error(response.error || 'Error al actualizar producto');
      }
    } catch (error) {
      toast.error('Error al actualizar producto');
    }
  }

  async deleteProduct(productId: number): Promise<void> {
    if (!confirm('¿Estás seguro de eliminar este producto?')) return;
    
    try {
      const response = await ApiService.deleteProduct(productId);
      
      if (response.success) {
        toast.success('Producto eliminado exitosamente');
        this.loadProducts();
      } else {
        toast.error(response.error || 'Error al eliminar producto');
      }
    } catch (error) {
      toast.error('Error al eliminar producto');
    }
  }

  private closeModal(): void {
    this.editModal.classList.remove('active');
    this.currentEditProduct = null;
  }
}
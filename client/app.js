// Configuración de la API
const API_URL = 'http://localhost:5001';

// Estado global
let currentEditItem = null;
let currentEditType = null;

// Inicialización
document.addEventListener('DOMContentLoaded', () => {
    initializeTabs();
    checkAPIHealth();
    loadUsers();
    loadProducts();
    setupForms();
    setupModal();
});

// ============================================================================
// TABS
// ============================================================================

function initializeTabs() {
    const tabButtons = document.querySelectorAll('.tab-button');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tabName = button.dataset.tab;
            switchTab(tabName);
        });
    });
}

function switchTab(tabName) {
    // Actualizar botones
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
    
    // Actualizar contenido
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    document.getElementById(tabName).classList.add('active');
}

// ============================================================================
// HEALTH CHECK
// ============================================================================

async function checkAPIHealth() {
    const statusIndicator = document.querySelector('.status-indicator');
    const statusText = document.querySelector('.status-text');
    
    try {
        const response = await fetch(`${API_URL}/api/health`);
        const data = await response.json();
        
        if (data.status === 'healthy') {
            statusIndicator.classList.add('healthy');
            statusText.textContent = 'API Conectada';
        } else {
            throw new Error('API no saludable');
        }
    } catch (error) {
        statusIndicator.classList.add('error');
        statusText.textContent = 'API Desconectada';
        showToast('No se pudo conectar con la API', 'error');
    }
}

// ============================================================================
// USUARIOS
// ============================================================================

async function loadUsers() {
    const usersList = document.getElementById('usersList');
    usersList.innerHTML = '<p class="loading">Cargando usuarios...</p>';
    
    try {
        const response = await fetch(`${API_URL}/api/users`);
        const data = await response.json();
        
        if (data.success) {
            if (data.data.length === 0) {
                usersList.innerHTML = `
                    <div class="empty-state">
                        <div class="empty-state-icon">👤</div>
                        <p>No hay usuarios registrados</p>
                    </div>
                `;
            } else {
                usersList.innerHTML = data.data.map(user => createUserCard(user)).join('');
            }
        }
    } catch (error) {
        usersList.innerHTML = '<p class="loading">Error al cargar usuarios</p>';
        showToast('Error al cargar usuarios', 'error');
    }
}

function createUserCard(user) {
    return `
        <div class="item-card">
            <div class="item-header">
                <div>
                    <div class="item-title">${escapeHtml(user.name)}</div>
                </div>
                <div class="item-actions">
                    <button class="btn btn-edit" onclick="editUser('${user.id}')">✏️ Editar</button>
                    <button class="btn btn-danger" onclick="deleteUser('${user.id}')">🗑️ Eliminar</button>
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

async function createUser(userData) {
    try {
        const response = await fetch(`${API_URL}/api/users`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(userData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            showToast('Usuario creado exitosamente', 'success');
            loadUsers();
            document.getElementById('createUserForm').reset();
        } else {
            showToast(data.error, 'error');
        }
    } catch (error) {
        showToast('Error al crear usuario', 'error');
    }
}

async function editUser(userId) {
    try {
        const response = await fetch(`${API_URL}/api/users/${userId}`);
        const data = await response.json();
        
        if (data.success) {
            currentEditItem = data.data;
            currentEditType = 'user';
            showEditModal(data.data, 'user');
        }
    } catch (error) {
        showToast('Error al cargar usuario', 'error');
    }
}

async function updateUser(userId, userData) {
    try {
        const response = await fetch(`${API_URL}/api/users/${userId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(userData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            showToast('Usuario actualizado exitosamente', 'success');
            loadUsers();
            closeModal();
        } else {
            showToast(data.error, 'error');
        }
    } catch (error) {
        showToast('Error al actualizar usuario', 'error');
    }
}

async function deleteUser(userId) {
    if (!confirm('¿Estás seguro de eliminar este usuario?')) return;
    
    try {
        const response = await fetch(`${API_URL}/api/users/${userId}`, {
            method: 'DELETE'
        });
        
        const data = await response.json();
        
        if (data.success) {
            showToast('Usuario eliminado exitosamente', 'success');
            loadUsers();
        } else {
            showToast(data.error, 'error');
        }
    } catch (error) {
        showToast('Error al eliminar usuario', 'error');
    }
}

// ============================================================================
// PRODUCTOS
// ============================================================================

async function loadProducts() {
    const productsList = document.getElementById('productsList');
    productsList.innerHTML = '<p class="loading">Cargando productos...</p>';
    
    // Obtener filtros
    const minPrice = document.getElementById('minPrice').value;
    const maxPrice = document.getElementById('maxPrice').value;
    const category = document.getElementById('categoryFilter').value;
    
    let url = `${API_URL}/api/products?`;
    if (minPrice) url += `min_price=${minPrice}&`;
    if (maxPrice) url += `max_price=${maxPrice}&`;
    if (category) url += `category=${category}&`;
    
    try {
        const response = await fetch(url);
        const data = await response.json();
        
        if (data.success) {
            if (data.data.length === 0) {
                productsList.innerHTML = `
                    <div class="empty-state">
                        <div class="empty-state-icon">📦</div>
                        <p>No hay productos registrados</p>
                    </div>
                `;
            } else {
                productsList.innerHTML = data.data.map(product => createProductCard(product)).join('');
            }
        }
    } catch (error) {
        productsList.innerHTML = '<p class="loading">Error al cargar productos</p>';
        showToast('Error al cargar productos', 'error');
    }
}

function createProductCard(product) {
    const stockClass = product.stock === 0 ? 'out' : product.stock < 10 ? 'low' : '';
    
    return `
        <div class="item-card">
            <div class="item-header">
                <div>
                    <div class="item-title">${escapeHtml(product.name)}</div>
                    <div class="item-price">$${product.price.toFixed(2)}</div>
                </div>
                <div class="item-actions">
                    <button class="btn btn-edit" onclick="editProduct('${product.id}')">✏️ Editar</button>
                    <button class="btn btn-danger" onclick="deleteProduct('${product.id}')">🗑️ Eliminar</button>
                </div>
            </div>
            <div class="item-details">
                <div class="item-detail">
                    <strong>Categoría:</strong> ${escapeHtml(product.category)}
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

async function createProduct(productData) {
    try {
        const response = await fetch(`${API_URL}/api/products`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(productData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            showToast('Producto creado exitosamente', 'success');
            loadProducts();
            document.getElementById('createProductForm').reset();
        } else {
            showToast(data.error, 'error');
        }
    } catch (error) {
        showToast('Error al crear producto', 'error');
    }
}

async function editProduct(productId) {
    try {
        const response = await fetch(`${API_URL}/api/products/${productId}`);
        const data = await response.json();
        
        if (data.success) {
            currentEditItem = data.data;
            currentEditType = 'product';
            showEditModal(data.data, 'product');
        }
    } catch (error) {
        showToast('Error al cargar producto', 'error');
    }
}

async function updateProduct(productId, productData) {
    try {
        const response = await fetch(`${API_URL}/api/products/${productId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(productData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            showToast('Producto actualizado exitosamente', 'success');
            loadProducts();
            closeModal();
        } else {
            showToast(data.error, 'error');
        }
    } catch (error) {
        showToast('Error al actualizar producto', 'error');
    }
}

async function deleteProduct(productId) {
    if (!confirm('¿Estás seguro de eliminar este producto?')) return;
    
    try {
        const response = await fetch(`${API_URL}/api/products/${productId}`, {
            method: 'DELETE'
        });
        
        const data = await response.json();
        
        if (data.success) {
            showToast('Producto eliminado exitosamente', 'success');
            loadProducts();
        } else {
            showToast(data.error, 'error');
        }
    } catch (error) {
        showToast('Error al eliminar producto', 'error');
    }
}

// ============================================================================
// FORMS
// ============================================================================

function setupForms() {
    // Form de crear usuario
    document.getElementById('createUserForm').addEventListener('submit', (e) => {
        e.preventDefault();
        const userData = {
            name: document.getElementById('userName').value,
            email: document.getElementById('userEmail').value
        };
        createUser(userData);
    });
    
    // Form de crear producto
    document.getElementById('createProductForm').addEventListener('submit', (e) => {
        e.preventDefault();
        const productData = {
            name: document.getElementById('productName').value,
            price: parseFloat(document.getElementById('productPrice').value),
            category: document.getElementById('productCategory').value,
            description: document.getElementById('productDescription').value,
            stock: parseInt(document.getElementById('productStock').value) || 0
        };
        createProduct(productData);
    });
}

// ============================================================================
// MODAL
// ============================================================================

function setupModal() {
    const modal = document.getElementById('editModal');
    const closeBtn = document.querySelector('.close');
    
    closeBtn.onclick = closeModal;
    
    window.onclick = (event) => {
        if (event.target === modal) {
            closeModal();
        }
    };
    
    document.getElementById('editForm').addEventListener('submit', (e) => {
        e.preventDefault();
        handleEditSubmit();
    });
}

function showEditModal(item, type) {
    const modal = document.getElementById('editModal');
    const modalTitle = document.getElementById('modalTitle');
    const formFields = document.getElementById('editFormFields');
    
    modalTitle.textContent = type === 'user' ? 'Editar Usuario' : 'Editar Producto';
    
    if (type === 'user') {
        formFields.innerHTML = `
            <div class="form-group">
                <label for="editName">Nombre:</label>
                <input type="text" id="editName" value="${escapeHtml(item.name)}" required>
            </div>
            <div class="form-group">
                <label for="editEmail">Email:</label>
                <input type="email" id="editEmail" value="${escapeHtml(item.email)}" required>
            </div>
        `;
    } else {
        formFields.innerHTML = `
            <div class="form-group">
                <label for="editName">Nombre:</label>
                <input type="text" id="editName" value="${escapeHtml(item.name)}" required>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label for="editPrice">Precio:</label>
                    <input type="number" id="editPrice" step="0.01" value="${item.price}" required>
                </div>
                <div class="form-group">
                    <label for="editStock">Stock:</label>
                    <input type="number" id="editStock" value="${item.stock}">
                </div>
            </div>
            <div class="form-group">
                <label for="editCategory">Categoría:</label>
                <input type="text" id="editCategory" value="${escapeHtml(item.category)}" required>
            </div>
            <div class="form-group">
                <label for="editDescription">Descripción:</label>
                <textarea id="editDescription" rows="3">${escapeHtml(item.description || '')}</textarea>
            </div>
        `;
    }
    
    modal.classList.add('active');
}

function closeModal() {
    document.getElementById('editModal').classList.remove('active');
    currentEditItem = null;
    currentEditType = null;
}

function handleEditSubmit() {
    if (!currentEditItem || !currentEditType) return;
    
    if (currentEditType === 'user') {
        const userData = {
            name: document.getElementById('editName').value,
            email: document.getElementById('editEmail').value
        };
        updateUser(currentEditItem.id, userData);
    } else {
        const productData = {
            name: document.getElementById('editName').value,
            price: parseFloat(document.getElementById('editPrice').value),
            category: document.getElementById('editCategory').value,
            description: document.getElementById('editDescription').value,
            stock: parseInt(document.getElementById('editStock').value) || 0
        };
        updateProduct(currentEditItem.id, productData);
    }
}

// ============================================================================
// UTILIDADES
// ============================================================================

function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast ${type} show`;
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('es-ES', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

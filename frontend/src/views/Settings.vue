<template>
  <div class="settings-container">
    <!-- Page Header -->
    <header class="settings-header">
      <div class="header-content">
        <h1 class="header-title">Settings</h1>
        <button @click="saveSettings" class="btn btn-primary" :disabled="!hasChanges">
          <span class="material-symbols-outlined">save</span>
          Save Changes
        </button>
      </div>
    </header>

    <!-- Settings Content -->
    <main class="settings-main">
      <div class="settings-grid">
        <!-- User Preferences -->
        <div class="settings-card">
          <div class="card-header">
            <h2>User Preferences</h2>
            <span class="material-symbols-outlined">person</span>
          </div>

          <div class="form-group">
            <label for="currency">Base Currency</label>
            <select v-model="settings.currency" id="currency">
              <option value="INR">₹ Indian Rupee (INR)</option>
              <option value="USD">$ US Dollar (USD)</option>
              <option value="EUR">€ Euro (EUR)</option>
              <option value="GBP">£ British Pound (GBP)</option>
            </select>
          </div>

          <div class="form-group">
            <label for="budget">Monthly Budget</label>
            <input
              v-model="settings.monthlyBudget"
              id="budget"
              type="number"
              min="0"
              step="100"
              placeholder="Enter your monthly budget"
            >
          </div>

          <div class="form-group">
            <label for="notifications">Notifications</label>
            <div class="toggle-group">
              <label class="toggle-label">
                <input v-model="settings.emailNotifications" type="checkbox">
                <span>Email Notifications</span>
              </label>
              <label class="toggle-label">
                <input v-model="settings.budgetAlerts" type="checkbox">
                <span>Budget Alerts</span>
              </label>
            </div>
          </div>
        </div>

        <!-- Categories Management -->
        <div class="settings-card">
          <div class="card-header">
            <h2>Expense Categories</h2>
            <span class="material-symbols-outlined">folder</span>
          </div>

          <div class="categories-list">
            <div v-if="categories.length === 0" class="empty-state">
              <p>No custom categories yet</p>
            </div>
            <div v-for="category in categories" :key="category" class="category-item">
              <span class="category-name">{{ category }}</span>
              <button
                @click="deleteCategory(category)"
                class="delete-btn"
                title="Delete"
              >
                <span class="material-symbols-outlined">delete</span>
              </button>
            </div>
          </div>

          <div class="add-category">
            <div class="form-group">
              <input
                v-model="newCategory"
                type="text"
                placeholder="New category name"
                @keyup.enter="addCategory"
              >
              <button @click="addCategory" class="btn btn-secondary">
                <span class="material-symbols-outlined">add</span>
                Add
              </button>
            </div>
          </div>
        </div>

        <!-- Data Management -->
        <div class="settings-card">
          <div class="card-header">
            <h2>Data Management</h2>
            <span class="material-symbols-outlined">download</span>
          </div>

          <div class="data-actions">
            <button @click="exportData" class="btn btn-secondary">
              <span class="material-symbols-outlined">download</span>
              Export as CSV
            </button>
            <button @click="exportJSON" class="btn btn-secondary">
              <span class="material-symbols-outlined">download</span>
              Export as JSON
            </button>
          </div>
        </div>

        <!-- About & Help -->
        <div class="settings-card">
          <div class="card-header">
            <h2>About</h2>
            <span class="material-symbols-outlined">info</span>
          </div>

          <div class="about-info">
            <div class="info-item">
              <span class="info-label">App Version</span>
              <span class="info-value">1.0.0</span>
            </div>
            <div class="info-item">
              <span class="info-label">Last Updated</span>
              <span class="info-value">{{ new Date().toLocaleDateString() }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Support</span>
              <a href="mailto:support@example.com" class="info-link">support@example.com</a>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Success Toast -->
    <div v-if="showSuccessMessage" class="toast toast-success">
      <span class="material-symbols-outlined">check_circle</span>
      <span>Settings saved successfully!</span>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch, onMounted } from 'vue';
import axios from 'axios';
import { API_BASE_URL } from '../utils/env.js';

const settings = reactive({
  currency: 'INR',
  monthlyBudget: 5000,
  emailNotifications: true,
  budgetAlerts: true
});

const categories = ref(['Food', 'Transport', 'Entertainment', 'Utilities', 'Shopping', 'Health']);
const newCategory = ref('');
const showSuccessMessage = ref(false);
const hasChanges = ref(false);

async function addCategory() {
  if (!newCategory.value.trim()) {
    alert('Please enter a category name');
    return;
  }

  if (categories.value.includes(newCategory.value)) {
    alert('This category already exists');
    return;
  }

  categories.value.push(newCategory.value);
  newCategory.value = '';
  hasChanges.value = true;
}

async function deleteCategory(category) {
  if (confirm(`Are you sure you want to delete "${category}"?`)) {
    categories.value = categories.value.filter(c => c !== category);
    hasChanges.value = true;
  }
}

async function saveSettings() {
  try {
    localStorage.setItem('appSettings', JSON.stringify(settings));
    localStorage.setItem('appCategories', JSON.stringify(categories.value));

    hasChanges.value = false;
    showSuccessMessage.value = true;
    setTimeout(() => { showSuccessMessage.value = false; }, 3000);
  } catch (error) {
    console.error('Error saving settings:', error);
    alert('Failed to save settings');
  }
}

function exportData() {
  try {
    axios.get(`${API_BASE_URL}/expenses/default-user`).then(res => {
      const expenses = res.data;
      let csv = 'Date,Category,Description,Amount,Payment Method\n';

      expenses.forEach(exp => {
        csv += `${exp.date},"${exp.category}","${exp.description || ''}",${exp.amount},"${exp.payment_method}"\n`;
      });

      const blob = new Blob([csv], { type: 'text/csv' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `expenses-${new Date().toISOString().split('T')[0]}.csv`;
      link.click();
      window.URL.revokeObjectURL(url);
    });
  } catch (error) {
    console.error('Error exporting data:', error);
    alert('Failed to export data');
  }
}

function exportJSON() {
  try {
    axios.get(`${API_BASE_URL}/expenses/default-user`).then(res => {
      const expenses = res.data;
      const dataToExport = {
        settings: { ...settings },
        categories: categories.value,
        expenses: expenses,
        exportDate: new Date().toISOString()
      };

      const blob = new Blob([JSON.stringify(dataToExport, null, 2)], { type: 'application/json' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `expenses-backup-${new Date().toISOString().split('T')[0]}.json`;
      link.click();
      window.URL.revokeObjectURL(url);
    });
  } catch (error) {
    console.error('Error exporting data:', error);
    alert('Failed to export data');
  }
}

function loadSettings() {
  const saved = localStorage.getItem('appSettings');
  const savedCategories = localStorage.getItem('appCategories');

  if (saved) {
    const parsed = JSON.parse(saved);
    Object.assign(settings, parsed);
  }
  if (savedCategories) {
    categories.value = JSON.parse(savedCategories);
  }
}

watch(settings, () => { hasChanges.value = true; }, { deep: true });

onMounted(() => {
  loadSettings();
});
</script>

<style scoped>
.settings-container {
  min-height: 100vh;
  background-color: var(--background);
}

.settings-header {
  background-color: rgba(247, 250, 249, 0.7);
  backdrop-filter: blur(20px);
  position: sticky;
  top: 0;
  z-index: 50;
  border-bottom: 1px solid rgba(0, 77, 76, 0.1);
  box-shadow: 0 24px 48px -12px rgba(24, 28, 28, 0.06);
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 2rem;
}

.header-title {
  margin: 0;
  font-size: 2.75rem;
  font-weight: 700;
  letter-spacing: -0.02em;
}

.settings-main {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.settings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
}

.settings-card {
  background-color: var(--surface-container-lowest);
  border-radius: var(--radius-lg);
  padding: 2rem;
  box-shadow: 0 24px 48px -12px rgba(24, 28, 28, 0.06);
  border: 1px solid rgba(0, 77, 76, 0.1);
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
}

.card-header h2 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 700;
}

.card-header .material-symbols-outlined {
  color: var(--primary);
  font-size: 1.5rem;
}

/* Form Groups */
.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.form-group label {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--on-surface);
}

.form-group input,
.form-group select {
  padding: 0.75rem 1rem;
  border: 1px solid rgba(0, 77, 76, 0.15);
  border-radius: var(--radius-md);
  background-color: var(--surface-container-high);
  color: var(--on-surface);
  font-family: var(--font-body);
  font-size: 1rem;
  transition: all 200ms ease;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  background-color: var(--surface-container-lowest);
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(0, 77, 76, 0.08);
}

/* Toggle Group */
.toggle-group {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.toggle-label {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
  font-size: 0.95rem;
}

.toggle-label input {
  margin: 0;
  width: auto;
}

/* Categories List */
.categories-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  max-height: 300px;
  overflow-y: auto;
}

.empty-state {
  padding: 2rem 1rem;
  text-align: center;
  color: var(--on-surface-variant);
  font-size: 0.95rem;
}

.category-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 1rem;
  background-color: var(--surface-container-low);
  border-radius: var(--radius-md);
  transition: all 200ms ease;
}

.category-item:hover {
  background-color: var(--surface-container);
}

.category-name {
  font-weight: 600;
  color: var(--on-surface);
}

.delete-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-md);
  transition: all 200ms ease;
}

.delete-btn:hover {
  background-color: rgba(186, 26, 26, 0.1);
}

.delete-btn .material-symbols-outlined {
  color: var(--error);
  font-size: 1.25rem;
}

/* Add Category */
.add-category {
  border-top: 1px solid rgba(0, 77, 76, 0.1);
  padding-top: 1.5rem;
}

.add-category .form-group {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 1rem;
  margin-bottom: 0;
}

.add-category input {
  min-height: 44px;
}

.add-category .btn {
  align-self: flex-end;
}

/* Data Actions */
.data-actions {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.data-actions .btn {
  width: 100%;
  justify-content: center;
}

/* About Info */
.about-info {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background-color: var(--surface-container-low);
  border-radius: var(--radius-md);
}

.info-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--on-surface-variant);
}

.info-value,
.info-link {
  font-weight: 600;
  color: var(--on-surface);
}

.info-link {
  text-decoration: none;
  color: var(--primary);
  transition: all 200ms ease;
}

.info-link:hover {
  text-decoration: underline;
}

/* Toast Notification */
.toast {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.5rem;
  border-radius: var(--radius-lg);
  box-shadow: 0 24px 48px -12px rgba(24, 28, 28, 0.12);
  animation: slideInRight 300ms ease;
  z-index: 1000;
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(100px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.toast-success {
  background-color: var(--secondary-container);
  color: var(--on-secondary-container);
}

.toast .material-symbols-outlined {
  font-size: 1.5rem;
}

/* Responsive */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    align-items: flex-start;
  }

  .header-title {
    font-size: 1.875rem;
  }

  .settings-main {
    padding: 1.5rem;
  }

  .settings-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .add-category .form-group {
    grid-template-columns: 1fr;
  }

  .toast {
    bottom: 1rem;
    right: 1rem;
    left: 1rem;
  }
}
</style>
<template>
  <div class="transactions-container">
    <!-- Page Header -->
    <header class="transactions-header">
      <div class="header-content">
        <h1 class="header-title">Transaction History</h1>
        <button @click="showAddModal = true" class="btn btn-primary">
          <span class="material-symbols-outlined">add</span>
          Add Expense
        </button>
      </div>
    </header>

    <!-- Filters Section -->
    <section class="filters-section">
      <div class="filters-container">
        <div class="filter-group">
          <label for="search">Search</label>
          <div class="search-input">
            <span class="material-symbols-outlined">search</span>
            <input
              id="search"
              v-model="search"
              type="text"
              placeholder="Search by description..."
            >
          </div>
        </div>

        <div class="filter-group">
          <label for="category">Category</label>
          <select v-model="categoryFilter" id="category">
            <option value="">All Categories</option>
            <option>Food</option>
            <option>Transport</option>
            <option>Entertainment</option>
            <option>Utilities</option>
            <option>Shopping</option>
            <option>Health</option>
            <option>Other</option>
          </select>
        </div>

        <div class="filter-group">
          <label for="from">From</label>
          <input v-model="dateFrom" id="from" type="date">
        </div>

        <div class="filter-group">
          <label for="to">To</label>
          <input v-model="dateTo" id="to" type="date">
        </div>

        <button v-if="hasFilters" @click="clearFilters" class="btn btn-secondary">
          <span class="material-symbols-outlined">clear_all</span>
          Clear Filters
        </button>
      </div>
    </section>

    <!-- Transactions List -->
    <main class="transactions-main">
      <div class="card">
        <div v-if="filteredExpenses.length === 0" class="empty-state">
          <span class="material-symbols-outlined">inbox</span>
          <h3>No transactions found</h3>
          <p>Try adjusting your filters or add a new expense to get started.</p>
        </div>

        <div v-else class="transactions-table">
          <div class="table-header">
            <div class="col-icon"></div>
            <div class="col-category">Category</div>
            <div class="col-description">Description</div>
            <div class="col-date">Date</div>
            <div class="col-method">Payment Method</div>
            <div class="col-amount">Amount</div>
            <div class="col-actions">Actions</div>
          </div>

          <div
            v-for="expense in filteredExpenses"
            :key="expense._id"
            class="table-row"
          >
            <div class="col-icon">
              <div
                class="icon-circle"
                :style="{ backgroundColor: getCategoryColor(expense.category) }"
              >
                <span class="material-symbols-outlined">{{ getCategoryIcon(expense.category) }}</span>
              </div>
            </div>
            <div class="col-category">{{ expense.category }}</div>
            <div class="col-description">{{ expense.description || '—' }}</div>
            <div class="col-date">{{ formatDate(expense.date) }}</div>
            <div class="col-method">{{ expense.payment_method }}</div>
            <div class="col-amount">
              <span class="amount-badge">-₹{{ expense.amount.toFixed(2) }}</span>
            </div>
            <div class="col-actions">
              <button
                @click="deleteExpense(expense._id)"
                class="action-btn delete-btn"
                title="Delete"
              >
                <span class="material-symbols-outlined">delete</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Add Expense Modal -->
    <AddExpenseModal v-if="showAddModal" @close="showAddModal = false" @expense-added="refreshData" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import AddExpenseModal from '../components/AddExpenseModal.vue'
import axios from 'axios'
import { API_BASE_URL } from '../utils/env.js'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

// Local reactive store data to avoid calling Pinia at module import
const expenses = ref([])

// Reactive state
const search = ref('')
const categoryFilter = ref('')
const dateFrom = ref('')
const dateTo = ref('')
const showAddModal = ref(false)

// Computed properties
const filteredExpenses = computed(() => {
  return expenses.value.filter(exp => {
    const matchesSearch = exp.description?.toLowerCase().includes(search.value.toLowerCase()) ||
                         exp.category?.toLowerCase().includes(search.value.toLowerCase())
    const matchesCategory = !categoryFilter.value || exp.category === categoryFilter.value
    const expDate = exp.date.split('T')[0]
    const matchesDate = (!dateFrom.value || expDate >= dateFrom.value) &&
                       (!dateTo.value || expDate <= dateTo.value)
    return matchesSearch && matchesCategory && matchesDate
  })
})

const hasFilters = computed(() => {
  return search.value || categoryFilter.value || dateFrom.value || dateTo.value
})

const categories = computed(() => {
  return ['Food', 'Transport', 'Entertainment', 'Utilities', 'Shopping', 'Health', 'Other']
})

// Methods
const clearFilters = () => {
  search.value = ''
  categoryFilter.value = ''
  dateFrom.value = ''
  dateTo.value = ''
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

const getCategoryIcon = (category) => {
  const icons = {
    'Food': 'restaurant',
    'Transport': 'directions_car',
    'Entertainment': 'movie',
    'Utilities': 'lightbulb',
    'Shopping': 'shopping_bag',
    'Health': 'favorite',
    'Other': 'category'
  }
  return icons[category] || 'category'
}

const getCategoryColor = (category) => {
  const colors = {
    'Food': '#6c3518',
    'Transport': '#004d4c',
    'Entertainment': '#486363',
    'Utilities': '#6c3518',
    'Shopping': '#004d4c',
    'Health': '#486363',
    'Other': '#6f7978'
  }
  return colors[category] || '#486363'
}

const deleteExpense = async (id) => {
  if (confirm('Are you sure you want to delete this expense?')) {
    try {
      await axios.delete(`${API_BASE_URL}/expenses/${id}`)
      // remove locally
      expenses.value = expenses.value.filter(exp => exp._id !== id)
    } catch (error) {
      console.error('Error deleting expense:', error)
      alert('Failed to delete expense')
    }
  }
}

const refreshData = async () => {
  try {
    const auth = useAuthStore()
    if (!auth || !auth.user || !auth.user._id) {
      const router = useRouter()
      router.push({ name: 'Login' })
      return
    }
    const response = await axios.get(`${API_BASE_URL}/expenses/${auth.user._id}`)
    expenses.value = response.data || []
  } catch (error) {
    console.error('Error refreshing expenses:', error)
  }
}

// Lifecycle hooks
onMounted(async () => {
  try {
    await refreshData()
  } catch (error) {
    expenses.value = []
  }
})
</script>

<style scoped>
.transactions-container {
  min-height: 100vh;
  background-color: var(--background);
}

.transactions-header {
  background-color: rgba(247, 250, 249, 0.7);
  backdrop-filter: blur(20px);
  position: sticky;
  top: 0;
  z-index: 50;
  border-bottom: 1px solid rgba(0, 77, 76, 0.1);
  box-shadow: 0 24px 48px -12px rgba(24, 28, 28, 0.06);
}

.header-content {
  max-width: 1400px;
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

.filters-section {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
  border-bottom: 1px solid rgba(0, 77, 76, 0.05);
}

.filters-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  align-items: flex-end;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filter-group label {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--on-surface);
  text-transform: capitalize;
}

.filter-group input,
.filter-group select {
  padding: 0.75rem 1rem;
  border: 1px solid rgba(0, 77, 76, 0.15);
  border-radius: var(--radius-md);
  background-color: var(--surface-container-low);
  color: var(--on-surface);
  font-family: var(--font-body);
  font-size: 0.95rem;
  transition: all 200ms ease;
}

.filter-group input:focus,
.filter-group select:focus {
  outline: none;
  background-color: var(--surface-container-lowest);
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(0, 77, 76, 0.08);
}

.search-input {
  position: relative;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.search-input .material-symbols-outlined {
  position: absolute;
  left: 0.75rem;
  color: var(--on-surface-variant);
  font-size: 1.25rem;
}

.search-input input {
  padding-left: 2.75rem;
  width: 100%;
}

.transactions-main {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

.card {
  background-color: var(--surface-container-lowest);
  border-radius: var(--radius-lg);
  box-shadow: 0 24px 48px -12px rgba(24, 28, 28, 0.06);
  border: 1px solid rgba(0, 77, 76, 0.1);
  overflow: hidden;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  padding: 4rem 2rem;
  color: var(--on-surface-variant);
  text-align: center;
}

.empty-state .material-symbols-outlined {
  font-size: 4rem;
  opacity: 0.3;
}

.empty-state h3 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
}

.empty-state p {
  margin: 0;
  font-size: 0.95rem;
}

.transactions-table {
  display: flex;
  flex-direction: column;
}

.table-header {
  display: grid;
  grid-template-columns: 50px 100px 150px 120px 150px 120px 80px;
  gap: 1rem;
  padding: 1.5rem 2rem;
  background-color: var(--surface-container-high);
  font-weight: 600;
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--on-surface-variant);
  border-bottom: 1px solid rgba(0, 77, 76, 0.1);
  position: sticky;
  top: 0;
}

.table-row {
  display: grid;
  grid-template-columns: 50px 100px 150px 120px 150px 120px 80px;
  gap: 1rem;
  padding: 1.5rem 2rem;
  align-items: center;
  border-bottom: 1px solid rgba(0, 77, 76, 0.05);
  transition: background-color 200ms ease;
}

.table-row:hover {
  background-color: var(--surface-container-low);
}

.col-icon {
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-circle {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1rem;
}

.col-category {
  font-weight: 600;
  color: var(--on-surface);
}

.col-description {
  color: var(--on-surface-variant);
  font-size: 0.95rem;
}

.col-date {
  color: var(--on-surface-variant);
  font-size: 0.95rem;
}

.col-method {
  font-size: 0.875rem;
  background-color: var(--surface-container-high);
  padding: 0.25rem 0.75rem;
  border-radius: var(--radius-full);
  display: inline-block;
  width: fit-content;
}

.col-amount {
  text-align: right;
}

.amount-badge {
  font-weight: 700;
  color: var(--on-surface);
  font-size: 1rem;
}

.col-actions {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
}

.action-btn {
  padding: 0.5rem;
  background: none;
  border: none;
  cursor: pointer;
  border-radius: var(--radius-md);
  transition: all 200ms ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-btn:hover {
  background-color: var(--surface-container-high);
}

.delete-btn .material-symbols-outlined {
  color: var(--error);
  font-size: 1.25rem;
}

/* Responsive */
@media (max-width: 1024px) {
  .table-header,
  .table-row {
    grid-template-columns: 50px 100px 1fr 100px 80px;
  }

  .col-date,
  .col-method {
    display: none;
  }
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    align-items: flex-start;
  }

  .filters-container {
    grid-template-columns: 1fr;
  }

  .table-header,
  .table-row {
    grid-template-columns: 50px 1fr 80px;
    gap: 0.75rem;
  }

  .col-category,
  .col-description,
  .col-date,
  .col-method {
    display: none;
  }

  .col-amount {
    text-align: left;
  }

  .transactions-table {
    gap: 0.5rem;
  }
}
</style>
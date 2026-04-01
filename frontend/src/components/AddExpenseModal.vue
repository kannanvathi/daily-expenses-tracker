<template>
  <div class="modal-overlay" @click="closeModal">
    <div class="modal" @click.stop>
      <div class="modal-header">
        <h2>Add New Expense</h2>
        <button class="close-btn" @click="closeModal">
          <span class="material-symbols-outlined">close</span>
        </button>
      </div>

      <form @submit.prevent="submitExpense" class="modal-form">
        <!-- Amount Input -->
        <div class="form-group">
          <label for="amount">Amount (₹)</label>
          <input
            id="amount"
            v-model="expense.amount"
            type="number"
            step="0.01"
            placeholder="Enter amount"
            required
          >
        </div>

        <!-- Category Select -->
        <div class="form-group">
          <label for="category">Category</label>
          <select v-model="expense.category" id="category" required>
            <option value="">Select a category</option>
            <option>Food</option>
            <option>Transport</option>
            <option>Entertainment</option>
            <option>Utilities</option>
            <option>Shopping</option>
            <option>Health</option>
            <option>Other</option>
          </select>
        </div>

        <!-- Date Input -->
        <div class="form-group">
          <label for="date">Date</label>
          <input
            id="date"
            v-model="expense.date"
            type="date"
            required
          >
        </div>

        <!-- Description Input -->
        <div class="form-group">
          <label for="description">Description (Optional)</label>
          <input
            id="description"
            v-model="expense.description"
            type="text"
            placeholder="Add notes..."
          >
        </div>

        <!-- Payment Method Select -->
        <div class="form-group">
          <label for="method">Payment Method</label>
          <select v-model="expense.payment_method" id="method" required>
            <option value="">Select payment method</option>
            <option value="Cash">Cash</option>
            <option value="Credit Card">Credit Card</option>
            <option value="Debit Card">Debit Card</option>
            <option value="Bank Transfer">Bank Transfer</option>
            <option value="Digital Wallet">Digital Wallet</option>
          </select>
        </div>

        <!-- Form Actions -->
        <div class="form-actions">
          <button type="button" class="btn btn-secondary" @click="closeModal">
            Cancel
          </button>
          <button type="submit" class="btn btn-primary" :disabled="isSubmitting">
            <span v-if="!isSubmitting" class="material-symbols-outlined">check</span>
            <span v-if="!isSubmitting">Add Expense</span>
            <span v-else>Saving...</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useCategoriesStore } from '../stores/categories'
import { useExpensesStore } from '../stores/expenses'
import { useAuthStore } from '../stores/auth'
const emit = defineEmits(['close', 'expense-added'])

// Reactive state
const expense = ref({
  user_id: '',
  amount: '',
  category: '',
  date: new Date().toISOString().split('T')[0],
  description: '',
  payment_method: ''
})
const isSubmitting = ref(false)

// Reactive properties
const categories = ref([])

// Methods
const loadCategories = async () => {
  try {
    const categoriesStore = useCategoriesStore()
    await categoriesStore.loadCategories()
    categories.value = categoriesStore.getAllCategories
  } catch (error) {
    console.error('Error loading categories:', error)
    categories.value = []
  }
}

const submitExpense = async () => {
  if (!expense.value.amount || !expense.value.category || !expense.value.date) {
    alert('Please fill in all required fields')
    return
  }

  isSubmitting.value = true
  try {
    const expenseData = {
      user_id: expense.value.user_id,
      amount: parseFloat(expense.value.amount),
      category: expense.value.category,
      date: expense.value.date,
      description: expense.value.description,
      payment_method: expense.value.payment_method
    }

    const expensesStore = useExpensesStore()
    await expensesStore.addExpense(expenseData)
    emit('expense-added')
    closeModal()
  } catch (error) {
    console.error('Error adding expense:', error)
    alert('Failed to add expense. Please try again.')
  } finally {
    isSubmitting.value = false
  }
}

const closeModal = () => {
  resetForm()
  emit('close')
}

const resetForm = () => {
  const auth = useAuthStore()
  expense.value = {
    user_id: auth.user && auth.user._id ? auth.user._id : '',
    amount: '',
    category: '',
    date: new Date().toISOString().split('T')[0],
    description: '',
    payment_method: ''
  }
}

// Lifecycle hooks
onMounted(() => {
  const auth = useAuthStore()
  if (auth && auth.user && auth.user._id) {
    expense.value.user_id = auth.user._id
  }
  loadCategories()
})
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background-color: rgba(24, 28, 28, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 200ms ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.modal {
  background-color: var(--surface-container-lowest);
  border-radius: var(--radius-lg);
  width: 90%;
  max-width: 500px;
  box-shadow: 0 24px 48px -12px rgba(24, 28, 28, 0.12);
  animation: slideUp 300ms ease;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 2rem;
  border-bottom: 1px solid rgba(0, 77, 76, 0.1);
}

.modal-header h2 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 700;
  letter-spacing: -0.02em;
}

.close-btn {
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

.close-btn:hover {
  background-color: var(--surface-container-high);
}

.close-btn .material-symbols-outlined {
  color: var(--on-surface-variant);
}

.modal-form {
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--on-surface);
  text-transform: capitalize;
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

.form-group input::placeholder {
  color: var(--on-surface-variant);
  opacity: 0.6;
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.form-actions .btn {
  flex: 1;
  padding: 0.875rem 1.5rem;
  font-size: 1rem;
}

.form-actions .btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Responsive */
@media (max-width: 640px) {
  .modal {
    width: 95%;
    max-width: none;
  }

  .modal-header {
    padding: 1.5rem;
  }

  .modal-form {
    padding: 1.5rem;
  }

  .form-actions {
    flex-direction: column;
  }
}
</style>

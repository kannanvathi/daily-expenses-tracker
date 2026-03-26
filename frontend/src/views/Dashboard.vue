<template>
  <div class="dashboard-container">
    <!-- Sticky Header with Glassmorphism -->
    <header class="dashboard-header">
      <div class="header-content">
        <h1 class="header-title">Expenditure Summary</h1>
        <div class="header-actions">
          <button @click="refreshData" class="btn btn-secondary">
            <span class="material-symbols-outlined">refresh</span>
            Refresh
          </button>
          <button @click="showAddModal = true" class="btn btn-primary">
            <span class="material-symbols-outlined">add</span>
            Add Expense
          </button>
        </div>
      </div>
    </header>

    <!-- Main Content Bento Grid -->
    <main class="dashboard-main">
      <div class="bento-grid">
        <!-- Monthly Summary Card (Left - 1/3) -->
        <div class="bento-one-third">
          <div class="card summary-card">
            <div class="summary-header">
              <h2>Budget Overview</h2>
              <span class="material-symbols-outlined text-primary">account_balance_wallet</span>
            </div>
            
            <div class="summary-content">
              <div class="metric">
                <span class="metric-label">Total Spent</span>
                <span class="metric-value text-primary">₹{{ totalSpent.toFixed(2) }}</span>
              </div>
              
              <div class="metric">
                <span class="metric-label">Remaining</span>
                <span class="metric-value text-secondary">₹{{ budgetRemaining.toFixed(2) }}</span>
              </div>

              <div class="progress-section">
                <span class="progress-label">Monthly Budget: ₹{{ monthlyBudget }}</span>
                <div class="progress-bar">
                  <div class="progress-fill" :style="{ width: progressPercent + '%' }"></div>
                </div>
                <span class="progress-percent">{{ progressPercent.toFixed(0) }}% used</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Mini Chart (Right - 2/3) -->
        <div class="bento-two-thirds">
          <div class="card">
            <div class="chart-header">
              <h3>7-Day Spending Trend</h3>
              <span class="material-symbols-outlined">trending_up</span>
            </div>
            <div class="mini-chart">
              <div class="chart-container">
                <div
                  v-for="(day, index) in last7Days"
                  :key="index"
                  class="chart-day"
                >
                  <div
                    class="chart-bar"
                    :style="{ height: getBarHeight(day.amount) + '%' }"
                    :title="`${day.date}: ₹${day.amount.toFixed(2)}`"
                  ></div>
                  <span class="chart-day-label">{{ day.label }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Recent Activity (Full width at bottom) -->
        <div class="bento-full">
          <div class="card">
            <div class="activity-header">
              <h3>Recent Transactions</h3>
              <router-link to="/transactions" class="link-more">
                View All <span class="material-symbols-outlined">arrow_forward</span>
              </router-link>
            </div>
            
            <div class="activity-list">
              <div v-if="recentExpenses.length === 0" class="empty-state">
                <span class="material-symbols-outlined">receipt_long</span>
                <p>No expenses yet. Add one to get started!</p>
              </div>
              
              <div v-for="expense in recentExpenses.slice(0, 5)" :key="expense._id" class="transaction-item">
                <div class="transaction-left">
                  <div 
                    class="transaction-icon"
                    :style="{ backgroundColor: getCategoryColor(expense.category) }"
                  >
                    <span class="material-symbols-outlined">{{ getCategoryIcon(expense.category) }}</span>
                  </div>
                  <div class="transaction-info">
                    <span class="transaction-category">{{ expense.category }}</span>
                    <span class="transaction-date">{{ formatDate(expense.date) }}</span>
                  </div>
                </div>
                <span class="transaction-amount">-₹{{ expense.amount.toFixed(2) }}</span>
              </div>
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
import { ref, computed, onMounted, onUnmounted } from 'vue'
import AddExpenseModal from '../components/AddExpenseModal.vue'
import axios from 'axios'
import { API_BASE_URL } from '../utils/env.js'

// Pinia store will be accessed inside lifecycle/hooks to avoid early import

// Reactive state
const showAddModal = ref(false)
const totalSpent = ref(0)
const budgetRemaining = ref(0)
const monthlyBudget = ref(5000)
const last7Days = ref([])
const recentExpenses = ref([])
const maxAmount = ref(0)
const interval = ref(null)

// Computed properties
const progressPercent = computed(() => {
  return (totalSpent.value / monthlyBudget.value) * 100
})

// Methods
const loadDashboardData = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/expenses/default-user`)
    const expenses = response.data || []

    // Calculate total spent
    totalSpent.value = expenses.reduce((sum, exp) => sum + exp.amount, 0)
    budgetRemaining.value = Math.max(0, monthlyBudget.value - totalSpent.value)

    // Sort by date descending
    recentExpenses.value = [...expenses].sort((a, b) => new Date(b.date) - new Date(a.date))

    // Calculate 7-day trend
    calculateLast7Days(expenses)
  } catch (error) {
    console.error('Error loading dashboard data:', error)
    recentExpenses.value = []
  }
}

const calculateLast7Days = (expenses) => {
  const days = []
  const dayLabels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

  for (let i = 6; i >= 0; i--) {
    const date = new Date()
    date.setDate(date.getDate() - i)
    const dateStr = date.toISOString().split('T')[0]

    const dayExpenses = expenses.filter(exp => exp.date.split('T')[0] === dateStr)
    const amount = dayExpenses.reduce((sum, exp) => sum + exp.amount, 0)

    days.push({
      date: dateStr,
      label: dayLabels[date.getDay()],
      amount: amount
    })
  }

  last7Days.value = days
  maxAmount.value = Math.max(...days.map(d => d.amount), 1)
}

const getBarHeight = (amount) => {
  return maxAmount.value > 0 ? (amount / maxAmount.value) * 100 : 0
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
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

const refreshData = async () => {
  await loadDashboardData()
}

// Lifecycle hooks
onMounted(async () => {
  // Fetch data directly so we don't depend on Pinia during initial render
  await loadDashboardData()
  // Refresh every 30 seconds
  interval.value = setInterval(() => loadDashboardData(), 30000)
})

onUnmounted(() => {
  clearInterval(interval.value)
})
</script>

<style scoped>
.dashboard-container {
  min-height: 100vh;
  background-color: var(--background);
}

.dashboard-header {
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
  padding: 2rem 2rem;
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
  color: var(--on-surface);
}

.header-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.dashboard-main {
  max-width: 1400px;
  margin: 0 auto;
  padding: 3rem 2rem;
}

.bento-grid {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 2rem;
}

.bento-one-third {
  grid-column: span 12;
}

.bento-two-thirds {
  grid-column: span 12;
}

.bento-full {
  grid-column: span 12;
}

@media (min-width: 768px) {
  .bento-one-third {
    grid-column: span 4;
  }

  .bento-two-thirds {
    grid-column: span 8;
  }
}

/* Summary Card */
.summary-card {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.summary-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.summary-header h2 {
  margin: 0;
  font-size: 1.375rem;
  font-weight: 700;
}

.summary-header .material-symbols-outlined {
  font-size: 2rem;
  color: var(--primary);
}

.summary-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.metric {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.metric-label {
  font-size: 0.875rem;
  color: var(--on-surface-variant);
  font-weight: 500;
}

.metric-value {
  font-size: 1.75rem;
  font-weight: 700;
  letter-spacing: -0.02em;
}

.progress-section {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-top: 0.5rem;
}

.progress-label {
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--on-surface-variant);
}

.progress-bar {
  height: 8px;
  background-color: var(--surface-container-high);
  border-radius: var(--radius-full);
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-container) 100%);
  border-radius: var(--radius-full);
  transition: width 300ms ease;
}

.progress-percent {
  font-size: 0.75rem;
  color: var(--on-surface-variant);
  text-align: right;
}

/* Chart */
.chart-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
}

.chart-header h3 {
  margin: 0;
  font-size: 1.375rem;
  font-weight: 700;
}

.chart-header .material-symbols-outlined {
  color: var(--primary);
  font-size: 2rem;
}

.mini-chart {
  padding: 1rem 0;
}

.chart-container {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 0.75rem;
  height: 200px;
}

.chart-day {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
}

.chart-bar {
  width: 100%;
  background: linear-gradient(180deg, var(--primary) 0%, var(--primary-container) 100%);
  border-radius: var(--radius-md) var(--radius-md) 0 0;
  transition: all 200ms ease;
  cursor: pointer;
  min-height: 4px;
}

.chart-bar:hover {
  opacity: 0.8;
  transform: translateY(-2px);
}

.chart-day-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--on-surface-variant);
}

/* Activity */
.activity-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
}

.activity-header h3 {
  margin: 0;
  font-size: 1.375rem;
  font-weight: 700;
}

.link-more {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--primary);
  text-decoration: none;
  font-weight: 600;
  transition: all 200ms ease;
}

.link-more:hover {
  gap: 0.75rem;
}

.link-more .material-symbols-outlined {
  font-size: 1.25rem;
}

.activity-list {
  display: flex;
  flex-direction: column;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  padding: 3rem 2rem;
  color: var(--on-surface-variant);
  text-align: center;
}

.empty-state .material-symbols-outlined {
  font-size: 3rem;
  opacity: 0.5;
}

.empty-state p {
  margin: 0;
  font-size: 0.875rem;
}

.transaction-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  margin: 0 -2rem;
  padding-left: 2rem;
  padding-right: 2rem;
  border-radius: var(--radius-md);
  transition: background-color 200ms ease;
}

.transaction-item:hover {
  background-color: var(--surface-container-low);
}

.transaction-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.transaction-icon {
  width: 3rem;
  height: 3rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.25rem;
  transition: transform 200ms ease;
}

.transaction-item:hover .transaction-icon {
  transform: scale(1.1);
}

.transaction-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.transaction-category {
  font-weight: 600;
  color: var(--on-surface);
  font-size: 0.95rem;
}

.transaction-date {
  font-size: 0.75rem;
  color: var(--on-surface-variant);
}

.transaction-amount {
  font-weight: 700;
  font-size: 1.1rem;
  color: var(--on-surface);
}

/* Responsive */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .header-title {
    font-size: 1.875rem;
  }

  .header-actions {
    width: 100%;
    flex-direction: column;
  }

  .header-actions button {
    width: 100%;
  }

  .dashboard-main {
    padding: 1.5rem 1rem;
  }

  .bento-grid {
    gap: 1.5rem;
  }
}
</style>
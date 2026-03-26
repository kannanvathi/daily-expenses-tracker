<template>
  <div class="reports-container">
    <!-- Page Header -->
    <header class="reports-header">
      <div class="header-content">
        <h1 class="header-title">Budgets & Reports</h1>
        <button @click="refreshData" class="btn btn-secondary">
          <span class="material-symbols-outlined">refresh</span>
          Refresh
        </button>
      </div>
    </header>

    <!-- Reports Content -->
    <main class="reports-main">
      <div class="reports-grid">
        <!-- Budget Overview Card -->
        <div class="report-card">
          <div class="card-header">
            <h2>Budget Overview</h2>
            <span class="material-symbols-outlined">wallet</span>
          </div>
          
          <div class="budget-list">
            <div class="budget-item" v-for="(category, index) in budgetCategories" :key="index">
              <div class="budget-header">
                <span class="category-name">{{ category.name }}</span>
                <span class="category-amount">₹{{ category.spent.toFixed(2) }} / ₹{{ category.budget }}</span>
              </div>
              <div class="progress-bar">
                <div class="progress-fill" :style="{ width: Math.min(100, (category.spent / category.budget) * 100) + '%' }"></div>
              </div>
              <div class="progress-info">
                <span class="progress-percent">{{ Math.min(100, ((category.spent / category.budget) * 100)).toFixed(0) }}%</span>
                <span class="remaining" :class="{ over: category.spent > category.budget }">
                  {{ category.spent > category.budget ? 'Over by' : 'Remaining' }} ₹{{ Math.abs(category.budget - category.spent).toFixed(2) }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- Category Distribution -->
        <div class="report-card">
          <div class="card-header">
            <h2>Spending Distribution</h2>
            <span class="material-symbols-outlined">donut_large</span>
          </div>
          
          <div class="category-stats">
            <div class="stat-item" v-for="(stat, index) in categoryStats" :key="index">
              <div class="stat-color" :style="{ backgroundColor: stat.color }"></div>
              <div class="stat-info">
                <span class="stat-label">{{ stat.category }}</span>
                <span class="stat-value">₹{{ stat.amount.toFixed(2) }}</span>
              </div>
              <span class="stat-percent">{{ stat.percent.toFixed(1) }}%</span>
            </div>
          </div>
        </div>

        <!-- Monthly Trends (Full width) -->
        <div class="report-card full-width">
          <div class="card-header">
            <h2>Monthly Spending Trend</h2>
            <span class="material-symbols-outlined">trending_up</span>
          </div>
          
          <div class="trend-chart">
            <div class="chart-container">
              <div
                v-for="(month, index) in monthlyTrend"
                :key="index"
                class="month-item"
              >
                <div class="month-bar-container">
                  <div
                    class="month-bar"
                    :style="{ height: getMonthBarHeight(month.amount) + '%' }"
                    :title="`${month.month}: ₹${month.amount.toFixed(2)}`"
                  ></div>
                </div>
                <span class="month-label">{{ month.monthShort }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Top Expenses -->
        <div class="report-card">
          <div class="card-header">
            <h2>Top Expenses</h2>
            <span class="material-symbols-outlined">trending_down</span>
          </div>
          
          <div class="top-expenses-list">
            <div v-if="topExpenses.length === 0" class="empty-state">
              <p>No expenses to display</p>
            </div>
            <div v-for="(expense, index) in topExpenses.slice(0, 5)" :key="index" class="expense-item">
              <div class="expense-rank">{{ index + 1 }}</div>
              <div class="expense-info">
                <span class="expense-category">{{ expense.category }}</span>
                <span class="expense-description">{{ expense.description || '—' }}</span>
              </div>
              <span class="expense-amount">₹{{ expense.amount.toFixed(2) }}</span>
            </div>
          </div>
        </div>

        <!-- Summary Stats -->
        <div class="report-card">
          <div class="card-header">
            <h2>Summary</h2>
            <span class="material-symbols-outlined">summary</span>
          </div>
          
          <div class="summary-stats">
            <div class="summary-item">
              <span class="summary-label">Total Spent</span>
              <span class="summary-value">₹{{ totalSpent.toFixed(2) }}</span>
            </div>
            <div class="summary-item">
              <span class="summary-label">Transactions</span>
              <span class="summary-value">{{ totalTransactions }}</span>
            </div>
            <div class="summary-item">
              <span class="summary-label">Avg. Transaction</span>
              <span class="summary-value">₹{{ avgTransaction.toFixed(2) }}</span>
            </div>
            <div class="summary-item">
              <span class="summary-label">Top Category</span>
              <span class="summary-value">{{ topCategory || '—' }}</span>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';
import { API_BASE_URL } from '../utils/env.js';

const expenses = ref([]);
const budgetCategories = ref([
  { name: 'Food', budget: 3000, spent: 0 },
  { name: 'Transport', budget: 2000, spent: 0 },
  { name: 'Entertainment', budget: 1500, spent: 0 },
  { name: 'Utilities', budget: 1000, spent: 0 },
  { name: 'Shopping', budget: 2000, spent: 0 },
  { name: 'Health', budget: 500, spent: 0 },
]);
const monthlyBudget = ref(5000);
const maxMonthlyAmount = ref(0);

const categoryStats = computed(() => {
  const stats = {};
  expenses.value.forEach(exp => {
    if (!stats[exp.category]) stats[exp.category] = 0;
    stats[exp.category] += exp.amount;
  });

  const total = totalSpent.value || 1;
  const colors = {
    'Food': '#6c3518',
    'Transport': '#004d4c',
    'Entertainment': '#486363',
    'Utilities': '#6c3518',
    'Shopping': '#004d4c',
    'Health': '#486363',
    'Other': '#6f7978'
  };

  return Object.entries(stats)
    .map(([category, amount]) => ({
      category,
      amount,
      percent: (amount / total) * 100,
      color: colors[category] || '#6f7978'
    }))
    .sort((a, b) => b.amount - a.amount);
});

const monthlyTrend = computed(() => {
  const months = [];
  for (let i = 5; i >= 0; i--) {
    const date = new Date();
    date.setMonth(date.getMonth() - i);
    const monthKey = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;

    const monthExpenses = expenses.value.filter(exp => {
      const expMonth = exp.date.substring(0, 7);
      return expMonth === monthKey;
    });

    const amount = monthExpenses.reduce((sum, exp) => sum + exp.amount, 0);
    months.push({
      month: date.toLocaleString('en-US', { month: 'long', year: 'numeric' }),
      monthShort: date.toLocaleString('en-US', { month: 'short' }),
      amount
    });
  }
  return months;
});

const topExpenses = computed(() => expenses.value.slice().sort((a, b) => b.amount - a.amount));
const totalSpent = computed(() => expenses.value.reduce((sum, exp) => sum + exp.amount, 0));
const totalTransactions = computed(() => expenses.value.length);
const avgTransaction = computed(() => (totalTransactions.value > 0 ? totalSpent.value / totalTransactions.value : 0));
const topCategory = computed(() => (categoryStats.value.length === 0 ? '' : categoryStats.value[0].category));

async function loadReports() {
  try {
    const response = await axios.get(`${API_BASE_URL}/expenses/default-user`);
    expenses.value = response.data;

    // Update budget tracking with actual data
    budgetCategories.value.forEach(budget => {
      const categoryExpenses = expenses.value.filter(exp => exp.category === budget.name);
      budget.spent = categoryExpenses.reduce((sum, exp) => sum + exp.amount, 0);
    });

    // Calculate max for trend chart
    const amounts = monthlyTrend.value.map(m => m.amount);
    maxMonthlyAmount.value = Math.max(...amounts, 1);
  } catch (error) {
    console.error('Error loading reports:', error);
  }
}

function getMonthBarHeight(amount) {
  return maxMonthlyAmount.value > 0 ? (amount / maxMonthlyAmount.value) * 100 : 0;
}

async function refreshData() {
  await loadReports();
}

onMounted(() => {
  loadReports();
});
</script>

<style scoped>
.reports-container {
  min-height: 100vh;
  background-color: var(--background);
}

.reports-header {
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

.reports-main {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

.reports-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.full-width {
  grid-column: 1 / -1;
}

.report-card {
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

/* Budget Items */
.budget-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.budget-item {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.budget-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.category-name {
  font-weight: 600;
  color: var(--on-surface);
}

.category-amount {
  font-size: 0.875rem;
  color: var(--on-surface-variant);
}

.progress-bar {
  height: 6px;
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

.progress-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.75rem;
}

.progress-percent {
  font-weight: 700;
  color: var(--primary);
}

.remaining {
  color: var(--on-surface-variant);
}

.remaining.over {
  color: var(--error);
}

/* Category Stats */
.category-stats {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem;
  border-radius: var(--radius-md);
  background-color: var(--surface-container-low);
  transition: all 200ms ease;
}

.stat-item:hover {
  background-color: var(--surface-container);
}

.stat-color {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  flex-shrink: 0;
}

.stat-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.stat-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--on-surface);
}

.stat-value {
  font-size: 0.75rem;
  color: var(--on-surface-variant);
}

.stat-percent {
  font-weight: 700;
  color: var(--on-surface);
  min-width: 40px;
  text-align: right;
}

/* Trend Chart */
.trend-chart {
  padding: 1.5rem 0;
}

.chart-container {
  display: flex;
  align-items: flex-end;
  justify-content: space-around;
  gap: 0.75rem;
  height: 250px;
  padding: 0 1rem;
}

.month-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
}

.month-bar-container {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: flex-end;
  justify-content: center;
}

.month-bar {
  width: 100%;
  max-width: 40px;
  background: linear-gradient(180deg, var(--primary) 0%, var(--primary-container) 100%);
  border-radius: var(--radius-md) var(--radius-md) 0 0;
  transition: all 200ms ease;
  cursor: pointer;
  min-height: 4px;
}

.month-bar:hover {
  opacity: 0.8;
  transform: translateY(-2px);
}

.month-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--on-surface-variant);
}

/* Top Expenses */
.top-expenses-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.empty-state {
  text-align: center;
  padding: 2rem 1rem;
  color: var(--on-surface-variant);
}

.expense-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem;
  border-radius: var(--radius-md);
  background-color: var(--surface-container-low);
  transition: all 200ms ease;
}

.expense-item:hover {
  background-color: var(--surface-container);
}

.expense-rank {
  font-weight: 700;
  font-size: 1.25rem;
  color: var(--primary);
  min-width: 2rem;
  text-align: center;
}

.expense-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.expense-category {
  font-weight: 600;
  color: var(--on-surface);
  font-size: 0.875rem;
}

.expense-description {
  font-size: 0.75rem;
  color: var(--on-surface-variant);
}

.expense-amount {
  font-weight: 700;
  color: var(--on-surface);
}

/* Summary Stats */
.summary-stats {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.summary-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 1rem;
  background-color: var(--surface-container-low);
  border-radius: var(--radius-md);
  text-align: center;
}

.summary-label {
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--on-surface-variant);
}

.summary-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--primary);
}

/* Responsive */
@media (max-width: 768px) {
  .reports-main {
    padding: 1.5rem;
  }

  .reports-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .chart-container {
    height: 200px;
  }

  .header-content {
    flex-direction: column;
    align-items: flex-start;
  }

  .header-title {
    font-size: 1.875rem;
  }
}
</style>
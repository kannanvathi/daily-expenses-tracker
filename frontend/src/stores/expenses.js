import { defineStore } from 'pinia'
import axios from 'axios'
import { API_BASE_URL } from '../utils/env.js'

export const useExpensesStore = defineStore('expenses', {
  state: () => ({
    expenses: [],
    loading: false,
    error: null
  }),

  getters: {
    // Get all expenses
    getAllExpenses: (state) => state.expenses,

    // Get expenses sorted by date (newest first)
    getSortedExpenses: (state) => {
      return [...state.expenses].sort((a, b) => new Date(b.date) - new Date(a.date))
    },

    // Get expense by ID
    getExpenseById: (state) => (id) => {
      return state.expenses.find(expense => expense._id === id)
    },

    // Get total expenses count
    getExpensesCount: (state) => state.expenses.length
  },

  actions: {
    // Load all expenses
    async loadExpenses() {
      this.loading = true
      this.error = null

      try {
        const response = await axios.get(`${API_BASE_URL}/expenses/default-user`)
        this.expenses = response.data
      } catch (error) {
        this.error = 'Failed to load expenses'
        console.error('Error loading expenses:', error)
      } finally {
        this.loading = false
      }
    },

    // Add a new expense
    async addExpense(expenseData) {
      this.loading = true
      this.error = null

      try {
        await axios.post(`${API_BASE_URL}/expenses`, expenseData)
        // Reload expenses after adding
        await this.loadExpenses()
      } catch (error) {
        this.error = 'Failed to add expense'
        console.error('Error adding expense:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    // Delete an expense
    async deleteExpense(id) {
      this.loading = true
      this.error = null

      try {
        await axios.delete(`${API_BASE_URL}/expenses/${id}`)
        // Remove from local state
        this.expenses = this.expenses.filter(expense => expense._id !== id)
      } catch (error) {
        this.error = 'Failed to delete expense'
        console.error('Error deleting expense:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    // Clear all expenses
    clearExpenses() {
      this.expenses = []
    }
  }
})

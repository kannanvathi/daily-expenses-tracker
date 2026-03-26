import { defineStore } from 'pinia'
import axios from 'axios'
import { API_BASE_URL } from '../utils/env.js'

export const useSettingsStore = defineStore('settings', {
  state: () => ({
    settings: {
      currency: 'INR',
      monthlyBudget: 0,
      theme: 'light',
      notifications: true
    },
    loading: false,
    error: null
  }),

  getters: {
    // Get all settings
    getSettings: (state) => state.settings,

    // Get specific setting by key
    getSetting: (state) => (key) => {
      return state.settings[key]
    },

    // Get monthly budget
    getMonthlyBudget: (state) => state.settings.monthlyBudget,

    // Get currency
    getCurrency: (state) => state.settings.currency
  },

  actions: {
    // Load settings
    async loadSettings() {
      this.loading = true
      this.error = null

      try {
        const response = await axios.get(`${API_BASE_URL}/settings/default-user`)
        this.settings = response.data
      } catch (error) {
        // If no settings exist, use default settings
        this.error = 'No settings found, using defaults'
        console.warn('No settings found, using defaults:', error)
      } finally {
        this.loading = false
      }
    },

    // Update settings
    async updateSettings(newSettings) {
      this.loading = true
      this.error = null

      try {
        await axios.put(`${API_BASE_URL}/settings/default-user`, newSettings)
        this.settings = { ...this.settings, ...newSettings }
      } catch (error) {
        this.error = 'Failed to update settings'
        console.error('Error updating settings:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    // Set monthly budget
    async setMonthlyBudget(budget) {
      await this.updateSettings({ monthlyBudget: budget })
    },

    // Set currency
    async setCurrency(currency) {
      await this.updateSettings({ currency })
    },

    // Reset settings to defaults
    resetSettings() {
      this.settings = {
        currency: 'INR',
        monthlyBudget: 0,
        theme: 'light',
        notifications: true
      }
    }
  }
})

import { defineStore } from "pinia";
import axios from "axios";
import { API_BASE_URL } from "../utils/env.js";
import { useAuthStore } from "./auth";

export const useCategoriesStore = defineStore("categories", {
  state: () => ({
    categories: [],
    loading: false,
    error: null,
  }),

  getters: {
    // Get all categories
    getAllCategories: (state) => state.categories,

    // Get category by name
    getCategoryByName: (state) => (name) => {
      return state.categories.find((category) => category.name === name);
    },

    // Get categories count
    getCategoriesCount: (state) => state.categories.length,
  },

  actions: {
    // Load all categories
    async loadCategories() {
      this.loading = true;
      this.error = null;

      try {
        const auth = useAuthStore();
        if (!auth || !auth.user || !auth.user._id) {
          throw new Error("Not authenticated");
        }
        const response = await axios.get(
          `${API_BASE_URL}/categories/${auth.user._id}`,
        );
        this.categories = response.data;
      } catch (error) {
        this.error = "Failed to load categories";
        console.error("Error loading categories:", error);
      } finally {
        this.loading = false;
      }
    },

    // Add a new category
    async addCategory(categoryData) {
      this.loading = true;
      this.error = null;

      try {
        await axios.post(`${API_BASE_URL}/categories`, categoryData);
        // Reload categories after adding
        await this.loadCategories();
      } catch (error) {
        this.error = "Failed to add category";
        console.error("Error adding category:", error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    // Delete a category
    async deleteCategory(id) {
      this.loading = true;
      this.error = null;

      try {
        await axios.delete(`${API_BASE_URL}/categories/${id}`);
        // Remove from local state
        this.categories = this.categories.filter(
          (category) => category._id !== id,
        );
      } catch (error) {
        this.error = "Failed to delete category";
        console.error("Error deleting category:", error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    // Clear all categories
    clearCategories() {
      this.categories = [];
    },
  },
});

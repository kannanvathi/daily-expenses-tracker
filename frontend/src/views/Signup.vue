<template>
  <div class="auth-page">
    <h2>Sign Up</h2>
    <form @submit.prevent="doSignup">
      <div>
        <label>Username</label>
        <input v-model="username" required :disabled="isSubmitting" />
      </div>
      <div>
        <label>Password</label>
        <input v-model="password" type="password" required :disabled="isSubmitting" />
      </div>
      <div>
        <button type="submit" :disabled="isSubmitting">
          {{ isSubmitting ? 'Creating Account...' : 'Create account' }}
        </button>
      </div>
      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>
    </form>
    <p>
      Already have an account? <router-link to="/login">Login</router-link>
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const username = ref('')
const password = ref('')
const errorMessage = ref('')
const isSubmitting = ref(false)
const router = useRouter()
const auth = useAuthStore()

const doSignup = async () => {
  // Reset previous error
  errorMessage.value = ''
  isSubmitting.value = true

  try {
    // First try to register
    await auth.register(username.value, password.value)
    // Then auto-login after successful signup
    await auth.login(username.value, password.value)
    router.push('/')
  } catch (error) {
    // Handle specific error messages
    if (error.response) {
      // Server responded with error status
      const errorData = error.response.data || {}
      
      if (error.response.status === 400) {
        // Check for FastAPI's detail field (username already registered, etc.)
        if (errorData.detail) {
          if (errorData.detail.includes('already registered')) {
            errorMessage.value = 'Username already exists. Please choose a different username.'
          } else {
            errorMessage.value = errorData.detail
          }
        } else if (errorData.message) {
          errorMessage.value = errorData.message
        } else if (errorData.errors) {
          // Handle validation errors
          const errorMessages = []
          Object.values(errorData.errors).forEach(errArray => {
            if (Array.isArray(errArray)) {
              errorMessages.push(...errArray)
            }
          })
          errorMessage.value = errorMessages.length > 0 
            ? errorMessages.join('. ')
            : 'Invalid data provided. Please check your inputs.'
        } else {
          errorMessage.value = 'Invalid data provided. Please check your inputs.'
        }
      } else if (error.response.status === 409) {
        errorMessage.value = 'Username already exists. Please choose a different username.'
      } else {
        errorMessage.value = `Registration failed: ${errorData.detail || errorData.message || error.message}`
      }
    } else if (error.request) {
      // Request was made but no response received
      errorMessage.value = 'No response from server. Please check your connection.'
    } else {
      // Something else happened
      errorMessage.value = `Registration failed: ${error.message}`
    }

    // Log the full error for debugging
    console.error('Signup error:', error)

    // Show the error to the user
    if (!errorMessage.value) {
      errorMessage.value = 'An unknown error occurred during registration.'
    }
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style scoped>
.auth-page { max-width: 420px; margin: 2rem auto; }
label { display:block; margin-bottom: .25rem }
input { width:100%; padding:.5rem; margin-bottom: .75rem }
button { padding:.5rem 1rem }
</style>

<template>
  <div class="auth-page">
    <h2>Login</h2>
    <form @submit.prevent="doLogin">
      <div>
        <label>Username</label>
        <input v-model="username" required />
      </div>
      <div>
        <label>Password</label>
        <input v-model="password" type="password" required />
      </div>
      <div>
        <button type="submit">Login</button>
      </div>
    </form>
    <p>
      Don't have an account? <router-link to="/signup">Sign up</router-link>
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const username = ref('')
const password = ref('')
const router = useRouter()
const auth = useAuthStore()

const doLogin = async () => {
  try {
    await auth.login(username.value, password.value)
    router.push('/')
  } catch (e) {
    alert('Login failed')
    console.error(e)
  }
}
</script>

<style scoped>
.auth-page { max-width: 420px; margin: 2rem auto; }
label { display:block; margin-bottom: .25rem }
input { width:100%; padding:.5rem; margin-bottom: .75rem }
button { padding:.5rem 1rem }
</style>

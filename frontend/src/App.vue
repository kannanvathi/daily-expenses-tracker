<script setup>
import { RouterLink, RouterView, useRouter } from 'vue-router'
import { useAuthStore } from './stores/auth'

const auth = useAuthStore()
const router = useRouter()

function doLogout() {
  auth.logout()
  router.push('/login')
}
</script>

<template>
  <div id="app">
    <!-- Global logout/toast -->
    <div v-if="auth.logoutReason" class="toast toast-warning">
      <span class="material-symbols-outlined">warning</span>
      <span>{{ auth.logoutReason }}</span>
      <button class="toast-close" @click="auth.clearLogoutReason()">✕</button>
    </div>
    <!-- Sticky Navigation Bar -->
    <header class="app-header">
      <nav class="app-nav">
        <div class="nav-logo">
          <span class="material-symbols-outlined logo-icon">wallet</span>
          <span class="logo-text">Expense Tracker</span>
        </div>

        <ul class="nav-links">
          <li>
            <RouterLink to="/" class="nav-link">
              <span class="material-symbols-outlined">dashboard</span>
              <span>Dashboard</span>
            </RouterLink>
          </li>
          <li>
            <RouterLink to="/transactions" class="nav-link">
              <span class="material-symbols-outlined">receipt_long</span>
              <span>Transactions</span>
            </RouterLink>
          </li>
          <li>
            <RouterLink to="/reports" class="nav-link">
              <span class="material-symbols-outlined">assessment</span>
              <span>Reports</span>
            </RouterLink>
          </li>
          <li>
            <RouterLink to="/settings" class="nav-link">
              <span class="material-symbols-outlined">settings</span>
              <span>Settings</span>
            </RouterLink>
          </li>
        </ul>

        <div class="auth-actions">
          <template v-if="!auth.isAuthenticated">
            <RouterLink to="/login" class="nav-link">Login</RouterLink>
            <RouterLink to="/signup" class="nav-link">Sign up</RouterLink>
          </template>
          <template v-else>
            <span class="user-badge">{{ auth.user ? auth.user._id.slice(0,8) : 'me' }}</span>
            <button class="btn-logout" @click="doLogout">Logout</button>
          </template>
        </div>
      </nav>
    </header>

    <!-- Main Content -->
    <main id="main-content">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
#app {
  min-height: 100vh;
  background-color: var(--background);
}

.app-header {
  background-color: rgba(247, 250, 249, 0.7);
  backdrop-filter: blur(20px);
  position: sticky;
  top: 0;
  z-index: 100;
  border-bottom: 1px solid rgba(0, 77, 76, 0.1);
  box-shadow: 0 24px 48px -12px rgba(24, 28, 28, 0.06);
}

.app-nav {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 4rem;
  font-family: var(--font-body);
}

.nav-logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  text-decoration: none;
  color: var(--primary);
  font-weight: 700;
  font-size: 1.25rem;
  letter-spacing: -0.02em;
  transition: all 200ms ease;
}

.nav-logo:hover {
  transform: scale(1.05);
}

.logo-icon {
  font-size: 1.75rem;
}

.nav-links {
  display: flex;
  list-style: none;
  gap: 0.5rem;
  margin: 0;
  padding: 0;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  color: var(--on-surface-variant);
  text-decoration: none;
  font-weight: 500;
  font-size: 0.95rem;
  border-radius: var(--radius-md);
  transition: all 200ms ease;
  white-space: nowrap;
}

.nav-link:hover {
  background-color: var(--surface-container-low);
  color: var(--primary);
}

.nav-link.router-link-active {
  background: linear-gradient(135deg, rgba(0, 77, 76, 0.1) 0%, rgba(0, 103, 102, 0.1) 100%);
  color: var(--primary);
  font-weight: 600;
  border-bottom: 2px solid var(--primary);
}

.nav-link .material-symbols-outlined {
  font-size: 1.25rem;
}

#main-content {
  display: flex;
  flex-direction: column;
}

/* Responsive */
@media (max-width: 768px) {
  .app-nav {
    padding: 0 1rem;
  }

  .logo-text {
    display: none;
  }

  .nav-link span:not(.material-symbols-outlined) {
    display: none;
  }

  .nav-links {
    gap: 0.25rem;
  }

  .nav-link {
    padding: 0.5rem 0.75rem;
  }

  .nav-link .material-symbols-outlined {
    font-size: 1.5rem;
  }

  .app-header {
    position: relative;
  }
}
</style>
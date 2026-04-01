import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "../stores/auth";
import Dashboard from "../views/Dashboard.vue";
import Transactions from "../views/Transactions.vue";
import Reports from "../views/Reports.vue";
import Settings from "../views/Settings.vue";
import Login from "../views/Login.vue";
import Signup from "../views/Signup.vue";

const routes = [
  {
    path: "/",
    name: "Dashboard",
    component: Dashboard,
    meta: { requiresAuth: true },
  },
  {
    path: "/transactions",
    name: "Transactions",
    component: Transactions,
    meta: { requiresAuth: true },
  },
  {
    path: "/reports",
    name: "Reports",
    component: Reports,
    meta: { requiresAuth: true },
  },
  {
    path: "/settings",
    name: "Settings",
    component: Settings,
    meta: { requiresAuth: true },
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
  },
  {
    path: "/signup",
    name: "Signup",
    component: Signup,
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

// simple global guard using localStorage token presence to avoid importing store early
router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some((r) => r.meta && r.meta.requiresAuth);
  if (!requiresAuth) return next();
  const auth = useAuthStore();
  if (!auth.isAuthenticated) {
    // clear any stale token and redirect with reason
    try {
      auth.forceLogout("Session expired");
    } catch (e) {
      auth.logout();
    }
    return next({ name: "Login" });
  }
  return next();
});

export default router;

import { defineStore } from "pinia";
import axios from "axios";
import { API_BASE_URL } from "../utils/env.js";

function parseJwt(token) {
  try {
    const payload = token.split(".")[1];
    const base64 = payload.replace(/-/g, "+").replace(/_/g, "/");
    const json = decodeURIComponent(
      atob(base64)
        .split("")
        .map(function (c) {
          return "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2);
        })
        .join(""),
    );
    return JSON.parse(json);
  } catch (e) {
    return null;
  }
}

export const useAuthStore = defineStore("auth", {
  state: () => ({
    token: localStorage.getItem("token") || null,
    user: JSON.parse(localStorage.getItem("user") || "null"),
    logoutReason: null,
  }),

  getters: {
    isAuthenticated: (state) => {
      if (!state.token) return false;
      try {
        const payload = parseJwt(state.token);
        if (!payload) return false;
        // exp is in seconds since epoch
        const now = Math.floor(Date.now() / 1000);
        return !!payload.exp && payload.exp > now;
      } catch (e) {
        return false;
      }
    },
  },

  actions: {
    setToken(token) {
      this.token = token;
      if (token) {
        localStorage.setItem("token", token);
        axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
        const payload = parseJwt(token);
        if (payload && payload.sub) {
          // store minimal user reference
          this.user = { _id: payload.sub };
          localStorage.setItem("user", JSON.stringify(this.user));
        }
      } else {
        localStorage.removeItem("token");
        delete axios.defaults.headers.common["Authorization"];
        this.user = null;
        localStorage.removeItem("user");
      }
    },

    async register(username, password) {
      // Log the request details for debugging
      console.log("Attempting registration with:", {
        username,
        password: "***",
      });

      // Try the most basic format first
      try {
        console.log("Trying registration with basic credentials");
        const res = await axios.post(`${API_BASE_URL}/auth/register`, {
          username,
          password,
        });
        console.log("Registration successful");
        return res.data;
      } catch (error) {
        // If basic format fails, try with email field
        try {
          console.log("Basic registration failed, trying with email field");
          const res = await axios.post(`${API_BASE_URL}/auth/register`, {
            username,
            password,
            email: `${username}@example.com`,
          });
          console.log("Registration successful with email");
          return res.data;
        } catch (error2) {
          // If email format also fails, enhance the error with more details
          const enhancedError = error2;

          // Add more context to the error
          if (error2.response) {
            enhancedError.response = {
              ...error2.response,
              config: {
                ...error2.response.config,
                data: JSON.parse(error2.response.config.data || "{}"),
              },
            };

            // Try to extract validation errors from the response
            if (error2.response.data && error2.response.data.errors) {
              enhancedError.validationErrors = error2.response.data.errors;
            }
          }

          console.error("All registration attempts failed", enhancedError);
          throw enhancedError;
        }
      }
    },

    async login(username, password) {
      // OAuth2 form-encoded login expected by backend
      const params = new URLSearchParams();
      params.append("username", username);
      params.append("password", password);
      const res = await axios.post(`${API_BASE_URL}/auth/login`, params);
      const token = res.data.access_token;
      this.setToken(token);
      return this.user;
    },

    logout() {
      this.setToken(null);
      this.logoutReason = null;
    },

    forceLogout(reason) {
      // clear token and set a transient reason for UI to show
      this.setToken(null);
      this.logoutReason = reason || "Logged out";
      // auto-clear reason after a few seconds
      setTimeout(() => {
        this.logoutReason = null;
      }, 4000);
    },

    clearLogoutReason() {
      this.logoutReason = null;
    },
  },
});

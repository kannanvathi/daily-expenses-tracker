import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import { createPinia } from "pinia";
import "./styles/design-system.css";
import axios from "axios";
import { API_BASE_URL } from "./utils/env.js";

// Configure axios base URL and restore token if present
axios.defaults.baseURL = API_BASE_URL;
const token = localStorage.getItem("token");
if (token) {
  axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
}

const app = createApp(App);

app.use(createPinia());
app.use(router);

app.mount("#app");

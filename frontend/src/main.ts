import { createApp } from "vue";
import { createPinia } from "pinia";
import { createVuetify } from "./plugins/vuetify";

import App from "./App.vue";
import router from "./router";

// import "./assets/main.css";

const app = createApp(App);

app.use(createPinia());
app.use(router);
app.use(createVuetify());

app.mount("#app");

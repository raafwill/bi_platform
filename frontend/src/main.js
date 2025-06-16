import { createApp } from 'vue';
import './style.css';
import App from './App.vue';
import router from "./router"; // Importa o roteador

const app = createApp(App);

app.use(router);
app.mount("#app");
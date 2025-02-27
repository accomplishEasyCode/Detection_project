
import { createApp } from "vue";
import App from "./App.vue";
import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
import axios from "axios";

const app = createApp(App);

// 全局挂载axios
// axios.defaults.baseURL = '/api'; // 设置后端 API 的基础路径
app.config.globalProperties.$axios = axios;

app.use(ElementPlus);
app.mount("#app");

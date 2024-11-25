import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import axios from 'axios'

axios.defaults.baseURL = 'http://127.0.0.1:5000/api'
createApp(App).use(router, axios).mount('#app')

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import config from './config'

import axios from 'axios'

axios.defaults.baseURL = 'http://127.0.0.1:5000/api/v1'

const app = createApp(App);
app.config.globalProperties.$config = config
app.use(store);
app.use(router);
app.use(axios);
app.mount('#app')

// createApp(App).use(store).use(router, axios).use.mount('#app')

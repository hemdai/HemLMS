import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AboutView from '../views/AboutView.vue'

const routes = [
    {
        path: '/',
        name: 'HomeView',
        component: HomeView
    
    },
    {
        path: '/about',
        name: 'AboutView',
        component: AboutView
    }
]

const router = createRouter({
    history: createWebHashHistory(import.meta.env.BASE_URL),
    routes
})

export default router
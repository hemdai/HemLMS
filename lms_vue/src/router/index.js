import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AboutView from '../views/AboutView.vue'
import SignUpView from '@/views/SignUpView.vue'
import LoginView from '@/views/LoginView.vue'
import MyAccount from '../views/dashboard/MyAccount.vue'
import CoursesVue from '@/views/CoursesVue.vue'
import CourseDetailView from '@/views/CourseDetailView.vue'
import BackofficeVue from '@/views/BackofficeVue.vue'
import AuthorsView from '@/views/AuthorsView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    component: AboutView
  },
  {
    path: '/signup',
    name: 'signup',
    component: SignUpView
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView
  }, {
    path: '/dashboard/my-account',
    name: 'MyAccount',
    component: MyAccount
  },
  {
    path: '/courses',
    name: 'CoursesVue',
    component: CoursesVue
  },
  {
    path: '/courses/:slug',
    name: 'CourseDetailView',
    component: CourseDetailView
  },
  {
    path: '/backoffice/',
    name: 'BackOffice',
    component: BackofficeVue
  },
  {
    path: '/authors/courses/:id',
    name: 'AuthorsView',
    component: AuthorsView
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router

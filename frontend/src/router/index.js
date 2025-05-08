import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '@/views/LoginView.vue'

const routes = [
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  // Позже добавим /dashboard
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
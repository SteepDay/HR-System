import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '@/views/LoginView.vue'
import DashboardView from '@/views/DashboardView.vue'

const routes = [
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: DashboardView,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Важно: Импортируем хранилище здесь, а не внутри хука
import { useAuthStore } from '@/stores/auth'

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  // Проверяем авторизацию только для защищенных роутов
  if (to.meta.requiresAuth) {
    if (authStore.token) {
      next()  // Пропускаем авторизованных
    } else {
      next('/login')  // Перенаправляем неавторизованных
    }
  } else {
    next()  // Пропускаем публичные роуты
  }
})

export default router
import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '@/views/LoginView.vue'
import DashboardView from '@/views/DashboardView.vue'
import VacanciesView from '@/views/VacanciesView.vue'
import CreateVacancyView from '@/views/CreateVacancyView.vue'
import HomeView from '@/views/HomeView.vue'
import RegisterView from '@/views/RegisterView.vue'

const routes = [
  {
  path: '/',
  name: 'home',
  component: HomeView
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
  path: '/register',
  name: 'register',
  component: RegisterView
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: DashboardView,
    meta: { requiresAuth: true }
  },
  {
    path: '/vacancies',
    name: 'vacancies',
    component: VacanciesView,
    meta: { requiresAuth: true }
  },
  {
    path: '/vacancies/new',
    name: 'create-vacancy',
    component: CreateVacancyView,
    meta: { requiresAuth: true, requiredRole: 'MANAGER' }
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
  
  // 1. Проверка авторизации
  if (to.meta.requiresAuth && !authStore.token) {
    next('/login')
    return  // Важно: прекращаем выполнение
  }

  // 2. Проверка ролей (только для авторизованных)
  if (to.meta.requiredRole) {
    // Ждем загрузки данных пользователя, если их нет
    if (!authStore.user) {
      try {
        await authStore.fetchUser()  // Добавим этот метод в хранилище
      } catch (error) {
        console.error('Ошибка загрузки данных пользователя:', error)
        next('/login')
        return
      }
    }

    // Проверяем роль
    if (authStore.user?.role !== to.meta.requiredRole) {
      next('/vacancies')  // Или /forbidden, если есть такая страница
      return
    }
  }

  next()  // Все проверки пройдены
})

export default router
<template>
  <div>
    <nav v-if="$route.name !== 'login'">
      <router-link to="/vacancies">Вакансии</router-link>
      <button @click="$router.push('/dashboard')">Кабинет</button>
      <button @click="handleLogout">Выйти</button>
    </nav>
    <router-view/>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>
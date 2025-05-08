<template>
  <div>
    <h1>Личный кабинет</h1>
    <p>Email: {{ user?.email }}</p>
    <p>Роль: {{ user?.role }}</p>
    <button @click="logout">Выйти</button>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const user = authStore.user

const logout = () => {
  authStore.logout()
  router.push('/login')
}
</script>
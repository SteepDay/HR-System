<template>
  <div class="home">
    <h1>Добро пожаловать в HR-систему!</h1>
    <div v-if="!authStore.token">
      <router-link to="/login" class="btn">Войти</router-link>
      <router-link to="/register" class="btn">Регистрация</router-link>
    </div>
    <div v-else>
      <router-link to="/dashboard" class="btn">Личный кабинет</router-link>
      <router-link to="/vacancies" class="btn">Вакансии</router-link>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
const authStore = useAuthStore()
</script>

<style scoped>
.home {
  text-align: center;
  padding: 2rem;
}
.btn {
  display: inline-block;
  margin: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: #42b983;
  color: white;
  border-radius: 4px;
  text-decoration: none;
}
</style>
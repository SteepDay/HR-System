<template>
  <div>
    <nav class="navbar">
      <router-link to="/">Главная</router-link>
      <template v-if="authStore.token">
        <router-link to="/dashboard">Кабинет</router-link>
        <router-link to="/vacancies">Вакансии</router-link>
        <button @click="authStore.logout()">Выйти</button>
      </template>
      <template v-else>
        <router-link to="/login">Войти</router-link>
      </template>
    </nav>
    <router-view/>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
const authStore = useAuthStore()
</script>

<style>
.navbar {
  padding: 1rem;
  background: #f0f0f0;
  margin-bottom: 2rem;
}
.navbar a, .navbar button {
  margin: 0 0.5rem;
  text-decoration: none;
  color: #333;
}
</style>
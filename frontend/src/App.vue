<template>
  <div id="app">
    <header class="header">
      <nav class="navbar">
        <router-link to="/" class="logo">HR System</router-link>
        <div class="nav-links">
          <!-- Кнопка "Кандидаты" ТОЛЬКО для авторизованных -->
          <router-link 
            v-if="authStore.token"
            to="/candidates"
            class="nav-link"
          >
            Кандидаты
          </router-link>
          <!-- Кнопка "Вакансии" ТОЛЬКО для авторизованных -->
          <router-link 
            v-if="authStore.token" 
            to="/vacancies"
          >
            Вакансии
          </router-link>
          
          <!-- Кнопка "Кабинет" ТОЛЬКО для авторизованных -->
          <router-link 
            v-if="authStore.token" 
            to="/dashboard"
          >
            Кабинет
          </router-link>
          
          <!-- Кнопка "Выйти" ТОЛЬКО для авторизованных -->
          <button 
            v-if="authStore.token" 
            @click="authStore.logout()" 
            class="btn btn-danger"
          >
            Выйти
          </button>
          
          <!-- Кнопка "Войти" ТОЛЬКО для неавторизованных -->
          <router-link 
            v-if="!authStore.token" 
            to="/login"
          >
            Войти
          </router-link>
        </div>
      </nav>
    </header>
    
    <main class="main">
      <router-view/>
    </main>
    
    <footer class="footer">
      © 2025 HR System. Все права защищены.
    </footer>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
const authStore = useAuthStore()
</script>
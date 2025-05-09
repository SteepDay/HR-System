<template>
  <div class="card hero-card">
    <h1>Добро пожаловать в HR-систему</h1>
    <p class="subtitle">Упрощаем подбор персонала для вашей компании</p>
    
    <div class="action-buttons">
      <template v-if="!authStore.token">
        <router-link to="/login" class="btn btn-primary">Войти</router-link>
        <router-link to="/register" class="btn btn-secondary">Регистрация</router-link>
      </template>
      <template v-else>
        <router-link to="/dashboard" class="btn btn-primary">
          <i class="icon-user"></i> Личный кабинет
        </router-link>
        <router-link to="/vacancies" class="btn btn-primary">
          <i class="icon-briefcase"></i> Вакансии
        </router-link>
      </template>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
const authStore = useAuthStore()
</script>

<style scoped>
.hero-card {
  text-align: center;
  padding: 3rem 2rem;
  margin: 2rem auto;
  max-width: 800px;
}

.subtitle {
  color: var(--secondary);
  margin: 1rem 0 2rem;
  font-size: 1.2rem;
}

.action-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 2rem;
}

.btn {
  text-decoration: none;
}

.btn-secondary {
  background: var(--secondary);
  color: white;
}

.btn-primary {
  color: white;
}

.icon-user, .icon-briefcase {
  margin-right: 0.5rem;
}

@media (max-width: 600px) {
  .action-buttons {
    flex-direction: column;
  }
  
  .btn {
    width: 100%;
  }
}
</style>
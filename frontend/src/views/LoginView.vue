<template>
  <div class="card login-card">
    <h1>Вход в систему</h1>
    <form @submit.prevent="handleLogin" class="form">
      <div class="form-group">
        <label>Email:</label>
        <input 
          v-model="email" 
          type="email" 
          class="form-control" 
          required 
          placeholder="Введите email"
        >
      </div>
      <div class="form-group">
        <label>Пароль:</label>
        <input
          v-model="password"
          type="password"
          class="form-control"
          required
          placeholder="Введите пароль"
        >
      </div>
      <div class="form-actions">
        <button type="submit" class="btn btn-primary">Войти</button>
      </div>
      <p v-if="error" class="error-message">{{ error }}</p>
    </form>
    <p class="text-center">
      Нет аккаунта? <router-link to="/register">Зарегистрируйтесь</router-link>
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const email = ref('')
const password = ref('')
const error = ref('')
const authStore = useAuthStore()
const router = useRouter()

const handleLogin = async () => {
  try {
    const success = await authStore.login(email.value, password.value)
    if (success) {
      router.push('/dashboard')
    }
  } catch (error) {
    error.value = error.response?.data?.detail || 
                 'Ошибка сервера. Попробуйте позже.'
    console.error('Full error:', error)
  }
}
</script>

<style scoped>
.login-card {
  max-width: 400px;
  margin: 2.5rem auto;
  padding: 2.5rem 2rem;
}
.form-actions {
  display: flex;
  justify-content: center;
  margin-top: 1.5rem;
}
.error-message {
  color: var(--danger);
  margin-top: 1rem;
  text-align: center;
}
.text-center {
  text-align: center;
  margin-top: 1rem;
}
</style>
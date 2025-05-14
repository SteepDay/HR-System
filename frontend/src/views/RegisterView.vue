<template>
  <div class="card auth-card">
    <h1>Регистрация</h1>
    <form @submit.prevent="submitForm" class="form">
      <div class="form-group">
        <label>Email:</label>
        <input 
          v-model="form.email" 
          type="email" 
          class="form-control" 
          placeholder="work@example.com" 
          required
        >
      </div>
      
      <div class="form-group">
        <label>Пароль:</label>
        <input
          v-model="form.password"
          type="password"
          class="form-control"
          placeholder="Не менее 8 символов"
          required
        >
      </div>
      
      <div class="form-group">
        <label>Роль:</label>
        <select v-model="form.role" class="form-control">
          <option value="HR">HR-специалист</option>
          <option value="MANAGER">Руководитель</option>
        </select>
      </div>
      <button type="submit" class="btn btn-primary" :disabled="isLoading">
        <span v-if="!isLoading">Зарегистрироваться</span>
        <span v-else>Регистрация...</span>
      </button>
      <p class="text-center mt-2">
        Уже есть аккаунт? <router-link to="/login">Войдите</router-link>
      </p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const form = ref({
  email: '',
  password: '',
  role: 'HR'
})
const router = useRouter()

const submitForm = async () => {
  try {
    await axios.post('http://localhost:8000/api/auth/register/', form.value)
    router.push('/login')
  } catch (error) {
    console.error('Ошибка:', error.response?.data)
  }
}
</script>

<style scoped>
.auth-card {
  max-width: 500px;
  margin: 2rem auto;
}

.mt-2 {
  margin-top: 1rem;
}
</style>
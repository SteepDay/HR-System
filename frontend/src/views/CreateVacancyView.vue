<template>
  <div class="card form-card">
    <h1>Создать вакансию</h1>
    
    <form @submit.prevent="submitForm" class="vacancy-form">
      <div class="form-group">
        <label>Название вакансии:</label>
        <input 
          v-model="form.title" 
          class="form-control" 
          placeholder="Например: Senior Python Developer" 
          required
        >
      </div>
      
      <div class="form-group">
        <label>Описание:</label>
        <textarea
          v-model="form.description"
          class="form-control"
          rows="5"
          placeholder="Опишите требования и условия работы..."
          required
        ></textarea>
      </div>
      
      <div class="form-actions">
        <button type="submit" class="btn btn-primary">Опубликовать</button>
        <router-link to="/vacancies" class="btn btn-secondary" style="text-decoration: none;">Отмена</router-link>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const form = ref({
  title: '',
  description: '',
  status: 'OPEN'
})
const router = useRouter()
const authStore = useAuthStore()

const submitForm = async () => {
  try {
    await axios.post('http://localhost:8000/api/vacancies/', form.value, {
      headers: {
        Authorization: `Bearer ${authStore.token}`
      }
    })
    router.push('/vacancies')
  } catch (error) {
    console.error('Ошибка:', error)
  }
}
</script>

<style scoped>
.form-card {
  max-width: 600px;
  margin: 2rem auto;
  padding: 2.5rem 2rem;
}
.vacancy-form {
  margin-top: 2rem;
}
.form-group {
  margin-bottom: 1.5rem;
}
.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
}
.btn {
  min-width: 140px;
  font-weight: 700;
  text-align: center;
}
.btn-secondary {
  margin-left: 0.5rem;
}
@media (max-width: 600px) {
  .form-actions {
    flex-direction: column;
    align-items: stretch;
  }
  .btn {
    width: 100%;
  }
}
</style>
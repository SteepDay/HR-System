<template>
  <div class="card form-card">
    <h1>Редактировать вакансию</h1>
    
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label>Название:</label>
        <input v-model="form.title" class="form-control" required>
      </div>
      
      <div class="form-group">
        <label>Описание:</label>
        <textarea v-model="form.description" class="form-control" rows="5" required></textarea>
      </div>
      
      <div class="form-group">
        <label>Статус:</label>
        <select v-model="form.status" class="form-control">
          <option value="DRAFT">TEST</option>
          <option value="OPEN">OPEN</option>
          <option value="CLOSED">CLOSED</option>
        </select>
      </div>
      
      <div class="form-actions">
        <button type="submit" class="btn btn-primary">Сохранить</button>
        <button @click="deleteVacancy" class="btn btn-danger">Удалить</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const form = ref({
  title: '',
  description: '',
  status: 'DRAFT'
})

// Загружаем данные вакансии
onMounted(async () => {
  try {
    const response = await axios.get(`http://localhost:8000/api/vacancies/${route.params.id}/`, {
      headers: {
        Authorization: `Bearer ${authStore.token}`
      }
    })
    form.value = response.data
  } catch (error) {
    console.error('Ошибка загрузки:', error)
  }
})

const submitForm = async () => {
  try {
    await axios.put(`http://localhost:8000/api/vacancies/${route.params.id}/`, form.value, {
      headers: {
        Authorization: `Bearer ${authStore.token}`
      }
    })
    router.push('/vacancies')
  } catch (error) {
    console.error('Ошибка сохранения:', error)
  }
}

const deleteVacancy = async () => {
  if (confirm('Удалить вакансию?')) {
    try {
      await axios.delete(`http://localhost:8000/api/vacancies/${route.params.id}/`, {
        headers: {
          Authorization: `Bearer ${authStore.token}`
        }
      })
      router.push('/vacancies')
    } catch (error) {
      console.error('Ошибка удаления:', error)
    }
  }
}
</script>

<style scoped>
.form-card {
  max-width: 600px;
  margin: 2rem auto;
  padding: 2.5rem 2rem;
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
.btn-danger {
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
<template>
  <div class="candidates-container">
    <div class="action-bar">
      <h1>Управление кандидатами</h1>
      <button 
        v-if="authStore.user?.role === 'HR'"
        @click="showCreateModal = true"
        class="btn btn-primary"
      >
        + Добавить кандидата
      </button>
    </div>

    <!-- Модальное окно создания кандидата -->
    <div v-if="showCreateModal" class="modal-overlay">
      <div class="modal-content">
        <h2>Новый кандидат</h2>
        <form @submit.prevent="createCandidate">
          <div class="form-group">
            <label>ФИО:</label>
            <input v-model="newCandidate.full_name" required class="form-control">
          </div>
          <div class="form-group">
            <label>Email:</label>
            <input v-model="newCandidate.email" type="email" required class="form-control">
          </div>
          <div class="form-group">
            <label>Телефон:</label>
            <input v-model="newCandidate.phone" class="form-control">
          </div>
          <div class="form-group">
            <label>Вакансия:</label>
            <select v-model="newCandidate.vacancy_id" required class="form-control">
              <option disabled value="">Выберите вакансию</option>
              <option v-for="vacancy in vacancies" :value="vacancy.id">
                {{ vacancy.title }}
              </option>
            </select>
          </div>
          <div class="form-actions">
            <button type="submit" class="btn btn-primary">Сохранить</button>
            <button type="button" @click="showCreateModal = false" class="btn btn-secondary">Отмена</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Фильтры -->
    <div class="filters">
      <select v-model="statusFilter" class="filter-select">
        <option value="">Все статусы</option>
        <option v-for="status in statusOptions" :value="status.value">
          {{ status.label }}
        </option>
      </select>
      <button @click="fetchCandidates" class="refresh-btn">Обновить</button>
    </div>

    <!-- Таблица кандидатов -->
    <div class="candidates-list">
      <div v-if="loading">Загрузка...</div>
      <div v-else-if="error" class="error">{{ error }}</div>
      <template v-else>
        <div v-for="candidate in filteredCandidates" :key="candidate.id" class="candidate-card">
          <h3>{{ candidate.full_name }}</h3>
          <p>Вакансия: {{ candidate.vacancy.title }}</p>
          <p>Статус: 
            <span :class="'status-' + candidate.status.toLowerCase()">
              {{ getStatusDisplay(candidate.status) }}
            </span>
          </p>
          <button 
            @click="viewDetails(candidate.id)"
            class="btn btn-primary"
          >
            Подробнее
          </button>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import axios from 'axios'

const authStore = useAuthStore()
const router = useRouter()
const candidates = ref([])
const vacancies = ref([])
const loading = ref(false)
const error = ref(null)
const statusFilter = ref('')
const showCreateModal = ref(false)

const newCandidate = ref({
  full_name: '',
  email: '',
  phone: '',
  vacancy_id: null,
  status: 'HR' // Статус по умолчанию
})

const statusOptions = [
  { value: 'HR', label: 'HR Собеседование' },
  { value: 'TECH', label: 'Тех. Собеседование' },
  { value: 'FINAL', label: 'На рассмотрении' }
]

const viewDetails = (id) => {
  router.push(`/candidates/${id}`)
}

const fetchCandidates = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await axios.get('http://localhost:8000/api/candidates/', {
      headers: {
        Authorization: `Bearer ${authStore.token}`
      }
    })
    candidates.value = response.data
  } catch (err) {
    error.value = err.response?.data?.detail || 'Ошибка загрузки данных'
  } finally {
    loading.value = false
  }
}

const fetchVacancies = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/vacancies/', {
      headers: {
        Authorization: `Bearer ${authStore.token}`
      }
    })
    vacancies.value = response.data
  } catch (err) {
    console.error('Ошибка загрузки вакансий:', err)
  }
}

const createCandidate = async () => {
  try {
    await axios.post('http://localhost:8000/api/candidates/', newCandidate.value, {
      headers: {
        Authorization: `Bearer ${authStore.token}`
      }
    })
    await fetchCandidates()
    showCreateModal.value = false
    // Сброс формы
    newCandidate.value = {
      full_name: '',
      email: '',
      phone: '',
      vacancy_id: null,
      status: 'HR'
    }
  } catch (err) {
    error.value = err.response?.data?.detail || 'Ошибка создания кандидата'
    console.error('Детали ошибки:', err.response)
  }
}

const filteredCandidates = computed(() => {
  if (!statusFilter.value) return candidates.value
  return candidates.value.filter(c => c.status === statusFilter.value)
})

const getStatusDisplay = (status) => {
  const statusMap = {
    'HR': 'HR Собеседование',
    'TECH': 'Тех. Собеседование',
    'FINAL': 'На рассмотрении',
    'HIRED': 'Принят',
    'REJECTED': 'Отклонен'
  }
  return statusMap[status] || status
}

onMounted(() => {
  fetchCandidates()
  fetchVacancies()
})
</script>

<style scoped>
.candidates-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.action-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.filters {
  margin: 20px 0;
  display: flex;
  gap: 10px;
}

.filter-select {
  padding: 8px;
  border-radius: 4px;
  border: 1px solid #ddd;
}

.candidates-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.candidate-card {
  border: 1px solid #eee;
  padding: 15px;
  border-radius: 8px;
  background: white;
}

.status-hr {
  color: #3498db;
}
.status-tech {
  color: #f39c12;
}
.status-final {
  color: #2ecc71;
}

/* Стили для модального окна */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 500px;
  max-width: 90%;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
}

.form-control {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}
</style>
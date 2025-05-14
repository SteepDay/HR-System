<template>
  <div class="candidates-container">
    <h1>Управление кандидатами</h1>
    
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
const loading = ref(false)
const error = ref(null)
const statusFilter = ref('')

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

onMounted(fetchCandidates)
</script>

<style scoped>
.candidates-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
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
</style>
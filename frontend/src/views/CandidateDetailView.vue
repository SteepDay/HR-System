<template>
  <div class="candidate-detail">
    <div v-if="loading">Загрузка данных кандидата...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else>
      <div class="header">
        <h1>Профиль кандидата: {{ candidate.full_name }}</h1>
        <button @click="$router.back()" class="btn btn-secondary">
          Вернуться к списку
        </button>
      </div>

      <div class="details-grid">
        <div class="detail-card">
          <h3>Основная информация</h3>
          <p><strong>Email:</strong> {{ candidate.email }}</p>
          <p><strong>Телефон:</strong> {{ candidate.phone || 'не указан' }}</p>
          <p><strong>Вакансия:</strong> {{ candidate.vacancy.title }}</p>
        </div>

        <div class="detail-card status-section">
          <h3>Текущий статус</h3>
          <p :class="'status-' + candidate.status.toLowerCase()">
            {{ getStatusDisplay(candidate.status) }}
          </p>

          <!-- Управление статусами для HR -->
          <div v-if="authStore.user?.role === 'HR'" class="status-controls">
            <select 
              v-model="selectedStatus" 
              class="status-select"
              @change="updateStatus"
            >
              <option 
                v-for="status in availableStatuses" 
                :value="status.value"
                :disabled="status.value === candidate.status"
              >
                {{ status.label }}
              </option>
            </select>
          </div>

          <!-- Управление статусами для менеджера -->
          <div 
            v-else-if="authStore.user?.role === 'MANAGER' && candidate.status === 'FINAL'" 
            class="manager-controls"
          >
            <button @click="changeStatus('HIRED')" class="btn btn-success">
              Нанять
            </button>
            <button @click="changeStatus('REJECTED')" class="btn btn-danger">
              Отклонить
            </button>
          </div>
        </div>

        <div class="detail-card comments">
          <h3>Комментарии</h3>
          <!-- Форма добавления комментария HR -->
          <div v-if="authStore.user?.role === 'HR'" class="comment-form">
            <h4>Добавить комментарий:</h4>
            <textarea 
              v-model="newHrComment" 
              class="comment-textarea"
              placeholder="Ваш комментарий..."
            ></textarea>
            <button 
              @click="saveHrComment"
              class="btn btn-primary"
            >
              Сохранить
            </button>
          </div>

          <!-- Форма добавления комментария менеджера -->
          <div v-if="authStore.user?.role === 'MANAGER'" class="comment-form">
            <h4>Добавить комментарий:</h4>
            <textarea 
              v-model="newTechComment" 
              class="comment-textarea"
              placeholder="Ваш комментарий..."
            ></textarea>
            <button 
              @click="saveTechComment"
              class="btn btn-primary"
            >
              Сохранить
            </button>
          </div>

          <!-- Отображение существующих комментариев -->
          <div v-if="candidate.hr_comment" class="comment-item">
            <h4>Комментарий HR:</h4>
            <p>{{ candidate.hr_comment }}</p>
            <small>{{ formatDate(candidate.hr_comment_updated_at) }}</small>
          </div>

          <div v-if="candidate.tech_comment" class="comment-item">
            <h4>Комментарий менеджера:</h4>
            <p>{{ candidate.tech_comment }}</p>
            <small>{{ formatDate(candidate.tech_comment_updated_at) }}</small>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const authStore = useAuthStore()
const newHrComment = ref('')
const newTechComment = ref('')
const candidate = ref({})
const loading = ref(true)
const error = ref(null)
const selectedStatus = ref('')

const statusOptions = {
  HR: [
    { value: 'HR', label: 'HR Собеседование' },
    { value: 'TECH', label: 'Тех. Собеседование' },
    { value: 'FINAL', label: 'На рассмотрении' },
    { value: 'REJECTED', label: 'Отклонен' }
  ],
  MANAGER: [
    { value: 'HIRED', label: 'Нанять' },
    { value: 'REJECTED', label: 'Отклонить' }
  ]
}

const availableStatuses = computed(() => {
  if (authStore.user?.role === 'HR') {
    return statusOptions.HR.filter(s => s.value !== candidate.value.status)
  }
  return []
})

const getStatusDisplay = (status) => {
  const statusMap = {
    'HR': 'HR Собеседование',
    'TECH': 'Тех. Собеседование',
    'FINAL': 'На рассмотрении руководителя',
    'HIRED': 'Принят',
    'REJECTED': 'Отклонен'
  }
  return statusMap[status] || status
}

const loadCandidate = async () => {
  try {
    const response = await axios.get(
      `http://localhost:8000/api/candidates/${route.params.id}/`,
      {
        headers: {
          Authorization: `Bearer ${authStore.token}`
        }
      }
    )
    candidate.value = response.data
    selectedStatus.value = response.data.status
  } catch (err) {
    error.value = err.response?.data?.detail || 'Ошибка загрузки данных кандидата'
  } finally {
    loading.value = false
  }
}

const changeStatus = async (newStatus) => {
  try {
    await axios.post(
      `http://localhost:8000/api/candidates/${route.params.id}/change_status/`,
      { status: newStatus },
      {
        headers: {
          Authorization: `Bearer ${authStore.token}`,
          'Content-Type': 'application/json'
        }
      }
    )
    await loadCandidate()
  } catch (err) {
    error.value = err.response?.data?.detail || 'Ошибка обновления статуса'
  }
}

const saveHrComment = async () => {
  try {
    console.log("Отправляемые данные:", { 
      hr_comment: newHrComment.value,
      candidate_id: route.params.id 
    })

    const response = await axios.patch(
      `http://localhost:8000/api/candidates/${route.params.id}/update_hr_comment/`,
      { 
        hr_comment: newHrComment.value 
      },
      {
        headers: {
          Authorization: `Bearer ${authStore.token}`,
          'Content-Type': 'application/json'
        }
      }
    )
    console.log('Ответ сервера:', response.data)
    await loadCandidate() // Перезагружаем данные
    newHrComment.value = ''
  } catch (err) {
    console.error("Полная ошибка:", {
      message: err.message,
      response: err.response,
      request: err.request
    }) // Расширенное логирование
    error.value = err.response?.data?.detail || 'Неизвестная ошибка сервера'
  }
}

const saveTechComment = async () => {
  try {
    console.log("Отправляемые данные (tech):", { 
      tech_comment: newTechComment.value,
      candidate_id: route.params.id 
    })

    const response = await axios.patch(
      `http://localhost:8000/api/candidates/${route.params.id}/update_tech_comment/`,
      { 
        tech_comment: newTechComment.value 
      },
      {
        headers: {
          Authorization: `Bearer ${authStore.token}`,
          'Content-Type': 'application/json'
        }
      }
    )
    console.log("Полный ответ сервера (tech):", response)
    await loadCandidate()
    newTechComment.value = ''
  } catch (err) {
    console.error("Полная ошибка (tech):", {
      message: err.message,
      response: err.response,
      request: err.request
    })
    error.value = err.response?.data?.detail || 'Ошибка сохранения технического комментария'
  }
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  return new Date(dateString).toLocaleString()
}

const updateStatus = async () => {
  if (selectedStatus.value) {
    await changeStatus(selectedStatus.value)
  }
}

onMounted(loadCandidate)
</script>

<style scoped>
.candidate-detail {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.details-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.detail-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.status-section {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.status-HR {
  color: #3498db;
  font-weight: bold;
}

.status-TECH {
  color: #f39c12;
  font-weight: bold;
}

.status-FINAL {
  color: #2ecc71;
  font-weight: bold;
}

.status-HIRED {
  color: #27ae60;
  font-weight: bold;
}

.status-REJECTED {
  color: #e74c3c;
  font-weight: bold;
}

.status-select {
  padding: 8px;
  border-radius: 4px;
  border: 1px solid #ddd;
  width: 100%;
  max-width: 300px;
}

.manager-controls {
  display: flex;
  gap: 10px;
  margin-top: 15px;
}

.comments {
  grid-column: 1 / -1;
}

.error {
  color: #e74c3c;
  padding: 10px;
  background-color: #fdecea;
  border-radius: 4px;
}

.comment-form {
  margin-bottom: 20px;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 8px;
}

.comment-textarea {
  width: 100%;
  min-height: 100px;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  resize: vertical;
}

.comment-item {
  margin-bottom: 20px;
  padding: 15px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.comment-item h4 {
  margin-top: 0;
  color: #333;
}

.comment-item small {
  color: #777;
  font-size: 0.8em;
}
</style>
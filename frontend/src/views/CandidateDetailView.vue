<template>
  <div class="candidate-detail">
    <div v-if="loading">Загрузка данных кандидата...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else>
      <div class="header">
        <h1>Профиль кандидата: {{ candidate.full_name }}</h1>
        <div class="header-actions">
          <button @click="$router.back()" class="btn btn-secondary">
            Вернуться к списку
          </button>
          
          <!-- Кнопки управления для HR -->
          <div v-if="authStore.user?.role === 'HR'" class="hr-actions">
            <button @click="isEditing = !isEditing" class="btn-action btn-edit">
              {{ isEditing ? 'Отменить' : 'Редактировать' }}
            </button>
            <button @click="confirmDelete" class="btn-action btn-delete">
              Удалить
            </button>
          </div>
        </div>
      </div>

      <!-- Форма редактирования -->
      <div v-if="isEditing" class="edit-form">
        <h3>Редактирование данных</h3>
        <div class="form-group">
          <label>ФИО:</label>
          <input v-model="editData.full_name" class="form-input">
        </div>
        <div class="form-group">
          <label>Email:</label>
          <input v-model="editData.email" type="email" class="form-input">
        </div>
        <div class="form-group">
          <label>Телефон:</label>
          <input v-model="editData.phone" class="form-input">
        </div>
        <button @click="saveChanges" class="btn btn-primary">Сохранить</button>
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
            <h4>Комментарий рукводителя:</h4>
            <p>{{ candidate.tech_comment }}</p>
            <small>{{ formatDate(candidate.tech_comment_updated_at) }}</small>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

// Состояния для данных кандидата
const candidate = ref({})
const loading = ref(true)
const error = ref(null)
const selectedStatus = ref('')

// Состояния для комментариев
const newHrComment = ref('')
const newTechComment = ref('')

// Состояния для редактирования
const isEditing = ref(false)
const editData = reactive({
  full_name: '',
  email: '',
  phone: ''
})

// Опции статусов
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

// Доступные статусы для текущего пользователя
const availableStatuses = computed(() => {
  if (authStore.user?.role === 'HR') {
    return statusOptions.HR.filter(s => s.value !== candidate.value.status)
  }
  return []
})

// Загрузка данных кандидата
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
    
    // Заполняем данные для редактирования
    Object.assign(editData, {
      full_name: response.data.full_name,
      email: response.data.email,
      phone: response.data.phone || ''
    })
  } catch (err) {
    error.value = err.response?.data?.detail || 'Ошибка загрузки данных кандидата'
  } finally {
    loading.value = false
  }
}

// Изменение статуса кандидата
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

// Сохранение HR комментария
const saveHrComment = async () => {
  try {
    const response = await axios.patch(
      `http://localhost:8000/api/candidates/${route.params.id}/update_hr_comment/`,
      { hr_comment: newHrComment.value },
      {
        headers: {
          Authorization: `Bearer ${authStore.token}`,
          'Content-Type': 'application/json'
        }
      }
    )
    await loadCandidate()
    newHrComment.value = ''
  } catch (err) {
    error.value = err.response?.data?.detail || 'Ошибка сохранения комментария HR'
  }
}

// Сохранение технического комментария
const saveTechComment = async () => {
  try {
    const response = await axios.patch(
      `http://localhost:8000/api/candidates/${route.params.id}/update_tech_comment/`,
      { tech_comment: newTechComment.value },
      {
        headers: {
          Authorization: `Bearer ${authStore.token}`,
          'Content-Type': 'application/json'
        }
      }
    )
    await loadCandidate()
    newTechComment.value = ''
  } catch (err) {
    error.value = err.response?.data?.detail || 'Ошибка сохранения технического комментария'
  }
}

// Обновление статуса через select
const updateStatus = async () => {
  if (selectedStatus.value) {
    await changeStatus(selectedStatus.value)
  }
}

// Сохранение изменений данных кандидата
const saveChanges = async () => {
  try {
    await axios.patch(
      `http://localhost:8000/api/candidates/${route.params.id}/`,
      editData,
      {
        headers: {
          Authorization: `Bearer ${authStore.token}`,
          'Content-Type': 'application/json'
        }
      }
    )
    await loadCandidate()
    isEditing.value = false
  } catch (err) {
    error.value = err.response?.data?.detail || 'Ошибка сохранения изменений'
  }
}

// Удаление кандидата
const deleteCandidate = async () => {
  try {
    await axios.delete(
      `http://localhost:8000/api/candidates/${route.params.id}/`,
      {
        headers: {
          Authorization: `Bearer ${authStore.token}`
        }
      }
    )
    router.push('/candidates')
  } catch (err) {
    error.value = err.response?.data?.detail || 'Ошибка удаления кандидата'
  }
}

// Подтверждение удаления
const confirmDelete = () => {
  if (confirm(`Вы уверены, что хотите удалить кандидата ${candidate.value.full_name}?`)) {
    deleteCandidate()
  }
}

// Форматирование даты
const formatDate = (dateString) => {
  if (!dateString) return ''
  return new Date(dateString).toLocaleString()
}

// Отображение статуса
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

// Загрузка данных при монтировании компонента
onMounted(loadCandidate)
</script>

<style scoped>
.candidate-detail {
  max-width: 1100px;
  margin: 2rem auto;
  padding: 2.5rem 2rem;
}
.header {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
  margin-bottom: 2rem;
}
.header-actions {
  display: flex;
  gap: 1.2rem;
  flex-wrap: wrap;
  align-items: center;
}
.hr-actions {
  display: flex;
  gap: 1rem;
}
.btn-action {
  min-width: 120px;
  font-weight: 700;
  border-radius: 6px;
  border: none;
  padding: 0.6rem 1.2rem;
  transition: background 0.3s, box-shadow 0.3s, transform 0.2s;
  box-shadow: 0 2px 8px rgba(56,182,168,0.10);
}
.btn-edit {
  background: var(--accent-hover);
  color: #fff;
}
.btn-edit:hover, .btn-edit:focus {
  background: var(--accent);
  color: #fff;
  box-shadow: 0 4px 24px 0 rgba(56,182,168,0.22);
  transform: scale(1.045);
}
.btn-delete {
  background: var(--danger);
  color: #fff;
}
.btn-delete:hover, .btn-delete:focus {
  background: #c0392b;
  color: #fff;
  box-shadow: 0 4px 24px 0 rgba(231,76,60,0.22);
  transform: scale(1.045);
}
.details-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 2rem;
  margin-top: 2rem;
}
.detail-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 24px rgba(56,182,168,0.10);
  padding: 1.5rem;
  border: 1.5px solid var(--border-main);
  transition: box-shadow 0.3s, border-color 0.3s;
}
.detail-card:hover {
  box-shadow: 0 8px 32px rgba(56,182,168,0.18);
  border-color: var(--border-strong);
}
.status-controls .status-select {
  min-width: 160px;
  margin-top: 1rem;
}
.manager-controls {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}
.comment-form .btn {
  margin-top: 1rem;
  min-width: 120px;
}
@media (max-width: 900px) {
  .details-grid {
    grid-template-columns: 1fr;
  }
}
.error {
  color: #e74c3c;
  padding: 10px;
  background-color: #fdecea;
  border-radius: 4px;
}
.edit-form {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}
.form-group {
  margin-bottom: 15px;
}
.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
}
.form-input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
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
.comments {
  grid-column: 1 / -1;
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
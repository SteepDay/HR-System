<template>
  <div class="card hero-card">
    <h1>Добро пожаловать в HR-систему</h1>
    <p class="subtitle">Упрощаем подбор персонала для вашей компании</p>

    <!-- Статистика (только для авторизованных) -->
    <div v-if="authStore.token" class="stats-container">
      <div class="stats-card">
        <h3>Кандидаты</h3>
        <div class="stats-grid">
          <div class="stat-item">
            <span class="stat-value">{{ candidatesData.total }}</span>
            <span class="stat-label">Всего</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">{{ candidatesData.hired }}</span>
            <span class="stat-label">Принято</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">{{ candidatesData.rejected }}</span>
            <span class="stat-label">Отклонено</span>
          </div>
        </div>
      </div>

      <div class="stats-card vacancy-scroll-container">
        <h3>Статистика по вакансиям</h3>
        <div class="vacancy-stats scrollable">
          <div v-for="vacancy in vacanciesData" :key="vacancy.id" class="vacancy-item">
            <span class="vacancy-title">{{ vacancy.title }}</span>
            <span class="vacancy-count">{{ vacancy.count }} кандидатов</span>
            <div class="vacancy-details">
              <span>Принято: {{ vacancy.hired }}</span>
              <span>В процессе: {{ vacancy.in_progress }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="action-buttons" v-if="!authStore.token">
      <router-link to="/login" class="btn btn-primary">Войти</router-link>
      <router-link to="/register" class="btn btn-secondary">Регистрация</router-link>
    </div>
    
    <div class="action-buttons" v-else>
      <router-link to="/dashboard" class="btn btn-primary">
        <i class="icon-user"></i> Личный кабинет
      </router-link>
      <router-link to="/vacancies" class="btn btn-primary">
        <i class="icon-briefcase"></i> Вакансии
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'

const authStore = useAuthStore()

const candidatesData = ref({
  total: 0,
  hired: 0,
  rejected: 0
})

const vacanciesData = ref([])

const fetchStats = async () => {
  try {
    // Загрузка статистики по кандидатам
    const candidatesResponse = await axios.get('http://localhost:8000/api/candidates/stats/', {
      headers: {
        Authorization: `Bearer ${authStore.token}`
      }
    })
    candidatesData.value = candidatesResponse.data

    // Загрузка статистики по вакансиям
    const vacanciesResponse = await axios.get('http://localhost:8000/api/vacancies/all_stats/', {
    headers: {
      Authorization: `Bearer ${authStore.token}`
    }
  })
    vacanciesData.value = vacanciesResponse.data
  } catch (error) {
    console.error('Ошибка загрузки статистики:', error)
  }
}

onMounted(() => {
  if (authStore.token) {
    fetchStats()
  }
})
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

.stats-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin: 2rem 0;
  text-align: left;
}

.stats-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-top: 1rem;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-value {
  font-size: 1.8rem;
  font-weight: bold;
  color: var(--primary);
}

.stat-label {
  font-size: 0.9rem;
  color: var(--secondary);
}

.vacancy-stats {
  margin-top: 1rem;
}

.vacancy-item {
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #eee;
}

.vacancy-title {
  font-weight: 500;
  display: block;
}

.vacancy-count {
  font-size: 0.9rem;
  color: var(--primary);
}

.vacancy-details {
  display: flex;
  justify-content: space-between;
  font-size: 0.8rem;
  margin-top: 0.5rem;
  color: var(--secondary);
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

@media (max-width: 768px) {
  .stats-container {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 600px) {
  .action-buttons {
    flex-direction: column;
  }
  
  .btn {
    width: 100%;
  }
}
.vacancy-scroll-container {
  max-height: 400px;
  overflow: hidden;
}

.scrollable {
  max-height: 350px;
  overflow-y: auto;
  padding-right: 8px;
}

/* Полоса прокрутки */
.scrollable::-webkit-scrollbar {
  width: 6px;
}

.scrollable::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.scrollable::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 3px;
}

.scrollable::-webkit-scrollbar-thumb:hover {
  background: #555;
}
</style>
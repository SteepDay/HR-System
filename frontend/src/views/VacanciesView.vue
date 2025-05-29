<template>
  <div>
    <div class="card action-bar">
      <h1>Вакансии</h1>
      <button 
        v-if="authStore.user?.role === 'MANAGER'"
        @click="$router.push('/vacancies/new')"
        class="btn btn-primary"
      >
        Создать вакансию
      </button>
    </div>
    
    <div class="vacancies-grid">
      <div v-for="vacancy in vacancies" :key="vacancy.id" class="card vacancy-card">
        <div class="vacancy-header">
          <h2>{{ vacancy.title }}</h2>
          <span class="status-badge" :class="vacancy.status.toLowerCase()">
            {{ getStatusText(vacancy.status) }}
          </span>
        </div>
        <p>{{ vacancy.description }}</p>
        
        <div class="vacancy-actions" v-if="authStore.user?.role === 'MANAGER'">
          <button 
            @click="$router.push(`/vacancies/edit/${vacancy.id}`)"
            class="btn btn-sm btn-edit"
          >
            Редактировать
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const vacancies = ref([])

const getStatusText = (status) => {
  const statusMap = {
    'DRAFT': 'TEST',
    'OPEN': 'OPEN',
    'CLOSED': 'CLOSED'
  }
  return statusMap[status] || status
}

onMounted(async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/vacancies/', {
      headers: {
        Authorization: `Bearer ${authStore.token}`
      }
    })
    vacancies.value = response.data
  } catch (error) {
    console.error('Ошибка загрузки:', error)
  }
})
</script>

<style scoped>
.action-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1.5rem;
  margin-bottom: 2rem;
}
.action-bar .btn {
  min-width: 160px;
}

.vacancies-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 2rem;
}

.vacancy-actions .btn {
  min-width: 120px;
}

.btn-edit {
  background: var(--warning);
  color: #fff;
  font-weight: 700;
  border: none;
  border-radius: 6px;
  box-shadow: 0 2px 8px rgba(243,156,18,0.14);
  transition: background 0.3s, box-shadow 0.3s, transform 0.2s;
}
.btn-edit:hover, .btn-edit:focus {
  background: #f1c40f;
  color: #fff;
  box-shadow: 0 4px 24px 0 rgba(243,156,18,0.22);
  transform: scale(1.045);
}

.btn-sm {
  padding: 0.3rem 0.6rem;
  font-size: 0.9rem;
}

.vacancy-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.status-badge {
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 500;
}

.status-badge.draft {
  background: #fff3cd;
  color: #856404;
}

.status-badge.open {
  background: #d4edda;
  color: #155724;
}

.status-badge.closed {
  background: #f8d7da;
  color: #721c24;
}
</style>
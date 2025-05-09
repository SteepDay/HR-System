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
        <h2>{{ vacancy.title }}</h2>
        <p>{{ vacancy.description }}</p>
        <span class="status-badge" :class="vacancy.status.toLowerCase()">
          {{ vacancy.status }}
        </span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.action-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.vacancies-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.vacancy-card {
  transition: transform 0.3s;
}

.vacancy-card:hover {
  transform: translateY(-5px);
}

.status-badge {
  display: inline-block;
  padding: 0.3rem 0.6rem;
  border-radius: 20px;
  font-size: 0.8rem;
  margin-top: 0.5rem;
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
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useAuthStore } from '@/stores/auth'
  import axios from 'axios'
  
  const authStore = useAuthStore()
  const vacancies = ref([])
  
  onMounted(async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/vacancies/', {
        headers: {
          Authorization: `Bearer ${authStore.token}`
        }
      })
      vacancies.value = response.data
    } catch (error) {
      console.error('Ошибка загрузки вакансий:', error)
    }
  })
  </script>
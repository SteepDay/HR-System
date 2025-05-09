<template>
    <div>
      <h1>Список вакансий</h1>
      <button 
        v-if="authStore.user?.role === 'MANAGER'" 
        @click="$router.push('/vacancies/new')"
      >
        Создать вакансию
      </button>
      <ul>
        <li v-for="vacancy in vacancies" :key="vacancy.id">
          <h3>{{ vacancy.title }}</h3>
          <p>{{ vacancy.description }}</p>
          <span>Статус: {{ vacancy.status }}</span>
        </li>
      </ul>
    </div>
  </template>
  
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
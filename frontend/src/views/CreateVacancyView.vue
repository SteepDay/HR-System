<template>
    <form @submit.prevent="submitForm">
      <input v-model="form.title" placeholder="Название" required>
      <textarea v-model="form.description" placeholder="Описание" required></textarea>
      <button type="submit">Создать</button>
    </form>
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
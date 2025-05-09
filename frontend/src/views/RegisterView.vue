<template>
  <form @submit.prevent="submitForm">
    <input v-model="form.email" type="email" placeholder="Email" required>
    <input v-model="form.password" type="password" placeholder="Пароль" required>
    <select v-model="form.role">
      <option value="HR">HR</option>
      <option value="MANAGER">Руководитель</option>
    </select>
    <button type="submit">Зарегистрироваться</button>
  </form>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const form = ref({
  email: '',
  password: '',
  role: 'HR'
})
const router = useRouter()

const submitForm = async () => {
  try {
    await axios.post('http://localhost:8000/api/auth/register/', form.value)
    router.push('/login')
  } catch (error) {
    console.error('Ошибка:', error.response?.data)
  }
}
</script>
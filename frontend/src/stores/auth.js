import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null,
  }),
  actions: {
    async login(email, password) {
        try {
          const response = await axios.post('http://localhost:8000/api/auth/login/', {
            email,
            password
          }, {
            headers: {
              'Content-Type': 'application/json'
            }
          })
          
          if (response.data.access) {
            this.token = response.data.access
            this.user = {
              email: response.data.email,
              role: response.data.role
            }
            localStorage.setItem('token', response.data.access)
            return true
          }
          return false
        } catch (error) {
          console.error('Login error:', error.response?.data || error.message)
          throw error  // Пробрасываем ошибку для обработки в компоненте
        }
    }
  }
})
<template>
  <div class="card dashboard-card">
    <div class="user-header">
      <h1>Личный кабинет</h1>
      <span class="user-badge" :class="user?.role.toLowerCase()">
        {{ user?.role }}
      </span>
    </div>
    
    <div class="user-info">
      <div class="info-item">
        <label>Email:</label>
        <p>{{ user?.email }}</p>
      </div>
      
      <div class="info-item">
        <label>Дата регистрации:</label>
        <p>{{ new Date().toLocaleDateString() }}</p>
      </div>
    </div>
    
    <button @click="logout" class="btn btn-danger">
      <i class="icon-logout"></i> Выйти
    </button>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const user = authStore.user

const logout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.dashboard-card {
  max-width: 600px;
  margin: 2rem auto;
  padding: 2.5rem 2rem;
}

.user-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.user-badge {
  padding: 0.3rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 500;
}

.user-badge.hr {
  background: #d4edda;
  color: #155724;
}

.user-badge.manager {
  background: #cce5ff;
  color: #004085;
}

.user-info {
  margin: 2rem 0;
}

.info-item {
  margin-bottom: 1.5rem;
}

.info-item label {
  display: block;
  font-weight: 500;
  color: var(--secondary);
  margin-bottom: 0.3rem;
}

.info-item p {
  font-size: 1.1rem;
}

.btn {
  display: block;
  margin: 2rem auto 0 auto;
  min-width: 180px;
  font-weight: 700;
  text-align: center;
}

.btn-danger {
  background: var(--danger);
  color: #fff;
  border: none;
  border-radius: 6px;
  box-shadow: 0 2px 8px rgba(231,76,60,0.14);
  transition: background 0.3s, box-shadow 0.3s, transform 0.2s;
}

.btn-danger:hover, .btn-danger:focus {
  background: #c0392b;
  color: #fff;
  box-shadow: 0 4px 24px 0 rgba(231,76,60,0.22);
  transform: scale(1.045);
}
</style>
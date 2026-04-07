import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import * as api from '../services/api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('token') || null)

  const isLoggedIn = computed(() => !!token.value)

  async function login(email, password) {
    const res = await api.login(email, password)
    token.value = res.data.token
    user.value = res.data.user
    localStorage.setItem('token', res.data.token)
  }

  async function register(name, email, password) {
    const res = await api.register(name, email, password)
    token.value = res.data.token
    user.value = res.data.user
    localStorage.setItem('token', res.data.token)
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
  }

  async function fetchMe() {
    try {
      const res = await api.getMe()
      user.value = res.data.user || res.data
    } catch {
      logout()
    }
  }

  return { user, token, isLoggedIn, login, register, logout, fetchMe }
})

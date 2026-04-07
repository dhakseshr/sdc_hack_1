import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import * as api from '../services/api'

export const useSearchStore = defineStore('search', () => {
  const results = ref({
    users: [],
    projects: [],
    opportunities: [],
  })
  const loading = ref(false)
  const lastQuery = ref('')

  async function search(query, type = 'all') {
    if (!query || query.length < 2) {
      results.value = { users: [], projects: [], opportunities: [] }
      return
    }

    loading.value = true
    lastQuery.value = query

    try {
      const res = await api.globalSearch(query, type)
      results.value = res.data.results || { users: [], projects: [], opportunities: [] }
    } catch (error) {
      console.error('Search failed:', error)
      results.value = { users: [], projects: [], opportunities: [] }
    } finally {
      loading.value = false
    }
  }

  async function searchUsers(query, skill = '') {
    loading.value = true
    try {
      const res = await api.searchUsers(query, skill)
      results.value.users = res.data.users || []
    } catch (error) {
      console.error('User search failed:', error)
      results.value.users = []
    } finally {
      loading.value = false
    }
  }

  async function searchProjectsByTech(tech) {
    loading.value = true
    try {
      const res = await api.searchProjectsByTech(tech)
      results.value.projects = res.data.projects || []
    } catch (error) {
      console.error('Tech search failed:', error)
      results.value.projects = []
    } finally {
      loading.value = false
    }
  }

  function clearSearch() {
    results.value = { users: [], projects: [], opportunities: [] }
    lastQuery.value = ''
  }

  return {
    results,
    loading,
    lastQuery,
    search,
    searchUsers,
    searchProjectsByTech,
    clearSearch,
  }
})

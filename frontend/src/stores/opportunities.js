import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as api from '../services/api'

export const useOpportunitiesStore = defineStore('opportunities', () => {
  const opportunities = ref([])
  const loading = ref(false)

  async function fetchOpportunities() {
    loading.value = true
    try {
      const res = await api.getOpportunities()
      opportunities.value = res.data.opportunities || res.data
    } catch (err) {
      console.error('Failed to fetch opportunities:', err)
      opportunities.value = []
    } finally {
      loading.value = false
    }
  }

  async function createOpportunity(data) {
    const res = await api.createOpportunity(data)
    opportunities.value.unshift(res.data.opportunity || res.data)
    return res.data
  }

  return { opportunities, loading, fetchOpportunities, createOpportunity }
})

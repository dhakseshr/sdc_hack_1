import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as api from '../services/api'

export const useProjectsStore = defineStore('projects', () => {
  const projects = ref([])
  const loading = ref(false)

  async function fetchProjects() {
    loading.value = true
    try {
      const res = await api.getProjects()
      projects.value = res.data.projects || res.data
    } catch (err) {
      console.error('Failed to fetch projects:', err)
      projects.value = []
    } finally {
      loading.value = false
    }
  }

  async function createProject(data) {
    const res = await api.createProject(data)
    projects.value.unshift(res.data.project || res.data)
    return res.data
  }

  async function joinProject(id) {
    await api.joinProject(id)
    const idx = projects.value.findIndex((p) => p._id === id || p.id === id)
    if (idx !== -1) {
      const p = { ...projects.value[idx] }
      p.memberCount = (p.memberCount || 0) + 1
      p.isMember = true
      projects.value[idx] = p
    }
  }

  async function leaveProject(id) {
    await api.leaveProject(id)
    const idx = projects.value.findIndex((p) => p._id === id || p.id === id)
    if (idx !== -1) {
      const p = { ...projects.value[idx] }
      p.memberCount = Math.max((p.memberCount || 1) - 1, 0)
      p.isMember = false
      projects.value[idx] = p
    }
  }

  return { projects, loading, fetchProjects, createProject, joinProject, leaveProject }
})

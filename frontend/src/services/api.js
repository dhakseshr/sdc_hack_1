import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:5000',
  headers: { 'Content-Type': 'application/json' },
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/'
    }
    return Promise.reject(error)
  }
)

// Auth
export const login = (email, password) =>
  api.post('/api/auth/login', { email, password })

export const register = (name, email, password) =>
  api.post('/api/auth/register', { name, email, password })

export const getMe = () => api.get('/api/auth/me')

export const updateProfile = (data) => api.put('/api/users/me', data)

// Users
export const getUsers = () => api.get('/api/users')

export const getUser = (id) => api.get(`/api/users/${id}`)

// Projects
export const getProjects = () => api.get('/api/projects')

export const createProject = (data) => api.post('/api/projects', data)

export const joinProject = (id) => api.post(`/api/projects/${id}/join`)

export const leaveProject = (id) => api.delete(`/api/projects/${id}/leave`)

export const getProjectDetail = (id) => api.get(`/api/projects/${id}`)

export const updateProject = (id, data) => api.put(`/api/projects/${id}`, data)

// Project Comments
export const getProjectComments = (projectId) =>
  api.get(`/api/comments/project/${projectId}`)

export const createProjectComment = (projectId, content) =>
  api.post(`/api/comments/project/${projectId}`, { content })

export const updateComment = (commentId, content) =>
  api.put(`/api/comments/${commentId}`, { content })

export const deleteComment = (commentId) =>
  api.delete(`/api/comments/${commentId}`)

// Opportunities
export const getOpportunities = () => api.get('/api/opportunities')

export const createOpportunity = (data) => api.post('/api/opportunities', data)

export const deleteOpportunity = (id) => api.delete(`/api/opportunities/${id}`)

export const respondToOpportunity = (oppId, message) =>
  api.post(`/api/opportunities/${oppId}/respond`, { message })

export const getOpportunityResponses = (oppId) =>
  api.get(`/api/opportunities/${oppId}/responses`)

// Feed
export const getFeed = () => api.get('/api/feed')

// Notifications
export const getNotifications = (unread = false) =>
  api.get(`/api/notifications?unread=${unread}`)

export const markNotificationRead = (id) =>
  api.put(`/api/notifications/${id}/read`)

export const markAllRead = () => api.put('/api/notifications/read-all')

export const deleteNotification = (id) =>
  api.delete(`/api/notifications/${id}`)

// Search
export const globalSearch = (query, type = 'all') =>
  api.get(`/api/search?q=${query}&type=${type}`)

export const searchUsers = (query, skill = '') =>
  api.get(`/api/search/users?q=${query}&skill=${skill}`)

export const searchProjectsByTech = (tech) =>
  api.get(`/api/search/projects/by-tech?tech=${tech}`)

export default api

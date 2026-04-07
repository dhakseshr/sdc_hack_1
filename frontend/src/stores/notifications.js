import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import * as api from '../services/api'

export const useNotificationsStore = defineStore('notifications', () => {
  const notifications = ref([])
  const unreadCount = ref(0)
  const loading = ref(false)

  async function fetchNotifications(unread = false) {
    loading.value = true
    try {
      const res = await api.getNotifications(unread)
      notifications.value = res.data.notifications || []
      unreadCount.value = res.data.unread_count || 0
    } catch (error) {
      console.error('Failed to fetch notifications:', error)
    } finally {
      loading.value = false
    }
  }

  async function markAsRead(id) {
    try {
      await api.markNotificationRead(id)
      const notif = notifications.value.find(n => n.id === id)
      if (notif) notif.read = true
      unreadCount.value = Math.max(0, unreadCount.value - 1)
    } catch (error) {
      console.error('Failed to mark as read:', error)
    }
  }

  async function markAllRead() {
    try {
      await api.markAllRead()
      notifications.value.forEach(n => (n.read = true))
      unreadCount.value = 0
    } catch (error) {
      console.error('Failed to mark all as read:', error)
    }
  }

  async function deleteNotification(id) {
    try {
      await api.deleteNotification(id)
      const index = notifications.value.findIndex(n => n.id === id)
      if (index > -1) {
        const wasUnread = !notifications.value[index].read
        notifications.value.splice(index, 1)
        if (wasUnread) unreadCount.value = Math.max(0, unreadCount.value - 1)
      }
    } catch (error) {
      console.error('Failed to delete notification:', error)
    }
  }

  return {
    notifications,
    unreadCount,
    loading,
    fetchNotifications,
    markAsRead,
    markAllRead,
    deleteNotification,
  }
})

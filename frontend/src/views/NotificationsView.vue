<template>
  <div class="page-wrapper">
    <!-- Header -->
    <div class="page-header">
      <div>
        <h1 class="page-title">Notifications</h1>
        <p class="page-sub">Stay updated with project and opportunity activities</p>
      </div>
      <button v-if="notificationsStore.unreadCount > 0" class="btn btn-secondary btn-sm" @click="markAllRead">
        Mark all as read
      </button>
    </div>

    <!-- Filters -->
    <div class="notification-filters">
      <button
        v-for="filter in ['all', 'unread']"
        :key="filter"
        :class="['filter-btn', { active: activeFilter === filter }]"
        @click="activeFilter = filter"
      >
        <span v-if="filter === 'unread'" class="unread-badge">{{ notificationsStore.unreadCount }}</span>
        {{ filter === 'all' ? 'All Notifications' : 'Unread' }}
      </button>
    </div>

    <!-- Loading -->
    <div v-if="notificationsStore.loading" class="notifications-list">
      <div v-for="i in 5" :key="i" class="skeleton-card" style="height: 80px;"></div>
    </div>

    <!-- Empty state -->
    <div v-else-if="filteredNotifications.length === 0" class="empty-state">
      <div class="empty-icon">🔔</div>
      <h3>{{ activeFilter === 'unread' ? 'No unread notifications' : 'No notifications yet' }}</h3>
      <p>You're all caught up!</p>
    </div>

    <!-- Notifications -->
    <div v-else class="notifications-list">
      <div
        v-for="notif in filteredNotifications"
        :key="notif.id"
        :class="['notification-item', { unread: !notif.read }]"
      >
        <div class="notif-icon">{{ getNotificationIcon(notif.type) }}</div>

        <div class="notif-content">
          <div class="notif-header">
            <h3 class="notif-title">{{ notif.title }}</h3>
            <span class="notif-time">{{ formatRelativeDate(notif.created_at) }}</span>
          </div>
          <p class="notif-message">{{ notif.message }}</p>
        </div>

        <div class="notif-actions">
          <button v-if="!notif.read" class="btn-link" @click="markAsRead(notif.id)">Mark read</button>
          <button class="btn-link text-danger" @click="deleteNotification(notif.id)">Delete</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useNotificationsStore } from '../stores/notifications'
import { formatRelativeDate } from '../utils/dateFormatter'

const notificationsStore = useNotificationsStore()
const activeFilter = ref('all')

const filteredNotifications = computed(() => {
  if (activeFilter.value === 'unread') {
    return notificationsStore.notifications.filter(n => !n.read)
  }
  return notificationsStore.notifications
})

function getNotificationIcon(type) {
  const icons = {
    project_invite: '📬',
    joined_project: '👥',
    new_comment: '💬',
    opp_response: '✉️',
  }
  return icons[type] || '🔔'
}

async function markAsRead(id) {
  await notificationsStore.markAsRead(id)
}

async function markAllRead() {
  await notificationsStore.markAllRead()
}

async function deleteNotification(id) {
  await notificationsStore.deleteNotification(id)
}

onMounted(() => {
  notificationsStore.fetchNotifications()
})
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.notification-filters {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
}

.filter-btn {
  padding: 8px 16px;
  border: 1px solid var(--border-color);
  background: var(--bg-elevated);
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s;
  position: relative;
}

.filter-btn:hover {
  border-color: var(--primary-color);
}

.filter-btn.active {
  background: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
}

.unread-badge {
  display: inline-block;
  background: #ef4444;
  color: white;
  border-radius: 999px;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: 600;
  margin-right: 6px;
}

.notifications-list {
  max-width: 800px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.notification-item {
  display: flex;
  gap: 16px;
  padding: 16px;
  background: var(--bg-elevated);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  transition: all 0.2s;
}

.notification-item:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.notification-item.unread {
  background: rgba(67, 126, 235, 0.05);
  border-color: #437eeb;
}

.notif-icon {
  font-size: 2rem;
  flex-shrink: 0;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-secondary);
  border-radius: 8px;
}

.notif-content {
  flex: 1;
  min-width: 0;
}

.notif-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  gap: 12px;
  margin-bottom: 4px;
}

.notif-title {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-primary);
}

.notif-time {
  font-size: 0.85rem;
  color: var(--text-secondary);
  white-space: nowrap;
}

.notif-message {
  margin: 0;
  font-size: 0.9rem;
  color: var(--text-secondary);
}

.notif-actions {
  display: flex;
  gap: 12px;
}

.btn-link {
  background: none;
  border: none;
  color: var(--primary-color);
  cursor: pointer;
  font-size: 0.85rem;
  padding: 0;
  text-decoration: none;
}

.btn-link:hover {
  text-decoration: underline;
}

.text-danger {
  color: #dc2626;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 20px;
}

@media (max-width: 640px) {
  .page-header {
    flex-direction: column;
    align-items: start;
  }

  .notification-item {
    flex-direction: column;
    gap: 12px;
  }

  .notif-header {
    flex-direction: column;
  }

  .notif-time {
    white-space: normal;
  }

  .notif-actions {
    justify-content: flex-start;
  }
}
</style>

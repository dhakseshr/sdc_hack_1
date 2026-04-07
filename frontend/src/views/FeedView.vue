<template>
  <div class="page-wrapper">
    <div class="feed-layout">
      <!-- Main feed column -->
      <div class="feed-main">
        <!-- Header -->
        <div class="feed-header">
          <div class="header-left">
            <h1 class="page-title">Community Feed</h1>
            <div class="live-indicator">
              <span class="live-dot"></span>
              <span class="live-text">Live</span>
            </div>
          </div>
          <button class="btn btn-secondary btn-sm" @click="feedStore.fetchFeed()">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="23 4 23 10 17 10"/><path d="M20.49 15a9 9 0 1 1-.08-4.67"/></svg>
            Refresh
          </button>
        </div>

        <!-- Loading skeletons -->
        <div v-if="feedStore.loading" class="feed-list">
          <div v-for="i in 3" :key="i" class="skeleton-card">
            <div class="skeleton-card-top">
              <div class="skeleton skeleton-circle" style="width:40px;height:40px;"></div>
              <div style="flex:1;display:flex;flex-direction:column;gap:8px;">
                <div class="skeleton skeleton-text" style="width:40%;"></div>
                <div class="skeleton skeleton-text" style="width:25%;height:10px;"></div>
              </div>
              <div class="skeleton skeleton-text" style="width:70px;height:22px;border-radius:999px;"></div>
            </div>
            <div style="display:flex;flex-direction:column;gap:8px;margin-top:12px;">
              <div class="skeleton skeleton-text" style="width:80%;"></div>
              <div class="skeleton skeleton-text" style="width:60%;"></div>
            </div>
          </div>
        </div>

        <!-- Empty state -->
        <div v-else-if="feedStore.posts.length === 0" class="empty-state">
          <div class="empty-state-icon">📡</div>
          <h3>No activity yet</h3>
          <p>Create a project or post an opportunity to get started</p>
          <div style="margin-top:20px;display:flex;gap:12px;justify-content:center;">
            <RouterLink to="/projects" class="btn btn-primary btn-sm">Create Project</RouterLink>
            <RouterLink to="/opportunities" class="btn btn-outline btn-sm">Post Opportunity</RouterLink>
          </div>
        </div>

        <!-- Feed posts -->
        <div v-else class="feed-list">
          <TransitionGroup name="feed-item">
            <article
              v-for="post in feedStore.posts"
              :key="post._id || post.id"
              class="feed-card"
            >
              <div class="feed-card-top">
                <div class="author-row">
                  <div class="avatar avatar-sm" :style="{ background: avatarColor(post.author?.name || post.user?.name || 'U') }">
                    {{ initial(post.author?.name || post.user?.name || 'U') }}
                  </div>
                  <div class="author-info">
                    <span class="author-name">{{ post.author?.name || post.user?.name || 'Anonymous' }}</span>
                    <span class="post-time">{{ timeAgo(post.createdAt || post.created_at) }}</span>
                  </div>
                </div>
                <span :class="['badge', typeBadge(post.type)]">
                  {{ formatType(post.type) }}
                </span>
              </div>

              <div class="feed-card-body">
                <h3 class="post-title" v-if="post.title">{{ post.title }}</h3>
                <p class="post-content">{{ post.content || post.description || post.body || '' }}</p>
              </div>

              <div class="feed-card-footer" v-if="post.project || post.opportunity">
                <RouterLink
                  v-if="post.project"
                  :to="`/projects`"
                  class="linked-item"
                >
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
                  {{ post.project?.name || 'View Project' }}
                </RouterLink>
              </div>
            </article>
          </TransitionGroup>
        </div>
      </div>

      <!-- Sidebar -->
      <aside class="feed-sidebar">
        <div class="sidebar-card">
          <h3 class="sidebar-title">Quick Actions</h3>
          <div class="quick-actions">
            <RouterLink to="/projects" class="quick-action-btn">
              <div class="qa-icon qa-purple">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="3"/><path d="M9 9h6M9 12h6M9 15h4"/></svg>
              </div>
              <div>
                <div class="qa-label">New Project</div>
                <div class="qa-desc">Start collaborating</div>
              </div>
            </RouterLink>
            <RouterLink to="/opportunities" class="quick-action-btn">
              <div class="qa-icon qa-cyan">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/></svg>
              </div>
              <div>
                <div class="qa-label">Post Opportunity</div>
                <div class="qa-desc">Find teammates</div>
              </div>
            </RouterLink>
            <RouterLink to="/explore" class="quick-action-btn">
              <div class="qa-icon qa-green">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
              </div>
              <div>
                <div class="qa-label">Explore Devs</div>
                <div class="qa-desc">Discover talent</div>
              </div>
            </RouterLink>
          </div>
        </div>

        <div class="sidebar-card">
          <h3 class="sidebar-title">Your Profile</h3>
          <div class="profile-preview">
            <div class="avatar avatar-md" v-if="authStore.user">
              {{ initial(authStore.user.name) }}
            </div>
            <div class="profile-preview-info">
              <div class="profile-preview-name">{{ authStore.user?.name || 'User' }}</div>
              <div class="profile-preview-role">{{ authStore.user?.bio?.slice(0, 40) || 'No bio yet' }}</div>
            </div>
          </div>
          <RouterLink to="/profile" class="btn btn-outline btn-sm" style="width:100%;margin-top:14px;justify-content:center;">
            View Profile
          </RouterLink>
        </div>
      </aside>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useFeedStore } from '../stores/feed'
import { useAuthStore } from '../stores/auth'

const feedStore = useFeedStore()
const authStore = useAuthStore()

onMounted(() => feedStore.fetchFeed())

function timeAgo(dateStr) {
  if (!dateStr) return 'just now'
  const date = new Date(dateStr)
  const now = new Date()
  const diff = Math.floor((now - date) / 1000)
  if (diff < 60) return 'just now'
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`
  if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`
  if (diff < 604800) return `${Math.floor(diff / 86400)}d ago`
  return date.toLocaleDateString()
}

function initial(name) {
  return (name || 'U').charAt(0).toUpperCase()
}

const AVATAR_COLORS = [
  'linear-gradient(135deg, #7c6aff, #9b59b6)',
  'linear-gradient(135deg, #06b6d4, #0891b2)',
  'linear-gradient(135deg, #f59e0b, #d97706)',
  'linear-gradient(135deg, #10b981, #059669)',
  'linear-gradient(135deg, #ef4444, #dc2626)',
  'linear-gradient(135deg, #8b5cf6, #7c3aed)',
]

function avatarColor(name) {
  const idx = (name || 'U').charCodeAt(0) % AVATAR_COLORS.length
  return AVATAR_COLORS[idx]
}

function typeBadge(type) {
  const map = {
    project: 'badge-blue',
    opportunity: 'badge-green',
    announcement: 'badge-purple',
    hackathon: 'badge-yellow',
    default: 'badge-cyan',
  }
  return map[type?.toLowerCase()] || map.default
}

function formatType(type) {
  if (!type) return 'Post'
  return type.charAt(0).toUpperCase() + type.slice(1)
}
</script>

<style scoped>
/* Layout */
.feed-layout {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 28px;
  align-items: start;
}

.feed-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.page-title {
  font-size: 1.6rem;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: -0.5px;
}

.live-indicator {
  display: flex;
  align-items: center;
  gap: 6px;
  background: rgba(74, 222, 128, 0.1);
  border: 1px solid rgba(74, 222, 128, 0.25);
  border-radius: 999px;
  padding: 3px 10px;
}

.live-dot {
  width: 7px;
  height: 7px;
  background: var(--success);
  border-radius: 50%;
  animation: pulse-dot 2s ease-in-out infinite;
}

.live-text {
  font-size: 0.72rem;
  font-weight: 700;
  color: var(--success);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Feed list */
.feed-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

/* Feed card */
.feed-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 20px;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
  cursor: default;
}

.feed-card:hover {
  border-color: rgba(124, 106, 255, 0.35);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
}

.feed-card-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14px;
}

.author-row {
  display: flex;
  align-items: center;
  gap: 10px;
}

.avatar-sm {
  width: 38px;
  height: 38px;
  font-size: 0.9rem;
}

.author-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.author-name {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-primary);
}

.post-time {
  font-size: 0.75rem;
  color: var(--text-muted);
}

.feed-card-body {
  margin-bottom: 12px;
}

.post-title {
  font-size: 1rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 6px;
}

.post-content {
  font-size: 0.9rem;
  color: var(--text-secondary);
  line-height: 1.65;
}

.feed-card-footer {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid var(--border);
}

.linked-item {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 0.78rem;
  color: var(--accent);
  font-weight: 500;
  transition: opacity 0.2s;
}
.linked-item:hover { opacity: 0.75; }

/* Skeleton card */
.skeleton-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 20px;
}

.skeleton-card-top {
  display: flex;
  align-items: center;
  gap: 12px;
}

/* Sidebar */
.feed-sidebar {
  display: flex;
  flex-direction: column;
  gap: 16px;
  position: sticky;
  top: 80px;
}

.sidebar-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 20px;
}

.sidebar-title {
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.8px;
  margin-bottom: 14px;
}

.quick-actions {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.quick-action-btn {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 11px 12px;
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  text-decoration: none;
  transition: all 0.2s;
  cursor: pointer;
}

.quick-action-btn:hover {
  border-color: var(--accent);
  background: rgba(124, 106, 255, 0.06);
  transform: translateX(2px);
}

.qa-icon {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.qa-purple { background: rgba(124, 106, 255, 0.15); color: var(--accent); }
.qa-cyan { background: rgba(6, 182, 212, 0.15); color: var(--accent2); }
.qa-green { background: rgba(74, 222, 128, 0.12); color: var(--success); }

.qa-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-primary);
}

.qa-desc {
  font-size: 0.72rem;
  color: var(--text-muted);
}

/* Profile preview */
.profile-preview {
  display: flex;
  align-items: center;
  gap: 12px;
}

.avatar-md {
  width: 44px;
  height: 44px;
  font-size: 1.1rem;
}

.profile-preview-name {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-primary);
}

.profile-preview-role {
  font-size: 0.75rem;
  color: var(--text-muted);
  margin-top: 2px;
}

/* Transitions */
.feed-item-enter-active,
.feed-item-leave-active {
  transition: all 0.3s ease;
}
.feed-item-enter-from {
  opacity: 0;
  transform: translateY(12px);
}
.feed-item-leave-to {
  opacity: 0;
  transform: translateX(-12px);
}

/* Responsive */
@media (max-width: 900px) {
  .feed-layout {
    grid-template-columns: 1fr;
  }
  .feed-sidebar {
    display: none;
  }
}
</style>

<template>
  <div class="explore-page">
    <div class="page-header">
      <div>
        <h1>Explore Developers</h1>
        <p class="page-sub">Discover talented student developers to collaborate with</p>
      </div>
    </div>

    <div class="search-bar">
      <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
      <input v-model="search" class="search-input" placeholder="Search by name or skill..." />
    </div>

    <div v-if="loading" class="dev-grid">
      <div v-for="i in 8" :key="i" class="skeleton-card">
        <div class="skeleton circle sm"></div>
        <div class="skeleton line w50"></div>
        <div class="skeleton line w70"></div>
        <div class="skeleton line w40"></div>
      </div>
    </div>

    <div v-else-if="filtered.length" class="dev-grid">
      <div v-for="dev in filtered" :key="dev.id" class="dev-card card">
        <div class="dev-avatar">{{ dev.name?.[0]?.toUpperCase() }}</div>
        <h3 class="dev-name">{{ dev.name }}</h3>
        <p class="dev-bio">{{ dev.bio || 'No bio yet.' }}</p>
        <div class="dev-skills">
          <span v-for="skill in (dev.skills || []).slice(0, 4)" :key="skill" class="skill-chip">{{ skill }}</span>
          <span v-if="(dev.skills?.length || 0) > 4" class="skill-more">+{{ dev.skills.length - 4 }}</span>
        </div>
        <RouterLink :to="`/profile/${dev.id}`" class="btn btn-outline btn-sm view-btn">View Profile</RouterLink>
      </div>
    </div>

    <div v-else class="empty-state">
      <div class="empty-icon">🔍</div>
      <h3>No developers found</h3>
      <p>Try a different search term</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getUsers } from '../services/api'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
const search = ref('')
const users = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const res = await getUsers()
    users.value = (res.data.users || res.data).filter(u => u.id !== authStore.user?.id)
  } catch {
    users.value = []
  } finally {
    loading.value = false
  }
})

const filtered = computed(() => {
  if (!search.value) return users.value
  const q = search.value.toLowerCase()
  return users.value.filter(u =>
    u.name?.toLowerCase().includes(q) ||
    (u.skills || []).some(s => s.toLowerCase().includes(q)) ||
    u.bio?.toLowerCase().includes(q)
  )
})
</script>

<style scoped>
.page-header { margin-bottom: 24px; }
.page-header h1 { font-size: 1.6rem; font-weight: 800; }
.page-sub { font-size: 0.875rem; color: var(--text-muted); margin-top: 4px; }

.search-bar {
  position: relative; margin-bottom: 28px;
}

.search-icon {
  position: absolute; left: 14px; top: 50%; transform: translateY(-50%);
  color: var(--text-muted); pointer-events: none;
}

.search-input {
  width: 100%; max-width: 480px;
  padding: 11px 14px 11px 42px;
  background: var(--bg-card); border: 1.5px solid var(--border);
  border-radius: var(--radius-sm); color: var(--text-primary); font-size: 0.9rem;
  transition: border-color 0.2s;
}

.search-input:focus { outline: none; border-color: var(--accent); }
.search-input::placeholder { color: var(--text-muted); }

.dev-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 16px;
}

.dev-card {
  display: flex; flex-direction: column; align-items: center;
  text-align: center; padding: 24px 20px; gap: 10px;
}

.dev-avatar {
  width: 64px; height: 64px;
  background: linear-gradient(135deg, var(--accent), #06b6d4);
  border-radius: 18px;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.5rem; font-weight: 800; color: white;
}

.dev-name { font-size: 1rem; font-weight: 700; color: var(--text-primary); }

.dev-bio {
  font-size: 0.8rem; color: var(--text-secondary); line-height: 1.5;
  display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;
}

.dev-skills { display: flex; flex-wrap: wrap; gap: 4px; justify-content: center; }

.skill-chip {
  background: rgba(124,106,255,0.12); color: #a98eff;
  border: 1px solid rgba(124,106,255,0.2); padding: 2px 8px;
  border-radius: 4px; font-size: 0.7rem; font-weight: 500;
}

.skill-more { font-size: 0.7rem; color: var(--text-muted); padding: 2px 0; }

.view-btn { width: 100%; justify-content: center; margin-top: 4px; }

/* Skeleton */
.skeleton-card {
  background: var(--bg-card); border: 1px solid var(--border);
  border-radius: 16px; padding: 24px 20px;
  display: flex; flex-direction: column; align-items: center; gap: 10px;
}

.skeleton { background: linear-gradient(90deg, var(--bg-elevated) 25%, rgba(255,255,255,0.06) 50%, var(--bg-elevated) 75%); background-size: 200% 100%; animation: shimmer 1.4s infinite; border-radius: 6px; }
.skeleton.circle.sm { width: 64px; height: 64px; border-radius: 18px; }
.skeleton.line { height: 12px; }
.skeleton.w50 { width: 50%; }
.skeleton.w70 { width: 70%; }
.skeleton.w40 { width: 40%; }
@keyframes shimmer { to { background-position: -200% 0; } }

.empty-state { text-align: center; padding: 60px 20px; }
.empty-icon { font-size: 3rem; margin-bottom: 16px; }
.empty-state h3 { font-size: 1.1rem; color: var(--text-secondary); margin-bottom: 8px; }
.empty-state p { color: var(--text-muted); font-size: 0.875rem; }
</style>

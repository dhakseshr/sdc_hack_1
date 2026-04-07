<template>
  <div class="page-wrapper">
    <!-- Header -->
    <div class="page-header">
      <div>
        <h1 class="page-title">Opportunity Board</h1>
        <p class="page-sub">Find hackathon teams, project roles, and collaborators</p>
      </div>
      <button class="btn btn-primary" @click="showModal = true">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
        Post Opportunity
      </button>
    </div>

    <!-- Tabs -->
    <div class="tabs-row">
      <button
        v-for="tab in TABS"
        :key="tab.value"
        :class="['tab-btn', { active: activeTab === tab.value }]"
        @click="activeTab = tab.value"
      >
        <span class="tab-icon">{{ tab.icon }}</span>
        {{ tab.label }}
        <span class="tab-count" v-if="countByTab(tab.value) > 0">{{ countByTab(tab.value) }}</span>
      </button>
    </div>

    <!-- Loading skeletons -->
    <div v-if="oppsStore.loading" class="opps-list">
      <div v-for="i in 4" :key="i" class="skeleton-card">
        <div style="display:flex;justify-content:space-between;margin-bottom:12px;">
          <div class="skeleton" style="width:100px;height:22px;border-radius:999px;"></div>
          <div class="skeleton skeleton-text" style="width:60px;height:12px;"></div>
        </div>
        <div class="skeleton skeleton-text" style="width:65%;height:18px;margin-bottom:10px;"></div>
        <div class="skeleton skeleton-text" style="width:90%;margin-bottom:6px;"></div>
        <div class="skeleton skeleton-text" style="width:75%;margin-bottom:16px;"></div>
        <div style="display:flex;justify-content:space-between;align-items:center;">
          <div class="skeleton skeleton-text" style="width:120px;height:12px;"></div>
          <div class="skeleton" style="width:90px;height:32px;border-radius:6px;"></div>
        </div>
      </div>
    </div>

    <!-- Empty state -->
    <div v-else-if="filteredOpps.length === 0" class="empty-state">
      <div class="empty-state-icon">📋</div>
      <h3>No opportunities here yet</h3>
      <p>Be the first to post an opportunity in this category!</p>
      <button class="btn btn-primary" style="margin-top:20px;" @click="showModal = true">Post Opportunity</button>
    </div>

    <!-- Opportunities list -->
    <div v-else class="opps-list">
      <article
        v-for="opp in filteredOpps"
        :key="opp._id || opp.id"
        class="opp-card"
      >
        <div class="opp-card-top">
          <span :class="['badge', categoryBadge(opp.category)]">
            {{ opp.category || 'General' }}
          </span>
          <span class="opp-time">{{ timeAgo(opp.createdAt || opp.created_at) }}</span>
        </div>

        <h3 class="opp-title">{{ opp.title }}</h3>
        <p class="opp-desc">{{ opp.description }}</p>

        <div class="opp-card-footer">
          <div class="opp-author">
            <div class="avatar avatar-xs" :style="{ background: avatarColor(opp.author?.name || opp.user?.name || 'U') }">
              {{ initial(opp.author?.name || opp.user?.name || 'U') }}
            </div>
            <span>{{ opp.author?.name || opp.user?.name || 'Anonymous' }}</span>
          </div>
          <button
            class="btn btn-sm"
            :class="interested.has(opp._id || opp.id) ? 'btn-success' : 'btn-outline'"
            @click="toggleInterest(opp._id || opp.id)"
          >
            {{ interested.has(opp._id || opp.id) ? '✓ Interested' : "I'm Interested" }}
          </button>
        </div>
      </article>
    </div>

    <!-- Post Opportunity Modal -->
    <Teleport to="body">
      <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
        <div class="modal" role="dialog" aria-modal="true">
          <div class="modal-header">
            <h2>Post an Opportunity</h2>
            <button class="modal-close" @click="closeModal">✕</button>
          </div>

          <form @submit.prevent="handleCreate">
            <div class="form-group">
              <label class="form-label">Title *</label>
              <input
                v-model="newOpp.title"
                class="form-input"
                placeholder="e.g. Looking for React dev for fintech startup"
                required
              />
            </div>

            <div class="form-group">
              <label class="form-label">Category *</label>
              <select v-model="newOpp.category" class="form-input" required>
                <option value="">Select a category...</option>
                <option value="Looking for Teammates">Looking for Teammates</option>
                <option value="Project Roles">Project Roles</option>
                <option value="Hackathons">Hackathons</option>
              </select>
            </div>

            <div class="form-group">
              <label class="form-label">Description *</label>
              <textarea
                v-model="newOpp.description"
                class="form-input"
                placeholder="Describe the opportunity, what skills are needed, and how to get in touch..."
                required
              ></textarea>
            </div>

            <div v-if="createError" class="error-banner">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
              {{ createError }}
            </div>

            <div class="modal-actions">
              <button type="button" class="btn btn-secondary" @click="closeModal">Cancel</button>
              <button type="submit" class="btn btn-primary" :disabled="createLoading">
                <span v-if="createLoading" class="btn-spinner"></span>
                {{ createLoading ? 'Posting...' : 'Post Opportunity' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useOpportunitiesStore } from '../stores/opportunities'

const oppsStore = useOpportunitiesStore()

const TABS = [
  { value: 'all', label: 'All', icon: '◎' },
  { value: 'Looking for Teammates', label: 'Teammates', icon: '🤝' },
  { value: 'Project Roles', label: 'Project Roles', icon: '⚙️' },
  { value: 'Hackathons', label: 'Hackathons', icon: '⚡' },
]

const activeTab = ref('all')
const showModal = ref(false)
const createLoading = ref(false)
const createError = ref('')
const interested = ref(new Set())

const newOpp = ref({ title: '', description: '', category: '' })

onMounted(() => oppsStore.fetchOpportunities())

const filteredOpps = computed(() => {
  if (activeTab.value === 'all') return oppsStore.opportunities
  return oppsStore.opportunities.filter((o) => o.category === activeTab.value)
})

function countByTab(tab) {
  if (tab === 'all') return oppsStore.opportunities.length
  return oppsStore.opportunities.filter((o) => o.category === tab).length
}

function categoryBadge(category) {
  return {
    'Hackathons': 'badge-purple',
    'Project Roles': 'badge-blue',
    'Looking for Teammates': 'badge-green',
  }[category] || 'badge-cyan'
}

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
]

function avatarColor(name) {
  return AVATAR_COLORS[(name || 'U').charCodeAt(0) % AVATAR_COLORS.length]
}

function toggleInterest(id) {
  const s = new Set(interested.value)
  if (s.has(id)) s.delete(id)
  else s.add(id)
  interested.value = s
}

function closeModal() {
  showModal.value = false
  createError.value = ''
  newOpp.value = { title: '', description: '', category: '' }
}

async function handleCreate() {
  createError.value = ''
  createLoading.value = true
  try {
    await oppsStore.createOpportunity({ ...newOpp.value })
    closeModal()
  } catch (err) {
    createError.value = err.response?.data?.message || 'Failed to post opportunity.'
  } finally {
    createLoading.value = false
  }
}
</script>

<style scoped>
.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 28px;
}
.page-title {
  font-size: 1.8rem;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: -0.5px;
}
.page-sub {
  font-size: 0.875rem;
  color: var(--text-muted);
  margin-top: 4px;
}

/* Tabs */
.tabs-row {
  display: flex;
  gap: 8px;
  margin-bottom: 28px;
  flex-wrap: wrap;
}
.tab-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border-radius: 999px;
  font-size: 0.85rem;
  font-weight: 600;
  background: var(--bg-elevated);
  border: 1.5px solid var(--border);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s;
}
.tab-btn:hover { border-color: var(--accent); color: var(--accent); }
.tab-btn.active {
  background: rgba(124, 106, 255, 0.15);
  border-color: var(--accent);
  color: var(--accent);
}
.tab-icon { font-size: 0.9rem; }
.tab-count {
  background: rgba(124, 106, 255, 0.2);
  color: var(--accent);
  border-radius: 999px;
  padding: 0 6px;
  font-size: 0.72rem;
  font-weight: 700;
  min-width: 18px;
  text-align: center;
}

/* List */
.opps-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

/* Opp card */
.opp-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 22px;
  transition: border-color 0.2s ease, box-shadow 0.2s ease, transform 0.2s ease;
}
.opp-card:hover {
  border-color: rgba(124, 106, 255, 0.4);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
  transform: translateY(-1px);
}
.opp-card-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}
.opp-time { font-size: 0.75rem; color: var(--text-muted); }
.opp-title {
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 8px;
  line-height: 1.35;
}
.opp-desc {
  font-size: 0.875rem;
  color: var(--text-secondary);
  line-height: 1.65;
  margin-bottom: 16px;
}
.opp-card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 14px;
  border-top: 1px solid var(--border);
}
.opp-author {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.82rem;
  color: var(--text-secondary);
  font-weight: 500;
}
.avatar-xs {
  width: 26px;
  height: 26px;
  font-size: 0.7rem;
}
.btn-success {
  background: rgba(74, 222, 128, 0.12) !important;
  border-color: var(--success) !important;
  color: var(--success) !important;
}

/* Skeleton */
.skeleton-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 22px;
}

/* Modal */
.error-banner {
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(248, 113, 113, 0.1);
  border: 1px solid rgba(248, 113, 113, 0.25);
  color: var(--danger);
  padding: 10px 14px;
  border-radius: var(--radius-sm);
  font-size: 0.85rem;
  margin-bottom: 12px;
}
.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 8px;
}
.btn-spinner {
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

@media (max-width: 600px) {
  .page-header { flex-direction: column; }
  .tabs-row { gap: 6px; }
  .tab-btn { padding: 7px 12px; font-size: 0.8rem; }
}
</style>

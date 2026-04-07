<template>
  <div class="page-wrapper">
    <!-- Header -->
    <div class="page-header">
      <div>
        <h1 class="page-title">Projects</h1>
        <p class="page-sub">Collaborate on real projects with student developers</p>
      </div>
      <button class="btn btn-primary" @click="showModal = true">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
        New Project
      </button>
    </div>

    <!-- Filters -->
    <div class="filters-row">
      <div class="search-wrapper">
        <svg class="search-icon" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
        <input v-model="search" class="search-input" placeholder="Search projects..." />
      </div>
      <select v-model="stackFilter" class="filter-select form-input">
        <option value="">All Tech Stacks</option>
        <option v-for="tech in allTechs" :key="tech" :value="tech">{{ tech }}</option>
      </select>
      <select v-model="statusFilter" class="filter-select form-input">
        <option value="">All Status</option>
        <option value="active">Active</option>
        <option value="recruiting">Recruiting</option>
        <option value="completed">Completed</option>
      </select>
    </div>

    <!-- Loading skeletons -->
    <div v-if="projectsStore.loading" class="projects-grid">
      <div v-for="i in 6" :key="i" class="skeleton-card">
        <div style="display:flex;justify-content:space-between;margin-bottom:14px;">
          <div class="skeleton skeleton-text" style="width:55%;height:18px;"></div>
          <div class="skeleton" style="width:70px;height:22px;border-radius:999px;"></div>
        </div>
        <div class="skeleton skeleton-text" style="width:90%;margin-bottom:8px;"></div>
        <div class="skeleton skeleton-text" style="width:70%;margin-bottom:16px;"></div>
        <div style="display:flex;gap:6px;margin-bottom:16px;">
          <div v-for="j in 3" :key="j" class="skeleton" style="width:56px;height:22px;border-radius:999px;"></div>
        </div>
        <div style="display:flex;justify-content:space-between;align-items:center;">
          <div class="skeleton skeleton-text" style="width:30%;height:12px;"></div>
          <div style="display:flex;gap:8px;">
            <div class="skeleton" style="width:60px;height:30px;border-radius:6px;"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty state -->
    <div v-else-if="filteredProjects.length === 0" class="empty-state">
      <div class="empty-state-icon">🔭</div>
      <h3>No projects found</h3>
      <p v-if="search || stackFilter || statusFilter">Try adjusting your filters</p>
      <p v-else>Be the first to create a project!</p>
      <button class="btn btn-primary" style="margin-top:20px;" @click="showModal = true">Create Project</button>
    </div>

    <!-- Projects grid -->
    <div v-else class="projects-grid">
      <article
        v-for="project in filteredProjects"
        :key="project._id || project.id"
        class="project-card"
      >
        <div class="project-card-top">
          <RouterLink :to="`/projects/${project.id}`">
            <h3 class="project-name">{{ project.name }}</h3>
          </RouterLink>
          <span :class="['badge', statusBadge(project.status)]">{{ project.status || 'active' }}</span>
        </div>

        <p class="project-desc">{{ truncate(project.description, 110) }}</p>

        <div class="tech-chips">
          <span
            v-for="tech in (project.stack || project.techStack || [])"
            :key="tech"
            class="tech-chip"
          >{{ tech }}</span>
        </div>

        <div class="project-card-footer">
          <div class="member-count">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
            {{ project.memberCount || (project.members?.length) || 0 }} members
          </div>
          <div class="project-actions">
            <RouterLink :to="`/projects/${project.id}`" class="btn btn-primary btn-sm">View</RouterLink>
            <button
              v-if="project.isMember || isProjectMember(project)"
              class="btn btn-danger btn-sm"
              :disabled="actionLoading === (project._id || project.id)"
              @click="handleLeave(project)"
            >
              {{ actionLoading === (project._id || project.id) ? '...' : 'Leave' }}
            </button>
            <button
              v-else
              class="btn btn-outline btn-sm"
              :disabled="actionLoading === (project._id || project.id)"
              @click="handleJoin(project)"
            >
              {{ actionLoading === (project._id || project.id) ? '...' : 'Join' }}
            </button>
          </div>
        </div>

        <p v-if="actionError === (project._id || project.id)" class="project-error">
          Action failed. Please try again.
        </p>
      </article>
    </div>

    <!-- Create Project Modal -->
    <Teleport to="body">
      <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
        <div class="modal" role="dialog" aria-modal="true">
          <div class="modal-header">
            <h2>Create New Project</h2>
            <button class="modal-close" @click="closeModal">✕</button>
          </div>

          <form @submit.prevent="handleCreate">
            <div class="form-group">
              <label class="form-label">Project Name *</label>
              <input v-model="newProject.name" class="form-input" placeholder="e.g. CampusNav, StudySync..." required />
            </div>

            <div class="form-group">
              <label class="form-label">Description *</label>
              <textarea v-model="newProject.description" class="form-input" placeholder="What are you building and who is it for?" required></textarea>
            </div>

            <div class="form-group">
              <label class="form-label">Tech Stack</label>
              <div class="tags-row" v-if="newProject.stack.length > 0">
                <span v-for="(tech, i) in newProject.stack" :key="i" class="chip">
                  {{ tech }}
                  <span class="chip-remove" @click="removeTech(i)">✕</span>
                </span>
              </div>
              <input
                v-model="techInput"
                class="form-input"
                :style="{ marginTop: newProject.stack.length ? '8px' : '0' }"
                placeholder="Type tech and press Enter (e.g. Vue, Python...)"
                @keydown.enter.prevent="addTech"
              />
              <p class="input-hint">Press Enter to add each technology</p>
            </div>

            <div class="form-group">
              <label class="form-label">Status</label>
              <select v-model="newProject.status" class="form-input">
                <option value="recruiting">Recruiting</option>
                <option value="active">Active</option>
                <option value="completed">Completed</option>
              </select>
            </div>

            <div v-if="createError" class="error-banner">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
              {{ createError }}
            </div>

            <div class="modal-actions">
              <button type="button" class="btn btn-secondary" @click="closeModal">Cancel</button>
              <button type="submit" class="btn btn-primary" :disabled="createLoading">
                <span v-if="createLoading" class="btn-spinner"></span>
                {{ createLoading ? 'Creating...' : 'Create Project' }}
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
import { RouterLink } from 'vue-router'
import { useProjectsStore } from '../stores/projects'
import { useAuthStore } from '../stores/auth'

const projectsStore = useProjectsStore()
const authStore = useAuthStore()

const search = ref('')
const stackFilter = ref('')
const statusFilter = ref('')
const showModal = ref(false)
const createLoading = ref(false)
const createError = ref('')
const actionLoading = ref(null)
const actionError = ref(null)
const techInput = ref('')

const newProject = ref({ name: '', description: '', stack: [], status: 'recruiting' })

onMounted(() => projectsStore.fetchProjects())

const allTechs = computed(() => {
  const set = new Set()
  projectsStore.projects.forEach((p) => {
    ;(p.stack || p.techStack || []).forEach((t) => set.add(t))
  })
  return Array.from(set).sort()
})

const filteredProjects = computed(() =>
  projectsStore.projects.filter((p) => {
    const q = search.value.toLowerCase()
    const matchSearch = !q || p.name?.toLowerCase().includes(q) || p.description?.toLowerCase().includes(q)
    const matchStack = !stackFilter.value || (p.stack || p.techStack || []).includes(stackFilter.value)
    const matchStatus = !statusFilter.value || p.status === statusFilter.value
    return matchSearch && matchStack && matchStatus
  })
)

function isProjectMember(project) {
  if (!authStore.user) return false
  const uid = authStore.user._id || authStore.user.id
  return (project.members || []).some((m) => (m._id || m.id || m) === uid)
}

function statusBadge(status) {
  return { active: 'badge-green', recruiting: 'badge-yellow', completed: 'badge-blue' }[status] || 'badge-cyan'
}

function truncate(str, n) {
  if (!str) return ''
  return str.length > n ? str.slice(0, n) + '…' : str
}

function addTech() {
  const t = techInput.value.trim()
  if (t && !newProject.value.stack.includes(t)) {
    newProject.value.stack.push(t)
  }
  techInput.value = ''
}

function removeTech(idx) {
  newProject.value.stack.splice(idx, 1)
}

function closeModal() {
  showModal.value = false
  createError.value = ''
  newProject.value = { name: '', description: '', stack: [], status: 'recruiting' }
  techInput.value = ''
}

async function handleCreate() {
  createError.value = ''
  createLoading.value = true
  try {
    await projectsStore.createProject({ ...newProject.value })
    closeModal()
  } catch (err) {
    createError.value = err.response?.data?.message || 'Failed to create project.'
  } finally {
    createLoading.value = false
  }
}

async function handleJoin(project) {
  const id = project._id || project.id
  actionLoading.value = id
  actionError.value = null
  try {
    await projectsStore.joinProject(id)
  } catch {
    actionError.value = id
    setTimeout(() => { actionError.value = null }, 3000)
  } finally {
    actionLoading.value = null
  }
}

async function handleLeave(project) {
  const id = project._id || project.id
  actionLoading.value = id
  actionError.value = null
  try {
    await projectsStore.leaveProject(id)
  } catch {
    actionError.value = id
    setTimeout(() => { actionError.value = null }, 3000)
  } finally {
    actionLoading.value = null
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

/* Filters */
.filters-row {
  display: flex;
  gap: 12px;
  margin-bottom: 28px;
  flex-wrap: wrap;
}
.search-wrapper {
  flex: 1;
  min-width: 200px;
  position: relative;
  display: flex;
  align-items: center;
}
.search-icon {
  position: absolute;
  left: 12px;
  color: var(--text-muted);
  pointer-events: none;
}
.search-input {
  width: 100%;
  padding: 10px 14px 10px 36px;
  background: var(--bg-elevated);
  border: 1.5px solid var(--border);
  border-radius: var(--radius-sm);
  color: var(--text-primary);
  font-size: 0.9rem;
  transition: border-color 0.2s;
  font-family: inherit;
}
.search-input:focus { border-color: var(--accent); outline: none; }
.search-input::placeholder { color: var(--text-muted); }
.filter-select { width: 160px; }

/* Grid */
.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(310px, 1fr));
  gap: 16px;
}

/* Project card */
.project-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  transition: border-color 0.2s ease, box-shadow 0.2s ease, transform 0.2s ease;
}
.project-card:hover {
  border-color: rgba(124, 106, 255, 0.4);
  box-shadow: 0 6px 28px rgba(0, 0, 0, 0.3);
  transform: translateY(-2px);
}
.project-card-top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 10px;
}
.project-name {
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1.3;
}
.project-desc {
  font-size: 0.875rem;
  color: var(--text-secondary);
  line-height: 1.6;
  flex: 1;
}
.tech-chips { display: flex; flex-wrap: wrap; gap: 6px; }
.tech-chip {
  padding: 3px 10px;
  background: rgba(59, 130, 246, 0.1);
  border: 1px solid rgba(59, 130, 246, 0.2);
  border-radius: 999px;
  font-size: 0.72rem;
  font-weight: 600;
  color: #60a5fa;
}
.project-card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 12px;
  border-top: 1px solid var(--border);
}
.member-count {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 0.78rem;
  color: var(--text-muted);
}
.project-actions { display: flex; gap: 8px; }
.project-error {
  font-size: 0.75rem;
  color: var(--danger);
  padding: 6px 10px;
  background: rgba(248, 113, 113, 0.08);
  border-radius: 6px;
}

/* Skeleton card */
.skeleton-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 20px;
}

/* Modal */
.tags-row { display: flex; flex-wrap: wrap; gap: 6px; }
.input-hint { font-size: 0.75rem; color: var(--text-muted); margin-top: 4px; }
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
  .projects-grid { grid-template-columns: 1fr; }
  .page-header { flex-direction: column; }
  .filters-row { flex-direction: column; }
  .filter-select { width: 100%; }
}
</style>

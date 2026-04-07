<template>
  <div class="page-wrapper">
    <!-- Loading state -->
    <div v-if="loading" class="profile-loading">
      <div class="profile-header-skeleton">
        <div class="skeleton skeleton-circle" style="width:90px;height:90px;flex-shrink:0;"></div>
        <div style="flex:1;display:flex;flex-direction:column;gap:12px;">
          <div class="skeleton skeleton-text" style="width:200px;height:22px;"></div>
          <div class="skeleton skeleton-text" style="width:300px;height:14px;"></div>
          <div style="display:flex;gap:8px;">
            <div v-for="i in 4" :key="i" class="skeleton" style="width:70px;height:26px;border-radius:999px;"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="empty-state">
      <div class="empty-state-icon">⚠️</div>
      <h3>Failed to load profile</h3>
      <p>{{ error }}</p>
      <button class="btn btn-primary" style="margin-top:20px;" @click="loadProfile">Retry</button>
    </div>

    <!-- Profile content -->
    <div v-else-if="profileUser">
      <!-- Profile header card -->
      <div class="profile-header-card">
        <div class="profile-header-inner">
          <div
            class="profile-avatar avatar"
            :style="{ background: avatarGradient(profileUser.name), width: '90px', height: '90px', fontSize: '2rem' }"
          >
            {{ initial(profileUser.name) }}
          </div>

          <div class="profile-info">
            <div class="profile-name-row">
              <h1 class="profile-name">{{ profileUser.name }}</h1>
              <span class="badge badge-purple" v-if="isOwnProfile">You</span>
            </div>
            <p class="profile-bio">{{ profileUser.bio || 'No bio added yet.' }}</p>

            <div class="profile-skills" v-if="profileUser.skills?.length">
              <span v-for="skill in profileUser.skills" :key="skill" class="skill-chip">{{ skill }}</span>
            </div>

            <div class="profile-links">
              <a
                v-if="profileUser.github"
                :href="profileUser.github"
                target="_blank"
                rel="noopener"
                class="profile-link"
              >
                <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.3 3.44 9.8 8.2 11.38.6.11.82-.26.82-.57v-2c-3.34.72-4.04-1.6-4.04-1.6-.55-1.38-1.34-1.75-1.34-1.75-1.09-.74.08-.73.08-.73 1.2.08 1.84 1.24 1.84 1.24 1.07 1.83 2.8 1.3 3.49 1 .1-.78.42-1.3.76-1.6-2.67-.3-5.47-1.33-5.47-5.93 0-1.31.47-2.38 1.24-3.22-.13-.3-.54-1.52.12-3.18 0 0 1.01-.32 3.3 1.23a11.5 11.5 0 0 1 3-.4c1.02 0 2.04.13 3 .4 2.28-1.55 3.29-1.23 3.29-1.23.66 1.66.25 2.88.12 3.18.77.84 1.24 1.91 1.24 3.22 0 4.61-2.81 5.62-5.49 5.92.43.37.81 1.1.81 2.22v3.29c0 .32.22.69.83.57C20.57 21.8 24 17.3 24 12c0-6.63-5.37-12-12-12z"/></svg>
                GitHub
              </a>
              <a
                v-if="profileUser.linkedin"
                :href="profileUser.linkedin"
                target="_blank"
                rel="noopener"
                class="profile-link"
              >
                <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M20.45 20.45h-3.56v-5.57c0-1.33-.03-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.34V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.45v6.29zM5.34 7.43a2.07 2.07 0 1 1 0-4.14 2.07 2.07 0 0 1 0 4.14zm1.78 13.02H3.56V9h3.56v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.72v20.56C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.72V1.72C24 .77 23.2 0 22.22 0z"/></svg>
                LinkedIn
              </a>
              <span v-if="profileUser.email" class="profile-email">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
                {{ profileUser.email }}
              </span>
            </div>
          </div>

          <button v-if="isOwnProfile" class="btn btn-outline" @click="showEditModal = true">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
            Edit Profile
          </button>
        </div>
      </div>

      <!-- Stats row -->
      <div class="stats-row">
        <div class="stat-box">
          <span class="stat-num">{{ profileUser.projects?.length || 0 }}</span>
          <span class="stat-label">Projects</span>
        </div>
        <div class="stat-box">
          <span class="stat-num">{{ profileUser.skills?.length || 0 }}</span>
          <span class="stat-label">Skills</span>
        </div>
      </div>

      <!-- Projects section -->
      <div class="section" v-if="profileUser.projects?.length">
        <div class="section-header">
          <h2 class="section-title">{{ isOwnProfile ? 'Your Projects' : 'Projects' }}</h2>
          <RouterLink to="/projects" class="section-link" v-if="isOwnProfile">Browse all →</RouterLink>
        </div>
        <div class="projects-grid">
          <div
            v-for="project in profileUser.projects"
            :key="project._id || project.id"
            class="project-card"
          >
            <div class="project-card-top">
              <h3 class="project-name">{{ project.name }}</h3>
              <span :class="['badge', statusBadge(project.status)]">{{ project.status || 'active' }}</span>
            </div>
            <p class="project-desc">{{ truncate(project.description, 90) }}</p>
            <div class="tech-chips">
              <span
                v-for="tech in (project.stack || project.techStack || [])"
                :key="tech"
                class="tech-chip"
              >{{ tech }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- No projects -->
      <div class="section" v-else>
        <div class="section-header">
          <h2 class="section-title">{{ isOwnProfile ? 'Your Projects' : 'Projects' }}</h2>
        </div>
        <div class="empty-section">
          <p>{{ isOwnProfile ? "You haven't joined any projects yet." : 'No projects to show.' }}</p>
          <RouterLink to="/projects" class="btn btn-outline btn-sm" style="margin-top:12px;display:inline-flex;" v-if="isOwnProfile">
            Browse Projects
          </RouterLink>
        </div>
      </div>
    </div>

    <!-- Edit Profile Modal -->
    <Teleport to="body">
      <div v-if="showEditModal" class="modal-overlay" @click.self="showEditModal = false">
        <div class="modal" role="dialog" aria-modal="true">
          <div class="modal-header">
            <h2>Edit Profile</h2>
            <button class="modal-close" @click="showEditModal = false">✕</button>
          </div>

          <form @submit.prevent="handleUpdateProfile">
            <div class="form-group">
              <label class="form-label">Name *</label>
              <input v-model="editForm.name" class="form-input" placeholder="Your name" required />
            </div>
            <div class="form-group">
              <label class="form-label">Bio</label>
              <textarea
                v-model="editForm.bio"
                class="form-input"
                placeholder="Tell others about yourself, your interests and goals..."
              ></textarea>
            </div>

            <div class="form-group">
              <label class="form-label">Skills</label>
              <div class="tags-row" v-if="editForm.skills.length > 0">
                <span v-for="(skill, i) in editForm.skills" :key="i" class="chip">
                  {{ skill }}
                  <span class="chip-remove" @click="removeSkill(i)">✕</span>
                </span>
              </div>
              <input
                v-model="skillInput"
                class="form-input"
                :style="{ marginTop: editForm.skills.length ? '8px' : '0' }"
                placeholder="Type skill and press Enter..."
                @keydown.enter.prevent="addSkill"
              />
              <p class="input-hint">Press Enter to add each skill</p>
            </div>

            <div class="form-group">
              <label class="form-label">GitHub URL</label>
              <input v-model="editForm.github" class="form-input" placeholder="https://github.com/yourname" />
            </div>
            <div class="form-group">
              <label class="form-label">LinkedIn URL</label>
              <input v-model="editForm.linkedin" class="form-input" placeholder="https://linkedin.com/in/yourname" />
            </div>

            <div v-if="editError" class="error-banner">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
              {{ editError }}
            </div>
            <div v-if="editSuccess" class="success-banner">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
              Profile updated successfully!
            </div>

            <div class="modal-actions">
              <button type="button" class="btn btn-secondary" @click="showEditModal = false">Cancel</button>
              <button type="submit" class="btn btn-primary" :disabled="editLoading">
                <span v-if="editLoading" class="btn-spinner"></span>
                {{ editLoading ? 'Saving...' : 'Save Changes' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { getUser, updateProfile } from '../services/api'

const route = useRoute()
const authStore = useAuthStore()

const profileUser = ref(null)
const loading = ref(false)
const error = ref('')
const showEditModal = ref(false)
const editLoading = ref(false)
const editError = ref('')
const editSuccess = ref(false)
const skillInput = ref('')

const editForm = ref({ name: '', bio: '', skills: [], github: '', linkedin: '' })

const isOwnProfile = computed(() => {
  if (!route.params.id) return true
  const uid = authStore.user?._id || authStore.user?.id
  return route.params.id === uid
})

async function loadProfile() {
  loading.value = true
  error.value = ''
  try {
    if (!route.params.id || isOwnProfile.value) {
      if (authStore.user) {
        profileUser.value = authStore.user
      }
      const uid = authStore.user?._id || authStore.user?.id
      if (uid) {
        const res = await getUser(uid)
        profileUser.value = res.data.user || res.data
      }
    } else {
      const res = await getUser(route.params.id)
      profileUser.value = res.data.user || res.data
    }
  } catch (e) {
    error.value = e.response?.data?.message || 'Failed to load profile.'
    // Fallback to store user if it's own profile
    if (isOwnProfile.value && authStore.user) {
      profileUser.value = authStore.user
      error.value = ''
    }
  } finally {
    loading.value = false
  }
}

onMounted(loadProfile)
watch(() => route.params.id, loadProfile)

watch(showEditModal, (val) => {
  if (val && profileUser.value) {
    editForm.value = {
      name: profileUser.value.name || '',
      bio: profileUser.value.bio || '',
      skills: [...(profileUser.value.skills || [])],
      github: profileUser.value.github || '',
      linkedin: profileUser.value.linkedin || '',
    }
    editError.value = ''
    editSuccess.value = false
  }
})

function addSkill() {
  const s = skillInput.value.trim()
  if (s && !editForm.value.skills.includes(s)) {
    editForm.value.skills.push(s)
  }
  skillInput.value = ''
}

function removeSkill(idx) {
  editForm.value.skills.splice(idx, 1)
}

async function handleUpdateProfile() {
  editError.value = ''
  editSuccess.value = false
  editLoading.value = true
  try {
    const res = await updateProfile({ ...editForm.value })
    const updated = res.data.user || res.data
    profileUser.value = { ...profileUser.value, ...updated }
    authStore.user = { ...authStore.user, ...updated }
    editSuccess.value = true
    setTimeout(() => {
      showEditModal.value = false
      editSuccess.value = false
    }, 1500)
  } catch (e) {
    editError.value = e.response?.data?.message || 'Failed to update profile.'
  } finally {
    editLoading.value = false
  }
}

function initial(name) {
  return (name || 'U').charAt(0).toUpperCase()
}

const GRADIENTS = [
  'linear-gradient(135deg, #7c6aff, #06b6d4)',
  'linear-gradient(135deg, #f59e0b, #ef4444)',
  'linear-gradient(135deg, #10b981, #06b6d4)',
  'linear-gradient(135deg, #8b5cf6, #ec4899)',
  'linear-gradient(135deg, #3b82f6, #7c6aff)',
]

function avatarGradient(name) {
  return GRADIENTS[(name || 'U').charCodeAt(0) % GRADIENTS.length]
}

function statusBadge(status) {
  return { active: 'badge-green', recruiting: 'badge-yellow', completed: 'badge-blue' }[status] || 'badge-cyan'
}

function truncate(str, n) {
  if (!str) return ''
  return str.length > n ? str.slice(0, n) + '…' : str
}
</script>

<style scoped>
.profile-header-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 28px;
  margin-bottom: 20px;
}
.profile-header-inner {
  display: flex;
  align-items: flex-start;
  gap: 24px;
}
.profile-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.profile-name-row {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}
.profile-name {
  font-size: 1.6rem;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: -0.5px;
}
.profile-bio {
  font-size: 0.95rem;
  color: var(--text-secondary);
  line-height: 1.65;
  max-width: 580px;
}
.profile-skills { display: flex; flex-wrap: wrap; gap: 6px; }
.skill-chip {
  padding: 4px 12px;
  background: rgba(124, 106, 255, 0.1);
  border: 1px solid rgba(124, 106, 255, 0.22);
  border-radius: 999px;
  font-size: 0.78rem;
  font-weight: 600;
  color: #a98eff;
}
.profile-links {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
}
.profile-link {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--text-secondary);
  padding: 5px 12px;
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: 999px;
  transition: all 0.2s;
  text-decoration: none;
}
.profile-link:hover { border-color: var(--accent); color: var(--accent); }
.profile-email {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 0.82rem;
  color: var(--text-muted);
}

/* Stats */
.stats-row {
  display: flex;
  gap: 12px;
  margin-bottom: 28px;
}
.stat-box {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 16px 28px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3px;
}
.stat-num {
  font-size: 1.6rem;
  font-weight: 800;
  color: var(--accent);
  line-height: 1;
}
.stat-label { font-size: 0.75rem; color: var(--text-muted); font-weight: 500; }

/* Section */
.section { margin-top: 8px; }
.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 18px;
}
.section-title {
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--text-primary);
}
.section-link {
  font-size: 0.82rem;
  color: var(--accent);
  font-weight: 600;
  text-decoration: none;
}
.section-link:hover { opacity: 0.75; }

/* Projects grid */
.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(290px, 1fr));
  gap: 14px;
}
.project-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 18px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  transition: border-color 0.2s, box-shadow 0.2s, transform 0.2s;
}
.project-card:hover {
  border-color: rgba(124, 106, 255, 0.4);
  box-shadow: 0 4px 18px rgba(0,0,0,0.25);
  transform: translateY(-2px);
}
.project-card-top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 8px;
}
.project-name { font-size: 0.95rem; font-weight: 700; color: var(--text-primary); }
.project-desc { font-size: 0.82rem; color: var(--text-secondary); line-height: 1.6; }
.tech-chips { display: flex; flex-wrap: wrap; gap: 5px; }
.tech-chip {
  padding: 2px 8px;
  background: rgba(59, 130, 246, 0.1);
  border: 1px solid rgba(59, 130, 246, 0.2);
  border-radius: 999px;
  font-size: 0.7rem;
  font-weight: 600;
  color: #60a5fa;
}

/* Empty */
.empty-section { padding: 32px 0; color: var(--text-muted); font-size: 0.875rem; }

/* Loading skeleton */
.profile-loading { padding: 20px 0; }
.profile-header-skeleton {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 28px;
  display: flex;
  gap: 20px;
}

/* Modal */
.tags-row { display: flex; flex-wrap: wrap; gap: 6px; min-height: 24px; }
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
.success-banner {
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(74, 222, 128, 0.1);
  border: 1px solid rgba(74, 222, 128, 0.25);
  color: var(--success);
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

@media (max-width: 700px) {
  .profile-header-inner { flex-direction: column; align-items: center; text-align: center; }
  .profile-name-row { justify-content: center; }
  .profile-links { justify-content: center; }
  .profile-skills { justify-content: center; }
  .stats-row { justify-content: center; }
  .projects-grid { grid-template-columns: 1fr; }
}
</style>

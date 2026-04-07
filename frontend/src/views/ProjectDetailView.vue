<template>
  <div class="page-wrapper">
    <!-- Loading state -->
    <div v-if="loading" class="container">
      <div class="skeleton-card" style="height: 300px;"></div>
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="error-state">
      <div style="text-align: center; padding: 60px 20px;">
        <div style="font-size: 3rem; margin-bottom: 20px;">⚠️</div>
        <h2>{{ error }}</h2>
        <RouterLink to="/projects" class="btn btn-primary" style="margin-top: 20px;">Back to Projects</RouterLink>
      </div>
    </div>

    <!-- Project detail -->
    <div v-else-if="project" class="project-detail">
      <!-- Header -->
      <div class="project-header-card">
        <div class="project-header-top">
          <div>
            <div class="status-badge" :class="`status-${project.status}`">{{ project.status }}</div>
            <h1 class="project-title">{{ project.name }}</h1>
            <p class="project-owner">by <strong>{{ project.owner_name }}</strong></p>
          </div>
          <div class="header-actions" v-if="authStore.isLoggedIn">
            <button
              v-if="!isMember"
              class="btn btn-primary"
              @click="joinProject"
              :disabled="joiningProject"
            >
              {{ joiningProject ? 'Joining...' : 'Join Project' }}
            </button>
            <button
              v-else-if="!isOwner"
              class="btn btn-outline"
              @click="leaveProject"
              :disabled="joiningProject"
            >
              Leave Project
            </button>
            <RouterLink v-else :to="`/projects/${project.id}/edit`" class="btn btn-secondary">
              Edit Project
            </RouterLink>
          </div>
        </div>

        <div class="project-meta">
          <div class="meta-item">
            <span class="meta-label">👥 Members</span>
            <span class="meta-value">{{ project.members?.length || 0 }}</span>
          </div>
          <div class="meta-item">
            <span class="meta-label">🛠️ Stack</span>
            <span class="meta-value">{{ project.stack?.length || 0 }} techs</span>
          </div>
          <div class="meta-item">
            <span class="meta-label">📅 Created</span>
            <span class="meta-value">{{ formatRelativeDate(project.created_at) }}</span>
          </div>
        </div>
      </div>

      <!-- Main content grid -->
      <div class="project-grid">
        <!-- Left column: Description & Comments -->
        <div class="project-main">
          <!-- Description -->
          <section class="section">
            <h2 class="section-title">About</h2>
            <p class="project-description">{{ project.description || 'No description provided' }}</p>
          </section>

          <!-- Tech Stack -->
          <section class="section" v-if="project.stack?.length">
            <h2 class="section-title">Tech Stack</h2>
            <div class="tech-list">
              <span v-for="tech in project.stack" :key="tech" class="tech-chip">{{ tech }}</span>
            </div>
          </section>

          <!-- Comments Section -->
          <section class="section">
            <div class="section-header">
              <h2 class="section-title">Comments ({{ comments.length }})</h2>
              <button v-if="!showCommentForm && isMember" class="btn btn-sm btn-secondary" @click="showCommentForm = true">
                Add Comment
              </button>
            </div>

            <!-- Comment Form -->
            <div v-if="showCommentForm && isMember" class="comment-form">
              <textarea
                v-model="newComment"
                placeholder="Share your thoughts about this project..."
                class="form-input"
                rows="3"
              ></textarea>
              <div class="form-actions">
                <button class="btn btn-primary btn-sm" @click="submitComment" :disabled="!newComment.trim() || submittingComment">
                  {{ submittingComment ? 'Posting...' : 'Post Comment' }}
                </button>
                <button class="btn btn-outline btn-sm" @click="showCommentForm = false">Cancel</button>
              </div>
            </div>

            <!-- Comments List -->
            <div v-if="comments.length" class="comments-list">
              <div v-for="comment in comments" :key="comment.id" class="comment">
                <div class="comment-header">
                  <strong class="comment-author">{{ comment.author_name }}</strong>
                  <span class="comment-time">{{ formatRelativeDate(comment.created_at) }}</span>
                </div>
                <p class="comment-content">{{ comment.content }}</p>
                <div v-if="comment.author_id === authStore.user?.id" class="comment-actions">
                  <button class="btn-link" @click="() => editingCommentId = comment.id">Edit</button>
                  <button class="btn-link text-danger" @click="deleteComment(comment.id)">Delete</button>
                </div>
              </div>
            </div>
            <div v-else class="empty-state-sm">
              <p>No comments yet. Be the first to comment!</p>
            </div>
          </section>
        </div>

        <!-- Right column: Members -->
        <div class="project-sidebar">
          <div class="sidebar-card">
            <h3 class="card-title">👥 Team Members ({{ project.members?.length || 0 }})</h3>
            <div class="members-list">
              <div v-for="member in project.members" :key="member.user_id" class="member-item">
                <div class="member-avatar" :title="member.name">
                  {{ member.name?.[0]?.toUpperCase() || '?' }}
                </div>
                <div class="member-info">
                  <div class="member-name">{{ member.name }}</div>
                  <div class="member-role">{{ member.role }}</div>
                </div>
                <RouterLink v-if="member.user_id !== authStore.user?.id" :to="`/profile/${member.user_id}`" class="btn-link">
                  View
                </RouterLink>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter, RouterLink } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import * as api from '../services/api'
import { formatRelativeDate } from '../utils/dateFormatter'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const project = ref(null)
const loading = ref(true)
const error = ref('')
const comments = ref([])

const newComment = ref('')
const showCommentForm = ref(false)
const submittingComment = ref(false)
const editingCommentId = ref(null)

const joiningProject = ref(false)

const projectId = computed(() => parseInt(route.params.id))
const isMember = computed(() => project.value && project.value.members?.some(m => m.user_id === authStore.user?.id))
const isOwner = computed(() => project.value && project.value.owner_id === authStore.user?.id)

async function loadProject() {
  loading.value = true
  error.value = ''
  try {
    const res = await api.getProjectDetail(projectId.value)
    project.value = res.data.project
    loadComments()
  } catch (err) {
    error.value = 'Failed to load project'
    console.error(err)
  } finally {
    loading.value = false
  }
}

async function loadComments() {
  try {
    const res = await api.getProjectComments(projectId.value)
    comments.value = res.data.comments || []
  } catch (err) {
    console.error('Failed to load comments:', err)
  }
}

async function submitComment() {
  if (!newComment.value.trim()) return

  submittingComment.value = true
  try {
    await api.createProjectComment(projectId.value, newComment.value)
    newComment.value = ''
    showCommentForm.value = false
    loadComments()
  } catch (err) {
    console.error('Failed to post comment:', err)
  } finally {
    submittingComment.value = false
  }
}

async function deleteComment(commentId) {
  if (!confirm('Delete this comment?')) return
  try {
    await api.deleteComment(commentId)
    loadComments()
  } catch (err) {
    console.error('Failed to delete comment:', err)
  }
}

async function joinProject() {
  joiningProject.value = true
  try {
    await api.joinProject(projectId.value)
    loadProject()
  } catch (err) {
    console.error('Failed to join project:', err)
  } finally {
    joiningProject.value = false
  }
}

async function leaveProject() {
  if (!confirm('Leave this project?')) return
  joiningProject.value = true
  try {
    await api.leaveProject(projectId.value)
    router.push('/projects')
  } catch (err) {
    console.error('Failed to leave project:', err)
  } finally {
    joiningProject.value = false
  }
}

onMounted(() => {
  loadProject()
})
</script>

<style scoped>
.project-detail {
  max-width: 1200px;
  margin: 0 auto;
}

.project-header-card {
  background: var(--bg-elevated);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 32px;
  margin-bottom: 32px;
}

.project-header-top {
  display: flex;
  justify-content: space-between;
  align-items: start;
  gap: 24px;
  margin-bottom: 24px;
}

.status-badge {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 999px;
  font-size: 0.875rem;
  font-weight: 500;
  margin-bottom: 12px;
  text-transform: capitalize;
}

.status-badge.status-recruiting {
  background: #fef3c7;
  color: #92400e;
}

.status-badge.status-active {
  background: #d1fae5;
  color: #065f46;
}

.status-badge.status-completed {
  background: #dbeafe;
  color: #1e40af;
}

.project-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0 0 8px 0;
  color: var(--text-primary);
}

.project-owner {
  font-size: 1rem;
  color: var(--text-secondary);
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.project-meta {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 24px;
  padding-top: 24px;
  border-top: 1px solid var(--border-color);
}

.meta-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.meta-label {
  font-size: 0.875rem;
  color: var(--text-secondary);
  font-weight: 500;
}

.meta-value {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text-primary);
}

.project-grid {
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: 32px;
}

.section {
  background: var(--bg-elevated);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.section-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
  color: var(--text-primary);
}

.project-description {
  font-size: 1rem;
  line-height: 1.6;
  color: var(--text-secondary);
  margin: 0;
  white-space: pre-wrap;
}

.tech-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tech-chip {
  display: inline-block;
  background: var(--bg-secondary);
  color: var(--text-primary);
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
}

/* Comments */
.comment-form {
  background: var(--bg-secondary);
  padding: 16px;
  border-radius: 8px;
  margin-bottom: 16px;
}

.comment-form textarea {
  resize: vertical;
  margin-bottom: 12px;
}

.form-actions {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.comment {
  padding: 16px;
  background: var(--bg-secondary);
  border-radius: 8px;
  border: 1px solid var(--border-color);
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.comment-author {
  color: var(--text-primary);
  font-size: 0.95rem;
}

.comment-time {
  font-size: 0.8rem;
  color: var(--text-secondary);
}

.comment-content {
  margin: 8px 0;
  color: var(--text-secondary);
  line-height: 1.5;
}

.comment-actions {
  display: flex;
  gap: 12px;
  margin-top: 8px;
}

.btn-link {
  background: none;
  border: none;
  color: var(--primary-color);
  cursor: pointer;
  font-size: 0.875rem;
  padding: 0;
  text-decoration: none;
}

.btn-link:hover {
  text-decoration: underline;
}

.text-danger {
  color: #dc2626;
}

.empty-state-sm {
  text-align: center;
  padding: 20px;
  color: var(--text-secondary);
  font-size: 0.95rem;
}

/* Sidebar */
.project-sidebar {
  position: sticky;
  top: 100px;
}

.sidebar-card {
  background: var(--bg-elevated);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 20px;
}

.card-title {
  margin: 0 0 16px 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-primary);
}

.members-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.member-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: var(--bg-secondary);
  border-radius: 8px;
}

.member-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.9rem;
  flex-shrink: 0;
}

.member-info {
  flex: 1;
  min-width: 0;
}

.member-name {
  font-weight: 500;
  color: var(--text-primary);
  font-size: 0.9rem;
}

.member-role {
  font-size: 0.75rem;
  color: var(--text-secondary);
  text-transform: capitalize;
}

.error-state {
  min-height: 50vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

@media (max-width: 768px) {
  .project-grid {
    grid-template-columns: 1fr;
  }

  .project-header-top {
    flex-direction: column;
  }

  .header-actions {
    flex-direction: column;
  }

  .header-actions button {
    width: 100%;
  }

  .project-title {
    font-size: 2rem;
  }

  .project-meta {
    grid-template-columns: 1fr;
  }

  .project-sidebar {
    position: static;
  }
}
</style>

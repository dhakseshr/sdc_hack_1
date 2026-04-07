<template>
  <div class="page-wrapper">
    <!-- Header -->
    <div class="page-header">
      <div>
        <h1 class="page-title">Settings</h1>
        <p class="page-sub">Manage your profile and preferences</p>
      </div>
    </div>

    <!-- Settings Tabs -->
    <div class="settings-container">
      <div class="settings-tabs">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          :class="['tab-btn', { active: activeTab === tab.id }]"
          @click="activeTab = tab.id"
        >
          <span class="tab-icon">{{ tab.icon }}</span>
          {{ tab.label }}
        </button>
      </div>

      <div class="settings-content">
        <!-- Profile Tab -->
        <div v-show="activeTab === 'profile'" class="tab-pane">
          <div class="form-section">
            <h3 class="section-title">Profile Information</h3>

            <div class="form-group">
              <label class="form-label">Full Name</label>
              <input v-model="profileForm.name" type="text" class="form-input" />
            </div>

            <div class="form-group">
              <label class="form-label">Bio</label>
              <textarea v-model="profileForm.bio" class="form-input" rows="4" placeholder="Tell us about yourself..."></textarea>
            </div>

            <div class="form-group">
              <label class="form-label">Skills</label>
              <div class="skills-input">
                <div class="skills-list">
                  <span v-for="skill in profileForm.skills" :key="skill" class="skill-tag">
                    {{ skill }}
                    <button type="button" @click="removeSkill(skill)" class="remove-btn">✕</button>
                  </span>
                </div>
                <div class="skill-input-group">
                  <input
                    v-model="newSkill"
                    type="text"
                    class="form-input"
                    placeholder="Add a skill and press Enter"
                    @keyup.enter="addSkill"
                  />
                  <button type="button" @click="addSkill" class="btn btn-secondary btn-sm">Add</button>
                </div>
              </div>
            </div>

            <div class="form-group">
              <label class="form-label">GitHub Profile</label>
              <input v-model="profileForm.github" type="url" class="form-input" placeholder="https://github.com/username" />
            </div>

            <div class="form-group">
              <label class="form-label">LinkedIn Profile</label>
              <input v-model="profileForm.linkedin" type="url" class="form-input" placeholder="https://linkedin.com/in/username" />
            </div>

            <button
              class="btn btn-primary"
              @click="saveProfile"
              :disabled="savingProfile"
            >
              {{ savingProfile ? 'Saving...' : 'Save Changes' }}
            </button>
          </div>
        </div>

        <!-- Preferences Tab -->
        <div v-show="activeTab === 'preferences'" class="tab-pane">
          <div class="form-section">
            <h3 class="section-title">Appearance</h3>

            <div class="preference-item">
              <div class="preference-content">
                <h4 class="preference-title">Dark Mode</h4>
                <p class="preference-desc">Use dark theme for the application</p>
              </div>
              <div class="toggle-switch">
                <input
                  type="checkbox"
                  id="dark-mode"
                  v-model="preferences.darkMode"
                  @change="updatePreferences"
                  class="toggle-input"
                />
                <label for="dark-mode" class="toggle-label"></label>
              </div>
            </div>

            <div class="preference-item">
              <div class="preference-content">
                <h4 class="preference-title">Email Notifications</h4>
                <p class="preference-desc">Receive email updates for project activities</p>
              </div>
              <div class="toggle-switch">
                <input
                  type="checkbox"
                  id="email-notif"
                  v-model="preferences.emailNotifications"
                  @change="updatePreferences"
                  class="toggle-input"
                />
                <label for="email-notif" class="toggle-label"></label>
              </div>
            </div>
          </div>

          <div class="form-section">
            <h3 class="section-title">Privacy</h3>

            <div class="preference-item">
              <div class="preference-content">
                <h4 class="preference-title">Public Profile</h4>
                <p class="preference-desc">Let other developers find and view your profile</p>
              </div>
              <div class="toggle-switch">
                <input
                  type="checkbox"
                  id="public-profile"
                  v-model="preferences.publicProfile"
                  @change="updatePreferences"
                  class="toggle-input"
                />
                <label for="public-profile" class="toggle-label"></label>
              </div>
            </div>
          </div>
        </div>

        <!-- Account Tab -->
        <div v-show="activeTab === 'account'" class="tab-pane">
          <div class="form-section">
            <h3 class="section-title">Account</h3>

            <div class="account-info">
              <div class="info-item">
                <span class="info-label">Email</span>
                <span class="info-value">{{ authStore.user?.email }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Member Since</span>
                <span class="info-value">{{ formatFullDate(authStore.user?.created_at) }}</span>
              </div>
            </div>
          </div>

          <div class="form-section danger-zone">
            <h3 class="section-title">Danger Zone</h3>

            <button class="btn btn-danger" @click="logout">
              Logout
            </button>

            <button class="btn btn-danger btn-outlined" @click="deleteAccount" v-if="false">
              Delete Account
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import * as api from '../services/api'
import { formatFullDate } from '../utils/dateFormatter'

const router = useRouter()
const authStore = useAuthStore()

const activeTab = ref('profile')
const savingProfile = ref(false)
const newSkill = ref('')

const tabs = [
  { id: 'profile', label: 'Profile', icon: '👤' },
  { id: 'preferences', label: 'Preferences', icon: '⚙️' },
  { id: 'account', label: 'Account', icon: '🔒' },
]

const profileForm = ref({
  name: '',
  bio: '',
  skills: [],
  github: '',
  linkedin: '',
})

const preferences = ref({
  darkMode: localStorage.getItem('darkMode') === 'true',
  emailNotifications: localStorage.getItem('emailNotifications') !== 'false',
  publicProfile: localStorage.getItem('publicProfile') !== 'false',
})

function addSkill() {
  const skill = newSkill.value.trim()
  if (skill && !profileForm.value.skills.includes(skill)) {
    profileForm.value.skills.push(skill)
    newSkill.value = ''
  }
}

function removeSkill(skill) {
  const index = profileForm.value.skills.indexOf(skill)
  if (index > -1) {
    profileForm.value.skills.splice(index, 1)
  }
}

async function saveProfile() {
  savingProfile.value = true
  try {
    await api.updateProfile({
      name: profileForm.value.name,
      bio: profileForm.value.bio,
      skills: profileForm.value.skills,
      github: profileForm.value.github,
      linkedin: profileForm.value.linkedin,
    })
    await authStore.fetchMe()
  } catch (error) {
    console.error('Failed to save profile:', error)
  } finally {
    savingProfile.value = false
  }
}

function updatePreferences() {
  localStorage.setItem('darkMode', preferences.value.darkMode)
  localStorage.setItem('emailNotifications', preferences.value.emailNotifications)
  localStorage.setItem('publicProfile', preferences.value.publicProfile)

  if (preferences.value.darkMode) {
    document.documentElement.classList.add('dark-mode')
  } else {
    document.documentElement.classList.remove('dark-mode')
  }
}

function logout() {
  authStore.logout()
  router.push('/')
}

function deleteAccount() {
  if (confirm('Are you sure? This action cannot be undone.')) {
    logout()
  }
}

onMounted(() => {
  if (authStore.user) {
    profileForm.value.name = authStore.user.name || ''
    profileForm.value.bio = authStore.user.bio || ''
    profileForm.value.skills = authStore.user.skills || []
    profileForm.value.github = authStore.user.github || ''
    profileForm.value.linkedin = authStore.user.linkedin || ''
  }
})
</script>

<style scoped>
.settings-container {
  display: grid;
  grid-template-columns: 200px 1fr;
  gap: 32px;
  max-width: 1000px;
  margin: 0 auto;
}

.settings-tabs {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.tab-btn {
  padding: 12px 16px;
  border: 1px solid var(--border-color);
  background: var(--bg-elevated);
  border-radius: 8px;
  cursor: pointer;
  text-align: left;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.95rem;
}

.tab-btn:hover {
  border-color: var(--primary-color);
}

.tab-btn.active {
  background: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
}

.settings-content {
  background: var(--bg-elevated);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 32px;
}

.tab-pane {
  animation: fadeIn 0.2s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0.8;
  }
  to {
    opacity: 1;
  }
}

.form-section {
  margin-bottom: 32px;
}

.form-section:last-child {
  margin-bottom: 0;
}

.section-title {
  margin: 0 0 16px 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-primary);
  padding-bottom: 12px;
  border-bottom: 2px solid var(--border-color);
}

.form-group {
  margin-bottom: 20px;
}

.form-label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: var(--text-primary);
}

.skills-input {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.skills-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.skill-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: var(--primary-color);
  color: white;
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 0.9rem;
}

.remove-btn {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  padding: 0;
  font-size: 1rem;
  line-height: 1;
}

.skill-input-group {
  display: flex;
  gap: 8px;
}

.skill-input-group .form-input {
  flex: 1;
}

/* Preferences */
.preference-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background: var(--bg-secondary);
  border-radius: 8px;
  margin-bottom: 12px;
}

.preference-content {
  flex: 1;
}

.preference-title {
  margin: 0 0 4px 0;
  font-weight: 600;
  font-size: 0.95rem;
  color: var(--text-primary);
}

.preference-desc {
  margin: 0;
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.toggle-switch {
  position: relative;
  display: inline-block;
  width: 50px;
  height: 28px;
}

.toggle-input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-label {
  display: block;
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: 0.4s;
  border-radius: 28px;
}

.toggle-label::before {
  content: '';
  position: absolute;
  height: 22px;
  width: 22px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: 0.4s;
  border-radius: 50%;
}

.toggle-input:checked + .toggle-label {
  background-color: var(--primary-color);
}

.toggle-input:checked + .toggle-label::before {
  transform: translateX(22px);
}

/* Account */
.account-info {
  background: var(--bg-secondary);
  border-radius: 8px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.info-label {
  font-weight: 500;
  color: var(--text-secondary);
}

.info-value {
  color: var(--text-primary);
  font-family: monospace;
}

.danger-zone {
  border: 2px solid #dc2626;
  background: rgba(220, 38, 38, 0.05);
}

.btn-danger {
  background: #dc2626;
  color: white;
}

.btn-danger:hover {
  background: #b91c1c;
}

.btn-danger.btn-outlined {
  background: transparent;
  border: 2px solid #dc2626;
  color: #dc2626;
}

@media (max-width: 768px) {
  .settings-container {
    grid-template-columns: 1fr;
  }

  .settings-tabs {
    display: flex;
    flex-direction: row;
    overflow-x: auto;
    gap: 8px;
  }

  .tab-btn {
    white-space: nowrap;
    flex-shrink: 0;
  }

  .preference-item {
    flex-direction: column;
    align-items: start;
    gap: 12px;
  }

  .info-item {
    flex-direction: column;
    align-items: start;
  }
}
</style>

<template>
  <div class="landing">
    <div class="landing-bg">
      <div class="grid-overlay"></div>
    </div>

    <div class="landing-content">
      <!-- Hero -->
      <div class="hero">
        <div class="hero-badge">
          <span class="pulse-dot"></span>
          Developer Collaboration Platform
        </div>
        <h1>Where Developers<br /><span class="gradient-text">Build Together</span></h1>
        <p class="hero-sub">
          Find teammates, discover projects, and collaborate on opportunities —
          all in one place for student developers.
        </p>
        <div class="hero-stats">
          <div class="stat"><strong>500+</strong> Developers</div>
          <div class="stat-divider"></div>
          <div class="stat"><strong>120+</strong> Projects</div>
          <div class="stat-divider"></div>
          <div class="stat"><strong>80+</strong> Opportunities</div>
        </div>
      </div>

      <!-- Auth Card -->
      <div class="auth-card">
        <div class="auth-tabs">
          <button :class="['tab', { active: mode === 'login' }]" @click="mode = 'login'">Sign In</button>
          <button :class="['tab', { active: mode === 'register' }]" @click="mode = 'register'">Join Now</button>
        </div>

        <transition name="fade" mode="out-in">
          <!-- Login -->
          <form v-if="mode === 'login'" key="login" @submit.prevent="handleLogin" class="auth-form">
            <div class="form-group">
              <label class="form-label">Email</label>
              <input v-model="form.email" type="email" class="form-input" placeholder="you@example.com" required />
            </div>
            <div class="form-group">
              <label class="form-label">Password</label>
              <input v-model="form.password" type="password" class="form-input" placeholder="••••••••" required />
            </div>
            <div v-if="error" class="error-msg">{{ error }}</div>
            <button type="submit" class="btn btn-primary btn-lg submit-btn" :disabled="loading">
              <span v-if="loading" class="spinner"></span>
              {{ loading ? 'Signing in...' : 'Sign In' }}
            </button>
            <p class="switch-text">No account? <button type="button" class="link-btn" @click="mode = 'register'">Create one</button></p>
          </form>

          <!-- Register -->
          <form v-else key="register" @submit.prevent="handleRegister" class="auth-form">
            <div class="form-group">
              <label class="form-label">Full Name</label>
              <input v-model="form.name" type="text" class="form-input" placeholder="Your name" required />
            </div>
            <div class="form-group">
              <label class="form-label">Email</label>
              <input v-model="form.email" type="email" class="form-input" placeholder="you@example.com" required />
            </div>
            <div class="form-group">
              <label class="form-label">Password</label>
              <input v-model="form.password" type="password" class="form-input" placeholder="Min. 6 characters" required minlength="6" />
            </div>
            <div v-if="error" class="error-msg">{{ error }}</div>
            <button type="submit" class="btn btn-primary btn-lg submit-btn" :disabled="loading">
              <span v-if="loading" class="spinner"></span>
              {{ loading ? 'Creating account...' : 'Get Started Free' }}
            </button>
            <p class="switch-text">Already have an account? <button type="button" class="link-btn" @click="mode = 'login'">Sign in</button></p>
          </form>
        </transition>
      </div>
    </div>

    <!-- Features row -->
    <div class="features">
      <div class="feature">
        <div class="feature-icon">👤</div>
        <h3>Developer Profiles</h3>
        <p>Showcase your skills, projects, and experience</p>
      </div>
      <div class="feature">
        <div class="feature-icon">🚀</div>
        <h3>Project Collaboration</h3>
        <p>Create or join projects, build teams</p>
      </div>
      <div class="feature">
        <div class="feature-icon">🎯</div>
        <h3>Opportunity Board</h3>
        <p>Find hackathons, roles, and teammates</p>
      </div>
      <div class="feature">
        <div class="feature-icon">📡</div>
        <h3>Live Feed</h3>
        <p>Stay updated with the community</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const mode = ref('login')
const loading = ref(false)
const error = ref('')
const form = reactive({ name: '', email: '', password: '' })

async function handleLogin() {
  error.value = ''
  loading.value = true
  try {
    await authStore.login(form.email, form.password)
    router.push('/feed')
  } catch (e) {
    error.value = e.response?.data?.error || 'Login failed. Please try again.'
  } finally {
    loading.value = false
  }
}

async function handleRegister() {
  error.value = ''
  loading.value = true
  try {
    await authStore.register(form.name, form.email, form.password)
    router.push('/feed')
  } catch (e) {
    error.value = e.response?.data?.error || 'Registration failed. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.landing {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
}

.landing-bg {
  position: fixed;
  inset: 0;
  background: radial-gradient(ellipse 80% 60% at 50% -10%, rgba(124, 106, 255, 0.18) 0%, transparent 60%),
              radial-gradient(ellipse 60% 40% at 80% 80%, rgba(6, 182, 212, 0.08) 0%, transparent 50%);
  pointer-events: none;
  z-index: 0;
}

.grid-overlay {
  position: absolute;
  inset: 0;
  background-image: linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
  background-size: 40px 40px;
}

.landing-content {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 80px;
  max-width: 1100px;
  margin: 0 auto;
  padding: 80px 24px 40px;
  flex-wrap: wrap;
}

/* Hero */
.hero {
  flex: 1;
  min-width: 300px;
  max-width: 520px;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(124, 106, 255, 0.12);
  border: 1px solid rgba(124, 106, 255, 0.3);
  color: #a98eff;
  padding: 6px 14px;
  border-radius: 999px;
  font-size: 0.78rem;
  font-weight: 600;
  letter-spacing: 0.3px;
  margin-bottom: 24px;
}

.pulse-dot {
  width: 8px;
  height: 8px;
  background: #4ade80;
  border-radius: 50%;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(0.8); }
}

.hero h1 {
  font-size: 3.2rem;
  font-weight: 800;
  line-height: 1.1;
  letter-spacing: -1.5px;
  color: var(--text-primary);
  margin-bottom: 20px;
}

.gradient-text {
  background: linear-gradient(135deg, #7c6aff 0%, #06b6d4 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-sub {
  font-size: 1.05rem;
  color: var(--text-secondary);
  line-height: 1.7;
  margin-bottom: 32px;
  max-width: 420px;
}

.hero-stats {
  display: flex;
  align-items: center;
  gap: 20px;
}

.stat { font-size: 0.875rem; color: var(--text-secondary); }
.stat strong { color: var(--text-primary); font-size: 1.1rem; display: block; }
.stat-divider { width: 1px; height: 32px; background: var(--border); }

/* Auth Card */
.auth-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 32px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
}

.auth-tabs {
  display: flex;
  gap: 4px;
  background: var(--bg-elevated);
  border-radius: 10px;
  padding: 4px;
  margin-bottom: 28px;
}

.tab {
  flex: 1;
  padding: 8px;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 600;
  background: transparent;
  color: var(--text-muted);
  transition: all 0.2s;
  border: none;
  cursor: pointer;
}

.tab.active {
  background: var(--accent);
  color: #fff;
  box-shadow: 0 2px 8px rgba(124, 106, 255, 0.4);
}

.auth-form { display: flex; flex-direction: column; }

.submit-btn {
  width: 100%;
  margin-top: 8px;
  gap: 8px;
}

.error-msg {
  background: rgba(248, 113, 113, 0.12);
  border: 1px solid rgba(248, 113, 113, 0.3);
  color: var(--danger);
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 0.85rem;
  margin-bottom: 12px;
}

.switch-text {
  text-align: center;
  margin-top: 16px;
  font-size: 0.85rem;
  color: var(--text-muted);
}

.link-btn {
  background: none;
  border: none;
  color: var(--accent);
  cursor: pointer;
  font-size: inherit;
  font-weight: 600;
  padding: 0;
}

.link-btn:hover { text-decoration: underline; }

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

/* Features */
.features {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1px;
  background: var(--border);
  border-top: 1px solid var(--border);
  margin-top: auto;
}

.feature {
  background: var(--bg-page);
  padding: 28px 24px;
  text-align: center;
}

.feature-icon {
  font-size: 1.8rem;
  margin-bottom: 10px;
}

.feature h3 {
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 6px;
}

.feature p {
  font-size: 0.82rem;
  color: var(--text-muted);
  line-height: 1.5;
}

.fade-enter-active, .fade-leave-active { transition: opacity 0.15s, transform 0.15s; }
.fade-enter-from { opacity: 0; transform: translateY(8px); }
.fade-leave-to { opacity: 0; transform: translateY(-8px); }

@media (max-width: 768px) {
  .hero h1 { font-size: 2rem; }
  .landing-content { padding: 48px 16px 32px; gap: 40px; }
  .features { grid-template-columns: repeat(2, 1fr); }
}
</style>

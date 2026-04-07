<template>
  <nav class="navbar">
    <div class="nav-inner">
      <!-- Logo -->
      <RouterLink to="/feed" class="brand">
        <span class="brand-icon">⬡</span>
        BuildSpace
      </RouterLink>

      <!-- Desktop nav links -->
      <div class="nav-links hide-mobile">
        <RouterLink to="/feed" class="nav-link">
          <span class="nav-icon">◈</span> Feed
        </RouterLink>
        <RouterLink to="/projects" class="nav-link">
          <span class="nav-icon">⬙</span> Projects
        </RouterLink>
        <RouterLink to="/opportunities" class="nav-link">
          <span class="nav-icon">◉</span> Opportunities
        </RouterLink>
        <RouterLink to="/explore" class="nav-link">
          <span class="nav-icon">◎</span> Explore
        </RouterLink>
        <RouterLink to="/search" class="nav-link">
          <span class="nav-icon">🔍</span> Search
        </RouterLink>
      </div>

      <!-- Right side -->
      <div class="nav-right">
        <!-- Search bar (desktop) -->
        <div class="search-bar hide-mobile">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
          </svg>
          <input placeholder="Search..." class="search-input" @focus="$router.push('/search')" />
        </div>

        <!-- Notifications -->
        <RouterLink to="/notifications" class="nav-action notification-icon" title="Notifications">
          <span>🔔</span>
          <span v-if="notificationsStore.unreadCount > 0" class="badge">{{ notificationsStore.unreadCount }}</span>
        </RouterLink>

        <!-- User menu -->
        <div class="user-menu" ref="menuRef">
          <button class="avatar-btn" @click="toggleDropdown">
            <div class="avatar avatar-sm">
              {{ userInitial }}
            </div>
            <span class="user-name hide-mobile">{{ authStore.user?.name?.split(' ')[0] || 'User' }}</span>
            <svg class="chevron hide-mobile" :class="{ open: dropdownOpen }" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="6 9 12 15 18 9"/>
            </svg>
          </button>

          <Transition name="dropdown">
            <div v-if="dropdownOpen" class="dropdown">
              <div class="dropdown-header">
                <div class="avatar avatar-md">{{ userInitial }}</div>
                <div>
                  <div class="dropdown-name">{{ authStore.user?.name || 'User' }}</div>
                  <div class="dropdown-email">{{ authStore.user?.email || '' }}</div>
                </div>
              </div>
              <div class="dropdown-divider"></div>
              <RouterLink to="/profile" class="dropdown-item" @click="dropdownOpen = false">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="8" r="4"/><path d="M4 20c0-4 3.6-7 8-7s8 3 8 7"/></svg>
                My Profile
              </RouterLink>
              <RouterLink to="/explore" class="dropdown-item" @click="dropdownOpen = false">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
                Explore Developers
              </RouterLink>
              <RouterLink to="/search" class="dropdown-item" @click="dropdownOpen = false">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
                Search
              </RouterLink>
              <RouterLink to="/notifications" class="dropdown-item" @click="dropdownOpen = false">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>
                Notifications
              </RouterLink>
              <RouterLink to="/settings" class="dropdown-item" @click="dropdownOpen = false">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M12 1v6m0 6v6M4.22 4.22l4.24 4.24m2.98 2.98l4.24 4.24M1 12h6m6 0h6m-1.78 7.78l-4.24-4.24m-2.98-2.98l-4.24-4.24"/></svg>
                Settings
              </RouterLink>
              <div class="dropdown-divider"></div>
              <button class="dropdown-item danger" @click="handleLogout">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
                Logout
              </button>
            </div>
          </Transition>
        </div>

        <!-- Hamburger for mobile -->
        <button class="hamburger hide-desktop" @click="mobileOpen = !mobileOpen">
          <span></span><span></span><span></span>
        </button>
      </div>
    </div>

    <!-- Mobile menu -->
    <Transition name="mobile-menu">
      <div v-if="mobileOpen" class="mobile-nav hide-desktop">
        <RouterLink to="/feed" class="mobile-link" @click="mobileOpen = false">Feed</RouterLink>
        <RouterLink to="/projects" class="mobile-link" @click="mobileOpen = false">Projects</RouterLink>
        <RouterLink to="/opportunities" class="mobile-link" @click="mobileOpen = false">Opportunities</RouterLink>
        <RouterLink to="/explore" class="mobile-link" @click="mobileOpen = false">Explore</RouterLink>
        <RouterLink to="/search" class="mobile-link" @click="mobileOpen = false">Search</RouterLink>
        <RouterLink to="/notifications" class="mobile-link" @click="mobileOpen = false">Notifications</RouterLink>
        <RouterLink to="/profile" class="mobile-link" @click="mobileOpen = false">My Profile</RouterLink>
        <RouterLink to="/settings" class="mobile-link" @click="mobileOpen = false">Settings</RouterLink>
        <button class="mobile-link danger-link" @click="handleLogout">Logout</button>
      </div>
    </Transition>
  </nav>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'
import { useNotificationsStore } from '../../stores/notifications'

const authStore = useAuthStore()
const notificationsStore = useNotificationsStore()
const router = useRouter()
const dropdownOpen = ref(false)
const mobileOpen = ref(false)
const menuRef = ref(null)

const userInitial = computed(() => {
  const name = authStore.user?.name || 'U'
  return name.charAt(0).toUpperCase()
})

function toggleDropdown() {
  dropdownOpen.value = !dropdownOpen.value
}

function handleLogout() {
  authStore.logout()
  dropdownOpen.value = false
  mobileOpen.value = false
  router.push('/')
}

function handleClickOutside(e) {
  if (menuRef.value && !menuRef.value.contains(e.target)) {
    dropdownOpen.value = false
  }
}

onMounted(() => document.addEventListener('click', handleClickOutside))
onUnmounted(() => document.removeEventListener('click', handleClickOutside))
</script>

<style scoped>
.navbar {
  background: rgba(22, 27, 39, 0.95);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
  gap: 16px;
}

/* Brand */
.brand {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 1.25rem;
  font-weight: 800;
  color: var(--accent);
  letter-spacing: -0.5px;
  flex-shrink: 0;
  text-decoration: none;
  transition: opacity 0.2s;
}
.brand:hover { opacity: 0.85; }
.brand-icon {
  font-size: 1.4rem;
  line-height: 1;
}

/* Nav links */
.nav-links {
  display: flex;
  align-items: center;
  gap: 4px;
  flex: 1;
  justify-content: center;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 7px 14px;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-secondary);
  text-decoration: none;
  transition: all 0.2s ease;
}

.nav-link:hover {
  background: var(--bg-elevated);
  color: var(--text-primary);
}

.nav-link.router-link-active {
  background: rgba(124, 106, 255, 0.12);
  color: var(--accent);
}

.nav-icon {
  font-size: 1rem;
  line-height: 1;
}

/* Right side */
.nav-right {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
}

/* Search bar */
.search-bar {
  display: flex;
  align-items: center;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 6px 12px;
  gap: 8px;
  width: 200px;
}

.search-bar svg {
  color: var(--text-secondary);
  flex-shrink: 0;
}

.search-input {
  background: none;
  border: none;
  outline: none;
  color: var(--text-primary);
  font-size: 0.9rem;
  width: 100%;
}

.search-input::placeholder {
  color: var(--text-secondary);
}

/* Notification icon */
.nav-action {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 8px;
  background: var(--bg-elevated);
  border: 1px solid var(--border-color);
  font-size: 1.2rem;
  cursor: pointer;
  transition: all 0.2s;
  text-decoration: none;
  color: inherit;
}

.nav-action:hover {
  border-color: var(--primary-color);
}

.badge {
  position: absolute;
  top: -6px;
  right: -6px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  background: #ef4444;
  color: white;
  border-radius: 50%;
  font-size: 0.7rem;
  font-weight: 600;
}

/* Avatar & user menu */
.user-menu {
  position: relative;
}

.avatar-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 6px 10px 6px 6px;
  cursor: pointer;
  transition: all 0.2s;
  color: var(--text-primary);
}
.avatar-btn:hover {
  border-color: var(--accent);
  background: rgba(124, 106, 255, 0.08);
}

.avatar-sm {
  width: 32px;
  height: 32px;
  font-size: 0.85rem;
}

.avatar-md {
  width: 40px;
  height: 40px;
  font-size: 1rem;
}

.user-name {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-primary);
}

.chevron {
  color: var(--text-muted);
  transition: transform 0.2s;
}
.chevron.open {
  transform: rotate(180deg);
}

/* Dropdown */
.dropdown {
  position: absolute;
  right: 0;
  top: calc(100% + 8px);
  width: 220px;
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 8px;
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.5);
  z-index: 200;
}

.dropdown-header {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px;
  margin-bottom: 4px;
}

.dropdown-name {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-primary);
}

.dropdown-email {
  font-size: 0.75rem;
  color: var(--text-muted);
  margin-top: 1px;
}

.dropdown-divider {
  height: 1px;
  background: var(--border);
  margin: 6px 0;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 9px 10px;
  border-radius: 8px;
  font-size: 0.875rem;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.15s;
  background: none;
  border: none;
  width: 100%;
  text-align: left;
  text-decoration: none;
}

.dropdown-item:hover {
  background: rgba(255, 255, 255, 0.06);
  color: var(--text-primary);
}

.dropdown-item.danger {
  color: var(--danger);
}

.dropdown-item.danger:hover {
  background: rgba(248, 113, 113, 0.1);
}

/* Hamburger */
.hamburger {
  display: flex;
  flex-direction: column;
  gap: 5px;
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 8px;
  cursor: pointer;
  transition: var(--transition);
}
.hamburger:hover {
  border-color: var(--accent);
}
.hamburger span {
  display: block;
  width: 18px;
  height: 2px;
  background: var(--text-secondary);
  border-radius: 2px;
}

/* Mobile nav */
.mobile-nav {
  border-top: 1px solid var(--border);
  padding: 12px 16px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  background: var(--bg-card);
}

.mobile-link {
  display: block;
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--text-secondary);
  text-decoration: none;
  transition: all 0.15s;
  background: none;
  border: none;
  text-align: left;
  cursor: pointer;
  width: 100%;
}

.mobile-link:hover,
.mobile-link.router-link-active {
  background: rgba(124, 106, 255, 0.1);
  color: var(--accent);
}

.danger-link {
  color: var(--danger) !important;
}
.danger-link:hover {
  background: rgba(248, 113, 113, 0.1) !important;
}

/* Transitions */
.dropdown-enter-active,
.dropdown-leave-active {
  transition: opacity 0.15s ease, transform 0.15s ease;
}
.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}

.mobile-menu-enter-active,
.mobile-menu-leave-active {
  transition: opacity 0.2s ease, max-height 0.25s ease;
  max-height: 300px;
  overflow: hidden;
}
.mobile-menu-enter-from,
.mobile-menu-leave-to {
  opacity: 0;
  max-height: 0;
}

/* Responsive */
@media (max-width: 768px) {
  .hide-mobile {
    display: none !important;
  }
}
@media (min-width: 769px) {
  .hide-desktop {
    display: none !important;
  }
}
</style>

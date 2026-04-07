<template>
  <div id="app">
    <NavBar v-if="authStore.isLoggedIn" />
    <main :class="['main-content', { 'with-nav': authStore.isLoggedIn }]">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { useAuthStore } from './stores/auth'
import NavBar from './components/layout/NavBar.vue'

const authStore = useAuthStore()
</script>

<style>
#app {
  min-height: 100vh;
  background: var(--bg-page);
}

.main-content {
  min-height: 100vh;
}

.main-content.with-nav {
  padding: 28px 24px;
  max-width: 1200px;
  margin: 0 auto;
  min-height: calc(100vh - 64px);
}

/* Global page-wrapper utility used by views */
.page-wrapper {
  width: 100%;
}

@media (max-width: 640px) {
  .main-content.with-nav {
    padding: 16px;
  }
}
</style>

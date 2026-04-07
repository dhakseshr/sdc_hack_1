<template>
  <div class="page-wrapper">
    <!-- Header -->
    <div class="page-header">
      <div>
        <h1 class="page-title">Search BuildSpace</h1>
        <p class="page-sub">Find developers, projects, and opportunities</p>
      </div>
    </div>

    <!-- Search Input -->
    <div class="search-bar-container">
      <div class="search-bar">
        <svg class="search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
        </svg>
        <input
          v-model="searchQuery"
          @keyup.enter="performSearch"
          type="text"
          class="search-input"
          placeholder="Search for developers, projects or opportunities..."
        />
        <button v-if="searchQuery" class="search-clear" @click="clearSearch">✕</button>
      </div>

      <div class="filter-tabs">
        <button
          v-for="type in ['all', 'users', 'projects', 'opportunities']"
          :key="type"
          :class="['filter-tab', { active: filterType === type }]"
          @click="filterType = type; performSearch()"
        >
          {{ type === 'all' ? '🔍 All' : type === 'users' ? '👥 Developers' : type === 'projects' ? '📁 Projects' : '📋 Opportunities' }}
        </button>
      </div>
    </div>

    <!-- Results -->
    <div v-if="searchStore.loading" class="results-container">
      <div class="skeleton-card" v-for="i in 4" :key="i" style="height: 100px;"></div>
    </div>

    <div v-else-if="searchQuery && hasResults" class="results-container">
      <!-- Developers -->
      <section v-if="results.users?.length" class="results-section">
        <h2 class="results-title">
          <span>👥 Developers</span>
          <span class="count">({{ results.users.length }})</span>
        </h2>
        <div class="results-grid">
          <div v-for="user in results.users" :key="user.id" class="result-card user-card">
            <div class="card-header">
              <div class="avatar" :title="user.name">{{ user.name?.[0]?.toUpperCase() }}</div>
              <h3 class="result-title">{{ user.name }}</h3>
            </div>
            <p class="result-bio">{{ user.bio || 'No bio' }}</p>
            <div v-if="user.skills?.length" class="skills-preview">
              <span v-for="skill in user.skills.slice(0, 3)" :key="skill" class="skill-chip">{{ skill }}</span>
              <span v-if="user.skills.length > 3" class="skill-more">+{{ user.skills.length - 3 }}</span>
            </div>
            <RouterLink :to="`/profile/${user.id}`" class="btn btn-sm btn-outline">View Profile</RouterLink>
          </div>
        </div>
      </section>

      <!-- Projects -->
      <section v-if="results.projects?.length" class="results-section">
        <h2 class="results-title">
          <span>📁 Projects</span>
          <span class="count">({{ results.projects.length }})</span>
        </h2>
        <div class="results-list">
          <div v-for="project in results.projects" :key="project.id" class="result-card project-card">
            <div class="card-content">
              <h3 class="result-title">{{ project.name }}</h3>
              <p class="result-desc">{{ project.description || 'No description' }}</p>
              <div v-if="project.stack?.length" class="tech-preview">
                <span v-for="tech in project.stack.slice(0, 4)" :key="tech" class="tech-chip">{{ tech }}</span>
              </div>
              <div class="card-footer">
                <span class="by-text">by {{ project.owner_name }}</span>
                <RouterLink :to="`/projects/${project.id}`" class="btn btn-sm btn-outline">View</RouterLink>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Opportunities -->
      <section v-if="results.opportunities?.length" class="results-section">
        <h2 class="results-title">
          <span>📋 Opportunities</span>
          <span class="count">({{ results.opportunities.length }})</span>
        </h2>
        <div class="results-list">
          <div v-for="opp in results.opportunities" :key="opp.id" class="result-card opp-card">
            <div class="card-content">
              <div class="opp-header">
                <h3 class="result-title">{{ opp.title }}</h3>
                <span class="opp-category">{{ opp.category }}</span>
              </div>
              <p class="result-desc">{{ opp.description || 'No description' }}</p>
              <div class="card-footer">
                <span class="by-text">by {{ opp.author_name }}</span>
                <RouterLink to="/opportunities" class="btn btn-sm btn-outline">View Board</RouterLink>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>

    <!-- Empty state -->
    <div v-else-if="searched && !searchStore.loading" class="empty-state">
      <div class="empty-icon">🔍</div>
      <h3>No results found</h3>
      <p>Try searching for something else</p>
    </div>

    <!-- Initial state -->
    <div v-else class="initial-state">
      <div style="text-align: center; padding: 60px 20px;">
        <div style="font-size: 4rem; margin-bottom: 20px;">🔍</div>
        <h3>Start searching</h3>
        <p>Find developers, projects, and opportunities to collaborate with</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { RouterLink } from 'vue-router'
import { useSearchStore } from '../stores/search'

const searchStore = useSearchStore()
const searchQuery = ref('')
const filterType = ref('all')
const searched = ref(false)

const results = computed(() => searchStore.results)
const hasResults = computed(() => results.value.users?.length || results.value.projects?.length || results.value.opportunities?.length)

function performSearch() {
  if (!searchQuery.value.trim()) {
    searchStore.clearSearch()
    searched.value = false
    return
  }

  searched.value = true
  searchStore.search(searchQuery.value, filterType.value)
}

function clearSearch() {
  searchQuery.value = ''
  searched.value = false
  searchStore.clearSearch()
}
</script>

<style scoped>
.page-header {
  margin-bottom: 32px;
}

.search-bar-container {
  margin-bottom: 32px;
}

.search-bar {
  display: flex;
  align-items: center;
  background: var(--bg-elevated);
  border: 2px solid var(--border-color);
  border-radius: 12px;
  padding: 12px 16px;
  margin-bottom: 16px;
  transition: border-color 0.2s;
}

.search-bar:focus-within {
  border-color: var(--primary-color);
}

.search-icon {
  color: var(--text-secondary);
  margin-right: 12px;
  flex-shrink: 0;
}

.search-input {
  flex: 1;
  background: none;
  border: none;
  outline: none;
  font-size: 1rem;
  color: var(--text-primary);
}

.search-input::placeholder {
  color: var(--text-secondary);
}

.search-clear {
  background: none;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  font-size: 1.2rem;
  padding: 0;
  margin-left: 12px;
}

.filter-tabs {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  padding-bottom: 8px;
}

.filter-tab {
  white-space: nowrap;
  padding: 8px 16px;
  border: 1px solid var(--border-color);
  background: var(--bg-page);
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.filter-tab:hover {
  border-color: var(--primary-color);
}

.filter-tab.active {
  background: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
}

.results-container {
  max-width: 1200px;
  margin: 0 auto;
}

.results-section {
  margin-bottom: 48px;
}

.results-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0 0 16px 0;
  display: flex;
  align-items: center;
  gap: 12px;
}

.count {
  font-size: 1rem;
  color: var(--text-secondary);
  font-weight: 400;
}

.results-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 16px;
}

.results-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.result-card {
  background: var(--bg-elevated);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 16px;
  transition: transform 0.2s, box-shadow 0.2s;
}

.result-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.user-card {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 12px;
}

.avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 1.2rem;
  flex-shrink: 0;
}

.result-title {
  margin: 0;
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text-primary);
}

.result-bio,
.result-desc {
  margin: 0;
  color: var(--text-secondary);
  font-size: 0.9rem;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.skills-preview,
.tech-preview {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.skill-chip,
.tech-chip {
  display: inline-block;
  background: var(--bg-secondary);
  color: var(--text-primary);
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
}

.skill-more {
  color: var(--text-secondary);
  font-size: 0.75rem;
}

.project-card,
.opp-card {
  display: flex;
  flex-direction: column;
}

.card-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.opp-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  gap: 12px;
}

.opp-category {
  display: inline-block;
  background: #fef3c7;
  color: #92400e;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
  white-space: nowrap;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: auto;
  padding-top: 12px;
  border-top: 1px solid var(--border-color);
}

.by-text {
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.empty-state,
.initial-state {
  text-align: center;
  padding: 60px 20px;
  color: var(--text-secondary);
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 20px;
}

@media (max-width: 640px) {
  .results-grid {
    grid-template-columns: 1fr;
  }

  .filter-tabs {
    flex-wrap: wrap;
  }
}
</style>

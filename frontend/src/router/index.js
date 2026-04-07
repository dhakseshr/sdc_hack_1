import { createRouter, createWebHistory } from 'vue-router'

const LandingView = () => import('../views/LandingView.vue')
const FeedView = () => import('../views/FeedView.vue')
const ProjectsView = () => import('../views/ProjectsView.vue')
const ProjectDetailView = () => import('../views/ProjectDetailView.vue')
const OpportunitiesView = () => import('../views/OpportunitiesView.vue')
const ProfileView = () => import('../views/ProfileView.vue')
const ExploreView = () => import('../views/ExploreView.vue')
const SearchView = () => import('../views/SearchView.vue')
const NotificationsView = () => import('../views/NotificationsView.vue')
const SettingsView = () => import('../views/SettingsView.vue')

const routes = [
  {
    path: '/',
    component: LandingView,
    meta: { guestOnly: true },
  },
  {
    path: '/feed',
    component: FeedView,
    meta: { requiresAuth: true },
  },
  {
    path: '/projects',
    component: ProjectsView,
    meta: { requiresAuth: true },
  },
  {
    path: '/projects/:id',
    component: ProjectDetailView,
    meta: { requiresAuth: true },
  },
  {
    path: '/opportunities',
    component: OpportunitiesView,
    meta: { requiresAuth: true },
  },
  {
    path: '/profile/:id?',
    component: ProfileView,
    meta: { requiresAuth: true },
  },
  {
    path: '/explore',
    component: ExploreView,
    meta: { requiresAuth: true },
  },
  {
    path: '/search',
    component: SearchView,
    meta: { requiresAuth: true },
  },
  {
    path: '/notifications',
    component: NotificationsView,
    meta: { requiresAuth: true },
  },
  {
    path: '/settings',
    component: SettingsView,
    meta: { requiresAuth: true },
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/',
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.meta.requiresAuth && !token) {
    next('/')
  } else if (to.meta.guestOnly && token) {
    next('/feed')
  } else {
    next()
  }
})

export default router

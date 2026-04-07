import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './style.css'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.mount('#app')

// Hydrate user on app start if token exists
const token = localStorage.getItem('token')
if (token) {
  import('./stores/auth.js').then(({ useAuthStore }) => {
    const authStore = useAuthStore()
    authStore.fetchMe()
  })
}

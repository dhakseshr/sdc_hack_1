import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    currentUser: null,
    isLoggedIn: false,
  }),
  actions: {
    setUser(user) {
      this.currentUser = user
      this.isLoggedIn = !!user
    },
    logout() {
      this.currentUser = null
      this.isLoggedIn = false
    },
  },
})

import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isAuthenticated: true,
    admin: { username: 'admin', password: 'admin123' }
  }),
  actions: {
    async logout(router) {
      this.isAuthenticated = false
      router.push('/login')
    }
  }
}) 
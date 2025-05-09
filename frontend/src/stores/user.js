import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    // Mock user, change role to 'passenger' or 'driver' for testing
    currentUser: {
      name: 'Jane Doe',
      username: 'janedoe',
      email: 'janedoe@example.com',
      phone: '+601139303135',
      role: 'passenger', // 'driver' / 'passenger'
      avatar: '/src/assets/images/image.png',
      qrCode: '/src/assets/images/qrcode.jpg',
      password: 'password123', // Default password for demo
      // Add more fields as needed
    },
    isAuthenticated: true // Set to false to simulate logged out
  }),
  actions: {
    logout() {
      this.isAuthenticated = false;
      this.currentUser = null;
    },
    loginAs(role) {
      this.isAuthenticated = true;
      this.currentUser = { name: 'Jane Doe', role };
    }
  }
}) 
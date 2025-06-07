import { defineStore } from 'pinia'
import { authService } from '../services/api'
import router from '../router'

export const useUserStore = defineStore('user', {
  state: () => ({
    currentUser: null,
    isAuthenticated: false,
    token: null,
    authError: null
  }),
  actions: {
    async login(email, password) {
      try {
        this.authError = null;
        const response = await authService.login({ email, password });
        const { token, expiresIn, user } = response.data;
        
        this.token = token;
        this.currentUser = user;
        this.isAuthenticated = true;
        
        // Store token in localStorage
        localStorage.setItem('token', token);
        localStorage.setItem('user', JSON.stringify(user));
        
        // Redirect based on role
        if (user.role === 'driver') {
          router.push('/create-ride');
        } else {
          router.push('/find-ride');
        }
        
        return true;
      } catch (error) {
        this.authError = error.response?.data?.error || 'Login failed';
        return false;
      }
    },
    
    async registerPassenger(userData) {
      try {
        this.authError = null;
        await authService.registerPassenger(userData);
        router.push('/login');
        return true;
      } catch (error) {
        this.authError = error.response?.data?.error || 'Registration failed';
        return false;
      }
    },
    
    async registerDriver(driverData) {
      try {
        this.authError = null;
        await authService.registerDriver(driverData);
        router.push('/login');
        return true;
      } catch (error) {
        this.authError = error.response?.data?.error || 'Driver registration failed';
        return false;
      }
    },
    
    logout() {
      this.isAuthenticated = false;
      this.currentUser = null;
      this.token = null;
      
      // Remove token from localStorage
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      
      router.push('/login-register');
    },
    
    initializeAuth() {
      const token = localStorage.getItem('token');
      const user = localStorage.getItem('user');
      
      if (token && user) {
        this.token = token;
        this.currentUser = JSON.parse(user);
        this.isAuthenticated = true;
      } else {
        // Ensure isAuthenticated is false if there's no token/user
        this.isAuthenticated = false;
        this.currentUser = null;
        this.token = null;
      }
    }
  }
}) 
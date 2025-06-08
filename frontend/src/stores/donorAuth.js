import { defineStore } from 'pinia';
import axios from 'axios';
import router from '../router';
import { useToastStore } from './toast';

const API_BASE_URL = 'http://localhost:5000/api';

export const useDonorAuthStore = defineStore('donorAuth', {
  state: () => ({
    donorToken: null,
    isDonorAuthenticated: false,
    donorUser: null,
    authError: null,
  }),
  
  actions: {
    async donorLogin(email, password) {
      try {
        this.authError = null;
        
        const response = await axios.post(`${API_BASE_URL}/auth/admin/login`, {
          email,
          password,
          userType: 'donor' // Add a flag to indicate this is a donor login
        });
        
        const { token, donor } = response.data;
        
        this.donorToken = token;
        this.donorUser = donor;
        this.isDonorAuthenticated = true;
        
        // Store token in localStorage
        localStorage.setItem('donorToken', token);
        
        // Show success toast
        const toastStore = useToastStore();
        toastStore.success('Login successful');
        
        return true;
      } catch (error) {
        this.authError = error.response?.data?.error || 'Login failed';
        return false;
      }
    },
    
    async donorRegister(userData) {
      try {
        this.authError = null;
        
        // Add donor type to user data
        userData.userType = 'donor';
        
        const response = await axios.post(`${API_BASE_URL}/auth/admin/register`, userData);
        
        const { token, donor } = response.data;
        
        this.donorToken = token;
        this.donorUser = donor;
        this.isDonorAuthenticated = true;
        
        // Store token in localStorage
        localStorage.setItem('donorToken', token);
        
        // Show success toast
        const toastStore = useToastStore();
        toastStore.success('Registration successful');
        
        return true;
      } catch (error) {
        this.authError = error.response?.data?.error || 'Registration failed';
        return false;
      }
    },
    
    donorLogout() {
      this.isDonorAuthenticated = false;
      this.donorToken = null;
      this.donorUser = null;
      
      // Remove token from localStorage
      localStorage.removeItem('donorToken');
      
      // Show logout toast
      const toastStore = useToastStore();
      toastStore.info('Logged out');
      
      // Redirect to login
      router.push('/portal/login');
    },
    
    initializeDonorAuth() {
      const token = localStorage.getItem('donorToken');
      
      if (token) {
        this.donorToken = token;
        this.isDonorAuthenticated = true;
        
        // You can fetch donor profile here if you have an endpoint for it
      } else {
        this.isDonorAuthenticated = false;
        this.donorToken = null;
        this.donorUser = null;
      }
    },
    
    // Check if the user is authenticated as a donor
    checkDonorAuth() {
      return this.isDonorAuthenticated && this.donorToken;
    }
  }
}); 
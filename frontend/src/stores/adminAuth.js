import { defineStore } from 'pinia';
import axios from 'axios';
import router from '../router';
import { useToastStore } from './toast';

const API_BASE_URL = 'http://localhost:5000/api';

export const useAdminAuthStore = defineStore('adminAuth', {
  state: () => ({
    adminToken: null,
    isAdminAuthenticated: false,
    adminUser: null,
    authError: null,
  }),
  
  actions: {
    async adminLogin(email, password) {
      try {
        this.authError = null;
        
        const response = await axios.post(`${API_BASE_URL}/auth/admin/login`, {
          email,
          password
        });
        
        const { token, admin } = response.data;
        
        this.adminToken = token;
        this.adminUser = admin;
        this.isAdminAuthenticated = true;
        
        // Store token in localStorage
        localStorage.setItem('adminToken', token);
        
        // Show success toast
        const toastStore = useToastStore();
        toastStore.success('Admin login successful');
        
        return true;
      } catch (error) {
        this.authError = error.response?.data?.error || 'Admin login failed';
        return false;
      }
    },
    
    adminLogout() {
      this.isAdminAuthenticated = false;
      this.adminToken = null;
      this.adminUser = null;
      
      // Remove token from localStorage
      localStorage.removeItem('adminToken');
      
      // Show logout toast
      const toastStore = useToastStore();
      toastStore.info('Admin logged out');
      
      // Redirect to admin login
      router.push('/portal/login');
    },
    
    initializeAdminAuth() {
      const token = localStorage.getItem('adminToken');
      
      if (token) {
        this.adminToken = token;
        this.isAdminAuthenticated = true;
        
        // You can fetch admin profile here if you have an endpoint for it
      } else {
        this.isAdminAuthenticated = false;
        this.adminToken = null;
        this.adminUser = null;
      }
    },
    
    // Check if the user is authenticated as an admin
    checkAdminAuth() {
      return this.isAdminAuthenticated && this.adminToken;
    }
  }
}); 
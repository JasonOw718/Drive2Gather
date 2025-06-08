import { defineStore } from 'pinia'
import { authService } from '../services/api'
import router from '../router'
import { useToastStore } from './toast'

export const useUserStore = defineStore('user', {
  state: () => ({
    currentUser: null,
    isAuthenticated: false,
    token: null,
    authError: null,
    profileLoading: false
  }),
  actions: {
    async login(email, password) {
      try {
        this.authError = null;
        const response = await authService.login({ email, password });
        console.log('Login response:', response.data);
        const { token, expiresIn, user } = response.data;
        
        // Extract user info from decoded JWT if possible
        try {
          const base64Url = token.split('.')[1];
          const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
          const decodedToken = JSON.parse(window.atob(base64));
          console.log('Decoded token:', decodedToken);
          
          // Merge JWT user data with response user data
          const enhancedUser = {
            ...user,
            user_id: decodedToken.user_id || decodedToken.sub,
            id: decodedToken.user_id || decodedToken.sub,
          };
          
          this.currentUser = enhancedUser;
          localStorage.setItem('user', JSON.stringify(enhancedUser));
        } catch (e) {
          console.error('Error decoding token:', e);
          this.currentUser = user;
          localStorage.setItem('user', JSON.stringify(user));
        }
        
        this.token = token;
        this.isAuthenticated = true;
        
        // Store token in localStorage
        localStorage.setItem('token', token);
        
        // Show success toast
        const toastStore = useToastStore();
        toastStore.success('Login successful!');
        
        // Navigate to home page after successful login
        router.push('/');
        
        return true;
      } catch (error) {
        this.authError = error.response?.data?.error || 'Login failed';
        
        // Show error toast
        const toastStore = useToastStore();
        toastStore.error(this.authError);
        
        return false;
      }
    },
    
    async registerPassenger(userData) {
      try {
        this.authError = null;
        await authService.registerPassenger(userData);
        
        // Show success toast
        const toastStore = useToastStore();
        toastStore.success('Registration successful! Please log in.');
        
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
        
        // Show success toast
        const toastStore = useToastStore();
        toastStore.info('Your driver account is under review. You will be notified once approved.');
        
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
      
      // Show logout toast
      const toastStore = useToastStore();
      toastStore.info('You have been logged out.');
      
      router.push('/login-register');
    },
    
    initializeAuth() {
      const token = localStorage.getItem('token');
      const user = localStorage.getItem('user');
      
      if (token && user) {
        this.token = token;
        const userData = JSON.parse(user);
        
        // Try to extract user ID from JWT if not in stored user data
        if (!userData.user_id && !userData.id) {
          try {
            const base64Url = token.split('.')[1];
            const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
            const decodedToken = JSON.parse(window.atob(base64));
            
            // Add user_id to user data
            userData.user_id = decodedToken.user_id || decodedToken.sub;
            userData.id = decodedToken.user_id || decodedToken.sub;
            
            // Update stored user data
            localStorage.setItem('user', JSON.stringify(userData));
          } catch (e) {
            console.error('Error decoding token:', e);
          }
        }
        
        this.currentUser = userData;
        this.isAuthenticated = true;
      } else {
        // Ensure isAuthenticated is false if there's no token/user
        this.isAuthenticated = false;
        this.currentUser = null;
        this.token = null;
      }
    },
    
    async fetchUserProfile() {
      if (!this.isAuthenticated) return false;
      
      this.profileLoading = true;
      try {
        const response = await authService.getUserProfile();
        const userData = response.data.user || response.data;
        
        // Update user data in store
        this.currentUser = userData;
        
        // Update user data in localStorage
        localStorage.setItem('user', JSON.stringify(userData));
        
        return userData;
      } catch (error) {
        console.error('Error fetching user profile:', error);
        if (error.response && error.response.status === 401) {
          // If unauthorized, logout user and redirect to login page
          this.logout();
          // Redirect will be handled by the API interceptor
        }
        return null;
      } finally {
        this.profileLoading = false;
      }
    },
    
    async changePassword(oldPassword, newPassword) {
      try {
        if (!this.currentUser || !this.currentUser.user_id) {
          return { success: false, error: 'User not authenticated' };
        }
        
        const response = await authService.changePassword({
          userId: this.currentUser.user_id,
          oldPassword,
          newPassword
        });
        
        return { success: true };
      } catch (error) {
        console.error('Error changing password:', error);
        return { 
          success: false, 
          error: error.response?.data?.error || 'Failed to change password' 
        };
      }
    }
  }
}) 
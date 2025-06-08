import axios from 'axios';
import { useUserStore } from '@/stores/user';
import { useToastStore } from '@/stores/toast';
import { useAdminAuthStore } from '@/stores/adminAuth';
import { useDonorAuthStore } from '@/stores/donorAuth';
import router from '@/router';

// Get API base URL from environment variables or use default
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

// Create axios instance with base URL
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
});

// Request interceptor for API calls
api.interceptors.request.use(
  config => {
    // Check if this is an admin endpoint
    const isAdminEndpoint = config.url.includes('/admin/');
    
    if (isAdminEndpoint) {
      // For admin endpoints, use admin token
      const adminAuthStore = useAdminAuthStore();
      const token = adminAuthStore.adminToken;
      
      if (token) {
        config.headers['Authorization'] = `Bearer ${token}`;
      }
    } else {
      // For regular endpoints, use user token
      const userStore = useUserStore();
      const token = userStore.token;
      
      if (token) {
        config.headers['Authorization'] = `Bearer ${token}`;
      }
    }
    
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  response => {
    return response;
  },
  error => {
    const toastStore = useToastStore();
    
    // Check for authentication errors (401 Unauthorized)
    if (error.response && error.response.status === 401) {
      // Handle token expiration or invalid credentials
      const path = router.currentRoute.value.path;
      
      // Check which type of authentication failed based on the request URL
      if (path.startsWith('/portal/admin')) {
        // Admin authentication failed
        const adminAuthStore = useAdminAuthStore();
        adminAuthStore.adminLogout();
        toastStore.error('Admin session expired. Please log in again.');
        router.push('/portal/login');
      } else if (path.startsWith('/portal/donor')) {
        // Donor authentication failed
        const donorAuthStore = useDonorAuthStore();
        donorAuthStore.donorLogout();
        toastStore.error('Session expired. Please log in again.');
        router.push('/portal/login');
      } else {
        // Regular user authentication failed
        const userStore = useUserStore();
        userStore.logout();
        toastStore.error('Session expired. Please log in again.');
        router.push('/login-register');
      }
      
      return Promise.reject(error);
    }
    
    // Handle other error types
    if (error.response) {
      // Server responded with an error status
      const errorMessage = error.response.data?.error || 'An error occurred with the request';
      toastStore.error(errorMessage);
    } else if (error.request) {
      // Request was made but no response received
      toastStore.error('No response received from server. Please check your connection.');
    } else {
      // Something happened in setting up the request
      toastStore.error('Request error: ' + error.message);
    }
    
    return Promise.reject(error);
  }
);

export default api;

// Helper function to handle API responses with toast notifications
const withToast = async (apiCall, successMessage) => {
  const toastStore = useToastStore();
  try {
    const response = await apiCall();
    if (successMessage) {
      toastStore.success(successMessage);
    }
    return response;
  } catch (error) {
    // Error is already handled by the response interceptor
    throw error;
  }
};

// Custom services built on top of the api instance
export const authService = {
  login: (credentials) => api.post('/auth/login', credentials),
  getUsers: () => api.get('/auth/users'),
  getDrivers: () => api.get('/auth/drivers'),
  registerPassenger: (userData) => withToast(
    () => api.post('/auth/users', userData),
    'Passenger registration successful!'
  ),
  registerDriver: (userData) => withToast(
    () => api.post('/auth/drivers', userData),
    'Driver registration successful!'
  ),
  getUserProfile: () => api.get('/auth/profile'),
  updateUserProfile: (userData) => withToast(
    () => api.put('/auth/profile', userData),
    'Profile updated successfully!'
  ),
  changePassword: (passwordData) => withToast(
    () => api.post('/auth/change-password', passwordData),
    'Password changed successfully!'
  )
};

export const donationService = {
  // Create a donation
  createDonation: (donationData) => withToast(
    () => api.post('/donations', donationData),
    'Donation sent successfully!'
  ),
  
  // Get donations received by the current user
  getReceivedDonations: (params) => api.get('/donations/received', { params }),
  
  // Get donations made by the current user
  getMadeDonations: (params) => api.get('/donations/made', { params })
};

export const notificationService = {
  // Get notifications for the current user
  getNotifications: (params) => api.get('/notifications', { params }),
  
  // Mark a notification as read
  markAsRead: (notificationId) => withToast(
    () => api.put(`/notifications/read/${notificationId}`),
    'Notification marked as read'
  ),
  
  // Mark all notifications as read
  markAllAsRead: () => withToast(
    () => api.put('/notifications/read-all'),
    'All notifications marked as read'
  )
};

export const feedbackService = {
  // Submit feedback/report about a ride
  submitFeedback: (feedbackData) => {
    const userStore = useUserStore();
    const token = userStore.token;
    
    // Create FormData object - this will ensure the request uses
    // application/x-www-form-urlencoded instead of application/json
    // which will avoid preflight for simple POST requests
    const formData = new URLSearchParams();
    formData.append('ride_id', feedbackData.rideId);
    formData.append('issue_type', feedbackData.issueType);
    formData.append('comments', feedbackData.description || '');
    formData.append('token', token);
    
    return withToast(
      () => axios.post(`${API_BASE_URL}/feedback`, formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      }),
      'Report submitted successfully!'
    );
  },
  
  // Get all feedback reports (admin only) - explicitly use admin token
  getAllFeedback: () => {
    const adminAuthStore = useAdminAuthStore();
    const token = adminAuthStore.adminToken;
    
    if (!token) {
      const toastStore = useToastStore();
      toastStore.error('Admin authentication required');
      return Promise.reject(new Error('Admin authentication required'));
    }
    
    return axios.get(`${API_BASE_URL}/feedback/admin/feedbacks`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      }
    });
  }
};

export const rideService = {
  // Ride search and creation
  searchRides: (params) => api.get('/rides', { params }),
  createRide: (rideData) => {
    if (!rideData.driverID) {
      return Promise.reject(new Error('Missing required field: driverID'));
    }
    
    return withToast(
      () => api.post('/rides', {
        driverID: parseInt(rideData.driverID),
        startingLocation: rideData.startingLocation,
        dropoffLocation: rideData.dropoffLocation,
        requestTime: rideData.requestTime,
        Passenger_count: parseInt(rideData.Passenger_count || 1)
      }),
      'Ride created successfully!'
    );
  },
  
  // Homepage data
  getHomepageData: () => api.get('/rides/homepage'),
  
  // Ride history and details
  getUserRideHistory: (params) => api.get('/rides/user-history', { params }),
  filterRides: (params) => api.get('/rides/filter', { params }),
  getRideDetails: (rideId) => api.get(`/rides/${rideId}`),
  getRideById: (rideId) => api.get(`/rides/${rideId}`),
  getRideDetailsWithPassengers: (rideId) => api.get(`/rides/${rideId}/details`),
  
  // Ride requests
  requestRide: (rideId, passengerData) => withToast(
    () => api.post(`/rides/requests`, { 
      rideID: rideId,
      passengerID: passengerData.passengerID || 1,
      seatCount: passengerData.seats || 1
    }),
    'Ride request submitted successfully!'
  ),
  getDriverRideRequests: (driverId) => api.get(`/rides/driver/${driverId}/requests`),
  getPassengerRideRequests: (passengerId) => api.get(`/rides/passenger/${passengerId}/requests`),
  approveRideRequest: (requestData) => withToast(
    () => api.post('/rides/requests/approve', {
      rideID: requestData.rideId,
      passengerID: requestData.passengerId
    }),
    'Ride request approved!'
  ),
  rejectRideRequest: (requestData) => withToast(
    () => api.post('/rides/requests/reject', {
      rideID: requestData.rideId,
      passengerID: requestData.passengerId
    }),
    'Ride request rejected'
  ),
  cancelRideRequest: (rideId) => withToast(
    () => api.post(`/rides/${rideId}/cancel`),
    'Ride request cancelled'
  ),
  
  // Mark ride as completed
  completeRide: (rideId) => withToast(
    () => api.post(`/rides/${rideId}/complete`),
    'Ride marked as completed!'
  )
};

export const chatService = {
  // Get chat for a ride
  getChatByRideId: (rideId) => api.get(`/chats/ride/${rideId}`),
  
  // Get messages for a chat
  getMessages: (chatId) => api.get(`/chats/${chatId}/messages`),
  
  // Send a message in a chat
  sendMessage: (chatId, content) => api.post(`/chats/${chatId}/messages`, { content }),
  
  // Get all chats for a user
  getUserChats: (userId) => api.get(`/chats/user/${userId}/chats`),
  
  // Create a new chat for a ride
  createChat: (rideId) => withToast(
    () => api.post('/chats', { ride_id: rideId }),
    'Chat room created successfully!'
  )
}; 
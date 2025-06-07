import axios from 'axios';
import { useUserStore } from '@/stores/user';

// Create axios instance with base URL
const api = axios.create({
  baseURL: 'http://127.0.0.1:5000/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
});

// Request interceptor for API calls
api.interceptors.request.use(
  config => {
    const userStore = useUserStore();
    const token = userStore.token;
    
    if (token) {
      console.log(`Adding token to request: ${token.substring(0, 15)}...`);
      config.headers['Authorization'] = `Bearer ${token}`;
    } else {
      console.log('No token available for request');
    }
    
    return config;
  },
  error => {
    console.error('Request interceptor error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for API calls
api.interceptors.response.use(
  response => {
    return response;
  },
  async error => {
    const originalRequest = error.config;
    console.log('Response error:', error.response?.status, error.response?.data);
    
    // Handle token refresh or redirect to login if 401
    if (error.response && error.response.status === 401 && !originalRequest._retry) {
      // Check for specific authentication errors that should trigger logout
      const errorMessage = error.response.data?.error || '';
      const authErrors = [
        'Token is missing',
        'Token has expired',
        'Invalid token',
        'User not found'
      ];
      
      // Only logout for specific authentication errors
      if (authErrors.some(msg => errorMessage.includes(msg))) {
        console.log(`Auth error detected: ${errorMessage}. Logging out.`);
        originalRequest._retry = true;
        
        const userStore = useUserStore();
        userStore.logout();
        
        // Use a small delay before redirecting to allow for state updates
        setTimeout(() => {
          window.location.href = '/login?reason=session_expired';
        }, 100);
      } else {
        console.log(`Non-auth 401 error: ${errorMessage}. Not logging out.`);
      }
    }
    
    return Promise.reject(error);
  }
);

export default api;

// Custom services built on top of the api instance
export const authService = {
  login: (credentials) => api.post('/auth/login', credentials),
  getUsers: () => api.get('/auth/users'),
  getDrivers: () => api.get('/auth/drivers'),
  registerPassenger: (userData) => api.post('/auth/users', userData),
  registerDriver: (userData) => api.post('/auth/drivers', userData),
  getUserProfile: () => api.get('/auth/profile'),
  updateUserProfile: (userData) => api.put('/auth/profile', userData)
};

export const notificationService = {
  // Get notifications for the current user
  getNotifications: (params) => api.get('/notifications', { params }),
  
  // Mark a notification as read
  markAsRead: (notificationId) => api.put(`/notifications/read/${notificationId}`),
  
  // Mark all notifications as read
  markAllAsRead: () => api.put('/notifications/read-all')
};

export const rideService = {
  // Ride search and creation
  searchRides: (params) => api.get('/rides', { params }),
  createRide: (rideData) => {
    console.log('Creating ride with data:', rideData);
    
    if (!rideData.driverID) {
      return Promise.reject(new Error('Missing required field: driverID'));
    }
    
    return api.post('/rides', {
      driverID: parseInt(rideData.driverID),
      startingLocation: rideData.startingLocation,
      dropoffLocation: rideData.dropoffLocation,
      requestTime: rideData.requestTime,
      Passenger_count: parseInt(rideData.Passenger_count || 1)
    });
  },
  
  // Ride history and details
  getUserRideHistory: (params) => api.get('/rides/user-history', { params }),
  getRideDetails: (rideId) => api.get(`/rides/${rideId}`),
  getRideById: (rideId) => api.get(`/rides/${rideId}`),
  getRideDetailsWithPassengers: (rideId) => api.get(`/rides/${rideId}/details`),
  
  // Ride requests
  requestRide: (rideId, passengerData) => api.post(`/rides/requests`, { 
    rideID: rideId,
    passengerID: passengerData.passengerID || 1,
    seatCount: passengerData.seats || 1
  }),
  getDriverRideRequests: (driverId) => api.get(`/rides/driver/${driverId}/requests`),
  getPassengerRideRequests: (passengerId) => api.get(`/rides/passenger/${passengerId}/requests`),
  approveRideRequest: (requestData) => api.post('/rides/requests/approve', {
    rideID: requestData.rideId,
    passengerID: requestData.passengerId
  }),
  rejectRideRequest: (requestData) => api.post('/rides/requests/reject', {
    rideID: requestData.rideId,
    passengerID: requestData.passengerId
  }),
  cancelRideRequest: (rideId) => api.post(`/rides/${rideId}/cancel`)
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
  createChat: (rideId) => api.post('/chats', { ride_id: rideId })
}; 
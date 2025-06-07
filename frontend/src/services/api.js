import axios from 'axios';
import { useUserStore } from '@/stores/user';
import { useToastStore } from '@/stores/toast';

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

// Response interceptor
api.interceptors.response.use(
  response => {
    return response;
  },
  error => {
    const toastStore = useToastStore();
    
    // Handle error and show toast message
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

export const rideService = {
  // Ride search and creation
  searchRides: (params) => api.get('/rides', { params }),
  createRide: (rideData) => {
    console.log('Creating ride with data:', rideData);
    
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
  sendMessage: (chatId, content) => withToast(
    () => api.post(`/chats/${chatId}/messages`, { content }),
    null // No toast for message sending to avoid spam
  ),
  
  // Get all chats for a user
  getUserChats: (userId) => api.get(`/chats/user/${userId}/chats`),
  
  // Create a new chat for a ride
  createChat: (rideId) => withToast(
    () => api.post('/chats', { ride_id: rideId }),
    'Chat room created successfully!'
  )
}; 
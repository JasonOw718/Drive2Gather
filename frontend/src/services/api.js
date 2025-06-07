import axios from 'axios';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: 'http://localhost:5000/api',
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000
});

// Request interceptor to add auth token to requests
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Authentication services
export const authService = {
  // Login user
  login(credentials) {
    return apiClient.post('/auth/login', credentials);
  },
  
  // Register passenger
  registerPassenger(userData) {
    return apiClient.post('/auth/users', userData);
  },
  
  // Register driver
  registerDriver(driverData) {
    return apiClient.post('/auth/drivers', driverData);
  },
  
  // Change password
  changePassword(passwordData) {
    return apiClient.post('/auth/change-password', passwordData);
  },
  
  // Forgot password
  forgotPassword(emailData) {
    return apiClient.post('/auth/forgot-password', emailData);
  }
};

// Ride services
export const rideService = {
  // Get all rides with filtering
  getAllRides(options = {}) {
    const { 
      page = 1, 
      size = 20, 
      starting_location = '', 
      dropoff_location = '', 
      request_time = '', 
      seats = '' 
    } = options;
    
    // Build query parameters
    const params = new URLSearchParams();
    params.append('page', page);
    params.append('size', size);
    
    if (starting_location) params.append('starting_location', starting_location);
    if (dropoff_location) params.append('dropoff_location', dropoff_location);
    if (request_time) params.append('request_time', request_time);
    if (seats) params.append('seats', seats);
    
    return apiClient.get(`/rides?${params.toString()}`);
  },
  
  // Get ride by ID
  getRideById(rideId) {
    return apiClient.get(`/rides/${rideId}`);
  },
  
  // Create new ride
  createRide(rideData) {
    return apiClient.post('/rides', rideData);
  },
  
  // Request a ride
  requestRide(rideId, passengerData) {
    return apiClient.post(`/rides/${rideId}/request`, passengerData);
  }
};

export default {
  auth: authService,
  rides: rideService
}; 
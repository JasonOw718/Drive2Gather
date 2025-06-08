<template>
  <div>
    <RightNavbar />
    <div class="min-h-screen bg-white px-6 pt-6 pb-20" style="max-width: 420px; margin: 0 auto;">
      <!-- Back Button -->
      <button
        class="absolute top-6 left-6 w-10 h-10 flex items-center justify-center rounded-lg bg-[#F5F5F5] z-20 border border-gray-200"
        @click="$router.back()"
        aria-label="Back"
      >
        <span class="w-6 h-6 text-primary">
          <font-awesome-icon icon="fa-arrow-left" class="text-[#C77DFF]" />
        </span>
      </button>
      
      <!-- Header -->
      <div class="mb-6 pt-8">
        <h1 class="text-2xl font-bold text-left text-[#303030] mb-2">Ride History</h1>
        <p class="text-[#8C8C8C] text-left">
          View all your past and upcoming rides
        </p>
      </div>

      <!-- Filter Tabs -->
      <div class="flex border-b border-gray-200 mb-6">
        <button 
          @click="activeTab = 'history'" 
          :class="[
            'py-2 px-4 font-medium text-sm focus:outline-none',
            activeTab === 'history' 
              ? 'text-[#C77DFF] border-b-2 border-[#C77DFF]' 
              : 'text-gray-500 hover:text-[#C77DFF]'
          ]"
        >
          Ride History
        </button>
        <button 
          @click="activeTab = 'pending'" 
          :class="[
            'py-2 px-4 font-medium text-sm focus:outline-none',
            activeTab === 'pending' 
              ? 'text-[#C77DFF] border-b-2 border-[#C77DFF]' 
              : 'text-gray-500 hover:text-[#C77DFF]'
          ]"
        >
          Pending Requests
        </button>
        <div class="flex-grow"></div>
        <button 
          @click="$router.push('/ride-filter')" 
          class="py-2 px-4 font-medium text-sm focus:outline-none text-[#C77DFF] hover:bg-[#F8F0FF] rounded-md"
        >
          <font-awesome-icon icon="fa-filter" class="mr-1" />
          Filter
        </button>
      </div>

      <!-- Pending Ride Requests Tab Content -->
      <div v-if="activeTab === 'pending'">
        <!-- Loading State for Requests -->
        <div v-if="loadingRequests" class="flex justify-center items-center py-8">
          <svg class="animate-spin h-8 w-8 text-[#C77DFF]" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"></path>
          </svg>
        </div>
        
        <!-- Empty State for Requests -->
        <div v-else-if="requests.length === 0" class="text-center text-gray-500 py-6 border border-gray-200 rounded-xl">
          No pending ride requests
        </div>
        
        <!-- Ride Requests List -->
        <div v-else class="space-y-4">
          <div v-for="(request, index) in requests" :key="index" class="border border-gray-200 rounded-xl p-4 shadow-sm">
            <!-- Request Card for Driver -->
            <div v-if="userStore.currentUser?.role === 'driver'" class="flex flex-col">
              <div class="flex justify-between items-start mb-3">
                <div>
                  <div class="text-base font-medium text-[#303030]">{{ request.passengerName }}</div>
                  <div class="text-xs text-gray-500">wants to join your ride</div>
                </div>
                <span class="text-xs rounded-full px-3 py-1 bg-yellow-100 text-yellow-800 font-medium">
                  Pending
                </span>
              </div>
              
              <div class="flex items-center gap-4 mb-3">
                <div class="text-base font-semibold text-[#303030] w-14 text-left">{{ formatTime(request.requestTime) }}</div>
                <div class="flex flex-col items-center justify-center h-14 relative">
                  <div class="w-1 h-14 bg-[#C77DFF] absolute left-1/2 top-0 -translate-x-1/2 z-0"></div>
                  <div class="w-3 h-3 rounded-full bg-[#C77DFF] z-10"></div>
                  <div class="flex-1"></div>
                  <div class="w-3 h-3 rounded-full bg-[#C77DFF] z-10"></div>
                </div>
                <div class="flex flex-col justify-between h-14 ml-2">
                  <div class="text-sm font-medium text-[#303030] text-left">{{ request.startingLocation }}</div>
                  <div class="flex-1"></div>
                  <div class="text-sm font-medium text-[#303030] text-left">{{ request.dropoffLocation }}</div>
                </div>
              </div>
              
              <div class="flex justify-end gap-2 mt-2">
                <button @click="respondToRequest(request.rideID, request.passengerID, 'accepted')" 
                  class="px-4 py-2 bg-[#C77DFF] text-white rounded-full text-sm">
                  Accept
                </button>
                <button @click="respondToRequest(request.rideID, request.passengerID, 'rejected')" 
                  class="px-4 py-2 border border-red-500 text-red-500 rounded-full text-sm">
                  Reject
                </button>
              </div>
            </div>
            
            <!-- Request Card for Passenger -->
            <div v-else class="flex flex-col">
              <div class="flex justify-between items-start mb-3">
                <div>
                  <div class="text-base font-medium text-[#303030]">Ride to {{ request.dropoffLocation }}</div>
                  <div class="text-xs text-gray-500">Request pending driver approval</div>
                </div>
                <span class="text-xs rounded-full px-3 py-1 bg-yellow-100 text-yellow-800 font-medium">
                  Pending
                </span>
              </div>
              
              <div class="flex items-center gap-4 mb-3">
                <div class="text-base font-semibold text-[#303030] w-14 text-left">{{ formatTime(request.requestTime) }}</div>
                <div class="flex flex-col items-center justify-center h-14 relative">
                  <div class="w-1 h-14 bg-[#C77DFF] absolute left-1/2 top-0 -translate-x-1/2 z-0"></div>
                  <div class="w-3 h-3 rounded-full bg-[#C77DFF] z-10"></div>
                  <div class="flex-1"></div>
                  <div class="w-3 h-3 rounded-full bg-[#C77DFF] z-10"></div>
                </div>
                <div class="flex flex-col justify-between h-14 ml-2">
                  <div class="text-sm font-medium text-[#303030] text-left">{{ request.startingLocation }}</div>
                  <div class="flex-1"></div>
                  <div class="text-sm font-medium text-[#303030] text-left">{{ request.dropoffLocation }}</div>
                </div>
              </div>
              
              <div class="mt-2 text-sm text-gray-500">
                <span>Driver: {{ request.driverName }}</span>
              </div>
              
              <div class="flex justify-end mt-2">
                <button @click="cancelRequest(request.rideID)" 
                  class="px-4 py-2 border border-red-500 text-red-500 rounded-full text-sm">
                  Cancel Request
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Ride History Tab Content -->
      <div v-if="activeTab === 'history'">
        <!-- Loading State -->
        <div v-if="loading" class="flex justify-center items-center h-64">
          <svg class="animate-spin h-12 w-12 text-[#C77DFF]" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"></path>
          </svg>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="text-center text-red-500 p-8">
          {{ error }}
          <button @click="loadRideHistory" class="block mx-auto mt-4 text-[#C77DFF] underline">Try Again</button>
        </div>

        <!-- Empty State -->
        <div v-else-if="rides.length === 0" class="text-center p-8">
          <font-awesome-icon icon="fa-car" class="text-gray-300 text-5xl mb-4" />
          <p class="text-gray-500">No ride history found</p>
          <button 
            v-if="userStore.currentUser?.role === 'passenger'"
            @click="$router.push('/find-ride')" 
            class="mt-4 px-4 py-2 bg-[#C77DFF] text-white rounded-full text-sm"
          >
            Find a Ride
          </button>
          <button 
            v-else-if="userStore.currentUser?.role === 'driver'"
            @click="$router.push('/create-ride')" 
            class="mt-4 px-4 py-2 bg-[#C77DFF] text-white rounded-full text-sm"
          >
            Create a Ride
          </button>
        </div>

        <!-- Ride List -->
        <div v-else class="space-y-4">
          <div v-for="(ride, index) in rides" :key="index" class="border border-gray-200 rounded-xl p-4 shadow-sm">
            <!-- Status Badge -->
            <div class="flex justify-end items-start mb-3">
              <span 
                :class="[
                  'text-xs rounded-full px-3 py-1 font-medium', 
                  getStatusClass(ride.status)
                ]"
              >
                {{ formatStatus(ride.status) }}
              </span>
            </div>

            <!-- Ride Details -->
            <div class="flex items-center gap-4 mb-3">
              <div class="text-base font-semibold text-[#303030] w-14 text-left">{{ formatTime(ride.requestTime) }}</div>
              <div class="flex flex-col items-center justify-center h-14 relative">
                <div class="w-1 h-14 bg-[#C77DFF] absolute left-1/2 top-0 -translate-x-1/2 z-0"></div>
                <div class="w-3 h-3 rounded-full bg-[#C77DFF] z-10"></div>
                <div class="flex-1"></div>
                <div class="w-3 h-3 rounded-full bg-[#C77DFF] z-10"></div>
              </div>
              <div class="flex flex-col justify-between h-14 ml-2">
                <div class="text-sm font-medium text-[#303030] text-left">{{ ride.startingLocation }}</div>
                <div class="flex-1"></div>
                <div class="text-sm font-medium text-[#303030] text-left">{{ ride.dropoffLocation }}</div>
              </div>
            </div>

            <!-- Date and Driver/Passengers -->
            <div class="flex justify-between items-center text-sm text-[#8C8C8C]">
              <div>{{ formatDate(ride.requestTime) }}</div>
              <div v-if="userStore.currentUser?.role === 'passenger'" class="text-right">
                <div>Driver: {{ ride.driverName || 'Unknown' }}</div>
                <div v-if="ride.carType">{{ ride.carType }} <span v-if="ride.carColor">({{ ride.carColor }})</span></div>
              </div>
              <div v-else>
                <span>Seats: {{ ride.passengerCount }}</span>
              </div>
            </div>

            <!-- Action Button for active rides -->
            <button 
              v-if="['pending', 'approved', 'accepted', 'active'].includes(ride.status) || userStore.currentUser?.role === 'driver'" 
              @click="viewRideDetails(ride)" 
              class="mt-3 w-full py-2 rounded-full text-[#C77DFF] border border-[#C77DFF] text-sm font-medium hover:bg-[#F8F0FF] transition"
            >
              View Details
            </button>
            
            <!-- View Details button for all passenger rides -->
            <button 
              v-if="userStore.currentUser?.role === 'passenger' && !['pending', 'approved', 'accepted', 'active'].includes(ride.status)" 
              @click="viewRideDetails(ride)" 
              class="mt-3 w-full py-2 rounded-full text-[#C77DFF] border border-[#C77DFF] text-sm font-medium hover:bg-[#F8F0FF] transition"
            >
              View Details
            </button>
          </div>
        </div>

        <!-- Pagination -->
        <div v-if="rides.length > 0" class="mt-6 flex justify-center items-center">
          <div class="flex items-center bg-gray-100 rounded-full p-1 shadow-sm">
            <button 
              @click="prevPage" 
              :disabled="pagination.currentPage <= 1" 
              :class="[
                'px-4 py-2 rounded-full text-sm font-medium transition-colors',
                pagination.currentPage <= 1 
                  ? 'text-gray-400 cursor-not-allowed' 
                  : 'text-[#C77DFF] hover:bg-white hover:shadow-sm'
              ]"
            >
              <font-awesome-icon icon="fa-chevron-left" class="mr-1" />
              Prev
            </button>
            
            <span class="px-3 py-1 text-sm font-medium text-gray-700">
              {{ pagination.currentPage }} / {{ pagination.totalPages }}
            </span>
            
            <button 
              @click="nextPage" 
              :disabled="!pagination.nextPage" 
              :class="[
                'px-4 py-2 rounded-full text-sm font-medium transition-colors',
                !pagination.nextPage 
                  ? 'text-gray-400 cursor-not-allowed' 
                  : 'text-[#C77DFF] hover:bg-white hover:shadow-sm'
              ]"
            >
              Next
              <font-awesome-icon icon="fa-chevron-right" class="ml-1" />
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/stores/user';
import { formatDateTime } from '@/utils/dateFormatter';
import api from '@/services/api';
import RightNavbar from './rightnavbar.vue';

const router = useRouter();
const userStore = useUserStore();

// State
const rides = ref([]);
const requests = ref([]);
const loading = ref(false);
const loadingRequests = ref(false);
const error = ref(null);
const pagination = ref({
  currentPage: 1,
  totalPages: 1,
  nextPage: false,
  prevPage: null
});
const activeTab = ref('history');

// Load ride history from API
const loadRideHistory = async () => {
  loading.value = true;
  error.value = null;
  
  try {
    // If we're authenticated but don't have user info, try to refresh it
    if (userStore.isAuthenticated && (!userStore.currentUser || !userStore.currentUser.id)) {
      console.log('User info missing but authenticated. Attempting to refresh profile...');
      await userStore.fetchUserProfile();
      console.log('Refreshed user profile:', userStore.currentUser);
    }
    
    // Check if user is authenticated
    if (!userStore.isAuthenticated || !userStore.currentUser) {
      console.error('User not authenticated. Redirecting to login...');
      error.value = 'Please log in to view your ride history.';
      setTimeout(() => router.push('/login'), 2000);
      return;
    }
    
    // Use the user-history endpoint with pagination
    const response = await api.get('/rides/user-history', {
      params: {
        page: pagination.value.currentPage,
        role: userStore.currentUser?.role || 'passenger'
      }
    });
    
    rides.value = response.data.rides;
    
    // Log ride statuses for debugging
    console.log('Loaded ride history:', rides.value);
    console.log('Ride statuses:', rides.value.map(ride => ({ id: ride.rideID, status: ride.status })));
    
    // Update pagination
    pagination.value.currentPage = response.data.page;
    pagination.value.totalPages = response.data.total_pages;
    pagination.value.nextPage = response.data.page < response.data.total_pages;
    pagination.value.prevPage = response.data.page > 1;
  } catch (err) {
    console.error('Error loading ride history:', err);
    
    // Check for authentication errors
    if (err.response?.status === 401 || err.response?.status === 403) {
      error.value = 'Authentication error. Please try logging in again.';
      // Redirect to login after a short delay
      setTimeout(() => {
        userStore.logout();
        router.push('/login');
      }, 2000);
    } else {
      error.value = 'Failed to load ride history. Please try again.';
    }
  } finally {
    loading.value = false;
  }
};

// Load pending ride requests
const loadPendingRequests = async () => {
  loadingRequests.value = true;
  
  try {
    // Get current user information
    let currentUser = userStore.currentUser;
    
    // Debug user information
    console.log('Current user state:', currentUser);
    console.log('User ID:', currentUser?.id);
    console.log('User role:', currentUser?.role);
    
    // If user info is missing but we're authenticated, try to refresh the profile
    if (userStore.isAuthenticated && (!currentUser || !currentUser.id)) {
      console.log('User info missing but authenticated. Attempting to refresh profile...');
      currentUser = await userStore.fetchUserProfile();
      console.log('Refreshed user profile:', currentUser);
    }
    
    // Check if user information is available
    if (!currentUser || !currentUser.id) {
      console.error('User information not available. Check if user is logged in properly.');
      error.value = 'Please log in to view your ride requests.';
      loadingRequests.value = false;
      return;
    }
    
    const userId = currentUser.id;
    const role = currentUser.role || 'passenger';
    
    let endpoint = '';
    if (role === 'driver') {
      endpoint = `/rides/driver/${userId}/requests`;
    } else {
      endpoint = `/rides/passenger/${userId}/requests`;
    }
    
    console.log(`Making request to: ${endpoint} for user ID: ${userId} with role: ${role}`);
    
    const response = await api.get(endpoint);
    requests.value = response.data.requests || [];
  } catch (err) {
    console.error('Error loading ride requests:', err);
    console.error('Error details:', err.response?.data || err.message);
    
    // Check for specific authentication errors
    if (err.response?.status === 401 || err.response?.status === 403) {
      error.value = 'Authentication error. Please try logging in again.';
      // Redirect to login after a short delay
      setTimeout(() => {
        userStore.logout();
        router.push('/login');
      }, 2000);
    } else {
      error.value = 'Failed to load ride requests. Please try again.';
    }
    
    requests.value = [];
  } finally {
    loadingRequests.value = false;
  }
};

// Respond to a ride request (accept/reject)
const respondToRequest = async (rideId, passengerId, action) => {
  try {
    if (action === 'accepted') {
      await api.post(`/rides/requests/approve`, { 
        rideID: rideId,
        passengerID: passengerId
      });
    } else {
      await api.post(`/rides/requests/reject`, { 
        rideID: rideId,
        passengerID: passengerId
      });
    }
    
    // Refresh the requests list
    loadPendingRequests();
  } catch (err) {
    console.error(`Error ${action} request:`, err);
    alert(`Failed to ${action} request. Please try again.`);
  }
};

// Cancel a ride request (for passengers)
const cancelRequest = async (rideId) => {
  try {
    await api.post(`/rides/${rideId}/cancel`);
    
    // Refresh the requests list
    loadPendingRequests();
  } catch (err) {
    console.error('Error cancelling request:', err);
    alert('Failed to cancel request. Please try again.');
  }
};

// Pagination handlers
const nextPage = () => {
  if (pagination.value.nextPage) {
    pagination.value.currentPage++;
    loadRideHistory();
  }
};

const prevPage = () => {
  if (pagination.value.currentPage > 1) {
    pagination.value.currentPage--;
    loadRideHistory();
  }
};

// Format dates and times
const formatTime = (dateString) => {
  if (!dateString) return '';
  return formatDateTime(dateString, 'HH:mm');
};

const formatDate = (dateString) => {
  if (!dateString) return '';
  return formatDateTime(dateString, 'MMM DD, YYYY');
};

// Format status text
const formatStatus = (status) => {
  if (!status) return '';
  
  const statusMap = {
    'pending': 'Pending',
    'approved': 'Approved',
    'accepted': 'Accepted',
    'active': 'Active',
    'completed': 'Completed',
    'cancelled': 'Cancelled',
    'rejected': 'Rejected'
  };
  
  return statusMap[status.toLowerCase()] || status;
};

// Get CSS class for status badge
const getStatusClass = (status) => {
  if (!status) return '';
  
  const statusClassMap = {
    'pending': 'bg-yellow-100 text-yellow-800',
    'approved': 'bg-blue-100 text-blue-800',
    'accepted': 'bg-blue-100 text-blue-800',
    'active': 'bg-green-100 text-green-800',
    'completed': 'bg-gray-100 text-gray-800',
    'cancelled': 'bg-red-100 text-red-800',
    'rejected': 'bg-red-100 text-red-800'
  };
  
  return statusClassMap[status.toLowerCase()] || 'bg-gray-100 text-gray-800';
};

// View ride details
const viewRideDetails = (ride) => {
  router.push({
    path: `/ride/${ride.rideID || ride.id}`,
    query: { from_history: 'true' }
  });
};

// Watch for tab changes
watch(activeTab, (newTab) => {
  if (newTab === 'history') {
    loadRideHistory();
  } else if (newTab === 'pending') {
    loadPendingRequests();
  }
});

// Check authentication and load data on mount
onMounted(async () => {
  console.log('RideHistory component mounted');
  
  // Ensure auth is initialized
  if (!userStore.isAuthenticated) {
    console.log('User not authenticated, initializing auth...');
    userStore.initializeAuth();
  }
  
  // If we have a token but no user data, try to fetch the profile
  if (userStore.token && (!userStore.currentUser || !userStore.currentUser.id)) {
    console.log('We have a token but missing user data, fetching profile...');
    try {
      await userStore.fetchUserProfile();
      console.log('User profile after refresh:', userStore.currentUser);
    } catch (err) {
      console.error('Failed to fetch user profile:', err);
      error.value = 'Authentication error. Please try logging in again.';
      setTimeout(() => {
        userStore.logout();
        router.push('/login');
      }, 2000);
      return;
    }
  }
  
  // Load data based on active tab
  if (activeTab.value === 'history') {
    loadRideHistory();
  } else {
    loadPendingRequests();
  }
});
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
</style> 
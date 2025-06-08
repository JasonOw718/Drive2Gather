<template>
  <div>
    <RightNavbar />
    <div class="min-h-screen bg-white px-6 pt-6 pb-20" style="max-width: 420px; margin: 0 auto;">
      <!-- Back Button -->
      <div class="flex items-center mb-4 mt-2">
        <button
          class="w-10 h-10 flex items-center justify-center rounded-lg bg-[#F5F5F5] border border-gray-200 shadow-md"
          @click="$router.back()"
          aria-label="Back"
        >
          <span class="w-6 h-6 text-primary">
            <font-awesome-icon icon="fa-arrow-left" class="text-[#C77DFF]" />
          </span>
        </button>
      </div>
      
      <!-- Header -->
      <div class="mb-6">
        <h1 class="text-2xl font-bold text-left text-[#303030] mb-2">Filter Rides</h1>
        <p class="text-[#8C8C8C] text-left">
          Find specific rides using various filters
        </p>
      </div>

      <!-- Filter Form -->
      <div class="bg-white rounded-xl shadow-sm p-6 mb-6">
        <div class="mb-4">
          <label class="block text-sm font-medium text-[#303030] mb-2">Filter Type</label>
          <select
            v-model="filterType"
            class="w-full px-4 py-3 bg-[#F8F9FA] border-none rounded-lg focus:outline-none focus:ring-2 focus:ring-[#C77DFF] text-[#303030]"
          >
            <option value="">Select a filter type</option>
            <option value="status">Status</option>
            <option value="time">Time</option>
            <option value="date">Date</option>
          </select>
        </div>

        <!-- Status Filter -->
        <div v-if="filterType === 'status'" class="mb-4">
          <label class="block text-sm font-medium text-[#303030] mb-2">Status</label>
          <select
            v-model="filterCriteria"
            class="w-full px-4 py-3 bg-[#F8F9FA] border-none rounded-lg focus:outline-none focus:ring-2 focus:ring-[#C77DFF] text-[#303030]"
          >
            <option value="">Select a status</option>
            <option value="pending">Pending</option>
            <option value="approved">Approved</option>
            <option value="completed">Completed</option>
            <option value="cancelled">Cancelled</option>
            <option value="rejected">Rejected</option>
          </select>
        </div>

        <!-- Time Filter -->
        <div v-if="filterType === 'time'" class="mb-4">
          <label class="block text-sm font-medium text-[#303030] mb-2">Time (HH:MM)</label>
          <input
            type="time"
            v-model="filterCriteria"
            class="w-full px-4 py-3 bg-[#F8F9FA] border-none rounded-lg focus:outline-none focus:ring-2 focus:ring-[#C77DFF] text-[#303030]"
          />
        </div>

        <!-- Date Filter -->
        <div v-if="filterType === 'date'" class="mb-4">
          <label class="block text-sm font-medium text-[#303030] mb-2">Date</label>
          <input
            type="date"
            v-model="filterCriteria"
            class="w-full px-4 py-3 bg-[#F8F9FA] border-none rounded-lg focus:outline-none focus:ring-2 focus:ring-[#C77DFF] text-[#303030]"
          />
        </div>

        <button
          @click="applyFilter"
          class="w-full py-3 mt-2 bg-[#C77DFF] text-white rounded-lg hover:bg-opacity-90 transition font-medium"
          :disabled="loading"
        >
          <span v-if="loading">
            <font-awesome-icon icon="fa-spinner" spin class="mr-2" />
            Filtering...
          </span>
          <span v-else>Apply Filter</span>
        </button>
      </div>

      <!-- Results -->
      <div>
        <h2 class="text-xl font-semibold text-left text-[#303030] mb-4">Results</h2>

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
          <button @click="applyFilter" class="block mx-auto mt-4 text-[#C77DFF] underline">Try Again</button>
        </div>

        <!-- Empty State -->
        <div v-else-if="rides.length === 0" class="text-center p-8">
          <font-awesome-icon icon="fa-filter" class="text-gray-300 text-5xl mb-4" />
          <p class="text-gray-500">No rides match your filter criteria</p>
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
                <span>Passengers: {{ ride.passengerCount }}</span>
              </div>
            </div>

            <!-- View Details Button -->
            <button 
              @click="viewRideDetails(ride)" 
              class="mt-3 w-full py-2 rounded-full text-[#C77DFF] border border-[#C77DFF] text-sm font-medium hover:bg-[#F8F0FF] transition"
            >
              View Details
            </button>
          </div>
        </div>

        <!-- Pagination -->
        <div v-if="rides.length > 0" class="mt-6 flex justify-between items-center">
          <button 
            @click="prevPage" 
            :disabled="pagination.currentPage <= 1" 
            :class="[
              'px-3 py-1 rounded text-sm',
              pagination.currentPage <= 1 
                ? 'text-gray-400 cursor-not-allowed' 
                : 'text-[#C77DFF] hover:bg-[#F8F0FF]'
            ]"
          >
            Previous
          </button>
          <span class="text-sm text-gray-600">
            Page {{ pagination.currentPage }} of {{ pagination.totalPages }}
          </span>
          <button 
            @click="nextPage" 
            :disabled="!pagination.nextPage" 
            :class="[
              'px-3 py-1 rounded text-sm',
              !pagination.nextPage 
                ? 'text-gray-400 cursor-not-allowed' 
                : 'text-[#C77DFF] hover:bg-[#F8F0FF]'
            ]"
          >
            Next
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '../../stores/user';
import { rideService } from '../../services/api';
import RightNavbar from './rightnavbar.vue';

const router = useRouter();
const userStore = useUserStore();

// Filter state
const filterType = ref('');
const filterCriteria = ref('');
const loading = ref(false);
const error = ref('');

// Ride data
const rides = ref([]);
const pagination = ref({
  currentPage: 1,
  pageSize: 10,
  totalPages: 1,
  totalRides: 0,
  nextPage: null,
  prevPage: null
});

// Apply the selected filter
async function applyFilter() {
  loading.value = true;
  error.value = '';
  
  try {
    const params = {
      page: pagination.value.currentPage,
      size: pagination.value.pageSize
    };
    
    // Add filter parameters if selected
    if (filterType.value) {
      params.filter_type = filterType.value;
    }
    
    if (filterCriteria.value) {
      params.criteria = filterCriteria.value;
    }
    
    const response = await rideService.filterRides(params);
    rides.value = response.data.rides;
    pagination.value = response.data.pagination;
  } catch (err) {
    console.error('Error filtering rides:', err);
    error.value = 'Failed to filter rides. Please try again.';
  } finally {
    loading.value = false;
  }
}

// Pagination functions
function nextPage() {
  if (pagination.value.nextPage) {
    pagination.value.currentPage++;
    applyFilter();
  }
}

function prevPage() {
  if (pagination.value.currentPage > 1) {
    pagination.value.currentPage--;
    applyFilter();
  }
}

// Format time from ISO string to readable time
function formatTime(isoString) {
  if (!isoString) return '';
  const date = new Date(isoString);
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

// Format date from ISO string to readable date
function formatDate(isoString) {
  if (!isoString) return '';
  const date = new Date(isoString);
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
}

// Format status for display
function formatStatus(status) {
  if (!status) return 'Unknown';
  
  const statusMap = {
    'pending': 'Pending',
    'approved': 'Approved',
    'completed': 'Completed',
    'cancelled': 'Cancelled',
    'rejected': 'Rejected',
    'active': 'Active'
  };
  
  return statusMap[status.toLowerCase()] || status;
}

// Get CSS class for status badge
function getStatusClass(status) {
  if (!status) return 'bg-gray-100 text-gray-800';
  
  const statusClasses = {
    'pending': 'bg-yellow-100 text-yellow-800',
    'approved': 'bg-blue-100 text-blue-800',
    'completed': 'bg-green-100 text-green-800',
    'cancelled': 'bg-red-100 text-red-800',
    'rejected': 'bg-red-100 text-red-800',
    'active': 'bg-purple-100 text-purple-800'
  };
  
  return statusClasses[status.toLowerCase()] || 'bg-gray-100 text-gray-800';
}

// View ride details
function viewRideDetails(ride) {
  router.push({ 
    name: 'RideDetail', 
    params: { id: ride.rideID },
    query: { from_filter: 'true' }
  });
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
</style> 
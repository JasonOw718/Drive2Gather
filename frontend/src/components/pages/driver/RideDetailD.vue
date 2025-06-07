<template>
    <div class="min-h-screen bg-white px-6 pt-[max(2.5rem,env(safe-area-inset-top))] pb-[max(env(safe-area-inset-bottom),2.5rem)] flex flex-col" style="max-width: 420px; margin: 0 auto; font-family: 'Poppins', sans-serif;">
      <!-- Header -->
      <div class="flex items-center mt-4 mb-4">
        <button @click="$router.back()" class="mt-4 absolute top-4 left-4 w-10 h-10 flex items-center justify-center rounded-lg bg-[#F5F5F5] z-20 border border-gray-200">
          <font-awesome-icon icon="fa-arrow-left" class="text-[#C77DFF] text-2xl" />
        </button>
      </div>
  
      <!-- Loading State -->
      <div v-if="loading" class="flex flex-col items-center justify-center flex-grow py-20">
        <svg class="animate-spin h-12 w-12 text-[#C77DFF]" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"></path>
        </svg>
        <p class="mt-4 text-gray-500">Loading ride details...</p>
      </div>
      
      <!-- Error State -->
      <div v-else-if="error" class="flex flex-col items-center justify-center flex-grow py-20">
        <font-awesome-icon icon="fa-circle-exclamation" class="text-red-500 text-5xl mb-4" />
        <p class="text-red-500 mb-4">{{ error }}</p>
        <button @click="fetchRideDetails" class="px-4 py-2 bg-[#C77DFF] text-white rounded-lg">
          Try Again
        </button>
      </div>
      
      <!-- Ride Details -->
      <template v-else>
        <div class="text-2xl font-bold text-left mb-2 text-[#000000] mt-8" style="font-family: 'Poppins', sans-serif; font-weight: 500;">Ride Details</div>
        
        <div class="text-sm text-[#8C8C8C] font-normal mb-6 text-left" style="font-family: 'Poppins', sans-serif;">
          {{ formatDate(rideDetails.requestTime) }} • {{ rideDetails.passengers.length }} Passenger(s)
        </div>
    
        <!-- Ride Detail Row -->
        <div class="flex items-center gap-4 mb-4">
          <div class="text-lg font-semibold text-[#303030] w-16 text-left flex-shrink-0 " style="font-family: 'Poppins', sans-serif; font-weight: 500;">
            {{ formatTime(rideDetails.requestTime) }}
          </div>
          <div class="flex flex-col items-center relative" style="min-height: 70px;">
            <div class="w-1 h-14 bg-[#C77DFF] absolute left-1/2 top-3 -translate-x-1/2 z-0"></div>
            <div class="w-4 h-4 rounded-full bg-[#C77DFF] z-10"></div>
            <div class="flex-1"></div>
            <div class="w-4 h-4 rounded-full bg-[#C77DFF] z-10"></div>
          </div>
          <div class="flex flex-col justify-between h-20 ml-2">
            <div class="text-base font-medium text-[#303030] text-left" style="font-family: 'Poppins', sans-serif; font-weight: 500;">
              {{ rideDetails.startingLocation }}
            </div>
            <div class="flex-1"></div>
            <div class="text-base font-medium text-[#303030] text-left" style="font-family: 'Poppins', sans-serif; font-weight: 500;">
              {{ rideDetails.dropoffLocation }}
            </div>
          </div>
        </div>
        <hr class="border-t-1 border-[#C77DFF] my-1 mb-3" />
        
        <!-- Ride Status -->
        <div class="mb-6">
          <div class="text-base font-medium text-[#303030] mb-2" style="font-family: 'Poppins', sans-serif; font-weight: 500;">
            Ride Status
          </div>
          <div class="flex items-center gap-2">
            <span 
              :class="[
                'px-3 py-1 rounded-full text-sm font-medium', 
                getStatusClass(rideDetails.status)
              ]"
            >
              {{ formatStatus(rideDetails.status) }}
            </span>
            <span 
              v-if="pendingRequestsCount > 0" 
              class="px-3 py-1 rounded-full bg-yellow-100 text-yellow-800 text-sm font-medium"
            >
              {{ pendingRequestsCount }} Pending Request(s)
            </span>
          </div>
        </div>
        
        <!-- Chat Room Button -->
        <div class="mb-6">
          <div 
            @click="navigateToChatRoom" 
            class="flex items-center justify-between py-3 px-4 rounded-xl cursor-pointer bg-gradient-to-r from-[#C77DFF] to-[#B266FF] shadow-sm hover:shadow-md transition-all duration-200"
          >
            <div class="flex items-center gap-2">
              <font-awesome-icon icon="fa-comments" class="text-white text-xl" />
              <span class="font-medium text-white">Chat Room</span>
            </div>
            <font-awesome-icon icon="fa-arrow-right" class="text-white" />
          </div>
        </div>
    
        <!-- Passengers Section -->
        <div>
          <div class="text-base font-medium text-[#303030] mb-3" style="font-family: 'Poppins', sans-serif; font-weight: 500;">
            Passengers
          </div>
          
          <!-- No passengers message -->
          <div v-if="rideDetails.passengers.length === 0" class="text-sm text-gray-500 mb-6">
            No passengers have joined this ride yet.
          </div>
          
          <!-- Passenger List -->
          <div v-else class="space-y-4 mb-6">
            <div v-for="passenger in rideDetails.passengers" :key="passenger.passengerID" class="border border-gray-200 rounded-lg p-3">
              <div class="flex justify-between items-start mb-3">
                <div class="font-medium text-base text-[#303030]">{{ passenger.name }}</div>
                <span 
                  :class="[
                    'text-xs rounded-full px-2 py-1', 
                    getStatusClass(passenger.status)
                  ]"
                >
                  {{ formatStatus(passenger.status) }}
                </span>
              </div>
              
              <div class="text-sm text-gray-500 mb-2">
                Requested to join your ride
              </div>
              
              <div class="flex items-center justify-between">
                <a :href="`tel:${passenger.phone}`" class="flex items-center gap-1 text-[#C77DFF]">
                  <font-awesome-icon icon="fa-phone" class="text-sm" />
                  <span class="text-sm">{{ passenger.phone }}</span>
                </a>
                
                <div v-if="passenger.status === 'pending'" class="flex gap-2">
                  <button 
                    @click="respondToRequest(passenger.passengerRideID, 'accepted')" 
                    class="px-3 py-1 bg-[#C77DFF] text-white text-sm rounded-full"
                  >
                    Accept
                  </button>
                  <button 
                    @click="respondToRequest(passenger.passengerRideID, 'rejected')" 
                    class="px-3 py-1 border border-red-500 text-red-500 text-sm rounded-full"
                  >
                    Reject
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </template>
    </div>
  </template>
  
  <script setup>
  import { useRoute, useRouter } from 'vue-router'
  import { ref, computed, onMounted } from 'vue'
  import { useUserStore } from '../../../stores/user'
  import { rideService } from '../../../services/api'
  
  const props = defineProps({
    id: {
      type: [String, Number],
      default: null
    }
  })
  
  const route = useRoute()
  const router = useRouter()
  const userStore = useUserStore()
  
  // State
  const rideDetails = ref({})
  const loading = ref(true)
  const error = ref(null)
  
  // Get ride ID from props or route query
  const rideId = computed(() => props.id || route.query.id)
  
  // Calculate pending requests count
  const pendingRequestsCount = computed(() => {
    if (!rideDetails.value || !rideDetails.value.passengers) return 0;
    return rideDetails.value.passengers.filter(p => p.status === 'pending').length;
  })
  
  // Fetch ride details on component mount
  onMounted(() => {
    if (rideId.value) {
      fetchRideDetails()
    } else {
      error.value = 'No ride ID provided'
      loading.value = false
    }
  })
  
  // Fetch ride details with passengers
  async function fetchRideDetails() {
    loading.value = true
    error.value = null
    
    try {
      const response = await rideService.getRideDetailsWithPassengers(rideId.value)
      rideDetails.value = response.data
    } catch (err) {
      console.error('Error fetching ride details:', err)
      error.value = err.response?.data?.error || 'Failed to load ride details'
    } finally {
      loading.value = false
    }
  }
  
  // Respond to a passenger request (accept/reject)
  async function respondToRequest(passengerRideId, action) {
    try {
      // Extract the user_id and ride_id from the composite key
      const [userId, rideId] = passengerRideId.split('_').map(Number);
      
      if (action === 'accepted') {
        await rideService.approveRideRequest({
          rideId: rideId,
          passengerId: userId
        });
      } else {
        await rideService.rejectRideRequest({
          rideId: rideId,
          passengerId: userId
        });
      }
      
      // Refresh ride details after responding
      fetchRideDetails();
    } catch (err) {
      console.error(`Error ${action} request:`, err);
      alert(`Failed to ${action} request. Please try again.`);
    }
  }
  
  // Format time from ISO string (HH:MM)
  function formatTime(isoTime) {
    if (!isoTime) return ''
    const date = new Date(isoTime)
    return `${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`
  }
  
  // Format date from ISO string
  function formatDate(isoTime) {
    if (!isoTime) return ''
    const date = new Date(isoTime)
    return date.toLocaleDateString('en-US', { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric' })
  }
  
  // Format ride status to be more user-friendly
  function formatStatus(status) {
    if (!status) return 'Unknown'
    
    const statusMap = {
      'pending': 'Pending',
      'accepted': 'Accepted',
      'active': 'In Progress',
      'completed': 'Completed',
      'cancelled': 'Cancelled',
      'rejected': 'Rejected'
    }
    
    return statusMap[status] || status.charAt(0).toUpperCase() + status.slice(1)
  }
  
  // Get CSS class for status badge
  function getStatusClass(status) {
    if (!status) return 'bg-gray-100 text-gray-800'
    
    const statusClassMap = {
      'pending': 'bg-yellow-100 text-yellow-800',
      'accepted': 'bg-blue-100 text-blue-800',
      'active': 'bg-purple-100 text-purple-800',
      'completed': 'bg-green-100 text-green-800',
      'cancelled': 'bg-red-100 text-red-800',
      'rejected': 'bg-red-100 text-red-800'
    }
    
    return statusClassMap[status] || 'bg-gray-100 text-gray-800'
  }
  
  // Navigate to chat room
  function navigateToChatRoom() {
    router.push({
      name: 'ChatRoom',
      params: { id: rideId.value }
    })
  }
  </script>
  
  <style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500&display=swap');
  </style>
  
<template>
  <div class="min-h-screen bg-white px-6 pt-[max(2.5rem,env(safe-area-inset-top))] pb-[max(env(safe-area-inset-bottom),2.5rem)] flex flex-col" style="max-width: 420px; margin: 0 auto; font-family: 'Poppins', sans-serif;">
    <!-- Header -->
    <div class="flex items-center mt-4 mb-4">
      <button @click="$router.back()" class="mt-4 absolute top-4 left-4 w-10 h-10 flex items-center justify-center rounded-lg bg-[#F5F5F5] z-20 border border-gray-200">
        <font-awesome-icon icon="fa-arrow-left" class="text-[#C77DFF] text-2xl" />
      </button>
    </div>

    <div class="text-2xl font-bold text-left mb-2 text-[#000000] mt-8" style="font-family: 'Poppins', sans-serif; font-weight: 500;">Ride Request</div>

    <div class="text-sm text-[#8C8C8C] font-normal mb-6 text-left" style="font-family: 'Poppins', sans-serif;">Seat Needed: {{ seatsLabel }}</div>

    <!-- Status Badge -->
    <div v-if="ride.status" class="flex justify-end items-start mb-3">
      <span 
        :class="[
          'text-xs rounded-full px-3 py-1 font-medium', 
          getStatusClass(ride.status)
        ]"
      >
        {{ formatStatus(ride.status) }}
      </span>
    </div>

    <!-- Loading state -->
    <div v-if="loading" class="flex justify-center items-center h-64">
      <svg class="animate-spin h-12 w-12 text-[#C77DFF]" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"></path>
      </svg>
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="text-center text-red-500 mt-10">
      {{ error }}
      <button @click="loadRideDetail" class="block mx-auto mt-4 text-[#C77DFF] underline">Try Again</button>
    </div>

    <div v-else>
      <!-- Ride Detail Row -->
      <div class="flex items-center gap-4 mb-4">
        <div class="text-lg font-semibold text-[#303030] w-16 text-left flex-shrink-0 " style="font-family: 'Poppins', sans-serif; font-weight: 500;">{{ departureTime }}</div>
        <div class="flex flex-col items-center relative" style="min-height: 70px;">
          <div class="w-1 h-14 bg-[#C77DFF] absolute left-1/2 top-3 -translate-x-1/2 z-0"></div>
          <div class="w-4 h-4 rounded-full bg-[#C77DFF] z-10"></div>
          <div class="flex-1"></div>
          <div class="w-4 h-4 rounded-full bg-[#C77DFF] z-10"></div>
        </div>
        <div class="flex flex-col justify-between h-20 ml-2">
          <div class="text-base font-medium text-[#303030] text-left" style="font-family: 'Poppins', sans-serif; font-weight: 500;">{{ ride.startingLocation }}</div>
          <div class="flex-1"></div>
          <div class="text-base font-medium text-[#303030] text-left" style="font-family: 'Poppins', sans-serif; font-weight: 500;">{{ ride.dropoffLocation }}</div>
        </div>
      </div>
      <hr class="border-t-1 border-[#C77DFF] my-1 mb-3" />

      <!-- Driver Detail Row -->
      <div class="flex items-center justify-between mb-4">
        <div class="flex flex-col">
          <div class="text-base font-medium text-[#303030] mb-1 text-left" style="font-family: 'Poppins', sans-serif; font-weight: 500;">{{ ride.driverName }}</div>
          <div class="flex items-center gap-1 mt-1">
            <template v-for="i in Number(ride.Passenger_count || 0)" :key="'seat-' + i">
              <font-awesome-icon
                icon="fa-solid fa-chair"
                :class="i <= Number(ride.seatsOccupied || 0) ? 'text-[#C77DFF] text-lg' : 'text-[#8C8C8C] text-lg'"
              />
            </template>
          </div>
        </div>
        <img src="@/assets/images/image.png" alt="Driver Avatar" class="w-10 h-10 rounded-full object-cover border border-gray-200" />
      </div>

      <!-- Chat Room Button -->
      <div @click="navigateToChatRoom" class="flex items-center justify-between py-3 px-4 rounded-xl mb-4 cursor-pointer bg-gradient-to-r from-[#C77DFF] to-[#B266FF] shadow-sm hover:shadow-md transition-all duration-200">
        <div class="flex items-center gap-2">
          <font-awesome-icon icon="fa-solid fa-comments" class="w-4 h-4 text-white"/>
          <span class="text-base font-medium text-white" style="font-family: 'Poppins', sans-serif;">Chat Room</span>
        </div>
        <font-awesome-icon icon="fa-arrow-right" class="text-white text-lg" />
      </div>

      <!-- Car Detail Row -->
      <div class="flex items-center gap-3 mb-4">
        <font-awesome-icon icon="fa-solid fa-car" class="text-[#303030] text-xl" />
        <span class="text-base text-[#000000]" style="font-family: 'Poppins', sans-serif;">{{ ride.carNumber || 'Not available' }}</span>
      </div>

      <!-- Car Type and Photo Row -->
      <div class="flex items-center justify-between mb-8">
        <div class="text-base text-[#303030] font-medium" style="font-family: 'Poppins', sans-serif;">{{ ride.carType || 'Not available' }}</div>
        <div class="flex gap-2">
          <img src="@/assets/images/carphoto.jpg" alt="Car Photo" class="w-20 h-14 object-cover rounded-lg border border-gray-200" />
          <img src="@/assets/images/carphoto.jpg" alt="Car Photo" class="w-20 h-14 object-cover rounded-lg border border-gray-200" />
        </div>
      </div>

      <!-- Spacer -->
      <div class="flex-1"></div>

      <!-- 
        Action Button - Only show if not viewing from history
        Debug info:
        - fromHistory: {{ fromHistory }}
        - route.query.from_history: {{ route.query.from_history }}
        - forceHideButton: {{ forceHideButton }}
      -->
      <button 
        v-if="!fromHistory"
        class="w-full py-3 px-4 rounded-full shadow-md bg-[#C77DFF] text-white text-base font-bold hover:bg-opacity-90 transition-all duration-300 mb-0" 
        style="max-width: 100%;"
        @click="requestRide"
        :disabled="loading || requestLoading"
      >
        {{ requestLoading ? 'Processing...' : 'Request for Ride' }}
      </button>

      <!-- Confirm Ride Button - Only show for approved or accepted rides from history -->
      <button 
        v-if="fromHistory && (ride.status === 'approved' || ride.status === 'accepted')"
        class="w-full py-3 px-4 rounded-full shadow-md bg-[#C77DFF] text-white text-base font-bold hover:bg-opacity-90 transition-all duration-300 mb-0" 
        style="max-width: 100%;"
        @click="completeRide"
        :disabled="loading || completeLoading"
      >
        {{ completeLoading ? 'Processing...' : 'Confirm Ride' }}
      </button>

      <!-- Complete Ride Button - Only show for active rides from history -->
      <button 
        v-if="fromHistory && ride.status === 'active'"
        class="w-full py-3 px-4 rounded-full shadow-md bg-[#C77DFF] text-white text-base font-bold hover:bg-opacity-90 transition-all duration-300 mb-0" 
        style="max-width: 100%;"
        @click="completeRide"
        :disabled="loading || completeLoading"
      >
        {{ completeLoading ? 'Processing...' : 'Complete Ride' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router'
import { ref, computed, onMounted } from 'vue'
import { usePassengerInputStore } from '../../../stores/passengerInput'
import { rideService } from '../../../services/api'
import { useToastStore } from '../../../stores/toast'

const route = useRoute()
const router = useRouter()
const passengerInputStore = usePassengerInputStore()
const toastStore = useToastStore()

// Get ride ID from route params
const rideId = route.params.id

// Force hide button regardless of route - set to true to always hide
const forceHideButton = false

// Check if we're coming from ride history or filter
const fromHistory = computed(() => {
  return route.query.from_history === 'true' || route.query.from_filter === 'true' || forceHideButton
})

// Reactive state
const ride = ref({})
const driverInfo = ref({})
const loading = ref(true)
const error = ref(null)
const requestLoading = ref(false)
const completeLoading = ref(false)

// Format time for display (HH:MM)
const departureTime = computed(() => {
  if (!ride.value.requestTime) return '';
  const date = new Date(ride.value.requestTime);
  return `${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`;
})

const seatsLabel = computed(() => {
  const seats = Number(passengerInputStore.seats)
  return seats === 1 ? '1 Passenger' : `${seats} Passengers`
})

const whatsappLink = computed(() => {
  const phone = driverInfo.value.phone || ''
  const msg = encodeURIComponent('Hi, I am a passenger from Ride2Gather.')
  return `https://wa.me/${phone}?text=${msg}`
})

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

async function loadRideDetail() {
  loading.value = true
  error.value = null
  
  try {
    // Fetch ride details
    const response = await rideService.getRideById(rideId)
    ride.value = response.data
    
    // Log ride details for debugging
    console.log('Loaded ride details:', ride.value)
    console.log('Ride status:', ride.value.status)
    
    // Additional driver info could be fetched here if needed
    if (ride.value.driverID) {
      // Use car information from API response
      driverInfo.value = {
        car_type: ride.value.carType || 'Sedan',
        car_number: ride.value.carNumber || 'ABC123',
        phone: ride.value.driverPhone || '60123456789'
      }
    }
  } catch (err) {
    console.error('Error loading ride details:', err)
    error.value = 'Failed to load ride details. Please try again.'
  } finally {
    loading.value = false
  }
}

// Navigate to chat room
function navigateToChatRoom() {
  router.push({
    name: 'ChatRoom',
    params: { id: rideId }
  })
}

async function requestRide() {
  requestLoading.value = true
  error.value = null
  
  try {
    // Check if user is authenticated
    const token = localStorage.getItem('token');
    if (!token) {
      error.value = "You must be logged in to request a ride";
      router.push('/login-register');
      return;
    }
    
    // Get user ID from store or localStorage
    const userData = JSON.parse(localStorage.getItem('user') || '{}');
    const userId = userData.id || userData.user_id || 1;
    
    // Prepare passenger data
    const passengerData = {
      passengerID: userId,
      seats: passengerInputStore.seats || 1
    }
    
    // Request the ride
    const response = await rideService.requestRide(rideId, passengerData)
    
    console.log('Ride request successful:', response.data)
    
    // Show success message
    toastStore.success('Ride requested successfully')
    
    // Redirect directly to homepage
    router.push('/')
  } catch (err) {
    console.error('Error requesting ride:', err)
    
    // Check for authentication errors
    if (err.message === 'User not authenticated' || 
        err.message === 'Authentication required' || 
        (err.response && err.response.status === 401)) {
      error.value = "You must be logged in to request a ride";
      setTimeout(() => {
        router.push('/login-register');
      }, 2000);
      return;
    }
    
    // Handle other errors
    error.value = err.response?.data?.error || 'Failed to request ride. Please try again.';
    
    // Show alert if error is not already displayed in the UI
    if (!error.value) {
      alert('Failed to request ride. Please try again.');
    }
  } finally {
    requestLoading.value = false
  }
}

// Complete ride function
async function completeRide() {
  completeLoading.value = true
  error.value = null
  
  try {
    // Mark the ride as completed
    await rideService.completeRide(rideId)
    
    // Navigate to passenger ride completed page
    router.push({
      name: 'RideComplete',
      query: {
        rideId: rideId,
        from: ride.value.startingLocation,
        to: ride.value.dropoffLocation,
        driverName: ride.value.driverName,
        driverAvatar: '@/assets/images/image.png',
        carPlate: ride.value.carNumber || 'ABC123',
        driverCarType: ride.value.carType || 'Sedan',
        driverId: ride.value.driverID
      }
    })
  } catch (err) {
    console.error('Error completing ride:', err)
    error.value = err.response?.data?.error || 'Failed to complete ride. Please try again.'
  } finally {
    completeLoading.value = false
  }
}

onMounted(() => {
  console.log('Route query params:', route.query);
  console.log('from_history param:', route.query.from_history);
  console.log('fromHistory computed value:', fromHistory.value);
  loadRideDetail()
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500&display=swap');
</style>

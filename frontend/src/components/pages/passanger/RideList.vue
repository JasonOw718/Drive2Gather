<template>
  <div class="min-h-screen bg-white px-6 pt-[max(2.5rem,env(safe-area-inset-top))] pb-[max(env(safe-area-inset-bottom),2.5rem)]" style="max-width: 420px; margin: 0 auto; font-family: 'Poppins', sans-serif;">
    <!-- Top Bar -->
    <div class="flex items-center gap-4 mb-6">
      <button @click="$router.back()" class="p-0 bg-transparent border-none focus:outline-none">
        <font-awesome-icon icon="fa-arrow-left" class="text-[#C77DFF] text-2xl" />
      </button>
      <div class="flex flex-col flex-1 ml-2">
        <div class="flex items-center text-lg font-medium text-[#303030]" style="font-family: 'Poppins', sans-serif; font-weight: 500;">
          {{ from }}
          <font-awesome-icon icon="fa-arrow-right-long" class="mx-2 text-[#C77DFF]" />
          {{ to }}
        </div>
        <div class="text-sm text-[#8C8C8C] font-normal text-left" style="font-family: 'Poppins', sans-serif;">
          {{ formatDateDisplay(date) }} | {{ time }} | {{ seatsLabel }}
        </div>
      </div>
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
      <button @click="loadRides" class="block mx-auto mt-4 text-[#C77DFF] underline">Try Again</button>
    </div>

    <!-- Ride List -->
    <div v-else-if="filteredRides.length > 0" class="flex flex-col gap-5">
      <div v-for="ride in filteredRides" :key="ride.id" @click="selectRide(ride)" class="rounded-2xl shadow-md p-4 bg-white cursor-pointer transition hover:shadow-lg">
        <!-- First Row: Time & Timeline & Locations -->
        <div class="flex items-center gap-4 mb-6">
          <div class="text-base font-semibold text-[#303030] w-14 text-left" style="font-family: 'Poppins', sans-serif; font-weight: 500;">{{ ride.departureTime }}</div>
          <div class="flex flex-col items-center justify-center h-14 relative">
            <div class="w-1 h-14 bg-[#C77DFF] absolute left-1/2 top-0 -translate-x-1/2 z-0"></div>
            <div class="w-3 h-3 rounded-full bg-[#C77DFF] z-10"></div>
            <div class="flex-1"></div>
            <div class="w-3 h-3 rounded-full bg-[#C77DFF] z-10"></div>
          </div>
          <div class="flex flex-col justify-between h-14 ml-2">
            <div class="text-sm font-medium text-[#303030] text-left" style="font-family: 'Poppins', sans-serif; font-weight: 500;">{{ ride.from }}</div>
            <div class="flex-1"></div>
            <div class="text-sm font-medium text-[#303030] text-left" style="font-family: 'Poppins', sans-serif; font-weight: 500;">{{ ride.to }}</div>
          </div>
        </div>
        <!-- Second Row: Driver & Seats -->
        <div class="flex items-center mt-2">
          <img :src="ride.driverAvatar" alt="Driver Avatar" class="w-9 h-9 rounded-full object-cover mr-3 border border-gray-200" />
          <div class="flex flex-col flex-1">
            <div class="text-sm font-medium text-[#303030] text-left" style="font-family: 'Poppins', sans-serif; font-weight: 500;">{{ ride.driverName }}</div>
            <div class="flex items-center gap-1 mt-1">
              <template v-for="n in ride.seatAvailable" :key="'seat-' + n">
                <font-awesome-icon
                  icon="fa-solid fa-chair"
                  :class="n <= ride.seatFilled ? 'text-[#C77DFF] text-lg' : 'text-[#8C8C8C] text-lg'"
                />
              </template>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="text-center text-[#8C8C8C] mt-10">No rides found for your search.</div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { usePassengerInputStore } from '../../../stores/passengerInput'
import { rideService } from '../../../services/api'

const router = useRouter()
const route = useRoute()

// Get search parameters from query params
const from = ref(route.query.from || 'From')
const to = ref(route.query.to || 'To')
const date = ref(route.query.date || new Date().toISOString().split('T')[0])
const time = ref(route.query.time || '09:00')
const seats = ref(Number(route.query.seats) || 1)

const passengerInputStore = usePassengerInputStore()
const rides = ref([])
const loading = ref(true)
const error = ref(null)

// Format time for display (HH:MM)
function formatTime(isoTime) {
  if (!isoTime) return '';
  const date = new Date(isoTime);
  return `${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`;
}

// Format date for display
function formatDateDisplay(dateStr) {
  if (!dateStr) return '';
  const options = { weekday: 'short', month: 'short', day: 'numeric' };
  return new Date(dateStr).toLocaleDateString('en-US', options);
}

// Load rides from API
async function loadRides() {
  loading.value = true;
  error.value = null;
  
  try {
    // Format date and time for API request
    const requestTime = `${date.value}T${time.value}:00`;
    
    const response = await rideService.searchRides({
      starting_location: from.value,
      dropoff_location: to.value,
      request_time: requestTime,
      seats: seats.value.toString()
    });
    
    rides.value = response.data.rides.map(ride => ({
      id: ride.rideID,
      departureTime: formatTime(ride.requestTime),
      from: ride.startingLocation,
      to: ride.dropoffLocation,
      driverName: ride.driverName,
      driverAvatar: '@/assets/images/image.png', // Default avatar
      seatAvailable: ride.Passenger_count,
      seatFilled: 0, // This would need to be calculated from passengers if available
      driverPhone: '123-456-7890', // This would come from the driver details
      driverCarType: 'Sedan', // This would come from the driver details
      carPlate: 'ABC123', // This would come from the driver details
      carPhoto: '@/assets/images/carphoto.jpg', // Default car image
      driverID: ride.driverID,
      status: ride.status,
      requestTime: ride.requestTime
    }));
  } catch (err) {
    console.error('Error loading rides:', err);
    error.value = 'Failed to load rides. Please try again.';
  } finally {
    loading.value = false;
  }
}

// Load rides when component mounts
onMounted(() => {
  loadRides();
});

// Format display values
const seatsLabel = computed(() => {
  return seats.value === 1 ? '1 Passenger' : `${seats.value} Passengers`
})

// Filter rides client-side if needed for additional criteria
const filteredRides = computed(() => {
  if (loading.value) return [];
  if (error.value) return [];
  return rides.value;
})

function selectRide(ride) {
  router.push({
    name: 'RideDetail',
    params: {
      id: ride.id
    }
  })
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500&display=swap');
</style>

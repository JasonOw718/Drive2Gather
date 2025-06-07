<template>
    <RightNavbar />
      <div class="bg-white flex flex-col px-6 pt-[max(2.5rem,env(safe-area-inset-top))] pb-[max(env(safe-area-inset-bottom),2.5rem)] h-full flex-grow" style="max-width: 420px; margin: 0 auto;">
        <!-- Main Title -->
        <div class="text-2xl font-bold text-left mb-8 text-[#000000] mt-1">Create a Ride</div>
    
        <!-- Where are you going? -->
        <div class="mb-6">
          <div class="text-base font-semibold text-[#333333] mb-2">Where are you going?</div>
          <input
            v-model="from"
            type="text"
            placeholder="From"
            class="w-full border border-gray-200 bg-[#F5F5F5] px-4 py-3 mb-3 text-base rounded-lg text-black focus:outline-none focus:ring-2 focus:ring-[#C77DFF] text-left"
          />
          <input
            v-model="to"
            type="text"
            placeholder="To"
            class="w-full border border-gray-200 bg-[#F5F5F5] px-4 py-3 text-base rounded-lg text-black focus:outline-none focus:ring-2 focus:ring-[#C77DFF] text-left"
          />
        </div>
    
        <!-- When? (Date and Time Picker) -->
        <div class="mb-6">
          <div class="text-base font-semibold text-[#333333] mb-2">When?</div>
          <input
            v-model="date"
            type="date"
            :min="minDate"
            class="w-full border border-gray-200 bg-[#F5F5F5] px-4 py-3 mb-3 text-base rounded-lg text-black focus:outline-none focus:ring-2 focus:ring-[#C77DFF] text-left"
          />
          <input
            v-model="time"
            type="time"
            :min="minTime"
            step="3600"
            class="w-full border border-gray-200 bg-[#F5F5F5] px-4 py-3 text-base rounded-lg text-black focus:outline-none focus:ring-2 focus:ring-[#C77DFF] text-left"
          />
        </div>
    
        <!-- Seat needed? (Custom Counter Input) -->
        <div class="mb-8">
          <div class="text-base font-semibold text-[#333333] mb-2">Seat available?</div>
          <div class="flex items-center gap-4">
            <button @click="decrement" :disabled="seats <= 1" class="p-2 rounded-full  text-[#000000] disabled:opacity-30">
              <font-awesome-icon icon="fa-solid fa-minus" />
            </button>
            <span class="text-xl font-bold text-[#C77DFF] w-8 text-center">{{ seats }}</span>
            <button @click="increment" :disabled="seats >= 10" class="p-2 rounded-full  text-[#000000] disabled:opacity-50">
              <font-awesome-icon icon="fa-solid fa-plus" />
            </button>
          </div>
        </div>
    
        <!-- Error message -->
        <div v-if="error" class="mb-4 text-red-500 text-sm">
          {{ error }}
        </div>
    
        <!-- Submit Button -->
        <button
          class="w-full py-3 px-4 rounded-full shadow-md bg-[#C77DFF] text-white text-base font-bold hover:bg-opacity-90 transition-all duration-300 mb-4"
          @click="publishRide"
          :disabled="loading"
        >
          <span v-if="loading" class="inline-flex items-center">
            <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"></path>
            </svg>
            Publishing...
          </span>
          <span v-else>Publish</span>
        </button>
      </div>
    </template>
    
    <script setup>
    import { ref, computed, onMounted } from 'vue'
    import { useRouter } from 'vue-router';
    import { useUserStore } from '../../../stores/user';
    import { rideService } from '../../../services/api';
    import RightNavbar from '../rightnavbar.vue'
    
    const router = useRouter();
    const userStore = useUserStore();
    
    const from = ref('')
    const to = ref('')
    const date = ref('')
    const time = ref('')
    const seats = ref(1)
    const loading = ref(false)
    const error = ref('')
    
    // Set default date to today
    onMounted(() => {
      const today = new Date();
      date.value = today.toISOString().split('T')[0];
      
      // Make sure auth is initialized
      userStore.initializeAuth();
      
      // Redirect if not a driver
      if (!userStore.isAuthenticated) {
        router.push('/login-register');
        return;
      }
      
      if (userStore.currentUser?.role !== 'driver') {
        router.push('/home');
      }
    });
    
    function pad(n) {
      return n < 10 ? '0' + n : n
    }
    
    // Compute min date as today
    const minDate = computed(() => {
      const today = new Date();
      return today.toISOString().split('T')[0];
    });
    
    // Compute min time as now, rounded up to next hour
    const minTime = computed(() => {
      const now = new Date()
      let hour = now.getHours()
      let min = now.getMinutes()
      if (min > 0) hour++
      return pad(hour) + ':00'
    })
    
    function increment() {
      if (seats.value < 10) seats.value++
    }
    
    function decrement() {
      if (seats.value > 1) seats.value--
    }
    
    async function publishRide() {
      // Debug logs
      console.log('Authentication state:', {
        isAuthenticated: userStore.isAuthenticated,
        currentUser: userStore.currentUser,
        role: userStore.currentUser?.role
      });
      
      // Validate inputs
      if (!from.value.trim()) {
        error.value = 'Please enter a starting location';
        return;
      }
      if (!to.value.trim()) {
        error.value = 'Please enter a destination';
        return;
      }
      if (!date.value) {
        error.value = 'Please select a date';
        return;
      }
      if (!time.value) {
        error.value = 'Please select a time';
        return;
      }
      
      // Reset error message
      error.value = '';
      loading.value = true;
      
      try {
        // Check if user is logged in and is a driver
        if (!userStore.isAuthenticated || !userStore.currentUser) {
          error.value = 'You must be logged in to create a ride';
          loading.value = false;
          return;
        }
        
        // Get user ID from user store (with detailed logging)
        console.log('Current user data:', userStore.currentUser);
        // For drivers, the user_id is what we need for driverID
        const driverId = userStore.currentUser.id || userStore.currentUser.user_id || userStore.currentUser.driverId;
        console.log('Using driver ID:', driverId);
        const isDriver = userStore.currentUser.role === 'driver';
        
        if (!isDriver) {
          error.value = 'You must have a driver account to create a ride';
          loading.value = false;
          return;
        }
        
        // Combine date and time to create ISO datetime string
        const requestTime = `${date.value}T${time.value}:00`;
        
        // Prepare request payload
        const rideData = {
          driverID: parseInt(driverId),
          startingLocation: from.value.trim(),
          dropoffLocation: to.value.trim(),
          requestTime: requestTime,
          Passenger_count: seats.value
        };
        
        // Ensure driverID is set
        if (!rideData.driverID) {
          error.value = 'Driver ID not found. Please try logging out and back in.';
          loading.value = false;
          return;
        }
        
                // Debug the request payload
        console.log('Sending ride data:', rideData);
        
        // Use the rideService for API call
        const response = await rideService.createRide(rideData);
        console.log('Response data:', response.data);
        const result = response.data;
        
        // Navigate back to homepage after successful ride creation
        router.push('/');
      } catch (err) {
        console.error('Error creating ride:', err);
        if (err.response && err.response.data && err.response.data.error) {
          // Extract error message from Axios response
          error.value = err.response.data.error;
        } else {
          error.value = err.message || 'Failed to create ride. Please try again.';
        }
      } finally {
        loading.value = false;
      }
    }
    </script>
    
<template>
  <div class="min-h-screen bg-white px-6 pt-[max(2.5rem,env(safe-area-inset-top))] pb-[max(env(safe-area-inset-bottom),2.5rem)] flex flex-col relative" style="max-width: 420px; margin: 0 auto; font-family: 'Roboto', sans-serif;">
    <!-- Back Button -->
    <button
      class="absolute top-4 left-4 w-10 h-10 flex items-center justify-center rounded-lg bg-[#F5F5F5] z-20 border border-gray-200"
      @click="$router.back()"
      aria-label="Back"
    >
      <span class="w-6 h-6 text-primary">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512" :fill="'#C77DFF'">
          <path d="M9.4 233.4c-12.5 12.5-12.5 32.8 0 45.3l160 160c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L109.2 288 416 288c17.7 0 32-14.3 32-32s-14.3-32-32-32l-306.7 0L214.6 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0l-160 160z"/>
        </svg>
      </span>
    </button>

    <!-- Heart Icon -->
    <div class="flex flex-col items-start mt-16 mb-4">
      <img src="/src/assets/images/heart.png" alt="Donation" class="w-20 h-20 object-contain mb-2" style="filter: drop-shadow(0 2px 8px #C77DFF33);" />
      <div class="text-2xl font-medium text-left mt-2" style="font-family: 'Roboto', sans-serif; color: #C77DFF;">Donation</div>
    </div>

    <!-- Loading state -->
    <div v-if="isLoading" class="flex flex-col items-center justify-center py-8">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-[#C77DFF]"></div>
      <p class="mt-4 text-gray-600">Loading driver information...</p>
    </div>

    <!-- Error state -->
    <div v-else-if="loadError" class="text-red-500 text-center py-8">
      {{ loadError }}
    </div>

    <!-- Driver Information -->
    <div v-else class="flex flex-row items-center mb-6 w-full">
      <img :src="driver.driverAvatar || '/src/assets/images/default-avatar.png'" alt="Driver Avatar" class="w-8 h-8 rounded-full object-cover border-0 border-[#C77DFF] mr-4" />
      <div class="flex flex-col flex-1">
        <div class="text-base font-medium text-left" style="font-family: 'Poppins', sans-serif; color: #000000;">{{ driver.driverName }}</div>
        <div class="text-sm mt-1 text-left" style="font-family: 'Poppins', sans-serif; color: #8C8C8C;">{{ driver.carPlate }} • {{ driver.driverCarType }}</div>
      </div>
    </div>

    <!-- Tip Section -->
    <div class="mb-2">
      <div class="text-base font-medium mb-2 text-left" style="font-family: 'Poppins', sans-serif; color: #303030;">Tip the driver?</div>
      <div class="flex flex-row items-center justify-center gap-6 mb-6">
        <button @click="decrement" :disabled="tipAmount <= 1" class="w-10 h-10 flex items-center justify-center rounded-full text-[#C77DFF] text-2xl disabled:opacity-40">
          <font-awesome-icon icon="fa-minus" />
        </button>
        <span class="text-2xl font-bold" style="color: #C77DFF; font-family: 'Roboto', sans-serif; min-width: 80px; text-align: center;">RM {{ tipAmount.toFixed(2) }}</span>
        <button @click="increment" :disabled="tipAmount >= 100" class="w-10 h-10 flex items-center justify-center rounded-full text-[#C77DFF] text-2xl disabled:opacity-40">
          <font-awesome-icon icon="fa-plus" />
        </button>
      </div>
    </div>

    <!-- Description Input -->
    <div class="mb-6">
      <div class="text-base font-medium mb-2 text-left" style="font-family: 'Poppins', sans-serif; color: #303030;">Add a message (optional)</div>
      <textarea 
        v-model="description" 
        class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-[#C77DFF]"
        placeholder="Write a thank you message..."
        rows="3"
        style="font-family: 'Poppins', sans-serif; resize: none;"
      ></textarea>
    </div>

    <!-- Error message -->
    <div v-if="error" class="text-red-500 text-sm mb-4 text-center">
      {{ error }}
    </div>

    <div class="flex-1"></div>

    <!-- Donate Button -->
    <button
      class="w-full py-3 px-4 rounded-full shadow-md text-base font-bold transition-all duration-300 mb-2 bg-[#C77DFF] text-white hover:bg-opacity-90 cursor-pointer disabled:bg-opacity-50 disabled:cursor-not-allowed"
      style="max-width: 100%; font-family: 'Roboto', sans-serif;"
      @click="donate"
      :disabled="loading || isLoading"
    >
      {{ loading ? 'Processing...' : 'Donate!' }}
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '../../../stores/user'
import { donationService } from '../../../services/api'
import api from '../../../services/api'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

// Get driver ID from route params
const driverId = route.params.driverId

// Driver data
const driver = ref({
  driverID: driverId,
  driverName: '',
  driverAvatar: '',
  carPlate: '',
  driverCarType: ''
})

const tipAmount = ref(1)
const description = ref('')
const loading = ref(false)
const error = ref('')
const isLoading = ref(true)
const loadError = ref('')

function increment() { if (tipAmount.value < 100) tipAmount.value++ }
function decrement() { if (tipAmount.value > 1) tipAmount.value-- }

// Fetch driver information
async function fetchDriverInfo() {
  isLoading.value = true
  loadError.value = ''
  
  try {
    // Get driver profile using the driver ID
    const response = await api.get(`/auth/users/${driverId}`)
    const driverData = response.data
    
    driver.value = {
      driverID: driverId,
      driverName: driverData.name || 'Driver',
      driverAvatar: driverData.avatar || '/src/assets/images/default-avatar.png',
      carPlate: driverData.carPlate || 'Unknown',
      driverCarType: driverData.carType || 'Vehicle'
    }
  } catch (err) {
    console.error('Error fetching driver info:', err)
    loadError.value = 'Failed to load driver information. Please try again.'
  } finally {
    isLoading.value = false
  }
}

async function donate() {
  loading.value = true
  error.value = ''
  
  try {
    // Get current user ID (donor)
    const donorId = userStore.currentUser?.id || userStore.currentUser?.user_id
    
    if (!donorId) {
      error.value = 'User not authenticated'
      return
    }
    
    // Prepare donation data
    const donationData = {
      userId: parseInt(driverId), // Driver's ID from route params
      donorId: donorId, // Current user's ID (passenger)
      amount: tipAmount.value,
      description: description.value
    }
    
    // Send donation data to the backend using the donation service
    const response = await donationService.createDonation(donationData)
    
    // Navigate to donation complete page
    router.push({ 
      name: 'DonateComplete', 
      query: { 
        tip: tipAmount.value,
        driverName: driver.value.driverName,
        driverAvatar: driver.value.driverAvatar,
        carPlate: driver.value.carPlate,
        driverCarType: driver.value.driverCarType
      } 
    })
  } catch (err) {
    console.error('Error making donation:', err)
    error.value = err.response?.data?.error || 'Failed to process donation. Please try again.'
  } finally {
    loading.value = false
  }
}

// Fetch driver info when component is mounted
onMounted(() => {
  fetchDriverInfo()
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&family=Poppins:wght@400;500&display=swap');
</style>
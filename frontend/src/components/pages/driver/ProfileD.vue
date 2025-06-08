<template> 
<RightNavbar />
  <div class="min-h-screen bg-white px-6 py-6 flex flex-col" style="max-width: 420px; margin: 0 auto;">
   
    <!-- Header -->
    <div class="text-2xl font-bold text-left mb-8 text-[#5D7285]">Profile</div>

    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center items-center h-64">
      <svg class="animate-spin h-12 w-12 text-[#C77DFF]" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"></path>
      </svg>
    </div>
    
    <!-- Error State -->
    <div v-else-if="error" class="text-center text-red-500 mt-10">
      {{ error }}
      <button @click="fetchProfile" class="block mx-auto mt-4 text-[#C77DFF] underline">Try Again</button>
    </div>

    <div v-else>
      <!-- Donation Card/Button -->
      <button @click="showQR = true" class="w-full h-32 rounded-xl border border-[#D2B7E5] mb-8 flex flex-col justify-between items-start relative text-left hover:bg-[#f0eaff] transition p-4">
        <div class="flex flex-col">
          <span class="text-base font-semibold text-[#000000]">Donation</span>
          <span class="text-sm text-gray-500">{{ userProfile.donation_count || 0 }} donations received</span>
        </div>
        <span class="absolute bottom-4 right-4 pl-6 text-xl font-bold text-[#C77DFF] text-[18px] whitespace-nowrap">RM {{ formatAmount(userProfile.total_donations) }}</span>
      </button>

      <!-- QR Code Modal -->
      <div v-if="showQR" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-40">
        <div class="bg-white rounded-2xl p-6 shadow-lg flex flex-col items-center relative w-80">
          <button @click="showQR = false" class="absolute top-2 right-2 text-[#C77DFF] text-2xl font-bold">&times;</button>
          
          <h3 class="text-lg font-bold text-[#C77DFF] mb-2">Your Donations</h3>
          
          <div class="flex justify-between w-full mb-4">
            <div class="text-center">
              <div class="text-2xl font-bold text-[#C77DFF]">{{ userProfile.donation_count || 0 }}</div>
              <div class="text-sm text-gray-500">Total Tips</div>
            </div>
            <div class="text-center">
              <div class="text-2xl font-bold text-[#C77DFF]">RM {{ formatAmount(userProfile.total_donations) }}</div>
              <div class="text-sm text-gray-500">Total Amount</div>
            </div>
          </div>
          
          <img :src="qrCodeImage" alt="Donation QR Code" class="w-64 h-64 object-contain mb-4" />
          <div class="text-[#5D7285] font-semibold">Scan to receive donations</div>
          <p class="text-sm text-gray-500 mt-2 text-center">Share this QR code with your passengers to receive tips</p>
        </div>
      </div>

      <!-- User Info Section -->
      <div class="flex flex-col gap-5 mb-10">
        <div>
          <label class="block text-[18px] font-semibold text-gray-800 mb-1 text-left">Name</label>
          <input type="text" :value="userProfile.name" disabled class="w-full border border-gray-200 bg-[#F5F5F5] px-4 py-3 text-base rounded-lg text-[#9D9FA0] focus:outline-none" />
        </div>
        <div>
          <label class="block text-[18px] font-semibold text-gray-800 mb-1 text-left">Email</label>
          <input type="email" :value="userProfile.email" disabled class="w-full border border-gray-200 bg-[#F5F5F5] px-4 py-3 text-base rounded-lg text-[#9D9FA0] focus:outline-none" />
        </div>
        <div>
          <label class="block text-[18px] font-semibold text-gray-800 mb-1 text-left">Phone Number</label>
          <input type="tel" :value="userProfile.phone" disabled class="w-full border border-gray-200 bg-[#F5F5F5] px-4 py-3 text-base rounded-lg text-[#9D9FA0] focus:outline-none" />
        </div>
        
        <!-- Driver-specific fields -->
        <div v-if="userProfile.car_type">
          <label class="block text-[18px] font-semibold text-gray-800 mb-1 text-left">Car Type</label>
          <input type="text" :value="userProfile.car_type" disabled class="w-full border border-gray-200 bg-[#F5F5F5] px-4 py-3 text-base rounded-lg text-[#9D9FA0] focus:outline-none" />
        </div>
        <div v-if="userProfile.car_number">
          <label class="block text-[18px] font-semibold text-gray-800 mb-1 text-left">Car Plate</label>
          <input type="text" :value="userProfile.car_number" disabled class="w-full border border-gray-200 bg-[#F5F5F5] px-4 py-3 text-base rounded-lg text-[#9D9FA0] focus:outline-none" />
        </div>
        <div v-if="userProfile.license_number">
          <label class="block text-[18px] font-semibold text-gray-800 mb-1 text-left">License Number</label>
          <input type="text" :value="userProfile.license_number" disabled class="w-full border border-gray-200 bg-[#F5F5F5] px-4 py-3 text-base rounded-lg text-[#9D9FA0] focus:outline-none" />
        </div>
      </div>

      <!-- Change Password Link -->
      <router-link to="/change-password" class="text-[#C77DFF] text-base font-semibold underline hover:opacity-80 transition self-start">Change Password?</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '../../../stores/user'
import RightNavbar from '../rightnavbar.vue'
import qrCodeImage from '../../../assets/images/qrcode.jpg'

const userStore = useUserStore()
const userProfile = ref({})
const loading = ref(true)
const error = ref(null)
const showQR = ref(false)

// Format amount to 2 decimal places
function formatAmount(amount) {
  return (amount || 0).toFixed(2)
}

async function fetchProfile() {
  loading.value = true
  error.value = null
  
  try {
    const userData = await userStore.fetchUserProfile()
    if (userData) {
      userProfile.value = userData
    } else {
      error.value = "Could not load profile data"
    }
  } catch (err) {
    console.error('Error in profile component:', err)
    error.value = "An error occurred while loading your profile"
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchProfile()
})
</script>
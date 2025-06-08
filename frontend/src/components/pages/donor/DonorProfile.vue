<template>
  <div class="max-w-3xl mx-auto bg-white rounded-2xl shadow-lg p-8">
    <h2 class="text-2xl font-bold text-gray-800 mb-6">Profile</h2>
    
    <!-- Loading indicator -->
    <div v-if="isLoading" class="flex justify-center items-center py-12">
      <svg class="animate-spin h-8 w-8 text-[#C77DFF]" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
    </div>
    
    <div v-else class="space-y-8">
      <!-- Profile Information -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="flex flex-col md:flex-row items-center md:items-start space-y-4 md:space-y-0 md:space-x-6">
          <div class="w-24 h-24 rounded-full bg-[#C77DFF] flex items-center justify-center">
            <span class="text-white font-bold text-2xl">{{ getUserInitials() }}</span>
          </div>
          <div class="text-center md:text-left">
            <h3 class="text-xl font-medium text-gray-800">{{ donorName }}</h3>
            <p class="text-gray-500">{{ donorUser?.email }}</p>
            <p class="text-gray-500">{{ donorUser?.phone || "No phone number" }}</p>
            <p class="mt-2 inline-flex items-center rounded-full bg-green-100 px-3 py-1 text-sm font-medium text-green-700">
              <span class="mr-1">●</span> Active Donor
            </p>
          </div>
        </div>
        
        <div class="bg-gray-50 p-6 rounded-lg">
          <h3 class="text-lg font-medium text-gray-800 mb-4">Donation Summary</h3>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <p class="text-sm text-gray-500">Total Donations</p>
              <p class="text-xl font-bold text-[#C77DFF]">{{ stats.totalDonations }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500">Total Amount</p>
              <p class="text-xl font-bold text-[#C77DFF]">RM {{ stats.totalAmount.toFixed(2) }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500">Last Donation</p>
              <p class="text-gray-700">{{ stats.lastDonation }}</p>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Update Profile Section -->
      <div class="border-t pt-8">
        <h3 class="text-lg font-medium text-gray-800 mb-6">Profile Information</h3>
        
        <form class="space-y-6">
          <!-- Error message -->
          <div v-if="error" class="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-lg mb-4">
            {{ error }}
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label for="name" class="block text-sm font-medium text-gray-700 mb-1">Full Name</label>
              <input 
                id="name" 
                v-model="formData.name" 
                type="text" 
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#C77DFF] bg-white text-black"
                placeholder="Your full name"
                readonly
              />
            </div>
            
            <div>
              <label for="phone" class="block text-sm font-medium text-gray-700 mb-1">Phone Number</label>
              <input 
                id="phone" 
                v-model="formData.phone" 
                type="tel" 
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#C77DFF] bg-white text-black"
                placeholder="Your phone number"
                readonly
              />
            </div>
          </div>
          
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700 mb-1">Email Address</label>
            <input 
              id="email" 
              v-model="formData.email" 
              type="email" 
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#C77DFF] bg-white text-black"
              placeholder="Your email address"
              disabled
            />
            <p class="text-xs text-gray-500 mt-1">Email address cannot be changed</p>
          </div>
        </form>
      </div>
      
      <!-- Change Password Section -->
      <div class="border-t pt-8">
        <h3 class="text-lg font-medium text-gray-800 mb-6">Change Password</h3>
        
        <form @submit.prevent="changePassword" class="space-y-6">
          <!-- Password change error message -->
          <div v-if="passwordError" class="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-lg mb-4">
            {{ passwordError }}
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label for="currentPassword" class="block text-sm font-medium text-gray-700 mb-1">Current Password</label>
              <input 
                id="currentPassword" 
                v-model="passwordData.currentPassword" 
                type="password" 
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#C77DFF] bg-white text-black"
                placeholder="Your current password"
              />
            </div>
            
            <div>
              <label for="newPassword" class="block text-sm font-medium text-gray-700 mb-1">New Password</label>
              <input 
                id="newPassword" 
                v-model="passwordData.newPassword" 
                type="password" 
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#C77DFF] bg-white text-black"
                placeholder="Your new password"
              />
            </div>
          </div>
          
          <div>
            <label for="confirmPassword" class="block text-sm font-medium text-gray-700 mb-1">Confirm New Password</label>
            <input 
              id="confirmPassword" 
              v-model="passwordData.confirmPassword" 
              type="password" 
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#C77DFF] bg-white text-black"
              placeholder="Confirm your new password"
            />
          </div>
          
          <div class="pt-4 flex justify-end">
            <button 
              type="submit" 
              class="px-6 py-3 bg-[#C77DFF] text-white font-medium rounded-lg hover:bg-[#a259e6] transition-all"
              :disabled="changingPassword"
            >
              {{ changingPassword ? 'Updating...' : 'Change Password' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useDonorAuthStore } from '../../../stores/donorAuth'
import { useToastStore } from '../../../stores/toast'
import axios from 'axios'

const donorAuthStore = useDonorAuthStore()
const toastStore = useToastStore()

// User data
const donorUser = computed(() => donorAuthStore.donorUser)
const donorName = computed(() => donorUser.value?.name || 'Donor')

// Stats
const stats = ref({
  totalDonations: 0,
  totalAmount: 0,
  lastDonation: 'N/A'
})

// Form data
const formData = ref({
  name: '',
  email: '',
  phone: ''
})

// Password change data
const passwordData = ref({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

// UI states
const isLoading = ref(true)
const updating = ref(false)
const changingPassword = ref(false)
const error = ref('')
const passwordError = ref('')

onMounted(async () => {
  await fetchDonorProfile()
  await fetchDonorStats()
  isLoading.value = false
})

async function fetchDonorProfile() {
  try {
    const response = await axios.get('http://127.0.0.1:5000/api/auth/profile', {
      headers: {
        'Authorization': `Bearer ${donorAuthStore.donorToken}`
      }
    })
    
    // Update form data with profile info
    formData.value.name = response.data.name || ''
    formData.value.email = response.data.email || ''
    formData.value.phone = response.data.phone || ''
    
    // Update donor user in store if needed
    if (donorAuthStore.donorUser) {
      donorAuthStore.donorUser = {
        ...donorAuthStore.donorUser,
        name: response.data.name,
        email: response.data.email,
        phone: response.data.phone
      }
    }
  } catch (err) {
    console.error('Error fetching donor profile:', err)
    error.value = 'Could not load profile information'
  }
}

async function fetchDonorStats() {
  try {
    const response = await axios.get('http://localhost:5000/api/donations/stats', {
      headers: {
        'Authorization': `Bearer ${donorAuthStore.donorToken}`
      }
    })
    
    stats.value = {
      totalDonations: response.data.totalDonations || 0,
      totalAmount: response.data.totalAmount || 0,
      lastDonation: formatDate(response.data.lastDonationDate) || 'N/A'
    }
  } catch (err) {
    console.error('Error fetching donor stats:', err)
    toastStore.error('Could not load donation statistics')
  }
}

function getUserInitials() {
  const name = donorUser.value?.name || ''
  return name
    .split(' ')
    .map(part => part[0])
    .join('')
    .toUpperCase()
    .substring(0, 2) || 'DN'
}

function formatDate(dateString) {
  if (!dateString) return 'N/A'
  
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

async function changePassword() {
  // Validate password inputs
  if (!passwordData.value.currentPassword || !passwordData.value.newPassword || !passwordData.value.confirmPassword) {
    passwordError.value = 'All password fields are required'
    return
  }
  
  if (passwordData.value.newPassword !== passwordData.value.confirmPassword) {
    passwordError.value = 'New password and confirmation do not match'
    return
  }
  
  if (passwordData.value.newPassword.length < 6) {
    passwordError.value = 'Password must be at least 6 characters long'
    return
  }
  
  changingPassword.value = true
  passwordError.value = ''
  
  try {
    // Change password through API
    await axios.post('http://127.0.0.1:5000/api/auth/change-password',
      {
        userId: donorAuthStore.donorUser?.id || donorAuthStore.donorUser?.user_id,
        oldPassword: passwordData.value.currentPassword,
        newPassword: passwordData.value.newPassword
      },
      {
        headers: {
          'Authorization': `Bearer ${donorAuthStore.donorToken}`
        }
      }
    )
    
    // Clear password fields
    passwordData.value = {
      currentPassword: '',
      newPassword: '',
      confirmPassword: ''
    }
    
    toastStore.success('Password changed successfully')
  } catch (err) {
    console.error('Error changing password:', err)
    passwordError.value = err.response?.data?.error || 'Failed to change password'
    toastStore.error('Failed to change password')
  } finally {
    changingPassword.value = false
  }
}
</script> 
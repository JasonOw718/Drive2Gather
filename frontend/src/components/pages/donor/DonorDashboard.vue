<template>
  <div class="w-full mx-auto bg-white rounded-2xl shadow-lg p-8">
    <!-- Welcome Section -->
    <div class="bg-[#F8F0FF] rounded-lg p-6 shadow-sm mb-8">
      <div class="flex items-center">
        <div class="w-16 h-16 rounded-full bg-[#C77DFF] flex items-center justify-center mr-6">
          <span class="text-white font-bold text-xl">{{ getUserInitials() }}</span>
        </div>
        <div>
          <p class="text-gray-600">Welcome back,</p>
          <h2 class="text-2xl font-bold text-gray-800">{{ donorName }}</h2>
        </div>
      </div>
    </div>

    <!-- Quick Stats Section -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      <div class="bg-white border border-gray-200 rounded-lg p-6 shadow-sm">
        <h3 class="text-lg font-medium text-gray-800 mb-2">Total Donations</h3>
        <p class="text-3xl font-bold text-[#C77DFF]">{{ recentDonations.length }}</p>
      </div>
      
      <div class="bg-white border border-gray-200 rounded-lg p-6 shadow-sm">
        <h3 class="text-lg font-medium text-gray-800 mb-2">Total Amount</h3>
        <p class="text-3xl font-bold text-[#C77DFF]">RM {{ totalAmount.toFixed(2) }}</p>
      </div>
      
      <div class="bg-white border border-gray-200 rounded-lg p-6 shadow-sm">
        <h3 class="text-lg font-medium text-gray-800 mb-2">Last Donation</h3>
        <p class="text-3xl font-bold text-[#C77DFF]">{{ formatLastDonationDate() }}</p>
      </div>
    </div>

    <!-- Recent Donations Section -->
    <div v-if="recentDonations.length > 0" class="mb-6">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-xl font-medium text-gray-800">Recent Donations</h3>
        <router-link 
          to="/portal/donor/history"
          class="text-[#C77DFF] text-sm font-medium hover:underline"
        >
          View All
        </router-link>
      </div>
      
      <div class="overflow-x-auto">
        <table class="min-w-full bg-white">
          <thead>
            <tr>
              <th class="py-3 px-4 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
              <th class="py-3 px-4 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Description</th>
              <th class="py-3 px-4 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Payment Method</th>
              <th class="py-3 px-4 bg-gray-50 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Amount</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            <tr v-for="donation in recentDonations" :key="donation.donation_id" class="hover:bg-gray-50">
              <td class="py-4 px-4 text-sm text-gray-500">{{ formatDate(donation.date) }}</td>
              <td class="py-4 px-4 text-sm text-gray-900">System Donation</td>
              <td class="py-4 px-4 text-sm text-gray-600">{{ formatPaymentMethod(donation.payment_method) }}</td>
              <td class="py-4 px-4 text-right text-sm font-medium text-[#C77DFF]">RM {{ donation.amount.toFixed(2) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <!-- No Donations State -->
    <div v-else class="bg-gray-50 rounded-lg p-8 text-center">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 mx-auto mb-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
      </svg>
      <p class="text-gray-600 mb-6">You haven't made any donations yet.</p>
      <router-link 
        to="/portal/donor/donate"
        class="px-6 py-3 bg-[#C77DFF] text-white rounded-lg text-sm font-medium hover:bg-[#a259e6] transition"
      >
        Make Your First Donation
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useDonorAuthStore } from '../../../stores/donorAuth'
import { useToastStore } from '../../../stores/toast'
import axios from 'axios'

const donorAuthStore = useDonorAuthStore()
const toastStore = useToastStore()

const donorName = computed(() => {
  return donorAuthStore.donorUser?.name || 'Donor'
})

const recentDonations = ref([])
const isLoading = ref(false)

onMounted(async () => {
  await fetchRecentDonations()
})

async function fetchRecentDonations() {
  isLoading.value = true
  
  try {
    const response = await axios.get('http://localhost:5000/api/donations/made', {
      headers: {
        'Authorization': `Bearer ${donorAuthStore.donorToken}`
      },
      params: {
        page: 1,
        size: 5
      }
    })
    
    recentDonations.value = response.data.donations || []
  } catch (error) {
    console.error('Error fetching recent donations:', error)
    toastStore.error('Could not load donation data')
  } finally {
    isLoading.value = false
  }
}

const totalAmount = computed(() => {
  if (!recentDonations.value || recentDonations.value.length === 0) return 0
  return recentDonations.value.reduce((sum, donation) => sum + donation.amount, 0)
})

function getUserInitials() {
  const name = donorAuthStore.donorUser?.name || ''
  return name
    .split(' ')
    .map(part => part[0])
    .join('')
    .toUpperCase()
    .substring(0, 2)
}

function formatDate(dateString) {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

function formatLastDonationDate() {
  if (!recentDonations.value || recentDonations.value.length === 0) return 'N/A'
  
  // Sort donations by date (newest first)
  const sortedDonations = [...recentDonations.value].sort((a, b) => 
    new Date(b.date) - new Date(a.date)
  )
  
  return formatDate(sortedDonations[0].date)
}

function formatPaymentMethod(method) {
  switch (method) {
    case 'stripe':
      return 'Credit Card'
    case 'paypal':
      return 'PayPal'
    default:
      return method
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');
</style> 
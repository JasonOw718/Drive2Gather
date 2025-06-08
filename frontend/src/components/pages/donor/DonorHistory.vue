<template>
  <div class="w-full mx-auto bg-white rounded-2xl shadow-lg p-8">
    <!-- Summary Card -->
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-6 mb-8">
      <div class="bg-[#F8F0FF] rounded-lg p-6 shadow-sm">
        <h3 class="text-lg font-medium text-gray-800 mb-2">Total Donations</h3>
        <p class="text-3xl font-bold text-[#C77DFF]">{{ donations.length }}</p>
      </div>
      
      <div class="bg-[#F8F0FF] rounded-lg p-6 shadow-sm">
        <h3 class="text-lg font-medium text-gray-800 mb-2">Total Amount</h3>
        <p class="text-3xl font-bold text-[#C77DFF]">RM {{ totalAmount.toFixed(2) }}</p>
      </div>
    </div>
    
    <!-- Filter Options -->
    <div class="flex justify-between items-center mb-6">
      <h3 class="text-xl font-medium text-gray-800">Donation History</h3>
      <div class="relative">
        <select 
          v-model="sortOption" 
          class="appearance-none bg-white border border-gray-300 rounded-lg px-4 py-2 pr-8 text-sm text-gray-700 focus:outline-none focus:ring-2 focus:ring-[#C77DFF]"
        >
          <option value="dateDesc">Newest First</option>
          <option value="dateAsc">Oldest First</option>
          <option value="amountDesc">Amount: High to Low</option>
          <option value="amountAsc">Amount: Low to High</option>
        </select>
        <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700">
          <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
          </svg>
        </div>
      </div>
    </div>
    
    <!-- Loading State -->
    <div v-if="isLoading" class="flex justify-center items-center py-12">
      <svg class="animate-spin h-8 w-8 text-[#C77DFF]" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
    </div>
    
    <!-- Donations List -->
    <div v-else-if="donations.length > 0">
      <div class="overflow-x-auto">
        <table class="min-w-full bg-white border border-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="py-3 px-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
              <th class="py-3 px-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Description</th>
              <th class="py-3 px-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Payment Method</th>
              <th class="py-3 px-4 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Amount</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            <tr v-for="donation in sortedDonations" :key="donation.donation_id" class="hover:bg-gray-50">
              <td class="py-4 px-4 text-sm text-gray-500">{{ formatDate(donation.date) }}</td>
              <td class="py-4 px-4 text-sm text-gray-900">
                System Donation
                <p v-if="donation.description" class="mt-1 text-xs text-gray-500">
                  {{ donation.description }}
                </p>
              </td>
              <td class="py-4 px-4 text-sm text-gray-600">{{ formatPaymentMethod(donation.payment_method) }}</td>
              <td class="py-4 px-4 text-right text-sm font-medium text-[#C77DFF]">RM {{ donation.amount.toFixed(2) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <!-- Pagination controls -->
      <div v-if="totalPages > 1" class="flex justify-center items-center space-x-4 mt-6">
        <button 
          @click="prevPage" 
          :disabled="currentPage === 1" 
          class="px-4 py-2 rounded-lg text-sm"
          :class="currentPage === 1 ? 'bg-gray-100 text-gray-400' : 'bg-[#F8F0FF] text-[#C77DFF] hover:bg-[#E0AAFF]'"
        >
          Previous
        </button>
        <span class="text-sm text-gray-600">Page {{ currentPage }} of {{ totalPages }}</span>
        <button 
          @click="nextPage" 
          :disabled="currentPage === totalPages" 
          class="px-4 py-2 rounded-lg text-sm"
          :class="currentPage === totalPages ? 'bg-gray-100 text-gray-400' : 'bg-[#F8F0FF] text-[#C77DFF] hover:bg-[#E0AAFF]'"
        >
          Next
        </button>
      </div>
    </div>
    
    <!-- Empty State -->
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
import { ref, computed, onMounted, watch } from 'vue'
import { useDonorAuthStore } from '../../../stores/donorAuth'
import { useToastStore } from '../../../stores/toast'
import axios from 'axios'

const donorAuthStore = useDonorAuthStore()
const toastStore = useToastStore()

const donations = ref([])
const isLoading = ref(false)
const sortOption = ref('dateDesc')
const currentPage = ref(1)
const totalPages = ref(1)
const pageSize = 10

onMounted(async () => {
  await fetchDonations()
})

watch(currentPage, async () => {
  await fetchDonations()
})

async function fetchDonations() {
  isLoading.value = true
  
  try {
    const response = await axios.get('http://localhost:5000/api/donations/made', {
      headers: {
        'Authorization': `Bearer ${donorAuthStore.donorToken}`
      },
      params: {
        page: currentPage.value,
        size: pageSize
      }
    })
    
    donations.value = response.data.donations || []
    totalPages.value = Math.ceil(response.data.total / pageSize)
  } catch (error) {
    console.error('Error fetching donations:', error)
    toastStore.error('Could not load donation history')
  } finally {
    isLoading.value = false
  }
}

const sortedDonations = computed(() => {
  if (!donations.value) return []
  
  return [...donations.value].sort((a, b) => {
    switch (sortOption.value) {
      case 'dateDesc':
        return new Date(b.date) - new Date(a.date)
      case 'dateAsc':
        return new Date(a.date) - new Date(b.date)
      case 'amountDesc':
        return b.amount - a.amount
      case 'amountAsc':
        return a.amount - b.amount
      default:
        return 0
    }
  })
})

const totalAmount = computed(() => {
  if (!donations.value || donations.value.length === 0) return 0
  return donations.value.reduce((sum, donation) => sum + donation.amount, 0)
})

function formatDate(dateString) {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

function formatPaymentMethod(method) {
  switch (method) {
    case 'stripe':
      return 'PayPal'
    case 'paypal':
      return 'Bank Transfer'
    default:
      return method
  }
}

function nextPage() {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
  }
}

function prevPage() {
  if (currentPage.value > 1) {
    currentPage.value--
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');
</style> 
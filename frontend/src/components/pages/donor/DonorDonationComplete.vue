<template>
  <div class="max-w-3xl mx-auto bg-white rounded-2xl shadow-lg p-8">
    <!-- Success Icon -->
    <div class="flex flex-col items-center justify-center mb-8">
      <div class="w-24 h-24 rounded-full bg-green-100 flex items-center justify-center mb-6">
        <svg class="w-14 h-14 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
        </svg>
      </div>
      <h2 class="text-3xl font-bold text-center text-gray-800 mb-2">Thank You!</h2>
      <p class="text-gray-600 text-center text-lg max-w-lg">
        Your generous donation will help us continue to provide quality ride-sharing services.
      </p>
    </div>
    
    <!-- Donation Details -->
    <div class="bg-gray-50 rounded-lg p-6 mb-8">
      <h3 class="text-lg font-medium text-gray-800 mb-4">Donation Details</h3>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div>
          <p class="text-sm text-gray-500 mb-1">Amount</p>
          <p class="text-xl font-bold text-[#C77DFF]">RM {{ amount }}</p>
        </div>
        <div>
          <p class="text-sm text-gray-500 mb-1">Payment Method</p>
          <p class="text-xl font-medium text-gray-800">{{ formattedPaymentMethod }}</p>
        </div>
        <div>
          <p class="text-sm text-gray-500 mb-1">Date</p>
          <p class="text-xl font-medium text-gray-800">{{ currentDate }}</p>
        </div>
      </div>
    </div>
    
    <!-- Action Buttons -->
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
      <button 
        @click="donate" 
        class="w-full py-3 px-4 bg-[#F8F0FF] text-[#C77DFF] font-medium rounded-lg hover:bg-[#E0AAFF] transition-all"
      >
        Make Another Donation
      </button>
      <button 
        @click="goHome" 
        class="w-full py-3 px-4 bg-[#C77DFF] text-white font-medium rounded-lg hover:bg-opacity-90 transition-all"
      >
        Return to Dashboard
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

// Get parameters passed from donation component
const amount = computed(() => {
  const val = route.query.amount
  return val ? parseFloat(val).toFixed(2) : '0.00'
})

const formattedPaymentMethod = computed(() => {
  return formatPaymentMethod(route.query.paymentMethod || 'stripe')
})

const currentDate = computed(() => {
  return getCurrentDate()
})

function formatPaymentMethod(method) {
  switch (method) {
    case 'stripe':
      return 'Stripe'
    case 'paypal':
      return 'Paypal'
    default:
      return method
  }
}

function getCurrentDate() {
  const date = new Date()
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

function donate() {
  router.push('/portal/donor/donate')
}

function goHome() {
  router.push('/portal/donor/dashboard')
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');
</style> 
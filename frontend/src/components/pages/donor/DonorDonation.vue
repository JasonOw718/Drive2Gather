<template>
  <div class="max-w-3xl mx-auto bg-white rounded-2xl shadow-lg p-8">
    <div class="flex items-start mb-6">
      <img src="@/assets/images/heart.png" alt="Donation" class="w-16 h-16 object-contain mr-4" style="filter: drop-shadow(0 2px 8px #C77DFF33);" />
      <div>
        <h2 class="text-2xl font-semibold text-[#C77DFF] mb-2">Support Ride2Gather</h2>
        <p class="text-gray-600">
          Your donation helps us maintain and improve Ride2Gather to provide better ride-sharing services for everyone. 
          Thank you for your support!
        </p>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mt-8">
      <div>
        <!-- Donation Amount Section -->
        <div class="mb-6">
          <label class="block text-lg font-medium text-gray-700 mb-2">Donation Amount</label>
          <div class="flex items-center justify-center border border-gray-300 rounded-lg overflow-hidden bg-white">
            <button 
              @click="decrement" 
              :disabled="donationAmount <= 5" 
              class="px-4 py-3 text-gray-700 hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed bg-white"
            >
              <font-awesome-icon icon="fa-minus" />
            </button>
            <div class="flex-1 text-center py-3 font-bold text-xl text-[#C77DFF] bg-white">
              RM {{ donationAmount.toFixed(2) }}
            </div>
            <button 
              @click="increment" 
              :disabled="donationAmount >= 1000" 
              class="px-4 py-3 text-gray-700 hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed bg-white"
            >
              <font-awesome-icon icon="fa-plus" />
            </button>
          </div>
        </div>

        <!-- Payment Method Selection -->
        <div class="mb-6">
          <label class="block text-lg font-medium text-gray-700 mb-2">Payment Method</label>
          <div class="grid grid-cols-2 gap-4">
            <button 
              @click="paymentMethod = 'stripe'" 
              :class="[
                'py-4 px-6 rounded-lg border transition-all duration-200 flex items-center justify-center gap-3',
                paymentMethod === 'stripe' 
                  ? 'border-[#C77DFF] bg-white' 
                  : 'border-gray-300 bg-white hover:bg-gray-50'
              ]"
            >
              <span class="text-xl" role="img" aria-label="PayPal">💳</span>
              <span class="font-medium" :class="paymentMethod === 'stripe' ? 'text-[#C77DFF]' : 'text-gray-700'">PayPal</span>
            </button>
            <button 
              @click="paymentMethod = 'paypal'" 
              :class="[
                'py-4 px-6 rounded-lg border transition-all duration-200 flex items-center justify-center gap-3',
                paymentMethod === 'paypal' 
                  ? 'border-[#C77DFF] bg-white' 
                  : 'border-gray-300 bg-white hover:bg-gray-50'
              ]"
            >
              <span class="text-xl" role="img" aria-label="Stripe">🏦</span>
              <span class="font-medium" :class="paymentMethod === 'paypal' ? 'text-[#C77DFF]' : 'text-gray-700'">Stripe</span>
            </button>
          </div>
        </div>
      </div>
      
      <div>
        <!-- Message Input -->
        <div class="mb-6">
          <label class="block text-lg font-medium text-gray-700 mb-2">Add a message (optional)</label>
          <textarea 
            v-model="message" 
            class="w-full p-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#C77DFF] bg-white text-black"
            placeholder="Leave a message or feedback..."
            rows="5"
          ></textarea>
        </div>

        <!-- Error message -->
        <div v-if="error" class="text-red-500 text-sm mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
          {{ error }}
        </div>

        <!-- Donate Button -->
        <button
          class="w-full py-3 px-4 rounded-lg shadow-md text-lg font-bold transition-all duration-300 bg-[#C77DFF] text-white hover:bg-opacity-90 cursor-pointer disabled:bg-opacity-50 disabled:cursor-not-allowed"
          @click="donateToSystem"
          :disabled="loading"
        >
          {{ loading ? 'Processing...' : 'Donate to Ride2Gather!' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useDonorAuthStore } from '../../../stores/donorAuth'
import { useToastStore } from '../../../stores/toast'
import axios from 'axios'

const router = useRouter()
const donorAuthStore = useDonorAuthStore()
const toastStore = useToastStore()

// Donation state
const donationAmount = ref(10) // Default amount
const message = ref('')
const paymentMethod = ref('stripe') // Default to Stripe
const loading = ref(false)
const error = ref('')

function increment() { 
  if (donationAmount.value < 1000) {
    if (donationAmount.value < 50) {
      donationAmount.value += 5
    } else if (donationAmount.value < 100) {
      donationAmount.value += 10
    } else {
      donationAmount.value += 50
    }
  }
}

function decrement() { 
  if (donationAmount.value > 5) {
    if (donationAmount.value <= 50) {
      donationAmount.value -= 5
    } else if (donationAmount.value <= 100) {
      donationAmount.value -= 10
    } else {
      donationAmount.value -= 50
    }
  }
}

async function donateToSystem() {
  loading.value = true
  error.value = ''
  
  try {
    // Get current donor ID
    const donorId = donorAuthStore.donorUser?.id || donorAuthStore.donorUser?.user_id
    
    if (!donorId) {
      error.value = 'User not authenticated'
      return
    }
    
    // Prepare donation data
    const donationData = {
      systemDonation: true,
      donorId: donorId,
      amount: donationAmount.value,
      paymentMethod: paymentMethod.value,
      message: message.value
    }
    
    // Make API call to process the donation
    await axios.post('http://localhost:5000/api/donations/system', donationData, {
      headers: {
        'Authorization': `Bearer ${donorAuthStore.donorToken}`
      }
    })
    
    // Show success message
    toastStore.success('Thank you for your donation!')
    
    // Navigate to donation complete page
    router.push({ 
      name: 'DonorDonationComplete', 
      query: { 
        amount: donationAmount.value,
        paymentMethod: paymentMethod.value,
        donorName: donorAuthStore.donorUser?.name || 'You'
      } 
    })
  } catch (err) {
    console.error('Error making donation:', err)
    error.value = err.response?.data?.error || 'Failed to process donation. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&family=Poppins:wght@400;500&display=swap');
</style> 
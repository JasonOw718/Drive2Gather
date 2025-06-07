<template>
  <div class="min-h-screen bg-white px-6 pt-[max(2.5rem,env(safe-area-inset-top))] pb-[max(env(safe-area-inset-bottom),2.5rem)] flex flex-col" style="max-width: 420px; margin: 0 auto; font-family: 'Roboto', sans-serif;">
    <div class="bg-gray-800 py-4 px-4 -mx-6 text-white text-center">
      <h1 class="text-lg font-medium">Donation Thanks Page</h1>
    </div>
    
    <div class="flex flex-col items-center justify-center flex-1 text-center py-8">
      <!-- Heart Icon -->
      <div class="mb-6">
        <div class="w-24 h-24 flex items-center justify-center">
          <svg width="96" height="96" viewBox="0 0 96 96" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M32 16C19.6 16 12 26.4 12 36.8C12 58.4 40 76 48 80C56 76 84 58.4 84 36.8C84 26.4 76.4 16 64 16C56.4 16 51.2 20 48 26.4C44.8 20 39.6 16 32 16Z" fill="#C77DFF" fill-opacity="0.6"/>
            <path d="M48 80C40 76 12 58.4 12 36.8C12 26.4 19.6 16 32 16C39.6 16 44.8 20 48 26.4V80Z" fill="#C77DFF"/>
            <path d="M70 44H58V36C58 33.8 56.2 32 54 32H52C49.8 32 48 33.8 48 36V44H36C33.8 44 32 45.8 32 48V50C32 52.2 33.8 54 36 54H48V78C48 80.2 49.8 82 52 82H54C56.2 82 58 80.2 58 78V54H70C72.2 54 74 52.2 74 50V48C74 45.8 72.2 44 70 44Z" fill="#F9D8AD"/>
            <path d="M36 44H48V36C48 33.8 49.8 32 52 32H54C56.2 32 58 33.8 58 36V44H70C72.2 44 74 45.8 74 48V50C74 52.2 72.2 54 70 54H58V78C58 80.2 56.2 82 54 82H52C49.8 82 48 80.2 48 78V54" stroke="#F9B56B" stroke-width="2"/>
          </svg>
        </div>
      </div>
      
      <!-- Thank You Message -->
      <h2 class="text-xl font-medium mb-6 text-[#C77DFF]">Thanks for your donation</h2>
      
      <!-- Driver Information Card -->
      <div class="w-full bg-white rounded-lg shadow-sm border border-gray-100 p-4 mb-6">
        <div class="flex items-center">
          <div class="w-10 h-10 bg-gray-200 rounded-full mr-3 overflow-hidden">
            <img :src="driverAvatar || '@/assets/images/default-avatar.png'" alt="Driver" class="w-full h-full object-cover" />
          </div>
          <div class="text-left">
            <h3 class="font-medium">{{ driverName }}</h3>
            <p class="text-sm text-gray-500">{{ carInfo }}</p>
          </div>
        </div>
      </div>
      
      <!-- Donation Details -->
      <div class="w-full flex justify-between items-center mb-2">
        <h3 class="text-lg font-medium">Tips</h3>
        <span class="text-lg font-medium text-[#C77DFF]">RM {{ tipAmount }}</span>
      </div>
      
      <!-- Payment Method -->
      <div class="w-full flex justify-between items-center mb-8">
        <h3 class="text-sm text-gray-600">Payment Method</h3>
        <span class="text-sm font-medium">
          <span class="mr-1" v-if="paymentMethod === 'paypal'">🅿️</span>
          <span class="mr-1" v-else>💳</span>
          {{ paymentMethod === 'paypal' ? 'PayPal' : 'Stripe' }}
        </span>
      </div>
      
      <!-- Download Receipt Button -->
      <button
        @click="downloadReceipt"
        class="w-full py-3 px-4 rounded-full mb-4 flex items-center justify-center gap-2 border border-[#C77DFF] text-[#C77DFF] font-medium"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clip-rule="evenodd" />
        </svg>
        Download Receipt
      </button>
      
      <!-- Back to Home Button -->
      <button
        @click="$router.push('/')"
        class="w-full py-3 px-4 rounded-full shadow-md bg-[#C77DFF] text-white font-medium"
      >
        Back to Home
      </button>
    </div>
    
    <!-- Loading overlay for PDF generation -->
    <div v-if="isGeneratingPdf" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white p-6 rounded-lg shadow-lg text-center">
        <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-[#C77DFF] mx-auto mb-4"></div>
        <p>Generating receipt...</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router'
import { ref, computed, onMounted } from 'vue'
import { jsPDF } from 'jspdf'

const route = useRoute()
const router = useRouter()

// Get donation details from route query params
const tipAmount = ref(route.query.tip || '0')
const driverName = ref(route.query.driverName || 'the driver')
const driverAvatar = ref(route.query.driverAvatar || '@/assets/images/default-avatar.png')
const carInfo = ref(route.query.carPlate ? `${route.query.carPlate} • ${route.query.driverCarType || 'Vehicle'}` : 'Vehicle')
const paymentMethod = ref(route.query.paymentMethod || 'stripe')
const donorName = ref(route.query.donorName || 'You')
const isGeneratingPdf = ref(false)
const qrCodeImage = '@/assets/images/qrcode.jpg'

// Format date for receipt
const formattedDate = computed(() => {
  const now = new Date()
  return now.toLocaleDateString('en-MY', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
})

// Generate unique receipt ID
const receiptId = computed(() => {
  return 'RCT-' + Math.random().toString(36).substring(2, 10).toUpperCase()
})

function downloadReceipt() {
  isGeneratingPdf.value = true
  
  setTimeout(() => {
    try {
      // Create a new PDF document
      const doc = new jsPDF({
        orientation: 'portrait',
        unit: 'mm',
        format: 'a5'
      })
      
      // Set font
      doc.setFont('helvetica', 'normal')
      
      // Add header
      doc.setFillColor(199, 125, 255) // #C77DFF
      doc.rect(0, 0, 148, 20, 'F')
      doc.setTextColor(255, 255, 255)
      doc.setFontSize(16)
      doc.text('Ride2Gather - Donation Receipt', 74, 12, { align: 'center' })
      
      // Add receipt details
      doc.setTextColor(0, 0, 0)
      doc.setFontSize(12)
      doc.text('Receipt ID: ' + receiptId.value, 20, 30)
      doc.text('Date: ' + formattedDate.value, 20, 38)
      
      // Add divider
      doc.setDrawColor(200, 200, 200)
      doc.line(20, 45, 128, 45)
      
      // Add donation details
      doc.setFontSize(14)
      doc.text('Donation Details', 20, 55)
      
      doc.setFontSize(12)
      doc.text('Donor: ' + donorName.value, 20, 65)
      doc.text('Recipient: ' + driverName.value, 20, 73)
      doc.text('Car: ' + carInfo.value, 20, 81)
      doc.text('Payment Method: ' + (paymentMethod.value === 'paypal' ? 'PayPal' : 'Stripe'), 20, 89)
      
      // Add amount
      doc.setFontSize(14)
      doc.text('Amount', 20, 105)
      doc.text('RM ' + tipAmount.value, 128, 105, { align: 'right' })
      
      // Add divider
      doc.line(20, 110, 128, 110)
      
      // Add total
      doc.setFontSize(16)
      doc.setFont('helvetica', 'bold')
      doc.text('Total', 20, 120)
      doc.text('RM ' + tipAmount.value, 128, 120, { align: 'right' })
      
      // Add thank you note
      doc.setFontSize(12)
      doc.setFont('helvetica', 'italic')
      doc.text('Thank you for your generosity!', 74, 135, { align: 'center' })
      
      // Add heart icon
      doc.setTextColor(199, 125, 255)
      doc.setFontSize(24)
      doc.text('♥', 74, 145, { align: 'center' })
      
      // Add footer
      doc.setFillColor(240, 240, 240)
      doc.rect(0, 190, 148, 15, 'F')
      doc.setFontSize(10)
      doc.setTextColor(100, 100, 100)
      doc.text('Ride2Gather - Making carpooling better together', 74, 198, { align: 'center' })
      
      // Save the PDF
      doc.save('donation-receipt-' + receiptId.value + '.pdf')
    } catch (error) {
      console.error('Error generating PDF:', error)
      alert('Failed to generate receipt. Please try again.')
    } finally {
      isGeneratingPdf.value = false
    }
  }, 1000) // Add a slight delay for better UX
}

onMounted(() => {
  console.log('Donation complete with amount:', tipAmount.value)
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&family=Poppins:wght@400;500&display=swap');
</style> 
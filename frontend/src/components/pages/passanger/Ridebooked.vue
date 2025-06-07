<template>
  <div ref="containerRef" class="min-h-screen flex flex-col justify-between items-center bg-white px-4 pt-[max(2.5rem,env(safe-area-inset-top))] pb-[max(env(safe-area-inset-bottom),2.5rem)]" style="max-width: 420px; margin: 0 auto; font-family: 'Roboto', sans-serif;">
    <!-- Header with Back Button -->
    <div class="w-full flex items-center justify-between mb-6">
      <button @click="goBack" class="flex items-center text-gray-700">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
        <span class="ml-1">Back</span>
      </button>
      <div class="text-lg font-medium text-gray-900">Ride Request Status</div>
      <div class="w-12"></div> <!-- Spacer for alignment -->
    </div>
    
    <!-- Success Animation -->
    <div class="flex flex-col items-center mb-6">
      <div class="bg-[#F0E5FF] rounded-full p-4 mb-4">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-[#C77DFF]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </div>

      <!-- Car Icon with Animation -->
      <div class="w-full flex items-center justify-center mt-2 mb-2 relative h-24">
        <img
          :key="isAccepted"
          :class="['w-28 h-20 object-contain', isAccepted ? 'car-animate' : '']"
          :style="carStyle"
          src="../../../../assets/images/caricon.jpg"
          alt="Car Icon"
        />
      </div>
    </div>

    <!-- Status Text -->
    <div class="relative w-full mb-6">
      <transition name="slide-left" mode="out-in">
        <div
          :key="isAccepted ? 'accepted' : 'pending'"
          class="text-xl font-semibold transition-colors duration-700 text-center w-full"
          :style="{
            color: isAccepted ? '#C77DFF' : '#303030',
            fontFamily: 'Roboto, sans-serif',
            lineHeight: '1.5'
          }"
        >
          {{ isAccepted ? 'Confirmed! Your ride request was accepted!' : 'Ride Request Submitted' }}
        </div>
      </transition>
             <p class="text-center text-gray-600 mt-2" v-if="!isAccepted">
         Your ride request has been submitted. Waiting for driver confirmation...
       </p>
    </div>

    <!-- Ride Details Card -->
    <div class="bg-white rounded-xl p-5 w-full mt-2 shadow-md border border-gray-100">
      <h3 class="text-lg font-semibold text-gray-800 mb-4">Ride Details</h3>
      
      <div class="flex items-start gap-4 mb-4">
        <div class="flex flex-col items-center mt-1">
          <div class="w-3 h-3 rounded-full bg-[#C77DFF] z-10"></div>
          <div class="w-1 h-14 bg-[#E5E5E5] mx-auto"></div>
          <div class="w-3 h-3 rounded-full bg-[#C77DFF] z-10"></div>
        </div>
        <div class="flex-1">
          <div class="mb-3">
            <div class="text-sm text-gray-500">From</div>
            <div class="text-base font-medium text-gray-900">{{ from }}</div>
          </div>
          <div>
            <div class="text-sm text-gray-500">To</div>
            <div class="text-base font-medium text-gray-900">{{ to }}</div>
          </div>
        </div>
      </div>
      
      <div class="border-t border-gray-100 pt-3 mt-3 grid grid-cols-2 gap-4">
        <div>
          <div class="text-sm text-gray-500">Time</div>
          <div class="text-base font-medium text-gray-900">{{ time }}</div>
        </div>
        <div>
          <div class="text-sm text-gray-500">Passengers</div>
          <div class="text-base font-medium text-gray-900">{{ seats }}</div>
        </div>
      </div>
      
      <div class="border-t border-gray-100 pt-3 mt-3">
        <div class="text-sm text-gray-500">Booking ID</div>
        <div class="text-base font-medium text-gray-900">#{{ rideId }}</div>
      </div>
    </div>



    <!-- Spacer -->
    <div class="flex-1"></div>

    <!-- Buttons -->
    <div class="w-full space-y-3 mb-4 mt-8">
      
      <!-- Cancel Request Button -->
      <button
        class="w-full py-3 px-4 rounded-full border border-red-500 text-base font-medium text-red-600 hover:bg-red-50 transition-all duration-300"
        @click="confirmCancel"
      >
        Cancel Request
      </button>
    </div>

    <!-- Demo: Toggle isAccepted -->
    <button class="mb-4 text-xs underline text-[#C77DFF]" @click="toggleAccepted">
      {{ isAccepted ? 'Simulate: Driver Cancelled' : 'Simulate: Driver Accepted' }}
    </button>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

// Get ride details from query parameters
const rideId = route.query.ride_id || 'N/A'
const from = route.query.from || 'Starting Location'
const to = route.query.to || 'Drop-off Location'
const time = route.query.time || '09:00'
const seats = parseInt(route.query.seats || '1')

const isAccepted = ref(false)
const animationCounter = ref(0)
const containerRef = ref(null)
const carWidth = 112 // 28 * 4 (tailwind w-28 is 7rem = 112px)
const safeMargin = 16 // px
const maxTranslateX = ref(0)
const outTranslateX = ref(0)

const updateMaxTranslateX = () => {
  if (containerRef.value) {
    const containerWidth = containerRef.value.offsetWidth
    maxTranslateX.value = Math.max(containerWidth - carWidth - safeMargin, 0)
    outTranslateX.value = Math.max(containerWidth + carWidth, 0) // move fully out of screen
  }
}

onMounted(() => {
  updateMaxTranslateX()
  window.addEventListener('resize', updateMaxTranslateX)
  
  // No auto-confirmation for now
})

watch(containerRef, updateMaxTranslateX)

const carStyle = computed(() => {
  if (isAccepted.value) {
    return {
      animation: `car-slide-dynamic-${animationCounter.value} 2.5s linear infinite`,
      '--max-x': `${maxTranslateX.value}px`,
      '--out-x': `${outTranslateX.value}px`,
      '--car-width': `${carWidth}px`
    }
  }
  return {}
})

function toggleAccepted() {
  isAccepted.value = !isAccepted.value
  if (isAccepted.value) {
    animationCounter.value++
    // Dynamically inject new keyframes for each animation name
    nextTick(() => {
      const styleId = `car-slide-dynamic-${animationCounter.value}`
      if (!document.getElementById(styleId)) {
        const style = document.createElement('style')
        style.id = styleId
        style.innerHTML = `
          @keyframes car-slide-dynamic-${animationCounter.value} {
            0% { transform: translateX(calc(-1 * var(--car-width, 112px))); opacity: 0; }
            5% { opacity: 1; }
            90% { transform: translateX(var(--max-x, 120px)); opacity: 1; }
            100% { transform: translateX(var(--out-x, 200vw)); opacity: 0; }
          }
        `
        document.head.appendChild(style)
      }
    })
  }
}

function goToOtwpage() {
  if (isAccepted.value) {
    router.push({ 
      name: 'Otwpage',
      query: {
        ride_id: rideId,
        from,
        to,
        time
      }
    })
  }
}

function goBack() {
  router.push('/')
}

function confirmCancel() {
  if (confirm('Are you sure you want to cancel this ride request?')) {
    // In a real app, this would call an API to cancel the ride
    router.push('/')
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap');

.car-animate {
  /* animation is set dynamically via style binding */
}

.slide-left-enter-active, .slide-left-leave-active {
  transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  position: absolute;
  width: 100%;
}
.slide-left-enter-from {
  opacity: 0;
  transform: translateX(-100%);
}
.slide-left-enter-to {
  opacity: 1;
  transform: translateX(0);
}
.slide-left-leave-from {
  opacity: 1;
  transform: translateX(0);
}
.slide-left-leave-to {
  opacity: 0;
  transform: translateX(-100%);
}
</style>

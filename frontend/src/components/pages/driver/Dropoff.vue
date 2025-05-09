<template>
    <div class="min-h-screen flex flex-col justify-between items-center bg-white px-4 pt-[max(2.5rem,env(safe-area-inset-top))] pb-[max(env(safe-area-inset-bottom),2.5rem)]" style="max-width: 420px; margin: 0 auto; font-family: 'Roboto', sans-serif;">
      <!-- Header Section -->
      <div class="w-full flex flex-col items-center mt-8 mb-2">
        <div class="text-2xl font-medium text-left" style="font-family: 'Roboto', sans-serif; color: #C77DFF;">
          Thanks for riding with Ride2Gather - enjoy the ride!
        </div>
        <div class="text-base mt-2 text-left" style="font-family: 'Poppins', sans-serif; color: #8C8C8C;">
          Your journey has begun. Relax and ride together.
        </div>
      </div>
  
      <!-- Ride Details Section: Timeline -->
      <div class="w-full flex flex-col items-start mt-6 mb-4">
        <div class="flex flex-row items-center w-full justify-between">
          <div class="flex flex-col items-center ml-4">
            <!-- Timeline -->
            <div class="flex flex-col items-center h-24 justify-between">
              <div class="w-4 h-4 rounded-full border-4 border-[#C77DFF] bg-white"></div>
              <div class="w-1 flex-1 bg-[#C77DFF] my-1" style="min-height: 32px;"></div>
              <div class="w-4 h-4 rounded-full border-4 border-[#C77DFF] bg-white"></div>
            </div>
          </div>
          <div class="flex flex-col justify-between h-24 flex-1">
            <div class="mb-2 ml-4 text-left">
              <span class="text-lg font-medium text-left" style="font-family: 'Poppins', sans-serif; color: #303030;">{{ ride.from }}</span>
            </div>
            <div class="mt-auto ml-4 text-left">
              <span class="text-lg font-medium text-left" style="font-family: 'Poppins', sans-serif; color: #303030;">{{ ride.to }}</span>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Passenger Information Section -->
      <div class="w-full flex flex-row items-center justify-between mt-4 mb-2 px-2">
        <img :src="passenger.avatar" alt="Passenger Avatar" class="w-14 h-14 rounded-full object-cover border-0 border-[#C77DFF]" />
        <div class="flex flex-col flex-1 ml-4">
          <div class="text-base font-medium text-left" style="font-family: 'Poppins', sans-serif; color: #000000;">{{ passenger.name }}</div>
          <div class="text-sm mt-1 text-left" style="font-family: 'Poppins', sans-serif; color: #8C8C8C;">{{ passenger.phone }}</div>
        </div>
      </div>
  
      <div class="flex-1"></div>
  
      <!-- Action Button -->
      <button
        class="w-full py-3 px-4 rounded-full shadow-md text-base font-bold transition-all duration-300 mb-2 bg-[#C77DFF] text-white hover:bg-opacity-90 cursor-pointer"
        style="max-width: 100%; font-family: 'Roboto', sans-serif;"
        @click="goToRideComplete"
      >
        Drop off
      </button>
    </div>
  </template>
  
  <script setup>
  import { onMounted } from 'vue'
  import { useRouter } from 'vue-router'
  import { useUserStore } from '../../../stores/user.js'
  import { rideList } from '../../../stores/rideList.js'

  
  const router = useRouter()
    
  // For demo, use the first ride in the list
  const ride = rideList[0]

  const userStore = useUserStore()
  const passenger = userStore.currentUser
  
  function goToRideComplete() {
    router.push({ name: 'RidecompleteD' })
  }
  </script>
  
  <style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&family=Poppins:wght@400;500&display=swap');
  </style>
  
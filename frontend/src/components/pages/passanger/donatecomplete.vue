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
        <div class="text-2xl font-medium text-left mt-2" style="font-family: 'Roboto', sans-serif; color: #C77DFF;">Thanks for your Donation</div>
      </div>
  
      <!-- Driver Information -->
      <div class="flex flex-row items-center mb-6 w-full">
        <img :src="driver.driverAvatar" alt="Driver Avatar" class="w-8 h-8 rounded-full object-cover border-0 border-[#C77DFF] mr-4" />
        <div class="flex flex-col flex-1">
          <div class="text-base font-medium text-left" style="font-family: 'Poppins', sans-serif; color: #000000;">{{ driver.driverName }}</div>
          <div class="text-sm mt-1 text-left" style="font-family: 'Poppins', sans-serif; color: #8C8C8C;">{{ driver.carPlate }} • {{ driver.driverCarType }}</div>
        </div>
      </div>
  
      <!-- Tip Section (Figma style: label left, value right) -->
      <div class="mb-8 w-full flex flex-row items-center justify-between">
        <div class="text-base font-medium text-left" style="font-family: 'Poppins', sans-serif; color: #303030;">Tips</div>
        <div class="text-base font-bold text-right" style="font-family: 'Roboto', sans-serif; color: #C77DFF; min-width: 80px;">RM {{ tipAmount }}.00</div>
      </div>
  
      <div class="flex-1"></div>
  
      <!-- Back to Home Button -->
      <router-link
        to="/"
        class="w-full py-3 px-4 rounded-full shadow-md text-base font-bold transition-all duration-300 mb-2 bg-[#C77DFF] text-white hover:bg-opacity-90 cursor-pointer flex items-center justify-center"
        style="max-width: 100%; font-family: 'Roboto', sans-serif;"
      >
        Back to Home
      </router-link>
    </div>
  </template>
  
  <script setup>
  import { useRoute } from 'vue-router'
  import { rideList } from '../../../stores/rideList.js'
  
  const route = useRoute()
  const driver = rideList[0] // Use the first driver/ride for demo; replace with the correct ride as needed
  const tipAmount = route.query.tip || 1
  </script>
  
  <style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&family=Poppins:wght@400;500&display=swap');
  </style>
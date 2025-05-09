<template>
    <div class="min-h-screen bg-white px-6 pt-[max(2.5rem,env(safe-area-inset-top))] pb-[max(env(safe-area-inset-bottom),2.5rem)] flex flex-col" style="max-width: 420px; margin: 0 auto; font-family: 'Poppins', sans-serif;">
      <!-- Header -->
      <div class="flex items-center mt-4 mb-4">
        <button @click="$router.back()" class="mt-4 absolute top-4 left-4 w-10 h-10 flex items-center justify-center rounded-lg bg-[#F5F5F5] z-20 border border-gray-200">
          <font-awesome-icon icon="fa-arrow-left" class="text-[#C77DFF] text-2xl" />
        </button>
      </div>
  
      <div class="text-2xl font-bold text-left mb-2 text-[#000000] mt-8" style="font-family: 'Poppins', sans-serif; font-weight: 500;">Ride Request</div>
  
      <div class="text-sm text-[#8C8C8C] font-normal mb-6 text-left" style="font-family: 'Poppins', sans-serif;">{{ seatsLabel }}</div>
  
      <!-- Ride Detail Row -->
      <div class="flex items-center gap-4 mb-4">
        <div class="text-lg font-semibold text-[#303030] w-16 text-left flex-shrink-0 " style="font-family: 'Poppins', sans-serif; font-weight: 500;">{{ ride.departureTime }}</div>
        <div class="flex flex-col items-center relative" style="min-height: 70px;">
          <div class="w-1 h-14 bg-[#C77DFF] absolute left-1/2 top-3 -translate-x-1/2 z-0"></div>
          <div class="w-4 h-4 rounded-full bg-[#C77DFF] z-10"></div>
          <div class="flex-1"></div>
          <div class="w-4 h-4 rounded-full bg-[#C77DFF] z-10"></div>
        </div>
        <div class="flex flex-col justify-between h-20 ml-2">
          <div class="text-base font-medium text-[#303030] text-left" style="font-family: 'Poppins', sans-serif; font-weight: 500;">{{ ride.from }}</div>
          <div class="flex-1"></div>
          <div class="text-base font-medium text-[#303030] text-left" style="font-family: 'Poppins', sans-serif; font-weight: 500;">{{ ride.to }}</div>
        </div>
      </div>
      <hr class="border-t-1 border-[#C77DFF] my-1 mb-3" />
  
  
      <!-- Driver Detail Row -->
      <div class="flex items-center justify-between mb-4">
        <div class="flex flex-col">
          <div class="text-base font-medium text-[#303030] mb-1 text-left" style="font-family: 'Poppins', sans-serif; font-weight: 500;">{{ ride.driverName }}</div>
        </div>
        <img :src="ride.driverAvatar" alt="Driver Avatar" class="w-10 h-10 rounded-full object-cover border border-gray-200" />
      </div>
  
      <!-- Contact Driver Row -->
      <a :href="whatsappLink" target="_blank" class="flex items-center justify-between  py-3 rounded-xl  mb-4 cursor-pointer ">
        <div class="flex items-center gap-2">
          <font-awesome-icon icon="fa-solid fa-phone" alt="WhatsApp" class="w-4 h-4 text-[#303030]"/>
          <span class="text-base font-medium text-[#303030]" style="font-family: 'Poppins', sans-serif;">Contact Passenger</span>
        </div>
        <font-awesome-icon icon="fa-arrow-right" class="text-[#C77DFF] text-lg" />
      </a>
  
  
      <!-- Spacer -->
      <div class="flex-1"></div>
  
      <!-- Action Button -->
      <button class="w-full py-3 px-4 rounded-full shadow-md bg-[#C77DFF] text-white text-base font-bold hover:bg-opacity-90 transition-all duration-300 mb-0" style="max-width: 100%;">
        Accept
      </button>
    </div>
  </template>
  
  <script setup>
  import { useRoute, useRouter } from 'vue-router'
  import { ref, computed, reactive } from 'vue'
  import { usePassengerInputStore } from '../../../stores/passengerInput'
  import { useUserStore } from '../../../stores/user'
  
  const route = useRoute()
  const router = useRouter()
  const passengerInputStore = usePassengerInputStore()
  const userStore = useUserStore()
  
  // Get ride details from route query
  const ride = reactive({
    departureTime: '08:30',
    from: 'Campus A',
    to: 'Campus B',
    driverName: 'John Driver',
    driverAvatar: 'https://randomuser.me/api/portraits/men/32.jpg',
    seatAvailable: 4,
    seatFilled: 1,
    // add other fields as needed
  })
  
  const seatNeeded = 2 // mock value
  
  const seatsLabel = computed(() => {
    return seatNeeded === 1 ? '1 Passenger' : `${seatNeeded} Passengers`
  })
  
  const passengerName = computed(() => userStore.currentUser?.name || 'Passenger')
  
  const whatsappLink = computed(() => {
    const phone = (userStore.currentUser?.phone || '').replace(/[^\d+]/g, '')
    const msg = encodeURIComponent(`Hi, I am ${passengerName.value} from Ride2Gather.`)
    return `https://wa.me/${phone}?text=${msg}`
  })
  </script>
  
  <style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500&display=swap');
  </style>
  
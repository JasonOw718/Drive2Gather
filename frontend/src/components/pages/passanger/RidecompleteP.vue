<template>
    <div class="min-h-screen flex flex-col justify-between items-center bg-white px-4 pt-[max(2.5rem,env(safe-area-inset-top))] pb-[max(env(safe-area-inset-bottom),2.5rem)]" style="max-width: 420px; margin: 0 auto; font-family: 'Roboto', sans-serif;">
      <!-- Header Section -->
      <div class="w-full flex flex-col items-center mt-8 mb-2">
        <div class="text-2xl font-medium text-left" style="font-family: 'Roboto', sans-serif; color: #C77DFF;">
            Thanks for using Ride2Gather - Carpooling!
        </div>
        <div class="text-base mt-2 text-left" style="font-family: 'Poppins', sans-serif; color: #8C8C8C;">
            Your've arrived - thanks for sharing the journey.
        </div>
      </div>
      <hr class="my-2 w-full"/>
  
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
  
      <!-- Driver Information Section -->
      <div class="w-full flex flex-row items-center justify-between mt-4 mb-2 px-2">
        <img src="@/assets/images/image.png" alt="Driver Avatar" class="w-14 h-14 rounded-full object-cover border-0 border-[#C77DFF]" />
        <div class="flex flex-col flex-1 ml-4">
          <div class="text-base font-medium text-left" style="font-family: 'Poppins', sans-serif; color: #000000;">{{ ride.driverName }}</div>
          <div class="text-sm mt-1 text-left" style="font-family: 'Poppins', sans-serif; color: #8C8C8C;">{{ ride.carPlate }} • {{ ride.driverCarType }}</div>
          <div class="text-xs mt-1 text-left" style="font-family: 'Poppins', sans-serif; color: #8C8C8C;">{{ ride.carColor || 'Color not specified' }}</div>
          <div class="text-xs mt-1 text-left" style="font-family: 'Poppins', sans-serif; color: #8C8C8C;">Ride ID: {{ ride.rideId || 'Not Available' }}</div>
        </div>
      </div>
  
      <div class="w-full text-right flex justify-end gap-4 mb-4">
        <router-link :to="{ 
          name: 'ReportPsg',
          query: {
            rideId: ride.rideId,
            driverName: ride.driverName,
            carPlate: ride.carPlate,
            driverCarType: ride.driverCarType
          }
        }" class="text-sm font-medium underline" style="font-family: 'Poppins', sans-serif; color: #C77DFF;">
          Report this driver
        </router-link>
        <router-link :to="{ 
          name: 'Donation', 
          params: { driverId: driverId },
          query: {
            driverName: ride.driverName,
            driverAvatar: ride.driverAvatar,
            carPlate: ride.carPlate,
            driverCarType: ride.driverCarType
          }
        }" class="text-sm font-medium underline" style="font-family: 'Poppins', sans-serif; color: #C77DFF;">
          Tip this driver
        </router-link>
      </div>
          
      <div class="flex-1"></div>
  
      <!-- Action Button Removed -->
      
    </div>
  </template>
  
  <script setup>
  import { useRouter, useRoute } from 'vue-router'
  import { ref, onMounted } from 'vue'
  
  const router = useRouter()
  const route = useRoute()
  
  // Define props
  const props = defineProps({
    from: {
      type: String,
      default: 'MMU, Cyberjaya Campus'
    },
    to: {
      type: String,
      default: 'MRT Cyberjaya Utara Station'
    },
    driverName: {
      type: String,
      default: 'Driver Name'
    },
    driverAvatar: {
      type: String,
      default: '@/assets/images/image.png'
    },
    carPlate: {
      type: String,
      default: 'ABC123'
    },
    driverCarType: {
      type: String,
      default: 'White Cultus 2015'
    },
    carColor: {
      type: String,
      default: 'White'
    },
    driverId: {
      type: [String, Number],
      default: '1'
    },
    rideId: {
      type: [String, Number],
      default: null
    }
  })
  
  // Create a reactive ride object from props
  const ride = ref({
    from: props.from,
    to: props.to,
    driverName: props.driverName,
    driverAvatar: props.driverAvatar,
    carPlate: props.carPlate,
    driverCarType: props.driverCarType,
    carColor: props.carColor,
    driverId: props.driverId,
    rideId: props.rideId
  })
  
  function goHome() {
    router.push({ name: 'Home' })
  }
  
  onMounted(() => {
    console.log('RidecompleteP mounted with props:', props)
    console.log('RidecompleteP mounted with route query:', route.query)
    console.log('RidecompleteP mounted with route params:', route.params)
    
    // Ensure rideId is in the ride object
    if (!ride.value.rideId && route.query.rideId) {
      ride.value.rideId = route.query.rideId
      console.log('Updated ride.rideId from query:', ride.value.rideId)
    }
    
    console.log('Final ride details:', ride.value)
  })
  </script>
  
  <style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&family=Poppins:wght@400;500&display=swap');
  
  .dot {
    transition: transform 0.3s cubic-bezier(0.4,0,0.2,1), background 0.3s;
  }
  .translate-x-6 {
    transform: translateX(24px);
  }
  </style>
  
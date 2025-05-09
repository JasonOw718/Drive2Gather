<template>
  <div class="min-h-screen bg-white px-6 pt-[max(2.5rem,env(safe-area-inset-top))] pb-[max(env(safe-area-inset-bottom),2.5rem)]" style="max-width: 420px; margin: 0 auto; font-family: 'Poppins', sans-serif;">
    <!-- Top Bar -->
    <div class="flex items-center gap-4 mb-6">
      <button @click="$router.back()" class="p-0 bg-transparent border-none focus:outline-none">
        <font-awesome-icon icon="fa-arrow-left" class="text-[#C77DFF] text-2xl" />
      </button>
      <div class="flex flex-col flex-1 ml-2">
        <div class="flex items-center text-lg font-medium text-[#303030]" style="font-family: 'Poppins', sans-serif; font-weight: 500;">
          {{ from }}
          <font-awesome-icon icon="fa-arrow-right-long" class="mx-2 text-[#C77DFF]" />
          {{ to }}
        </div>
        <div class="text-sm text-[#8C8C8C] font-normal text-left" style="font-family: 'Poppins', sans-serif;">
          {{ time }} | {{ seatsLabel }}
        </div>
      </div>
    </div>

    <!-- Ride List -->
    <div v-if="filteredRides.length > 0" class="flex flex-col gap-5">
      <div v-for="(ride, idx) in filteredRides" :key="idx" @click="selectRide(ride)" class="rounded-2xl shadow-md p-4 bg-white cursor-pointer transition hover:shadow-lg">
        <!-- First Row: Time & Timeline & Locations -->
        <div class="flex items-center gap-4 mb-6">
          <div class="text-base font-semibold text-[#303030] w-14 text-left" style="font-family: 'Poppins', sans-serif; font-weight: 500;">{{ ride.departureTime }}</div>
          <div class="flex flex-col items-center justify-center h-14 relative">
            <div class="w-1 h-14 bg-[#C77DFF] absolute left-1/2 top-0 -translate-x-1/2 z-0"></div>
            <div class="w-3 h-3 rounded-full bg-[#C77DFF] z-10"></div>
            <div class="flex-1"></div>
            <div class="w-3 h-3 rounded-full bg-[#C77DFF] z-10"></div>
          </div>
          <div class="flex flex-col justify-between h-14 ml-2">
            <div class="text-sm font-medium text-[#303030] text-left" style="font-family: 'Poppins', sans-serif; font-weight: 500;">{{ ride.from }}</div>
            <div class="flex-1"></div>
            <div class="text-sm font-medium text-[#303030] text-left" style="font-family: 'Poppins', sans-serif; font-weight: 500;">{{ ride.to }}</div>
          </div>
        </div>
        <!-- Second Row: Driver & Seats -->
        <div class="flex items-center mt-2">
          <img :src="ride.driverAvatar" alt="Driver Avatar" class="w-9 h-9 rounded-full object-cover mr-3 border border-gray-200" />
          <div class="flex flex-col flex-1">
            <div class="text-sm font-medium text-[#303030] text-left" style="font-family: 'Poppins', sans-serif; font-weight: 500;">{{ ride.driverName }}</div>
            <div class="flex items-center gap-1 mt-1">
                <template v-for="n in ride.seatAvailable" :key="'seat-' + n">
                    <font-awesome-icon
                        icon="fa-solid fa-chair"
                        :class="n <= ride.seatFilled ? 'text-[#C77DFF] text-lg' : 'text-[#8C8C8C] text-lg'"
                    />
                </template>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="text-center text-[#8C8C8C] mt-10">No rides found for your search.</div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { rideList } from '../../../stores/rideList'
import { usePassengerInputStore } from '../../../stores/passengerInput'

const router = useRouter()
const route = useRoute()

// Assume these are passed as route query params
const from = ref(route.query.from || 'From')
const to = ref(route.query.to || 'To')
const time = ref(route.query.time || '09:00')
const seats = ref(Number(route.query.seats) || 1)

const passengerInputStore = usePassengerInputStore()

function parseTime(str) {
  const [h, m] = str.split(':').map(Number)
  return h * 60 + m
}

const filteredRides = computed(() => {
  const baseTime = parseTime(time.value)
  const seatsNeeded = Number(passengerInputStore.seats)
  return rideList
    .filter(ride => {
      const rideTime = parseTime(ride.departureTime)
      const availableSeats = Number(ride.seatAvailable) - Number(ride.seatFilled)
      return (
        ride.from === from.value &&
        ride.to === to.value &&
        rideTime >= baseTime &&
        rideTime <= baseTime + 120 &&
        availableSeats >= seatsNeeded
      )
    })
    .sort((a, b) => parseTime(a.departureTime) - parseTime(b.departureTime))
})

const dateLabel = computed(() => {
  // For demo, always show 'Today'.
  return 'Today'
})
const seatsLabel = computed(() => {
  return seats.value === 1 ? '1 Passenger' : `${seats.value} Passengers`
})

function selectRide(ride) {
  router.push({
    name: 'RideDetail',
    query: {
      departureTime: ride.departureTime,
      from: ride.from,
      to: ride.to,
      driverName: ride.driverName,
      driverPhone: ride.driverPhone,
      driverCarType: ride.driverCarType,
      carPlate: ride.carPlate,
      seatAvailable: ride.seatAvailable,
      seatFilled: ride.seatFilled,
      driverAvatar: ride.driverAvatar,
      carPhoto: ride.carPhoto
    }
  })
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500&display=swap');
</style>

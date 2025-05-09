<template>
    <RightNavbar />
      <div class="bg-white flex flex-col px-6 pt-[max(2.5rem,env(safe-area-inset-top))] pb-[max(env(safe-area-inset-bottom),2.5rem)] h-full flex-grow" style="max-width: 420px; margin: 0 auto;">
        <!-- Main Title -->
        <div class="text-2xl font-bold text-left mb-8 text-[#000000] mt-1">Create a Ride</div>
    
        <!-- Where are you going? -->
        <div class="mb-6">
          <div class="text-base font-semibold text-[#333333] mb-2">Where are you going?</div>
          <input
            v-model="from"
            type="text"
            placeholder="From"
            class="w-full border border-gray-200 bg-[#F5F5F5] px-4 py-3 mb-3 text-base rounded-lg text-black focus:outline-none focus:ring-2 focus:ring-[#C77DFF] text-left"
          />
          <input
            v-model="to"
            type="text"
            placeholder="To"
            class="w-full border border-gray-200 bg-[#F5F5F5] px-4 py-3 text-base rounded-lg text-black focus:outline-none focus:ring-2 focus:ring-[#C77DFF] text-left"
          />
        </div>
    
        <!-- When? (Time Picker) -->
        <div class="mb-6">
          <div class="text-base font-semibold text-[#333333] mb-2">When?</div>
          <input
            v-model="time"
            type="time"
            :min="minTime"
            step="3600"
            class="w-full border border-gray-200 bg-[#F5F5F5] px-4 py-3 text-base rounded-lg text-black focus:outline-none focus:ring-2 focus:ring-[#C77DFF] text-left"
          />
        </div>
    
        <!-- Seat needed? (Custom Counter Input) -->
        <div class="mb-8">
          <div class="text-base font-semibold text-[#333333] mb-2">Seat available?</div>
          <div class="flex items-center gap-4">
            <button @click="decrement" :disabled="seats <= 1" class="p-2 rounded-full  text-[#000000] disabled:opacity-30">
              <font-awesome-icon icon="fa-solid fa-minus" />
            </button>
            <span class="text-xl font-bold text-[#C77DFF] w-8 text-center">{{ seats }}</span>
            <button @click="increment" :disabled="seats >= 10" class="p-2 rounded-full  text-[#000000] disabled:opacity-50">
              <font-awesome-icon icon="fa-solid fa-plus" />
            </button>
          </div>
        </div>
    
        <!-- Search Button -->
        <button
          class="w-full py-3 px-4 rounded-full shadow-md bg-[#C77DFF] text-white text-base font-bold hover:bg-opacity-90 transition-all duration-300 mb-4"
          @click="onSearch"
        >
          Search
        </button>
      </div>
    </template>
    
    <script setup>
    import { ref, computed } from 'vue'
    import RightNavbar from '../rightnavbar.vue'
    
    const from = ref('')
    const to = ref('')
    const time = ref('')
    const seats = ref(1)
    
    function pad(n) {
      return n < 10 ? '0' + n : n
    }
    // Compute min time as now, rounded up to next hour
    const minTime = computed(() => {
      const now = new Date()
      let hour = now.getHours()
      let min = now.getMinutes()
      if (min > 0) hour++
      return pad(hour) + ':00'
    })
    
    function increment() {
      if (seats.value < 10) seats.value++
    }
    function decrement() {
      if (seats.value > 1) seats.value--
    }
    function onSearch() {
      console.log({ from: from.value, to: to.value, time: time.value, seats: seats.value })
    }
    </script>
    
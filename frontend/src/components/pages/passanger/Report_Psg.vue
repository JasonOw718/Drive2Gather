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

    <!-- Main Label -->
    <div class="text-2xl font-medium text-left mb-4 mt-16 text-left" style="font-family: 'Roboto', sans-serif; color: #C77DFF;">Report an Issue with Your Ride</div>

    <!-- Driver Information Section -->
    <div class="mb-4">
      <div class="text-base font-semibold mb-1 text-left " style="font-family: 'Poppins', sans-serif; color: #8C8C8C;">Driver Information</div><hr>
      <div class="mb-3">
        <label class="block text-base font-semibold mt-2 mb-1 text-left" style="font-family: 'Poppins', sans-serif; color: #333333;">Driver Name</label>
        <input type="text" :value="ride.driverName" disabled class="w-full border border-gray-200 bg-[#F5F5F5] px-4 py-3 rounded-lg text-base font-semibold text-[#333333]" style="font-family: 'Poppins', sans-serif;" />
      </div>
      <div class="mb-3">
        <label class="block text-base font-semibold mb-1 text-left" style="font-family: 'Poppins', sans-serif; color: #333333;">Car Plate Number</label>
        <input type="text" :value="ride.carPlate" disabled class="w-full border border-gray-200 bg-[#F5F5F5] px-4 py-3 rounded-lg text-base font-semibold text-[#333333]" style="font-family: 'Poppins', sans-serif;" />
      </div>
      <div class="mb-3">
        <label class="block text-base font-semibold mb-1 text-left" style="font-family: 'Poppins', sans-serif; color: #333333;">Car Model</label>
        <input type="text" :value="ride.driverCarType" disabled class="w-full border border-gray-200 bg-[#F5F5F5] px-4 py-3 rounded-lg text-base font-semibold text-[#333333]" style="font-family: 'Poppins', sans-serif;" />
      </div>
    </div>
    <hr class="my-2">

    <!-- Issue Type Section -->
    <div class="mb-6">
  <label class="block text-base font-semibold mt-2 mb-2 text-left" 
         style="font-family: 'Poppins', sans-serif; color: #333333;">
    Issue Type
    </label>
    <div class="relative w-full">
        <select v-model="issueType" 
                class="w-full max-w-full border border-gray-200 bg-white px-3 py-3 rounded-md text-base font-semibold text-[#333333] focus:outline-none focus:ring-2 focus:ring-[#C77DFF] custom-select overflow-x-auto" 
                style="font-family: 'Poppins', sans-serif;">
        <option value="" disabled selected>Select an issue</option>
        <option v-for="option in issueOptions" :key="option" :value="option" class="custom-option">{{ option }}</option>
        </select>
    </div>
    </div>

    <!-- Issue Description Section -->
    <div class="mb-8">
      <label class="block text-base font-semibold mb-2 text-left" style="font-family: 'Poppins', sans-serif; color: #333333;">Please describe the Issue (optional)</label>
      <textarea v-model="description" rows="4" placeholder="Text area..." class="w-full border border-gray-200 bg-white px-4 py-3 rounded-lg text-base font-semibold text-[#333333] focus:outline-none focus:ring-2 focus:ring-[#C77DFF] resize-none" style="font-family: 'Poppins', sans-serif;"></textarea>
    </div>

    <div class="flex-1"></div>

    <!-- Submit Button -->
    <button
      class="w-full py-3 px-4 rounded-full shadow-md text-base font-bold transition-all duration-300 mb-2 bg-[#C77DFF] text-white hover:bg-opacity-90 cursor-pointer"
      :disabled="!issueType"
      :class="{ 'bg-gray-300 text-gray-400 cursor-not-allowed': !issueType }"
      style="max-width: 100%; font-family: 'Roboto', sans-serif;"
      @click="onSubmit"
    >
      Submit
    </button>

    <!-- Success Message Overlay -->
    <div v-if="showSuccess" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-40">
      <div class="bg-[#C77DFF] text-white rounded-2xl px-6 py-4 shadow-lg text-center text-lg font-semibold">
        Report Submitted Successfully!
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { rideList } from '../../../stores/rideList.js'

const router = useRouter()
const ride = rideList[0] // For demo, use the first ride

const issueType = ref('')
const description = ref('')
const showSuccess = ref(false)

const issueOptions = [
  'Rude Behavior',
  'Dangerous Driving',
  'Unclean Vehicle',
  'Late or Unpunctual',
  'Sexual Harassment or Inappropriate Comments',
  'Asked for Extra Payment',
  'Smoking or Drinking During Ride',
  'Other (please specify)'
]

function onSubmit() {
  if (!issueType.value) return
  // Store the report data (for demo, just log it)
  const report = {
    driverName: ride.driverName,
    carPlate: ride.carPlate,
    carModel: ride.driverCarType,
    issueType: issueType.value,
    description: description.value
  }
  // You can push this to a store or send to backend here
  console.log('Report submitted:', report)
  showSuccess.value = true
  setTimeout(() => {
    showSuccess.value = false
    router.push({ name: 'Otwpage' })
  }, 1200)
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&family=Poppins:wght@400;500&display=swap');

.custom-select {
  max-width: 100vw;
  width: 100%;
  box-sizing: border-box;
}

.custom-option {
  white-space: normal !important; /* Try to allow wrapping, but may not work on all browsers */
  word-break: break-word;
  overflow-wrap: break-word;
}

</style>

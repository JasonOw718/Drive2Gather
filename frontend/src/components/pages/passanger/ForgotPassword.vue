<template>
  <div class="min-h-screen pt-10 px-6 bg-white flex flex-col justify-between relative" style="padding-top: max(2.5rem, env(safe-area-inset-top));">
    <!-- Back Button -->
    <button
      class="absolute top-4 left-4 w-10 h-10 flex items-center justify-center rounded-full bg-[#F5F5F5] z-20"
      @click="$router.back()"
      aria-label="Back"
    >
      <font-awesome-icon :icon="'fa-arrow-left'" class="text-[#C77DFF] w-5 h-5" />
    </button>

    <!-- Form Section -->
    <form class="flex flex-col pt-10 flex-1" @submit.prevent="onSubmit">
      <!-- Title -->
      <div class="block font-medium text-left text-2xl text-gray-900 mt-20 mb-6">Forgot Password?</div>
      <!-- Email Input -->
      <div class="mb-2">
        <label for="email" class="block text-sm font-semibold text-gray-800 mb-1">Email</label>
        <input
          id="email"
          v-model="email"
          type="email"
          placeholder="Email"
          class="w-full border border-gray-200 bg-white px-4 py-3 focus:outline-none focus:ring-2 focus:ring-[#C77DFF] text-base rounded-lg text-black"
        />
        <p v-if="emailError" class="text-red-500 text-sm mt-1">{{ emailError }}</p>
      </div>
      <!-- Send Email Button -->
      <button
        type="submit"
        class="mt-6 px-6 w-11/12 max-w-md mx-auto py-3 rounded-full shadow-md bg-[#C77DFF] text-white text-base font-bold hover:bg-opacity-90 transition-all duration-300"
      >
        Send Email
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const email = ref('')
const emailError = ref('')

function validateEmail(val) {
  // Must be a valid email
  return /.+@.+\.[a-zA-Z]{2,}$/.test(val)
}
function onSubmit() {
  emailError.value = ''
  if (!validateEmail(email.value)) {
    emailError.value = 'Please enter a valid email.'
    return
  }
  // Handle send email logic here
  alert('Password reset email sent!')
}
</script>

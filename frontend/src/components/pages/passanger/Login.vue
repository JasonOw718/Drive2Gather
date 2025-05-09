<template>
  <div class="min-h-screen pt-10 px-6 bg-white flex flex-col justify-between relative" style="padding-top: max(2.5rem, env(safe-area-inset-top));">
    <!-- Back Button -->
    <button
      class="absolute top-4 left-4 w-10 h-10 flex items-center justify-center rounded-lg bg-[#F5F5F5] z-20 border border-gray-200"
      @click="$router.back()"
      aria-label="Back"
    >
      <span class="w-6 h-6 text-primary">
        <!-- Arrow-left SVG -->
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512" :fill="'#C77DFF'">
          <path d="M9.4 233.4c-12.5 12.5-12.5 32.8 0 45.3l160 160c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L109.2 288 416 288c17.7 0 32-14.3 32-32s-14.3-32-32-32l-306.7 0L214.6 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0l-160 160z"/>
        </svg>
      </span>
    </button>

    <!-- Form Section -->
    <form class="flex flex-col pt-10 pb-32 flex-1" @submit.prevent="onSubmit">
      <!-- Label above email input -->
      <div class="block font-medium text-left text-2xl text-gray-900 mt-12 mb-6">Your email and password</div>
      <!-- Email Input -->
      <div class="mb-4">
        <input
          id="email"
          v-model="email"
          type="email"
          placeholder="Email"
          class="w-full border border-gray-200 bg-white px-4 py-3 focus:outline-none focus:ring-2 focus:ring-[#C77DFF] text-base rounded-lg text-black"
        />
        <p v-if="emailError" class="text-red-500 text-sm mt-1">{{ emailError }}</p>
      </div>
      <!-- Password Input -->
      <div class="mb-2">
        <div class="flex items-center w-full bg-white border border-gray-200 rounded-lg focus-within:ring-2 focus-within:ring-[#C77DFF]">
          <input
            id="password"
            :type="showPassword ? 'text' : 'password'"
            v-model="password"
            placeholder="Password"
            class="flex-1 min-w-0 bg-transparent px-4 py-3 text-base text-black focus:outline-none rounded-lg"
          />
          <button
            type="button"
            class="shrink-0 ml-[-2.5rem] mr-3 h-full flex items-center justify-center bg-transparent border-none focus:outline-none"
            @click="showPassword = !showPassword"
            tabindex="-1"
            aria-label="Toggle password visibility"
          >
            <font-awesome-icon :icon="showPassword ? 'fa-eye-slash' : 'fa-eye'" class="text-[#C77DFF] w-5 h-5" />
          </button>
        </div>
        <p v-if="passwordError" class="text-red-500 text-sm mt-1">{{ passwordError }}</p>
      </div>

      <!-- Forgot Password Link -->
      <router-link
        to="/forgot-password"
        class="inline p-0 m-0 leading-none"
      >
        <span class="text-[#C77DFF] text-sm font-medium underline hover:opacity-80">
          Forgot password?
        </span>
      </router-link>

    </form>

    <!-- Fixed Log In Button -->

    <div class="w-full pb-10 fixed bottom-0 left-0 flex flex-col items-center px-5">
      <button
        class="w-full max-w-md py-3 px-4 rounded-full shadow-md bg-[#C77DFF] text-white text-base font-bold hover:bg-opacity-90 transition-all duration-300"
        @click="onSubmit"
      >
        Log In
      </button>
    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const email = ref('')
const password = ref('')
const showPassword = ref(false)
const emailError = ref('')
const passwordError = ref('')

function validateEmail(val) {
  // Must contain @ and end with domain.com
  return /.+@.+\.[a-zA-Z]{2,}$/.test(val) && val.includes('@domain.com')
}
function validatePassword(val) {
  // At least 8 chars, includes letters and numbers
  return /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/.test(val)
}
function onSubmit() {
  emailError.value = ''
  passwordError.value = ''
  let valid = true
  if (!validateEmail(email.value)) {
    emailError.value = 'Please enter a valid @domain.com email.'
    valid = false
  }
  if (!validatePassword(password.value)) {
    passwordError.value = 'Password must be at least 8 characters and include letters and numbers.'
    valid = false
  }
  if (valid) {
    // Handle login logic here
    // router.push('/dashboard')
    alert('Login successful!')
  }
}
</script>

<template>
  <div class="min-h-screen pt-[max(2.5rem,env(safe-area-inset-top))] pb-[max(env(safe-area-inset-bottom),2.5rem)] px-6 bg-white flex flex-col justify-between relative" style="max-width:375px;margin:0 auto;">
    <!-- Back Button -->
    <button
      class="absolute top-4 left-4 w-10 h-10 flex items-center justify-center rounded-lg bg-[#F5F5F5] z-20 border border-gray-200"
      @click="$router.back()"
      aria-label="Back"
    >
      <span class="w-5 h-5 text-primary">
        <font-awesome-icon icon="fa-arrow-left" class="text-[#C77DFF] w-5 h-5" />
      </span>
    </button>
    <!-- Title -->
    <div class="block font-medium text-left text-[24px] text-gray-900 mt-10">Log in</div>
    
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

      <!-- Auth Error Message -->
      <p v-if="userStore.authError" class="text-red-500 text-sm mt-2">{{ userStore.authError }}</p>

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
        :disabled="isLoading"
      >
        {{ isLoading ? 'Logging in...' : 'Log In' }}
      </button>
    </div>

    <!-- Approval Pending Modal -->
    <div v-if="showPendingModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center px-4 z-50">
      <div class="bg-white rounded-lg shadow-lg p-6 max-w-sm w-full">
        <h3 class="text-xl font-bold text-[#C77DFF] mb-4">Account Approval Pending</h3>
        <p class="mb-6 text-gray-800">Your driver account is still under review. Please wait for admin approval before logging in.</p>
        <button 
          @click="showPendingModal = false"
          class="w-full py-3 px-4 rounded-full shadow-md bg-[#C77DFF] text-white text-base font-bold hover:bg-opacity-90 transition-all duration-300"
        >
          Okay
        </button>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '../../../stores/user'
import { useRoute, useRouter } from 'vue-router'

const userStore = useUserStore()
const route = useRoute()
const router = useRouter()
const email = ref('')
const password = ref('')
const showPassword = ref(false)
const emailError = ref('')
const passwordError = ref('')
const isLoading = ref(false)
const showPendingModal = ref(false)

function validateEmail(val) {
  return /.+@.+\.[a-zA-Z]{2,}$/.test(val)
}

async function onSubmit() {
  emailError.value = ''
  passwordError.value = ''
  let valid = true

  if (!email.value) {
    emailError.value = 'Email is required.'
    valid = false
  } else if (!validateEmail(email.value)) {
    emailError.value = 'Please enter a valid email.'
    valid = false
  }

  if (!password.value) {
    passwordError.value = 'Password is required.'
    valid = false
  }

  if (valid) {
    isLoading.value = true
    try {
      const result = await userStore.login(email.value, password.value)
      
      if (result) {
        // Check if there's a redirect path in query params
        const redirectPath = route.query.redirect
        if (redirectPath) {
          router.push(redirectPath)
        } else {
          router.push('/')
        }
      }
      // Check if the error contains "pending" or "review" which would indicate a driver approval issue
      else if (userStore.authError && 
          (userStore.authError.toLowerCase().includes('pending') || 
           userStore.authError.toLowerCase().includes('review'))) {
        showPendingModal.value = true
      }
    } finally {
      isLoading.value = false
    }
  }
}
</script>

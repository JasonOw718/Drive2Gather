<template>
  <div class="min-h-screen bg-white px-6 py-6 flex flex-col" style="max-width: 420px; margin: 0 auto;">
    <!-- Back Button -->
    <button
      class="absolute top-4 left-4 w-10 h-10 flex items-center justify-center rounded-lg bg-[#F5F5F5] z-20 border border-gray-200"
      @click="$router.back()"
      aria-label="Back"
    >
      <span class="w-5 h-5 text-primary">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512" :fill="'#C77DFF'" class="w-5 h-5">
          <path d="M9.4 233.4c-12.5 12.5-12.5 32.8 0 45.3l160 160c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L109.2 288 416 288c17.7 0 32-14.3 32-32s-14.3-32-32-32l-306.7 0L214.6 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0l-160 160z"/>
        </svg>
      </span>
    </button>

    <!-- Main Label -->
    <div class="text-2xl font-bold text-left mb-8 text-[#5D7285] mt-14">Change Password</div>

    <!-- Input Fields -->
    <form class="flex flex-col gap-6" @submit.prevent="onSubmit">
      <div>
        <label class="block text-[18px] font-semibold text-gray-800 mb-1 text-left">Old Password</label>
        <input
          type="password"
          v-model="oldPassword"
          placeholder="Enter your old password"
          class="w-full border border-gray-200 bg-[#F5F5F5] px-4 py-3 text-base rounded-sm text-black focus:outline-none focus:ring-2 focus:ring-[#C77DFF]"
        />
        <p v-if="oldPasswordError" class="text-red-500 text-sm mt-1">{{ oldPasswordError }}</p>
      </div>
      <div>
        <label class="block text-[18px] font-semibold text-gray-800 mb-1 text-left">New Password</label>
        <input
          type="password"
          v-model="newPassword"
          placeholder="Enter your new password"
          class="w-full border border-gray-200 bg-[#F5F5F5] px-4 py-3 text-base rounded-sm text-black focus:outline-none focus:ring-2 focus:ring-[#C77DFF]"
        />
        <p v-if="newPasswordError" class="text-red-500 text-sm mt-1">{{ newPasswordError }}</p>
      </div>
      <div>
        <label class="block text-[18px] font-semibold text-gray-800 mb-1 text-left">Confirm New Password</label>
        <input
          type="password"
          v-model="confirmPassword"
          placeholder="Confirm your new password"
          class="w-full border border-gray-200 bg-[#F5F5F5] px-4 py-3 text-base rounded-sm text-black focus:outline-none focus:ring-2 focus:ring-[#C77DFF]"
        />
        <p v-if="confirmPasswordError" class="text-red-500 text-sm mt-1">{{ confirmPasswordError }}</p>
      </div>
      <button 
        type="submit" 
        class="w-full py-3 px-4 rounded-full shadow-md bg-[#C77DFF] text-white text-base font-bold hover:bg-opacity-90 transition-all duration-300 mt-2"
        :disabled="isSubmitting"
      >
        {{ isSubmitting ? 'Changing Password...' : 'Change Password' }}
      </button>
    </form>

    <!-- Error message -->
    <p v-if="generalError" class="text-red-500 text-sm mt-4 text-center">{{ generalError }}</p>

    <!-- Success Overlay -->
    <div v-if="showSuccess" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-40">
      <div class="bg-[#C77DFF] text-white rounded-2xl px-6 py-2 shadow-lg text-center text-lg font-semibold">
        Password Changed Successfully
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '../../../stores/user'
import { useRouter } from 'vue-router'

const userStore = useUserStore()
const router = useRouter()

const oldPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const oldPasswordError = ref('')
const newPasswordError = ref('')
const confirmPasswordError = ref('')
const generalError = ref('')
const showSuccess = ref(false)
const isSubmitting = ref(false)

async function onSubmit() {
  // Reset errors
  oldPasswordError.value = ''
  newPasswordError.value = ''
  confirmPasswordError.value = ''
  generalError.value = ''
  
  // Validate inputs
  let valid = true
  
  if (!oldPassword.value) {
    oldPasswordError.value = 'Old password is required.'
    valid = false
  }
  
  if (!newPassword.value) {
    newPasswordError.value = 'New password is required.'
    valid = false
  } else if (newPassword.value.length < 8) {
    newPasswordError.value = 'New password must be at least 8 characters.'
    valid = false
  }
  
  if (newPassword.value !== confirmPassword.value) {
    confirmPasswordError.value = 'Passwords do not match.'
    valid = false
  }
  
  if (!valid) return
  
  // Submit to API
  isSubmitting.value = true
  
  try {
    const result = await userStore.changePassword(oldPassword.value, newPassword.value)
    
    if (result.success) {
      // Show success message
      showSuccess.value = true
      
      // Reset form
      oldPassword.value = ''
      newPassword.value = ''
      confirmPassword.value = ''
      
      // Navigate back after delay
      setTimeout(() => {
        showSuccess.value = false
        router.back()
      }, 1500)
    } else {
      // Show error
      generalError.value = result.error || 'Failed to change password. Please try again.'
      
      // If it's specifically an old password issue, show it in the right field
      if (result.error && result.error.toLowerCase().includes('current password is incorrect')) {
        oldPasswordError.value = 'Current password is incorrect.'
        generalError.value = ''
      }
    }
  } catch (error) {
    console.error('Error changing password:', error)
    generalError.value = 'An unexpected error occurred. Please try again.'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8 bg-white p-8 rounded-xl shadow-lg">
      <div>
        <img src="@/assets/images/Logo.png" alt="Logo" class="mx-auto h-16">
        <h2 class="mt-6 text-center text-3xl font-bold text-[#C77DFF]">{{ isLoginMode ? 'Login' : 'Sign Up as Donor' }}</h2>
        <p class="mt-2 text-center text-gray-600">
          {{ isLoginMode 
              ? 'Sign in as an admin or donor to access your dashboard' 
              : 'Create a donor account to support Ride2Gather' 
          }}
        </p>
        
        <!-- Toggle between admin and donor login -->
        <div v-if="isLoginMode" class="mt-4 flex justify-center">
          <div class="bg-gray-200 rounded-lg p-1 inline-flex">
            <button 
              @click="userType = 'admin'" 
              :class="[
                'px-4 py-2 rounded-md text-sm font-medium transition-colors',
                userType === 'admin' ? 'bg-[#C77DFF] text-white' : 'text-gray-700'
              ]"
            >
              Admin
            </button>
            <button 
              @click="userType = 'donor'" 
              :class="[
                'px-4 py-2 rounded-md text-sm font-medium transition-colors',
                userType === 'donor' ? 'bg-[#C77DFF] text-white' : 'text-gray-700'
              ]"
            >
              Donor
            </button>
          </div>
        </div>
      </div>
      
      <form class="mt-8 space-y-6" @submit.prevent="onSubmit">
        <!-- Name field (only for donor signup) -->
        <div v-if="!isLoginMode" class="rounded-md shadow-sm -space-y-px">
          <div>
            <label for="name" class="sr-only">Full Name</label>
            <input 
              id="name" 
              name="name" 
              type="text" 
              v-model="name"
              required 
              class="appearance-none rounded-md relative block w-full px-4 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-[#C77DFF] focus:border-[#C77DFF] focus:z-10 bg-gray-50 mb-3" 
              placeholder="Full Name"
            >
          </div>
        </div>
      
        <div class="rounded-md shadow-sm -space-y-px">
          <div>
            <label for="email" class="sr-only">Email address</label>
            <input 
              id="email" 
              name="email" 
              type="email" 
              autocomplete="email" 
              v-model="email"
              required 
              class="appearance-none rounded-t-md relative block w-full px-4 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-[#C77DFF] focus:border-[#C77DFF] focus:z-10 bg-gray-50" 
              placeholder="Email address"
            >
          </div>
          <div>
            <label for="password" class="sr-only">Password</label>
            <input 
              id="password" 
              name="password" 
              :type="showPassword ? 'text' : 'password'" 
              autocomplete="current-password" 
              v-model="password"
              required 
              class="appearance-none rounded-b-md relative block w-full px-4 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-[#C77DFF] focus:border-[#C77DFF] focus:z-10 bg-gray-50" 
              placeholder="Password"
            >
          </div>
        </div>

        <!-- Phone field (only for donor signup) -->
        <div v-if="!isLoginMode" class="rounded-md shadow-sm">
          <div>
            <label for="phone" class="sr-only">Phone Number</label>
            <input 
              id="phone" 
              name="phone" 
              type="tel" 
              v-model="phone"
              required 
              class="appearance-none rounded-md relative block w-full px-4 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-[#C77DFF] focus:border-[#C77DFF] focus:z-10 bg-gray-50" 
              placeholder="Phone Number"
            >
          </div>
        </div>

        <div class="flex items-center">
          <div class="flex items-center">
            <input 
              id="show-password" 
              name="show-password" 
              type="checkbox" 
              v-model="showPassword"
              class="h-4 w-4 text-[#C77DFF] focus:ring-[#C77DFF] border-gray-300 rounded"
            >
            <label for="show-password" class="ml-2 block text-sm text-gray-900">
              Show password
            </label>
          </div>
        </div>

        <div>
          <button 
            type="submit" 
            class="group relative w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-[#C77DFF] hover:bg-[#a259e6] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#C77DFF] disabled:opacity-70 disabled:cursor-not-allowed"
            :disabled="isLoading"
          >
            <span v-if="isLoading" class="absolute left-0 inset-y-0 flex items-center pl-3">
              <!-- Loading spinner -->
              <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            </span>
            {{ isLoading ? 'Processing...' : (isLoginMode ? 'Sign In' : 'Sign Up') }}
          </button>
        </div>
        
        <!-- Demo Admin Login -->
        <div v-if="isLoginMode && userType === 'admin'" class="text-center mt-4">
          <button 
            type="button"
            @click="useDemoAdmin"
            class="text-sm text-[#C77DFF] hover:underline"
          >
            Use Demo Admin
          </button>
        </div>
        
        <!-- Toggle between login/signup -->
        <div class="text-center mt-4">
          <button 
            type="button"
            @click="toggleMode"
            class="text-sm text-[#C77DFF] hover:underline"
          >
            {{ isLoginMode ? 'New donor? Sign up here' : 'Already have an account? Sign in' }}
          </button>
        </div>
      </form>

      <!-- Error Message -->
      <div v-if="error" class="mt-4 bg-red-50 border border-red-200 text-red-600 rounded-md p-4 text-sm">
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAdminAuthStore } from '../../../stores/adminAuth';
import { useDonorAuthStore } from '../../../stores/donorAuth';
import { useToastStore } from '../../../stores/toast';

const router = useRouter();
const adminAuthStore = useAdminAuthStore();
const donorAuthStore = useDonorAuthStore();
const toastStore = useToastStore();

// For login/signup fields
const email = ref('');
const password = ref('');
const name = ref('');
const phone = ref('');
const showPassword = ref(false);

// UI state
const isLoading = ref(false);
const error = ref('');
const isLoginMode = ref(true);
const userType = ref('admin'); // 'admin' or 'donor'

function toggleMode() {
  isLoginMode.value = !isLoginMode.value;
  error.value = '';
  if (!isLoginMode.value) {
    userType.value = 'donor'; // Sign up is only for donors
  }
}

async function onSubmit() {
  // Validate inputs
  if (isLoginMode.value) {
    if (!email.value || !password.value) {
      error.value = 'Please enter both email and password';
      return;
    }
  } else {
    if (!name.value || !email.value || !password.value || !phone.value) {
      error.value = 'Please fill in all fields';
      return;
    }
  }
  
  isLoading.value = true;
  error.value = '';
  
  try {
    if (isLoginMode.value) {
      // Handle login for admin or donor
      if (userType.value === 'admin') {
        const success = await adminAuthStore.adminLogin(email.value, password.value);
        
        if (success) {
          // Check if there's a redirect query param
          const redirectFrom = router.currentRoute.value.query.redirectFrom;
          if (redirectFrom === 'admin') {
            // Redirect to admin dashboard or the specific page they were trying to access
            router.push('/portal/admin/account-management');
          } else {
            router.push('/portal/admin/account-management');
          }
        } else {
          error.value = adminAuthStore.authError || 'Login failed';
        }
      } else {
        // Donor login
        const success = await donorAuthStore.donorLogin(email.value, password.value);
        
        if (success) {
          // Check if there's a redirect query param
          const redirectFrom = router.currentRoute.value.query.redirectFrom;
          if (redirectFrom === 'donor') {
            // Redirect to donor dashboard or the specific page they were trying to access
            router.push('/portal/donor/dashboard');
          } else {
            router.push('/portal/donor/dashboard');
          }
        } else {
          error.value = donorAuthStore.authError || 'Login failed';
        }
      }
    } else {
      // Handle donor signup
      const userData = {
        name: name.value,
        email: email.value,
        password: password.value,
        phone: phone.value
      };
      
      const success = await donorAuthStore.donorRegister(userData);
      
      if (success) {
        // Redirect to donor dashboard
        router.push('/portal/donor/dashboard');
      } else {
        error.value = donorAuthStore.authError || 'Registration failed';
      }
    }
  } catch (err) {
    console.error('Authentication failed:', err);
    error.value = 'Authentication failed. Please try again.';
  } finally {
    isLoading.value = false;
  }
}

function useDemoAdmin() {
  // Hardcoded admin credentials - Use for development only!
  email.value = 'admin@ride2gather.com';
  password.value = 'admin123';
  
  // Auto-submit after a short delay
  setTimeout(() => {
    onSubmit();
  }, 100);
}
</script> 
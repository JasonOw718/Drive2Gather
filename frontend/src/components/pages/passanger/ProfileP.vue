<template> 
    <RightNavbar />
      <div class="min-h-screen bg-white px-6 py-6 flex flex-col" style="max-width: 420px; margin: 0 auto;">
       
        <!-- Header -->
        <div class="text-2xl font-bold text-left mb-8 text-[#000000]">Profile</div>
        <!-- User Info Section -->
        <div class="flex flex-col gap-5 mb-10">
          <div>
            <label class="block text-[18px] font-semibold text-gray-800 mb-1 text-left">Username</label>
            <input type="text" :value="user.username" disabled class="w-full border border-gray-200 bg-[#F5F5F5] px-4 py-3 text-base rounded-lg text-[#9D9FA0] focus:outline-none" />
          </div>
          <div>
            <label class="block text-[18px] font-semibold text-gray-800 mb-1 text-left">Email</label>
            <input type="email" :value="user.email" disabled class="w-full border border-gray-200 bg-[#F5F5F5] px-4 py-3 text-base rounded-lg text-[#9D9FA0] focus:outline-none" />
          </div>
          <div>
            <label class="block text-[18px] font-semibold text-gray-800 mb-1 text-left">Phone Number</label>
            <input type="tel" :value="user.phone" disabled class="w-full border border-gray-200 bg-[#F5F5F5] px-4 py-3 text-base rounded-lg text-[#9D9FA0] focus:outline-none" />
          </div>
        </div>
    
        <!-- Change Password Link -->
        <router-link to="/change-password" class="text-[#C77DFF] text-base font-semibold underline hover:opacity-80 transition self-start">Change Password?</router-link>
      </div>
    </template>
    
    <script setup>
    import { ref } from 'vue'
    import { useUserStore } from '../../../stores/user'
    import RightNavbar from '../rightnavbar.vue'
    const userStore = useUserStore()
    const user = userStore.currentUser
    const showQR = ref(false)
    </script>
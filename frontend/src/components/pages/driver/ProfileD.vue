<template> 
<RightNavbar />
  <div class="min-h-screen bg-white px-6 py-6 flex flex-col" style="max-width: 420px; margin: 0 auto;">
   
    <!-- Header -->
    <div class="text-2xl font-bold text-left mb-8 text-[#5D7285]">Profile</div>

    <!-- Donation Card/Button -->
    <button @click="showQR = true" class="w-40 h-32  rounded-1xl border-[#D2B7E5] mb-8 flex flex-col justify-between items-start relative text-left hover:bg-[#f0eaff] transition p-4">
      <!-- <button @click="goToDonation" class="w-40 h-32  rounded-1xl border-[#D2B7E5] mb-8 flex flex-col justify-between items-start relative text-left hover:bg-[#f0eaff] transition p-4"> -->

      <span class="text-base font-semibold text-[#000000]">Donation</span>
      <span class="absolute bottom-4 right-4 pl-6 text-xl font-bold text-[#C77DFF] text-[18px] whitespace-nowrap">RM 123.00</span>
    </button>

    <!-- QR Code Modal -->
    <div v-if="showQR" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-40">
      <div class="bg-white rounded-2xl p-6 shadow-lg flex flex-col items-center relative w-80">
        <img :src="user.qrCode" alt="Donation QR Code" class="w-68 h-68 object-contain mb-4" />
        <button @click="showQR = false" class="absolute top-2 right-2 text-[#C77DFF] text-2xl font-bold">&times;</button>
        <div class="text-[#5D7285] font-semibold mt-2">Scan to Donate</div>
      </div>
    </div>

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
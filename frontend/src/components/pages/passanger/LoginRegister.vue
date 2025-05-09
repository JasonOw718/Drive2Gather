<template>
  <div class="min-h-screen flex flex-col bg-white relative">
    <!-- Logo at 20-25% from top -->
    <div class="flex flex-col items-center" style="margin-top: 24vh;">
      <img src="/src/assets/images/Logo.png" alt="Logo" class="object-contain mb-8" />
    </div>
    <!-- Spacer to push footer down -->
    <div class="flex-1"></div>
    <!-- Fixed Footer -->
    <div class="w-full px-6 pb-10 fixed bottom-0 flex flex-col items-center gap-5">
      <span class="text-lg font-semibold text-[#C77DFF] mb-[30px]">Your ride, Your Choice</span>
      <router-link to="/register-passenger" class="w-full py-3 px-4 rounded-full shadow-md bg-[#C77DFF] text-white text-base font-bold hover:bg-opacity-90 transition-all duration-300">Sign Up</router-link>
      <router-link to="/login" class="w-full py-3 px-4 rounded-full text-[#C77DFF] text-base font-bold hover:bg-opacity-90 transition-all duration-300 text-center">Log in</router-link>
      <router-link to="/register-driver" class="w-full py-3 px-4 rounded-full shadow-md bg-[#E0AAFF] text-white text-base font-bold hover:bg-opacity-90 transition-all duration-300">Sign Up as Driver</router-link>
    </div>
  </div>
</template>

<script setup>
// No logic yet, purely presentational
</script>

<template>
  <div>
    <!-- Header -->
    <header class="flex items-center justify-between px-4 pt-safe-top pb-2 bg-white shadow-sm z-30 relative min-h-[48px]">
      <!-- Centered label absolutely -->
      <span class="absolute left-1/2 top-1/2 transform -translate-x-1/2 -translate-y-1/2 font-semibold text-lg md:text-xl text-[#5D7285] pointer-events-none select-none w-max" style="font-family: 'Roboto', sans-serif;">Ride2Gather</span>
      <!-- Right-aligned menu icon -->
      <button @click="openMenu" aria-label="Open menu" class="p-2 ml-auto">
        <font-awesome-icon icon="fa-solid fa-bars" class="text-xl text-[#5D7285]" />
      </button>
    </header>

    <!-- Overlay Menu -->
    <transition name="slide-right-navbar">
      <div v-if="menuOpen" class="fixed inset-0 z-40">
        <!-- Overlay background -->
        <div class="absolute inset-0 bg-black bg-opacity-30" @click="closeMenu"></div>
        <!-- Menu panel -->
        <nav class="absolute top-0 right-0 h-full w-64 bg-white shadow-lg flex flex-col py-8 px-6 animate-slide-in" @click.stop>
          <!-- User Avatar -->
          <img
            :src="userStore.currentUser.avatar"
            alt="User Avatar"
            class="w-12 h-12 rounded-full object-cover mb-10 ml-2"
          />
          <!-- Menu Items -->
          <router-link to="/" class="mb-6 text-lg font-medium flex items-center gap-2 text-[#5D7285]" @click="closeMenu">
            <font-awesome-icon icon="fa-home" class="text-[#5D7285]" /> Home
          </router-link>
          <router-link v-if="userRole === 'passenger'" to="/find-ride" class="mb-6 text-lg font-medium flex items-center gap-2 text-[#5D7285]" @click="closeMenu">
            <font-awesome-icon icon="fa-search" class="text-[#5D7285]" /> Search Ride
          </router-link>
          <router-link v-if="userRole === 'driver'" to="/create-ride" class="mb-6 text-lg font-medium flex items-center gap-2 text-[#5D7285]" @click="closeMenu">
            <font-awesome-icon icon="fa-plus-circle" class="text-[#5D7285]" /> Publish a ride
          </router-link>
          <router-link to="/profile" class="mb-6 text-lg font-medium flex items-center gap-2 text-[#5D7285]" @click="closeMenu">
            <font-awesome-icon icon="fa-user-circle" class="text-[#5D7285]" /> Account
          </router-link>
          <button v-if="isAuthenticated" @click="logout" class="mt-auto text-lg font-medium flex items-center gap-2 text-[#5D7285]">
            <font-awesome-icon icon="fa-sign-out-alt" /> Logout
          </button>
        </nav>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../../stores/user'

const menuOpen = ref(false)
const router = useRouter()
const userStore = useUserStore()

const userRole = computed(() => userStore.currentUser?.role)
const isAuthenticated = computed(() => userStore.isAuthenticated)

function openMenu() {
  menuOpen.value = true
}
function closeMenu() {
  menuOpen.value = false
}
function logout() {
  userStore.logout()
  closeMenu()
  router.push('/login-register')
}
</script>

<style scoped>
.pt-safe-top {
  padding-top: max(1rem, env(safe-area-inset-top));
}
.slide-right-navbar-enter-active,
.slide-right-navbar-leave-active {
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.slide-right-navbar-enter-from,
.slide-right-navbar-leave-to {
  transform: translateX(100%);
}
.slide-right-navbar-enter-to,
.slide-right-navbar-leave-from {
  transform: translateX(0);
}
.animate-slide-in {
  animation: slideInRight 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
@keyframes slideInRight {
  from { transform: translateX(100%); }
  to { transform: translateX(0); }
}
</style>

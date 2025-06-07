<template>
  <div>
    <RightNavbar />
    <div class="min-h-screen bg-white px-6 py-6 flex flex-col" style="max-width: 420px; margin: 0 auto;">
      <!-- Welcome Section -->
      <div class="mb-8">
        <h1 class="text-2xl font-bold text-left text-[#303030] mb-2">
          Welcome, {{ userStore.currentUser?.name || 'Rider' }}!
        </h1>
        <p class="text-[#8C8C8C] text-left">
          {{ welcomeMessage }}
        </p>
      </div>

      <!-- Activity Stats -->
      <div class="grid grid-cols-2 gap-4 mb-8">
        <div class="bg-[#F8F0FF] rounded-xl p-4 flex flex-col items-start">
          <span class="text-sm text-[#8C8C8C] mb-1">Total Rides</span>
          <span class="text-2xl font-bold text-[#303030]">{{ statistics.totalRides }}</span>
        </div>
        <div class="bg-[#F8F0FF] rounded-xl p-4 flex flex-col items-start">
          <span class="text-sm text-[#8C8C8C] mb-1">{{ userRole === 'driver' ? 'Passengers' : 'Drivers' }}</span>
          <span class="text-2xl font-bold text-[#303030]">{{ statistics.connections }}</span>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="mb-8">
        <h2 class="text-xl font-semibold text-left text-[#303030] mb-4">Quick Actions</h2>
        <div class="grid grid-cols-2 gap-4">
          <button v-if="userRole === 'passenger'" 
                  @click="navigateTo('FindRide')"
                  class="bg-[#C77DFF] text-white rounded-xl p-4 flex flex-col items-start h-32 transition hover:bg-opacity-90">
            <font-awesome-icon icon="fa-search" class="text-xl mb-2" />
            <span class="text-lg font-medium">Find a Ride</span>
            <span class="text-sm mt-1">Search for available rides</span>
          </button>
          <button v-if="userRole === 'driver'" 
                  @click="navigateTo('CreateRide')"
                  class="bg-[#C77DFF] text-white rounded-xl p-4 flex flex-col items-start h-32 transition hover:bg-opacity-90">
            <font-awesome-icon icon="fa-plus-circle" class="text-xl mb-2" />
            <span class="text-lg font-medium">Publish Ride</span>
            <span class="text-sm mt-1">Create a new ride offer</span>
          </button>
          <button @click="navigateTo('Profile')"
                  class="bg-white border border-[#C77DFF] text-[#C77DFF] rounded-xl p-4 flex flex-col items-start h-32 transition hover:bg-[#F8F0FF]">
            <font-awesome-icon icon="fa-user-circle" class="text-xl mb-2" />
            <span class="text-lg font-medium">Profile</span>
            <span class="text-sm mt-1">View and edit your profile</span>
          </button>
        </div>
      </div>

      <!-- Recent Activity -->
      <div>
        <h2 class="text-xl font-semibold text-left text-[#303030] mb-4">Recent Activity</h2>
        <div v-if="recentActivity.length === 0" class="text-center text-[#8C8C8C] py-8">
          No recent activity
        </div>
        <div v-else class="space-y-4">
          <div v-for="(activity, index) in recentActivity" :key="index" 
               class="bg-white border border-gray-200 rounded-xl p-4 flex items-start shadow-sm hover:shadow-md transition">
            <div class="w-10 h-10 rounded-full bg-[#F8F0FF] flex items-center justify-center mr-4 flex-shrink-0">
              <font-awesome-icon :icon="activity.icon" class="text-[#C77DFF]" />
            </div>
            <div class="flex-1">
              <h3 class="text-base font-medium text-[#303030]">{{ activity.title }}</h3>
              <p class="text-sm text-[#8C8C8C] mt-1">{{ activity.description }}</p>
              <p class="text-xs text-[#8C8C8C] mt-2">{{ formatDate(activity.date) }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '../../stores/user';
import RightNavbar from './rightnavbar.vue';

const router = useRouter();
const userStore = useUserStore();

// Initialize auth when component mounts
onMounted(() => {
  if (!userStore.isAuthenticated) {
    userStore.initializeAuth();
  }
});

// Dynamic welcome message based on time of day
const welcomeMessage = computed(() => {
  const hour = new Date().getHours();
  if (hour < 12) return "Good morning! Ready for your commute?";
  if (hour < 18) return "Good afternoon! Need a ride?";
  return "Good evening! Planning a night out?";
});

const userRole = computed(() => userStore.currentUser?.role || 'passenger');

// Mock statistics - would be fetched from backend in a real app
const statistics = ref({
  totalRides: userRole.value === 'driver' ? 47 : 12,
  connections: userRole.value === 'driver' ? 83 : 9
});

// Mock recent activity - would be fetched from backend in a real app
const recentActivity = ref([
  {
    title: 'Ride Completed',
    description: 'Your ride from KL Sentral to KLCC has been completed.',
    date: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000), // 2 days ago
    icon: 'fa-check-circle'
  },
  {
    title: 'New Message',
    description: 'You received a new message from your driver.',
    date: new Date(Date.now() - 4 * 24 * 60 * 60 * 1000), // 4 days ago
    icon: 'fa-comment'
  },
  {
    title: 'Ride Booked',
    description: 'You booked a ride from KLCC to Bangsar.',
    date: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000), // 7 days ago
    icon: 'fa-car'
  }
]);

// Format date for display
function formatDate(date) {
  const now = new Date();
  const diffInDays = Math.floor((now - date) / (1000 * 60 * 60 * 24));
  
  if (diffInDays === 0) {
    return 'Today';
  } else if (diffInDays === 1) {
    return 'Yesterday';
  } else if (diffInDays < 7) {
    return `${diffInDays} days ago`;
  } else {
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  }
}

// Navigate to specified route
function navigateTo(routeName) {
  router.push({ name: routeName });
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
</style> 
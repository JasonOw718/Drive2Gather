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
          <span v-if="loading" class="text-2xl font-bold text-[#303030]">...</span>
          <span v-else class="text-2xl font-bold text-[#303030]">{{ statistics.totalRides }}</span>
        </div>
        <div class="bg-[#F8F0FF] rounded-xl p-4 flex flex-col items-start">
          <span class="text-sm text-[#8C8C8C] mb-1">Pending Requests</span>
          <span v-if="loading" class="text-2xl font-bold text-[#303030]">...</span>
          <span v-else class="text-2xl font-bold text-[#303030]">{{ statistics.pendingRequests }}</span>
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
        <div v-if="loading" class="text-center py-8">
          <font-awesome-icon icon="fa-spinner" spin class="text-[#C77DFF] text-2xl" />
        </div>
        <div v-else-if="recentActivity.length === 0" class="text-center text-[#8C8C8C] py-8">
          No recent activity
        </div>
        <div v-else class="space-y-4">
          <div v-for="activity in recentActivity" :key="activity.id" 
               class="bg-white border border-gray-200 rounded-xl p-4 flex items-start shadow-sm hover:shadow-md transition"
               :class="{'bg-[#F8F0FF] bg-opacity-50': !activity.isRead}">
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
import { rideService } from '../../services/api';

const router = useRouter();
const userStore = useUserStore();
const loading = ref(false);

// Statistics data
const statistics = ref({
  totalRides: 0,
  pendingRequests: 0
});

// Recent activity from notifications
const recentActivity = ref([]);

// Initialize auth and fetch homepage data when component mounts
onMounted(async () => {
  if (!userStore.isAuthenticated) {
    userStore.initializeAuth();
  }
  
  await fetchHomepageData();
});

// Fetch homepage data from API
async function fetchHomepageData() {
  loading.value = true;
  try {
    const response = await rideService.getHomepageData();
    const data = response.data;
    
    // Update statistics
    statistics.value = {
      totalRides: data.total_rides || 0,
      pendingRequests: data.pending_requests || 0
    };
    
    // Convert notifications to activity format
    recentActivity.value = (data.recent_notifications || []).map(notification => {
      let icon = 'fa-bell';
      
      // Determine icon based on notification message content
      if (notification.message.includes('completed')) {
        icon = 'fa-check-circle';
      } else if (notification.message.includes('message')) {
        icon = 'fa-comment';
      } else if (notification.message.includes('ride') || notification.message.includes('trip')) {
        icon = 'fa-car';
      } else if (notification.message.includes('approved')) {
        icon = 'fa-thumbs-up';
      } else if (notification.message.includes('rejected')) {
        icon = 'fa-thumbs-down';
      }
      
      return {
        id: notification.id,
        title: 'Notification',
        description: notification.message,
        date: new Date(notification.created_at),
        icon: icon,
        isRead: notification.is_read
      };
    });
  } catch (error) {
    console.error('Error fetching homepage data:', error);
  } finally {
    loading.value = false;
  }
}

// Dynamic welcome message based on time of day
const welcomeMessage = computed(() => {
  const hour = new Date().getHours();
  if (hour < 12) return "Good morning! Ready for your commute?";
  if (hour < 18) return "Good afternoon! Need a ride?";
  return "Good evening! Planning a night out?";
});

const userRole = computed(() => userStore.currentUser?.role || 'passenger');

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
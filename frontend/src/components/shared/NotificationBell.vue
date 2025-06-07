<template>
  <div class="relative">
    <!-- Notification Bell Icon -->
    <button 
      @click="toggleNotifications" 
      class="relative p-2 rounded-full hover:bg-gray-100 focus:outline-none"
      aria-label="Notifications"
    >
      <svg 
        xmlns="http://www.w3.org/2000/svg" 
        class="h-6 w-6 text-gray-700" 
        fill="none" 
        viewBox="0 0 24 24" 
        stroke="currentColor"
      >
        <path 
          stroke-linecap="round" 
          stroke-linejoin="round" 
          stroke-width="2" 
          d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" 
        />
      </svg>

      <!-- Notification Counter -->
      <span 
        v-if="unreadCount > 0" 
        class="absolute top-0 right-0 inline-flex items-center justify-center px-2 py-1 text-xs font-bold leading-none text-red-100 transform translate-x-1/2 -translate-y-1/2 bg-red-600 rounded-full"
      >
        {{ displayCount }}
      </span>
    </button>

    <!-- Notifications Dropdown -->
    <div 
      v-if="isOpen" 
      class="absolute right-0 mt-2 w-80 bg-white rounded-md shadow-lg overflow-hidden z-50"
      :class="{ 'origin-top-right': true }"
    >
      <div class="py-2">
        <div class="px-4 py-2 text-sm flex justify-between items-center border-b border-gray-100">
          <h3 class="font-semibold text-gray-700">Notifications</h3>
          <button 
            v-if="notifications.length > 0"
            @click="markAllAsRead" 
            class="text-xs text-purple-600 hover:text-purple-800"
          >
            Mark all as read
          </button>
        </div>

        <div v-if="loading" class="px-4 py-6 text-center text-gray-500">
          <svg class="animate-spin mx-auto h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"></path>
          </svg>
          <p class="mt-2 text-sm">Loading notifications...</p>
        </div>

        <div v-else-if="notifications.length === 0" class="px-4 py-6 text-center text-gray-500">
          <svg xmlns="http://www.w3.org/2000/svg" class="mx-auto h-8 w-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
          </svg>
          <p class="mt-2 text-sm">No notifications</p>
        </div>

        <template v-else>
          <div class="max-h-64 overflow-y-auto">
            <div 
              v-for="notification in notifications" 
              :key="notification.id"
              :class="{ 
                'border-l-4 border-purple-500': !notification.read,
                'border-l-4 border-transparent': notification.read
              }"
              class="px-4 py-3 hover:bg-gray-50 flex items-start"
            >
              <!-- Notification Content -->
              <div class="flex-1">
                <p class="text-sm text-gray-700">{{ notification.message }}</p>
                <p class="text-xs text-gray-500 mt-1">{{ formatTime(notification.time) }}</p>
              </div>
              
              <!-- Mark as Read Button (only for unread notifications) -->
              <button 
                v-if="!notification.read"
                @click="markAsRead(notification.id)" 
                class="ml-2 text-xs text-gray-400 hover:text-gray-600"
                aria-label="Mark as read"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
              </button>
            </div>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { notificationService } from '../../services/api';

// State
const notifications = ref([]);
const unreadCount = ref(0);
const isOpen = ref(false);
const loading = ref(false);
const pollingInterval = ref(null);

// Computed properties
const displayCount = computed(() => {
  return unreadCount.value > 99 ? '99+' : unreadCount.value;
});

// Methods
const toggleNotifications = async () => {
  isOpen.value = !isOpen.value;
  
  if (isOpen.value) {
    await fetchNotifications();
  }
};

const fetchNotifications = async () => {
  loading.value = true;
  try {
    const response = await notificationService.getNotifications();
    notifications.value = response.data.notifications;
    unreadCount.value = response.data.unreadCount;
  } catch (error) {
    console.error('Error fetching notifications:', error);
  } finally {
    loading.value = false;
  }
};

const checkUnreadCount = async () => {
  try {
    const response = await notificationService.getNotifications({ 
      unread_only: true,
      page: 1,
      size: 1 
    });
    unreadCount.value = response.data.unreadCount;
  } catch (error) {
    console.error('Error checking unread count:', error);
  }
};

const markAsRead = async (notificationId) => {
  try {
    await notificationService.markAsRead(notificationId);
    // Update the notification in the list
    const index = notifications.value.findIndex(n => n.id === notificationId);
    if (index !== -1) {
      notifications.value[index].read = true;
      unreadCount.value = Math.max(0, unreadCount.value - 1);
    }
  } catch (error) {
    console.error('Error marking notification as read:', error);
  }
};

const markAllAsRead = async () => {
  try {
    await notificationService.markAllAsRead();
    // Update all notifications in the list
    notifications.value.forEach(notification => {
      notification.read = true;
    });
    unreadCount.value = 0;
  } catch (error) {
    console.error('Error marking all notifications as read:', error);
  }
};

const formatTime = (isoString) => {
  const date = new Date(isoString);
  const now = new Date();
  const diffMs = now - date;
  const diffSec = Math.floor(diffMs / 1000);
  const diffMin = Math.floor(diffSec / 60);
  const diffHour = Math.floor(diffMin / 60);
  const diffDay = Math.floor(diffHour / 24);
  
  if (diffSec < 60) {
    return 'Just now';
  } else if (diffMin < 60) {
    return `${diffMin} minute${diffMin !== 1 ? 's' : ''} ago`;
  } else if (diffHour < 24) {
    return `${diffHour} hour${diffHour !== 1 ? 's' : ''} ago`;
  } else if (diffDay < 7) {
    return `${diffDay} day${diffDay !== 1 ? 's' : ''} ago`;
  } else {
    return date.toLocaleDateString();
  }
};

// Handle click outside to close dropdown
const handleClickOutside = (event) => {
  const dropdown = document.querySelector('.notifications-dropdown');
  if (isOpen.value && dropdown && !dropdown.contains(event.target)) {
    isOpen.value = false;
  }
};

// Lifecycle hooks
onMounted(() => {
  // Initial check for unread notifications
  checkUnreadCount();
  
  // Set up polling to check for new notifications (every minute)
  pollingInterval.value = setInterval(checkUnreadCount, 60000);
  
  // Add click outside listener
  document.addEventListener('click', handleClickOutside);
});

onUnmounted(() => {
  // Clear polling interval
  if (pollingInterval.value) {
    clearInterval(pollingInterval.value);
  }
  
  // Remove click outside listener
  document.removeEventListener('click', handleClickOutside);
});
</script>

<style scoped>
/* Add any additional styles here */
.notifications-dropdown {
  transition: all 0.3s ease;
}
</style> 
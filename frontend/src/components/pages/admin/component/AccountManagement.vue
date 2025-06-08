<template>
    <div class="w-full mx-auto mt-10 bg-white rounded-2xl shadow-lg p-8">
      <!-- System Donation Summary -->
      <div class="mb-8 p-6 bg-[#F8F0FF] rounded-xl shadow-sm">
        <h2 class="text-xl font-bold text-[#C77DFF] mb-4 flex items-center">
          <font-awesome-icon icon="fa-solid fa-hand-holding-heart" class="mr-2" />
          System Donation Summary
        </h2>
        
        <div v-if="donationStatsLoading" class="flex justify-center py-4">
          <div class="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-[#C77DFF]"></div>
        </div>
        
        <div v-else-if="donationStatsError" class="text-red-500 text-center py-4">
          {{ donationStatsError }}
          <div class="mt-2">
            <button 
              @click="fetchDonationStats"
              class="bg-[#C77DFF] text-white px-4 py-2 rounded-lg hover:bg-[#a259e6]"
            >
              Try Again
            </button>
          </div>
        </div>
        
        <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="bg-white p-4 rounded-lg shadow text-center">
            <h3 class="text-lg font-medium text-gray-500">Total Donations</h3>
            <p class="text-3xl font-bold text-[#C77DFF] mt-2">{{ donationStats.totalDonations }}</p>
          </div>
          
          <div class="bg-white p-4 rounded-lg shadow text-center">
            <h3 class="text-lg font-medium text-gray-500">Total Amount</h3>
            <p class="text-3xl font-bold text-[#C77DFF] mt-2">RM {{ formatAmount(donationStats.totalAmount) }}</p>
          </div>
          
          <div class="bg-white p-4 rounded-lg shadow text-center">
            <h3 class="text-lg font-medium text-gray-500">Last Donation</h3>
            <p class="text-lg font-medium text-gray-700 mt-2">{{ formatDate(donationStats.lastDonationDate) }}</p>
          </div>
        </div>
      </div>
      
      <div class="overflow-x-auto">
        <div class="min-w-[700px]">
          <!-- Header Row -->
          <div class="grid grid-cols-4 gap-4 pb-4 border-b border-[#C77DFF]">
            <div class="flex items-center text-[#C77DFF] font-semibold text-lg min-w-[180px]">
              <font-awesome-icon icon="fa-solid fa-user" class="mr-2" />
              Name
            </div>
            <div class="flex items-center text-[#C77DFF] font-semibold text-lg min-w-[220px]">
              <font-awesome-icon icon="fa-solid fa-user-pen" class="mr-2" />
              Email
            </div>
            <div class="flex items-center text-[#C77DFF] font-semibold text-lg min-w-[100px]">
              <font-awesome-icon icon="fa-solid fa-phone" class="mr-2" />
              Phone
            </div>
            <div class="flex items-center text-[#C77DFF] font-semibold text-lg min-w-[180px]">
              <font-awesome-icon icon="fa-solid fa-cog" class="mr-2" />
              Actions
            </div>
          </div>
  
          <!-- Loading State -->
          <div v-if="isLoading" class="text-center py-8">
            <p class="text-[#C77DFF] font-bold text-xl">Loading accounts...</p>
          </div>

          <!-- Error State -->
          <div v-else-if="error" class="text-center text-red-500 py-8">
            {{ error }}
            <div class="mt-2">
              <button 
                @click="fetchUsers"
                class="bg-[#C77DFF] text-white px-4 py-2 rounded-lg hover:bg-[#a259e6]"
              >
                Try Again
              </button>
            </div>
          </div>
  
          <!-- User List -->
          <div v-else class="divide-y divide-gray-200">
            <div
              v-if="users.length === 0"
              class="text-center text-[#C77DFF] py-8"
            >
              No users found.
            </div>
            <div
              v-for="user in users"
              :key="user.id"
              class="grid grid-cols-4 gap-4 items-center pl-2 py-4 bg-[#F8F8F8] rounded-lg mt-1"
            >
              <div class="text-[#C77DFF] font-medium text-left break-words whitespace-normal min-w-[180px]">
                {{ user.name }}
              </div>
              <div class="text-[#C77DFF] font-medium text-left break-words whitespace-normal min-w-[220px]">
                {{ user.email }}
              </div>
              <div class="text-[#C77DFF] font-medium text-left break-words whitespace-normal min-w-[100px]">
                {{ user.phone }}
              </div>
              <div class="flex items-center justify-end min-w-[180px]">
                <button
                  class="flex items-center gap-2 bg-[#C77DFF] text-white px-4 py-2 rounded-lg shadow hover:bg-[#a259e6] transition mr-2"
                  @click="viewAccount(user)"
                >
                  View
                  <font-awesome-icon icon="fa-solid fa-eye" />
                </button>
                <button
                  class="flex items-center gap-2 bg-red-500 text-white px-4 py-2 rounded-lg shadow hover:bg-red-600 transition"
                  @click="confirmDelete(user)"
                >
                  Delete
                  <font-awesome-icon icon="fa-solid fa-trash" />
                </button>
              </div>
            </div>
          </div>

          <!-- Pagination -->
          <div v-if="totalPages > 1" class="flex justify-center mt-4">
            <div class="flex space-x-2">
              <button 
                @click="goToPage(currentPage - 1)" 
                :disabled="currentPage === 1"
                class="px-3 py-1 rounded-md bg-[#E0AAFF] text-white disabled:opacity-50"
              >
                Prev
              </button>
              <div v-for="page in displayPages" :key="page" class="px-3 py-1">
                <button 
                  @click="goToPage(page)" 
                  class="w-8 h-8 rounded-full"
                  :class="page === currentPage ? 'bg-[#C77DFF] text-white' : 'bg-gray-200'"
                >
                  {{ page }}
                </button>
              </div>
              <button 
                @click="goToPage(currentPage + 1)" 
                :disabled="currentPage === totalPages"
                class="px-3 py-1 rounded-md bg-[#E0AAFF] text-white disabled:opacity-50"
              >
                Next
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Delete Confirmation Modal -->
      <div v-if="showDeleteModal" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
        <div class="bg-white p-6 rounded-lg shadow-lg max-w-md w-full">
          <h2 class="text-xl font-bold text-gray-800 mb-4">Confirm Deletion</h2>
          <p class="text-gray-600 mb-3">
            Are you sure you want to delete the account for <span class="font-semibold text-[#C77DFF]">{{ userToDelete?.name }}</span>?
          </p>
          <div class="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-4">
            <div class="flex">
              <div class="flex-shrink-0">
                <font-awesome-icon icon="fa-solid fa-exclamation-triangle" class="text-yellow-400" />
              </div>
              <div class="ml-3">
                <p class="text-sm text-yellow-700">
                  <strong>Warning:</strong> This will permanently delete the user account and <strong>ALL</strong> related data including:
                </p>
                <ul class="list-disc list-inside mt-2 text-xs text-yellow-700 pl-2">
                  <li>Donation history</li>
                  <li>Ride history and bookings</li>
                  <li>Feedback and reports</li>
                  <li>Chat messages</li>
                  <li>Notifications</li>
                  <li>User profiles (driver/donor)</li>
                </ul>
                <p class="text-sm text-yellow-700 mt-2">
                  This action cannot be undone.
                </p>
              </div>
            </div>
          </div>
          <div class="flex justify-end space-x-3">
            <button 
              @click="showDeleteModal = false"
              class="px-4 py-2 bg-gray-300 text-gray-800 rounded-lg hover:bg-gray-400"
              :disabled="isLoading"
            >
              Cancel
            </button>
            <button 
              @click="deleteUser"
              class="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 flex items-center"
              :disabled="isLoading"
            >
              <span v-if="isLoading" class="mr-2">
                <svg class="animate-spin h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
              </span>
              {{ isLoading ? 'Deleting...' : 'Delete' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, onMounted } from 'vue';
  import axios from 'axios';
  import { useToastStore } from '../../../../stores/toast';
  import { useRouter } from 'vue-router';
  import { useAdminAuthStore } from '../../../../stores/adminAuth';
  
  const API_BASE_URL = 'http://127.0.0.1:5000/api';
  const toastStore = useToastStore();
  const router = useRouter();
  const adminAuthStore = useAdminAuthStore();
  
  // User state
  const users = ref([]);
  const isLoading = ref(false);
  const error = ref(null);
  const currentPage = ref(1);
  const perPage = ref(10);
  const totalUsers = ref(0);
  const totalPages = ref(0);
  const showDeleteModal = ref(false);
  const userToDelete = ref(null);
  
  // Donation stats state
  const donationStats = ref({
    totalDonations: 0,
    totalAmount: 0,
    lastDonationDate: null,
    monthlyDonations: []
  });
  const donationStatsLoading = ref(false);
  const donationStatsError = ref(null);
  
  // Computed properties for pagination
  const displayPages = computed(() => {
    if (totalPages.value <= 5) {
      return Array.from({ length: totalPages.value }, (_, i) => i + 1);
    }
    
    if (currentPage.value <= 3) {
      return [1, 2, 3, 4, 5];
    }
    
    if (currentPage.value >= totalPages.value - 2) {
      return [
        totalPages.value - 4,
        totalPages.value - 3,
        totalPages.value - 2,
        totalPages.value - 1,
        totalPages.value
      ];
    }
    
    return [
      currentPage.value - 2,
      currentPage.value - 1,
      currentPage.value,
      currentPage.value + 1,
      currentPage.value + 2
    ];
  });
  
  // Methods
  const fetchUsers = async () => {
    isLoading.value = true;
    error.value = null;
    
    try {
      const response = await axios.get(`${API_BASE_URL}/admin/users`, {
        params: {
          page: currentPage.value,
          per_page: perPage.value
        }
      });
      
      users.value = response.data.users;
      totalUsers.value = response.data.pagination.total_users;
      totalPages.value = response.data.pagination.total_pages;
    } catch (err) {
      console.error('Failed to fetch users:', err);
      error.value = err.response?.data?.error || 'Failed to load users';
      toastStore.error(error.value);
    } finally {
      isLoading.value = false;
    }
  };
  
  const fetchDonationStats = async (retryCount = 0) => {
    donationStatsLoading.value = true;
    donationStatsError.value = null;
    
    try {
      console.log('Fetching donation stats from:', `${API_BASE_URL}/donations/system/stats`);
      console.log('Using admin token:', adminAuthStore.adminToken ? 'Token available' : 'No token');
      
      const response = await axios.get(`${API_BASE_URL}/donations/system/stats`, {
        headers: {
          'Authorization': `Bearer ${adminAuthStore.adminToken}`
        }
      });
      
      console.log('Donation stats response:', response.data);
      
      if (response.data) {
        donationStats.value = response.data;
      } else {
        throw new Error('Empty response data');
      }
    } catch (err) {
      console.error('Failed to fetch donation stats:', err);
      donationStatsError.value = err.response?.data?.error || 'Failed to load donation statistics';
      
      // Retry up to 3 times with exponential backoff
      if (retryCount < 3) {
        const retryDelay = Math.pow(2, retryCount) * 1000; // 1s, 2s, 4s
        console.log(`Retrying in ${retryDelay}ms... (Attempt ${retryCount + 1}/3)`);
        
        setTimeout(() => {
          fetchDonationStats(retryCount + 1);
        }, retryDelay);
        return;
      }
      
      toastStore.error(donationStatsError.value);
    } finally {
      donationStatsLoading.value = false;
    }
  };
  
  const formatAmount = (amount) => {
    return parseFloat(amount).toFixed(2);
  };
  
  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };
  
  const goToPage = (page) => {
    if (page < 1 || page > totalPages.value) return;
    currentPage.value = page;
    fetchUsers();
  };
  
  const confirmDelete = (user) => {
    userToDelete.value = user;
    showDeleteModal.value = true;
  };
  
  const viewAccount = (user) => {
    router.push({ name: 'Account_Details', params: { id: user.id } });
  };
  
  const deleteUser = async () => {
    if (!userToDelete.value) return;
    
    try {
      isLoading.value = true; // Show loading state
      
      // Add a confirmation message about cascade deletion
      const response = await axios.delete(`${API_BASE_URL}/admin/users/${userToDelete.value.id}`, {
        headers: {
          'Authorization': `Bearer ${adminAuthStore.adminToken}`
        }
      });
      
      console.log("Delete user response:", response.data);
      
      toastStore.success(`User ${userToDelete.value.name} and all associated data have been deleted`);
      showDeleteModal.value = false;
      userToDelete.value = null;
      
      // Refresh the user list
      fetchUsers();
      // Also refresh donation stats in case the deleted user had donations
      fetchDonationStats();
    } catch (err) {
      console.error('Failed to delete user:', err);
      const errorMsg = err.response?.data?.error || 'Failed to delete user and associated data';
      toastStore.error(errorMsg);
    } finally {
      isLoading.value = false;
    }
  };
  
  // Lifecycle hooks
  onMounted(() => {
    fetchUsers();
    fetchDonationStats();
  });
  </script> 
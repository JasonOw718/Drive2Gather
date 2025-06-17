<template>
  <div v-if="user" class="max-w-3xl mx-auto mt-10">
    <!-- User Info Card -->
    <div class="bg-white rounded-2xl shadow-lg p-8">
      <h2 class="text-2xl font-bold text-[#C77DFF] mb-6">
        User Account Details
      </h2>

      <div class="flex items-center mb-8">
        <div
          class="w-24 h-24 bg-gray-200 rounded-full overflow-hidden mr-6 flex-shrink-0"
        >
          <img
            v-if="user.profile_pic"
            :src="user.profile_pic"
            alt="User profile"
            class="w-full h-full object-cover"
          />
          <div
            v-else
            class="w-full h-full flex items-center justify-center bg-[#E0AAFF]"
          >
            <span class="text-3xl font-bold text-white">{{
              getInitials(user.name)
            }}</span>
          </div>
        </div>
        <div>
          <h3 class="text-xl font-bold text-gray-800">{{ user.name }}</h3>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label class="block text-[#C77DFF] font-semibold mb-1">Email</label>
          <div
            class="bg-[#F8F8F8] rounded-lg px-4 py-2 text-gray-700 w-full min-w-0 break-words whitespace-normal"
          >
            {{ user.email }}
          </div>
        </div>
        <div>
          <label class="block text-[#C77DFF] font-semibold mb-1">Phone</label>
          <div
            class="bg-[#F8F8F8] rounded-lg px-4 py-2 text-gray-700 w-full min-w-0 break-words whitespace-normal"
          >
            {{ user.phone }}
          </div>
        </div>
        <div>
          <label class="block text-[#C77DFF] font-semibold mb-1">User ID</label>
          <div
            class="bg-[#F8F8F8] rounded-lg px-4 py-2 text-gray-700 w-full min-w-0 break-words whitespace-normal"
          >
            {{ user.id || user.user_id }}
          </div>
        </div>
        <div>
          <label class="block text-[#C77DFF] font-semibold mb-1"
            >User Type</label
          >
          <div
            class="bg-[#F8F8F8] rounded-lg px-4 py-2 text-gray-700 w-full min-w-0 break-words whitespace-normal"
          >
            {{ user.role || user.user_type || "Passenger" }}
          </div>
        </div>
      </div>

      <div class="flex flex-row-reverse gap-4 mt-8">
        <button
          type="button"
          class="bg-[#C77DFF] text-white px-8 py-2 rounded-lg font-semibold shadow hover:bg-[#a259e6] transition"
          @click="goBack"
        >
          Back to List
        </button>
      </div>
    </div>
  </div>
  <div v-else-if="isLoading" class="max-w-3xl mx-auto mt-10 text-center">
    <p class="text-[#C77DFF] font-bold text-xl">Loading user details...</p>
  </div>
  <div v-else class="max-w-3xl mx-auto mt-10 text-center text-red-500">
    <p>User not found or error loading user details.</p>
    <button
      @click="goBack"
      class="mt-4 bg-[#C77DFF] text-white px-8 py-2 rounded-lg font-semibold shadow hover:bg-[#a259e6] transition"
    >
      Back to User List
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useToastStore } from "../../../../stores/toast";
import axios from "axios";

const API_BASE_URL = "http://localhost:5000/api";
const route = useRoute();
const router = useRouter();
const toastStore = useToastStore();

const userId = route.params.id;
const user = ref(null);
const isLoading = ref(true);

// Get user details from API
const fetchUserDetails = async () => {
  isLoading.value = true;

  try {
    const response = await axios.get(`${API_BASE_URL}/admin/users/${userId}`);
    user.value = response.data.user;
  } catch (error) {
    console.error("Error fetching user details:", error);
    toastStore.error("Failed to load user details");
  } finally {
    isLoading.value = false;
  }
};

const getInitials = (name) => {
  if (!name) return "?";
  return name
    .split(" ")
    .map((part) => part[0]?.toUpperCase() || "")
    .slice(0, 2)
    .join("");
};

const formatDate = (dateString) => {
  if (!dateString) return "N/A";
  const date = new Date(dateString);
  return date.toLocaleDateString();
};

const goBack = () => {
  router.push({ name: "Account_Management" });
};

onMounted(() => {
  fetchUserDetails();
});
</script>

<template>
  <div class="w-full mx-auto mt-10 bg-white rounded-2xl shadow-lg p-8">
    <div class="overflow-x-auto">
      <div class="min-w-[700px]">
        <!-- Header Row -->
        <div class="grid grid-cols-3 gap-4 pb-4 border-b border-[#C77DFF]">
          <div class="flex items-center text-[#C77DFF] font-semibold text-lg min-w-[180px]">
            <font-awesome-icon icon="fa-solid fa-user" class="mr-2" />
            Ride Information
          </div>
          <div class="flex items-center text-[#C77DFF] font-semibold text-lg min-w-[220px]">
            <font-awesome-icon icon="fa-solid fa-pencil" class="mr-2" />
            Issue
          </div>
          <div class="flex items-center text-[#C77DFF] font-semibold text-lg min-w-[180px]">
            <font-awesome-icon icon="fa-solid fa-clock" class="mr-2" />
            Report Date
          </div>
        </div>

        <!-- Loading State -->
        <div v-if="reportStore.isLoading" class="text-center py-8">
          <p class="text-[#C77DFF] font-bold text-xl">Loading reports...</p>
        </div>

        <!-- Error State -->
        <div v-else-if="reportStore.error" class="text-center text-red-500 py-8">
          {{ reportStore.error }}
          <div class="mt-2">
            <button 
              @click="fetchReports"
              class="bg-[#C77DFF] text-white px-4 py-2 rounded-lg hover:bg-[#a259e6]"
            >
              Try Again
            </button>
          </div>
        </div>

        <!-- Report List -->
        <div v-else class="divide-y divide-gray-200">
          <div
            v-if="sortedReports.length === 0"
            class="text-center text-[#C77DFF] py-8"
          >
            No report found.
          </div>
          <div
            v-for="report in sortedReports"
            :key="report.id"
            class="grid grid-cols-3 gap-4 items-center py-4 bg-[#F8F8F8] pl-2 rounded-lg mt-1"
          >
            <div class="text-[#C77DFF] font-medium text-left break-words whitespace-normal min-w-[180px]">
              Ride ID: {{ report.rideId }}
            </div>
            <div class="text-[#C77DFF] font-medium text-left break-words whitespace-normal min-w-[220px]">
              {{ report.issue }}
            </div>
            <div class="flex items-center justify-between min-w-[180px]">
              <span class="text-[#C77DFF] font-medium text-left break-words whitespace-normal">
                {{ report.date }}
              </span>
              <button
                class="ml-4 flex items-center gap-2 bg-[#C77DFF] text-white px-4 py-2 rounded-lg shadow hover:bg-[#a259e6] transition"
                @click="viewReportDetails(report)"
              >
                Detail
                <font-awesome-icon icon="fa-solid fa-arrow-right" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useReportStore } from "../../../../stores/report.js";
import { useToastStore } from "../../../../stores/toast.js";

const router = useRouter();
const reportStore = useReportStore();
const toastStore = useToastStore();

// Sort reports by date descending (newest first)
const sortedReports = computed(() => {
  return [...reportStore.reports].sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
});

const viewReportDetails = (report) => {
  router.push({ name: "Report_Details", params: { id: report.id } });
};

const fetchReports = () => {
  reportStore.fetchReports();
};

onMounted(() => {
  fetchReports();
});
</script>
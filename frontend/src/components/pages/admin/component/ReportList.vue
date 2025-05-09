<template>
  <div class="w-full mx-auto mt-10 bg-white rounded-2xl shadow-lg p-8">
    <div class="overflow-x-auto">
      <div class="min-w-[700px]">
        <!-- Header Row -->
        <div class="grid grid-cols-3 gap-4 pb-4 border-b border-[#C77DFF]">
          <div class="flex items-center text-[#C77DFF] font-semibold text-lg min-w-[180px]">
            <font-awesome-icon icon="fa-solid fa-user" class="mr-2" />
            Driver Name
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

        <!-- Report List -->
        <div class="divide-y divide-gray-200">
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
              {{ report.driverName }}
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
                @click="goToDetails(report.id)"
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
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { useReportStore } from "../../../stores/report.js";

const router = useRouter();
const reportStore = useReportStore();

// Sort reports by date ascending (assuming date is in a sortable format like YYYY-MM-DD or ISO string)
const sortedReports = computed(() => {
  return [...reportStore.reports].sort((a, b) => new Date(a.date) - new Date(b.date));
});

const goToDetails = (id) => {
  router.push({ name: "Report_Details", params: { id: id } });
};
</script>
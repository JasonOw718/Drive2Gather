<template>
  <div v-if="report" class="max-w-3xl mx-auto mt-10">
    <!-- Report Info Card -->
    <div class="bg-white rounded-2xl shadow-lg p-8">
      <h2 class="text-2xl font-bold text-[#C77DFF] mb-6">Report Details</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label class="block text-[#C77DFF] font-semibold mb-1">Driver Name</label>
          <div class="bg-[#F8F8F8] rounded-lg px-4 py-2 text-gray-700 w-full min-w-0 break-words whitespace-normal">{{ report.driverName }}</div>
        </div>
        <div>
          <label class="block text-[#C77DFF] font-semibold mb-1">Report Date</label>
          <div class="bg-[#F8F8F8] rounded-lg px-4 py-2 text-gray-700 w-full min-w-0 break-words whitespace-normal">{{ report.date }}</div>
        </div>
        <div>
          <label class="block text-[#C77DFF] font-semibold mb-1">Issue</label>
          <div class="bg-[#F8F8F8] rounded-lg px-4 py-2 text-gray-700 w-full min-w-0 break-words whitespace-normal">{{ report.issue }}</div>
        </div>
        <div>
          <label class="block text-[#C77DFF] font-semibold mb-1">Reported By</label>
          <div class="bg-[#F8F8F8] rounded-lg px-4 py-2 text-gray-700 w-full min-w-0 break-words whitespace-normal">{{ report.passengerName }}</div>
        </div>
      </div>
      <div class="mt-6">
        <label class="block text-[#C77DFF] font-semibold mb-1">Comments</label>
        <div class="bg-[#F8F8F8] rounded-lg px-4 py-2 text-gray-700 w-full min-w-0 break-words whitespace-normal">{{ report.comments }}</div>
      </div>
      <div class="flex flex-row-reverse gap-4 mt-8">
        <button type="button" class="bg-[#C77DFF] text-white px-8 py-2 rounded-lg font-semibold shadow hover:bg-[#a259e6] transition" @click="goBack">Back to List</button>
      </div>
    </div>
  </div>
  <div v-else class="max-w-3xl mx-auto mt-10 text-center text-red-500">
    <p>Report not found. It may have been deleted or the ID is invalid.</p>
    <button type="button" class="mt-4 bg-[#C77DFF] text-white px-8 py-2 rounded-lg font-semibold shadow hover:bg-[#a259e6] transition" @click="goBack">Back to List</button>
  </div>
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router';
import { useReportStore } from "../../../../stores/report.js";

const route = useRoute();
const router = useRouter();
const reportStore = useReportStore();
const reportId = parseInt(route.params.id);
const report = reportStore.getReportById(reportId);

function goBack() {
  router.push({ name: 'Report_List' });
}
</script>
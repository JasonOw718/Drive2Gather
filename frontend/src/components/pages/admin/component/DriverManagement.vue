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
              <font-awesome-icon icon="fa-solid fa-user-pen" class="mr-2" />
              Email
            </div>
            <div class="flex items-center text-[#C77DFF] font-semibold text-lg min-w-[180px]">
              <font-awesome-icon icon="fa-solid fa-phone" class="mr-2" />
              Phone Number
            </div>
          </div>
  
          <!-- Driver List -->
          <div class="divide-y divide-gray-200">
            <div
              v-if="driverStore.drivers.filter(d => d.status === 'activate').length === 0"
              class="text-center text-[#C77DFF] py-8"
            >
              No Activate drivers found.
            </div>
            <div
              v-for="driver in driverStore.drivers.filter(d => d.status === 'activate')"
              :key="driver.id"
              class="grid grid-cols-3 gap-4 items-center pl-2 py-4 bg-[#F8F8F8] rounded-lg mt-1"
            >
              <div class="text-[#C77DFF] font-medium text-left break-words whitespace-normal min-w-[180px]">
                {{ driver.name }}
              </div>
              <div class="text-[#C77DFF] font-medium text-left break-words whitespace-normal min-w-[220px]">
                {{ driver.email }}
              </div>
              <div class="flex items-center justify-between min-w-[180px]">
                <span class="text-[#C77DFF] font-medium text-left break-words whitespace-normal">
                  {{ driver.phone }}
                </span>
                <button
                  class="ml-4 flex items-center gap-2 bg-[#C77DFF] text-white px-4 py-2 rounded-lg shadow hover:bg-[#a259e6] transition"
                  @click="goToDetails(driver.id)"
                >
                  Details
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
  import { useRouter } from "vue-router";
  import { useDriverStore } from '../../../stores/driver.js';
  
  const router = useRouter();
  const driverStore = useDriverStore();
  
  const goToDetails = (driverId) => {
    router.push({ name: "Driver_Details", params: { id: driverId } });
  };
  </script>
  
  
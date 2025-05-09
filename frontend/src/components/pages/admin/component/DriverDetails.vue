<template>
    <div v-if="driver" class="max-w-5xl mx-auto mt-10">
        <!-- Driver Info Card -->
        <div class="bg-white rounded-2xl shadow-lg p-8 grid grid-cols-1 md:grid-cols-3 gap-8 items-center">
            <!-- Left: Info -->
            <div class="md:col-span-2 space-y-4">
                <h2 class="text-2xl font-bold text-[#C77DFF] mb-4">Driver Details</h2>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                        <label class="block text-[#C77DFF] font-semibold mb-1">Driver Name</label>
                        <div class="bg-[#F8F8F8] rounded-lg px-4 py-2 text-gray-700 w-full min-w-0 break-words whitespace-normal">{{ driver.name }}</div>
                    </div>
                    <div>
                        <label class="block text-[#C77DFF] font-semibold mb-1">Phone Number</label>
                        <div class="bg-[#F8F8F8] rounded-lg px-4 py-2 text-gray-700 w-full min-w-0 break-words whitespace-normal">{{ driver.phone }}</div>
                    </div>
                    <div>
                        <label class="block text-[#C77DFF] font-semibold mb-1">Email</label>
                        <div class="bg-[#F8F8F8] rounded-lg px-4 py-2 text-gray-700 w-full min-w-0 break-words whitespace-normal">{{ driver.email }}</div>
                    </div>
                    <div>
                        <label class="block text-[#C77DFF] font-semibold mb-1">Car Plate</label>
                        <div class="bg-[#F8F8F8] rounded-lg px-4 py-2 text-gray-700 w-full min-w-0 break-words whitespace-normal">{{ driver.carPlate }}</div>
                    </div>
                    <div>
                        <label class="block text-[#C77DFF] font-semibold mb-1">Car Type</label>
                        <div class="bg-[#F8F8F8] rounded-lg px-4 py-2 text-gray-700 w-full min-w-0 break-words whitespace-normal">{{ driver.carType }}</div>
                    </div>
                    <div>
                        <label class="block text-[#C77DFF] font-semibold mb-1">Seats Available</label>
                        <div class="bg-[#F8F8F8] rounded-lg px-4 py-2 text-gray-700 w-full min-w-0 break-words whitespace-normal">{{ driver.seatAvailable }}</div>
                    </div>
                </div>
            </div>
            <!-- Right: Avatar -->
            <div class="flex flex-col items-center justify-center">
                <label class="block text-[#C77DFF] font-semibold mb-2">Profile Picture</label>
                <img :src="driver.avatar" alt="avatar" class="rounded-full border-4 border-[#C77DFF] w-32 h-32 object-cover" />
            </div>
        </div>

        <!-- License Photos -->
        <div class="bg-white rounded-2xl shadow-lg p-8 mt-8">
            <h3 class="text-xl font-bold text-[#C77DFF] mb-4">License Photos</h3>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
                <div v-for="(img, idx) in driver.licenseImages" :key="'license-' + idx" class="flex justify-center">
                    <img :src="img" alt="License Photo" class="w-48 h-32 object-cover rounded-xl border-2 border-[#C77DFF]" />
                </div>
            </div>
        </div>

        <!-- Car Photos -->
        <div class="bg-white rounded-2xl shadow-lg p-8 mt-8">
            <h3 class="text-xl font-bold text-[#C77DFF] mb-4">Car Photos</h3>
            <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-6">
                <div v-for="(img, idx) in driver.carPhotos" :key="'car-' + idx" class="flex justify-center">
                    <img :src="img" alt="Car Photo" class="w-36 h-24 object-cover rounded-xl border-2 border-[#C77DFF]" />
                </div>
            </div>
        </div>

        <!-- Action Buttons -->
        <div class="flex flex-row-reverse gap-4 mt-8">
            <button class="bg-[#C77DFF] text-white px-8 py-2 rounded-lg font-semibold shadow hover:bg-[#a259e6] transition" @click="approveDriver">Approve</button>
            <button class="border-2 border-[#C77DFF] text-[#C77DFF] bg-white px-8 py-2 rounded-lg font-semibold hover:bg-[#F8F8F8] transition" @click="rejectDriver">Reject</button>
        </div>
    </div>
</template>

<script setup>
import { computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useDriverStore } from "../../../stores/driver";

const route = useRoute();
const router = useRouter();
const driverStore = useDriverStore();
const driverId = parseInt(route.params.id);
const driver = computed(() => driverStore.drivers.find(d => d.id === driverId));

function approveDriver() {
    driverStore.approveDriver(driverId);
    router.push({ name: 'Driver_Registration_List' });
}
function rejectDriver() {
    driverStore.rejectDriver(driverId);
    router.push({ name: 'Driver_Registration_List' });
}
</script>
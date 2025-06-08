<template>
    <div class="flex h-screen bg-gray-100">
        <!-- Sidebar -->
        <aside class="fixed inset-y-0 left-0 w-72 bg-[#F8F8F8] flex flex-col z-20">
            <RouterLink to="/portal/donor/dashboard" class="flex items-center gap-3 px-8 py-6">
                <img src="../../../assets/images/logo.png" alt="Logo" class="h-10" />
                <!-- <span class="text-2xl font-bold text-white">Drive2Gather Donor</span> -->
            </RouterLink>
            <nav class="flex-1 mt-6">
                <ul class="flex flex-col gap-2">
                    <li>
                        <RouterLink
                            to="/portal/donor/dashboard"
                            class="flex items-center gap-3 px-8 py-3 transition"
                            :class="route.name === 'DonorDashboard'
                                ? 'bg-[#C77DFF] text-white'
                                : 'text-gray-700 hover:bg-[#E0AAFF] hover:text-white'"
                        >
                            <font-awesome-icon icon="fa-solid fa-gauge" />
                            <span class="font-medium">Dashboard</span>
                        </RouterLink>
                    </li>
                    <li>
                        <RouterLink
                            to="/portal/donor/donate"
                            class="flex items-center gap-3 px-8 py-3 transition"
                            :class="route.name === 'DonorDonation'
                                ? 'bg-[#C77DFF] text-white'
                                : 'text-gray-700 hover:bg-[#E0AAFF] hover:text-white'"
                        >
                            <font-awesome-icon icon="fa-solid fa-hand-holding-heart" />
                            <span class="font-medium">Make Donation</span>
                        </RouterLink>
                    </li>
                    <li>
                        <RouterLink
                            to="/portal/donor/history"
                            class="flex items-center gap-3 px-8 py-3 transition"
                            :class="route.name === 'DonorHistory'
                                ? 'bg-[#C77DFF] text-white'
                                : 'text-gray-700 hover:bg-[#E0AAFF] hover:text-white'"
                        >
                            <font-awesome-icon icon="fa-solid fa-clock-rotate-left" />
                            <span class="font-medium">Donation History</span>
                        </RouterLink>
                    </li>
                    <li>
                        <RouterLink
                            to="/portal/donor/profile"
                            class="flex items-center gap-3 px-8 py-3 transition"
                            :class="route.name === 'DonorProfile'
                                ? 'bg-[#C77DFF] text-white'
                                : 'text-gray-700 hover:bg-[#E0AAFF] hover:text-white'"
                        >
                            <font-awesome-icon icon="fa-solid fa-user" />
                            <span class="font-medium">Profile</span>
                        </RouterLink>
                    </li>
                </ul>
            </nav>
            <div class="mt-auto mb-6 px-8">
                <button
                    @click="signOut"
                    class="flex items-center gap-3 w-full py-3 px-3 rounded-l-lg text-gray-700 hover:bg-red-500 hover:text-white transition"
                >
                    <font-awesome-icon icon="fa-solid fa-right-from-bracket" />
                    <span class="font-medium">Sign Out</span>
                </button>
            </div>
        </aside>

        <!-- Main Content -->
        <div class="flex-1 ml-72 flex flex-col">
            <header class="bg-[#F8F8F8] shadow flex items-center h-20 px-12 text-xl font-bold text-[#C77DFF]">
                {{ getPageTitle() }}
            </header>
            <main class="flex-1 overflow-auto p-8">
                <router-view></router-view>
            </main>
        </div>
    </div>
</template>

<script setup>
import { useRoute } from "vue-router";
import { useDonorAuthStore } from "../../../stores/donorAuth";
import { useRouter } from "vue-router";

const router = useRouter();
const route = useRoute();
const donorAuthStore = useDonorAuthStore();

const signOut = async () => {
    donorAuthStore.donorLogout();
};

const getPageTitle = () => {
    switch(route.name) {
        case 'DonorDashboard':
            return 'Donor Dashboard';
        case 'DonorDonation':
            return 'Make Donation';
        case 'DonorDonationComplete':
            return 'Donation Complete';
        case 'DonorHistory':
            return 'Donation History';
        case 'DonorProfile':
            return 'Donor Profile';
        default:
            return 'Donor Portal';
    }
};
</script>

<style scoped>
/* Any specific styles for the donor layout can go here */
</style> 
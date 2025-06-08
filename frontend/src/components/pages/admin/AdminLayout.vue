<template>
    <div class="flex h-screen bg-gray-100">
        <!-- Sidebar -->
        <aside class="fixed inset-y-0 left-0 w-72 bg-[#F8F8F8] flex flex-col z-20">
            <RouterLink to="/admin/driver-management" class="flex items-center gap-3 px-8 py-6">
                <img src="../../../assets/images/logo.png" alt="Logo" class="h-10" />
                <!-- <span class="text-2xl font-bold text-white">Ride2Gather Admin</span> -->
            </RouterLink>
            <nav class="flex-1 mt-6">
                <ul class="flex flex-col gap-2">
                    <li>
                        <RouterLink
                            to="/admin/account-management"
                            class="flex items-center gap-3 px-8 py-3 transition"
                            :class="route.name === 'Account_Management'
                                ? 'bg-[#C77DFF] text-white'
                                : 'text-gray-700 hover:bg-[#E0AAFF] hover:text-white'"
                        >
                            <font-awesome-icon icon="fa-solid fa-user-group" />
                            <span class="font-medium">Manage Accounts</span>
                        </RouterLink>
                    </li>
                    <li>
                        <RouterLink
                            to="/admin/driver-management"
                            class="flex items-center gap-3 px-8 py-3 transition"
                            :class="route.name === 'Driver_Management'
                                ? 'bg-[#C77DFF] text-white'
                                : 'text-gray-700 hover:bg-[#E0AAFF] hover:text-white'"
                        >
                            <font-awesome-icon icon="fa-solid fa-car" />
                            <span class="font-medium">Driver Registration</span>
                        </RouterLink>
                    </li>
                    <li>
                        <RouterLink
                            to="/admin/report-list"
                            class="flex items-center gap-3 px-8 py-3 transition"
                            :class="route.name === 'Report_List'
                                ? 'bg-[#C77DFF] text-white'
                                : 'text-gray-700 hover:bg-[#E0AAFF] hover:text-white'"
                        >
                            <font-awesome-icon icon="fa-solid fa-layer-group" />
                            <span class="font-medium">Report</span>
                        </RouterLink>
                    </li>
                </ul>
            </nav>
            <div class="mt-auto mb-6 px-8">
                <button
                    @click="signOut"
                    class="flex items-center gap-3 w-full py-3 px-3 rounded-l-lg text-gray-300 hover:bg-red-500 hover:text-white transition"
                >
                    <font-awesome-icon icon="fa-solid fa-right-from-bracket" />
                    <span class="font-medium">Sign Out</span>
                </button>
            </div>
        </aside>

        <!-- Main Content -->
        <div class="flex-1 ml-72 flex flex-col">
            <header class="bg-[#F8F8F8] shadow flex items-center h-20 px-12 text-xl font-bold text-[#C77DFF]">
                {{ route.name ? route.name.replace(/_/g, " ") : "" }}
            </header>
            <main class="flex-1 overflow-auto p-8">
                <router-view></router-view>
            </main>
        </div>
    </div>
</template>

<script setup>
import { useRoute } from "vue-router";
import { useAdminAuthStore } from "../../../stores/adminAuth";
import { useRouter } from "vue-router";

const router = useRouter();
const route = useRoute();
const adminAuthStore = useAdminAuthStore();

const signOut = async () => {
    adminAuthStore.adminLogout();
};
</script>

<style scoped>

</style>

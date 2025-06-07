<template>
  <div 
    class="fixed top-4 right-4 z-50 flex flex-col gap-2 pointer-events-none max-w-md"
    style="max-height: calc(100vh - 2rem); overflow-y: auto;"
  >
    <TransitionGroup name="toast">
      <div 
        v-for="toast in toastStore.toasts" 
        :key="toast.id" 
        class="pointer-events-auto flex items-center justify-between p-4 mb-2 rounded-lg shadow-lg transform transition-all duration-300"
        :class="toastClasses(toast.type)"
      >
        <div class="flex items-center">
          <span class="mr-2">
            <font-awesome-icon :icon="toastIcon(toast.type)" />
          </span>
          <span>{{ toast.message }}</span>
        </div>
        <button 
          @click="toastStore.removeToast(toast.id)" 
          class="ml-4 text-sm opacity-70 hover:opacity-100 focus:outline-none"
        >
          <font-awesome-icon icon="fa-times" />
        </button>
      </div>
    </TransitionGroup>
  </div>
</template>

<script setup>
import { useToastStore } from '../../stores/toast'

const toastStore = useToastStore()

// Get appropriate icon based on toast type
function toastIcon(type) {
  switch (type) {
    case 'success':
      return 'fa-check-circle'
    case 'error':
      return 'fa-exclamation-circle'
    case 'warning':
      return 'fa-exclamation-triangle'
    case 'info':
    default:
      return 'fa-info-circle'
  }
}

// Get appropriate classes based on toast type
function toastClasses(type) {
  switch (type) {
    case 'success':
      return 'bg-green-100 text-green-800 border-l-4 border-green-500'
    case 'error':
      return 'bg-red-100 text-red-800 border-l-4 border-red-500'
    case 'warning':
      return 'bg-yellow-100 text-yellow-800 border-l-4 border-yellow-500'
    case 'info':
    default:
      return 'bg-blue-100 text-blue-800 border-l-4 border-blue-500'
  }
}
</script>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.toast-leave-to {
  opacity: 0;
  transform: translateY(-30px);
}
</style> 
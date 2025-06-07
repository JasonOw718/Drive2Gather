import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useToastStore = defineStore('toast', () => {
  // Array to hold all toast messages
  const toasts = ref([])
  
  // Generate unique ID for each toast
  const generateId = () => `toast-${Date.now()}-${Math.floor(Math.random() * 1000)}`
  
  // Add a new toast
  function addToast(message, type = 'success', duration = 3000) {
    const id = generateId()
    
    // Add toast to array
    toasts.value.push({
      id,
      message,
      type, // success, error, info, warning
      duration,
    })
    
    // Remove toast after duration
    setTimeout(() => {
      removeToast(id)
    }, duration)
    
    return id
  }
  
  // Shorthand methods for different toast types
  function success(message, duration = 3000) {
    return addToast(message, 'success', duration)
  }
  
  function error(message, duration = 4000) {
    return addToast(message, 'error', duration)
  }
  
  function info(message, duration = 3000) {
    return addToast(message, 'info', duration)
  }
  
  function warning(message, duration = 3000) {
    return addToast(message, 'warning', duration)
  }
  
  // Remove a toast by ID
  function removeToast(id) {
    const index = toasts.value.findIndex(toast => toast.id === id)
    if (index !== -1) {
      toasts.value.splice(index, 1)
    }
  }
  
  return {
    toasts,
    addToast,
    success,
    error,
    info,
    warning,
    removeToast
  }
}) 
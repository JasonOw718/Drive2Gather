import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../../services/api'
import { useToastStore } from '../../stores/toast'

// API base URL - Make sure this matches your backend configuration
const API_BASE_URL = 'http://localhost:5000/api'

export const useDriverStore = defineStore('driver', () => {
  // State
  const drivers = ref([])
  const loading = ref(false)
  const error = ref(null)
  
  // Getters
  const driversList = computed(() => drivers.value)
  
  // Actions
  async function fetchDrivers() {
    if (drivers.value.length > 0) return drivers.value
    
    loading.value = true
    error.value = null
    
    try {
      const response = await api.get('/auth/drivers')
      drivers.value = response.data
      return drivers.value
    } catch (error) {
      error.value = 'Failed to fetch drivers'
      return []
    } finally {
      loading.value = false
    }
  }
  
  async function fetchAllDrivers() {
      const toastStore = useToastStore()
    loading.value = true
    error.value = null
      
      try {
      const response = await api.get('/admin/drivers')
        
        if (response.data && response.data.drivers) {
          // Convert API drivers to the format expected by the frontend
          const apiDrivers = response.data.drivers.map(driver => ({
            id: driver.id,
            name: driver.name,
            email: driver.email,
            phone: driver.phone,
            carPlate: driver.car_number,
            carType: driver.car_type,
            seatAvailable: 2, // Default value
            status: 'activate', // Assume all drivers from API are activated
            avatar: '/src/assets/images/image.png', // Default avatar
            licenseImages: ['/src/assets/images/carphoto.jpg', '/src/assets/images/carphoto.jpg'], // Default images
            carPhotos: [
              '/src/assets/images/carphoto.jpg',
              '/src/assets/images/carphoto.jpg',
              '/src/assets/images/carphoto.jpg',
              '/src/assets/images/carphoto.jpg',
            ] // Default images
          }))
          
          // Replace mock data with API data while preserving any local changes
          // First keep any pending or rejected drivers (these might be local only)
        const pendingOrRejected = drivers.value.filter(d => d.status !== 'activate')
          
          // Then add the API drivers (all marked as activated)
        drivers.value = [...pendingOrRejected, ...apiDrivers]
        }
      } catch (error) {
        console.error('Failed to fetch drivers:', error)
      error.value = error.response?.data?.error || 'Failed to load drivers'
      toastStore.error(error.value)
      } finally {
      loading.value = false
      }
    }
  
  function approveDriver(id) {
    const driver = drivers.value.find(d => d.id === id)
    if (driver) driver.status = 'activate'
  }
  
  function rejectDriver(id) {
    const driver = drivers.value.find(d => d.id === id)
    if (driver) driver.status = 'rejected'
  }
  
  return {
    // State
    drivers,
    loading,
    error,
    
    // Getters
    driversList,
    
    // Actions
    fetchDrivers,
    fetchAllDrivers,
    approveDriver,
    rejectDriver
  }
}) 
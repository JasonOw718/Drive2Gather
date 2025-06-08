import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../services/api'
import { useToastStore } from './toast'

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
  
  function approveDriver(id) {
    const driver = drivers.value.find(d => d.id === id)
    if (driver) {
      driver.status = 'activate'
      
      // Call the backend API to update the driver status
      api.put(`${API_BASE_URL}/admin/drivers/${id}/status`, {
        status: 'approved'
      }).catch(error => {
        const toastStore = useToastStore()
        toastStore.error(`Failed to update driver status: ${error.response?.data?.error || error.message}`)
      })
    }
  }
  
  function rejectDriver(id) {
    const driver = drivers.value.find(d => d.id === id)
    if (driver) {
      driver.status = 'rejected'
      
      // Call the backend API to update the driver status
      api.put(`${API_BASE_URL}/admin/drivers/${id}/status`, {
        status: 'rejected'
      }).catch(error => {
        const toastStore = useToastStore()
        toastStore.error(`Failed to update driver status: ${error.response?.data?.error || error.message}`)
      })
    }
  }
  
  // New action to fetch all drivers from the API using the admin endpoint
  async function fetchAllDrivers(page = 1, perPage = 10, status = null) {
    const toastStore = useToastStore()
    loading.value = true
    error.value = null
    
    try {
      const params = { page, per_page: perPage }
      if (status) params.status = status
      
      const response = await api.get('/admin/drivers', { params })
      
      if (response.data && response.data.drivers) {
        // Convert API drivers to the format expected by the frontend
        const apiDrivers = response.data.drivers.map(driver => {
          // Map verification_status to UI status
          let uiStatus = 'pending'
          if (driver.verification_status === 'approved') uiStatus = 'activate'
          else if (driver.verification_status === 'rejected') uiStatus = 'rejected'
          
          return {
            id: driver.id,
            name: driver.name,
            email: driver.email,
            phone: driver.phone,
            carPlate: driver.car_number,
            carType: driver.car_type,
            carColor: driver.car_color,
            seatAvailable: 2, // Default value
            status: uiStatus, // Map from verification_status
            avatar: '/src/assets/images/image.png', // Default avatar
            licenseImages: ['/src/assets/images/carphoto.jpg', '/src/assets/images/carphoto.jpg'], // Default images
            carPhotos: [
              '/src/assets/images/carphoto.jpg',
              '/src/assets/images/carphoto.jpg',
              '/src/assets/images/carphoto.jpg',
              '/src/assets/images/carphoto.jpg',
            ] // Default images
          }
        })
        
        // Replace mock data with API data while preserving any local changes
        drivers.value = apiDrivers
        
        // Update pagination info
        this.pagination = {
          page: response.data.pagination.page,
          perPage: response.data.pagination.per_page,
          totalPages: response.data.pagination.total_pages,
          totalDrivers: response.data.pagination.total_drivers
        }
      }
    } catch (error) {
      console.error('Failed to fetch drivers:', error)
      error.value = error.response?.data?.error || 'Failed to load drivers'
      toastStore.error(error.value)
    } finally {
      loading.value = false
    }
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
    approveDriver,
    rejectDriver,
    fetchAllDrivers
  }
}) 
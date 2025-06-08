import { defineStore } from 'pinia'
import axios from 'axios'
import { useToastStore } from './toast'

// API base URL - Make sure this matches your backend configuration
const API_BASE_URL = 'http://localhost:5000/api'

export const useDriverStore = defineStore('driver', {
  state: () => ({
    drivers: [
      {
        id: 1,
        name: 'Ali Khan testtesttesttesttesttesttesttesttesttesttesttesttesttest',
        phone: '+923001234567',
        email: 'ali.khan@example.com',
        carPlate: 'ABC-1234',
        carType: 'Toyota Corolla',
        seatAvailable: 2,
        status: 'pending',
        avatar: '/src/assets/images/image.png',
        licenseImages: ['/src/assets/images/carphoto.jpg', '/src/assets/images/carphoto.jpg'],
        carPhotos: [
          '/src/assets/images/carphoto.jpg',
          '/src/assets/images/carphoto.jpg',
          '/src/assets/images/carphoto.jpg',
          '/src/assets/images/carphoto.jpg',
        ],
      },
      {
        id: 2,
        name: 'Sara Ahmed',
        phone: '+923004567890',
        email: 'sara.ahmed@example.com',
        carPlate: 'XYZ-5678',
        carType: 'Honda Civic',
        seatAvailable: 3,
        status: 'activate',
        avatar: '/src/assets/images/image.png',
        licenseImages: ['/src/assets/images/carphoto.jpg', '/src/assets/images/carphoto.jpg'],
        carPhotos: [
          '/src/assets/images/carphoto.jpg',
          '/src/assets/images/carphoto.jpg',
          '/src/assets/images/carphoto.jpg',
          '/src/assets/images/carphoto.jpg',
        ],
      },
      {
        id: 3,
        name: 'Bilal Sheikh',
        phone: '+923008765432',
        email: 'bilal.sheikh@example.com',
        carPlate: 'LMN-2468',
        carType: 'Suzuki Swift',
        seatAvailable: 1,
        status: 'rejected',
        avatar: '/src/assets/images/image.png',
        licenseImages: ['/src/assets/images/carphoto.jpg', '/src/assets/images/carphoto.jpg'],
        carPhotos: [
          '/src/assets/images/carphoto.jpg',
          '/src/assets/images/carphoto.jpg',
          '/src/assets/images/carphoto.jpg',
          '/src/assets/images/carphoto.jpg',
        ],
      },
      // Add more mock drivers as needed
    ],
    isLoading: false,
    error: null,
    pagination: {
      page: 1,
      perPage: 10,
      totalPages: 1,
      totalDrivers: 0
    }
  }),
  actions: {
    approveDriver(id) {
      const driver = this.drivers.find(d => d.id === id)
      if (driver) {
        driver.status = 'activate'
        
        // Call the backend API to update the driver status
        axios.put(`${API_BASE_URL}/admin/drivers/${id}/status`, {
          status: 'approved'
        }).catch(error => {
          const toastStore = useToastStore()
          toastStore.error(`Failed to update driver status: ${error.response?.data?.error || error.message}`)
        })
      }
    },
    
    rejectDriver(id) {
      const driver = this.drivers.find(d => d.id === id)
      if (driver) {
        driver.status = 'rejected'
        
        // Call the backend API to update the driver status
        axios.put(`${API_BASE_URL}/admin/drivers/${id}/status`, {
          status: 'rejected'
        }).catch(error => {
          const toastStore = useToastStore()
          toastStore.error(`Failed to update driver status: ${error.response?.data?.error || error.message}`)
        })
      }
    },
    
    // New action to fetch all drivers from the API using the admin endpoint
    async fetchAllDrivers(page = 1, perPage = 10, status = null) {
      const toastStore = useToastStore()
      this.isLoading = true
      this.error = null
      
      try {
        const params = { page, per_page: perPage }
        if (status) params.status = status
        
        const response = await axios.get(`${API_BASE_URL}/admin/drivers`, { params })
        
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
          this.drivers = apiDrivers
          
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
        this.error = error.response?.data?.error || 'Failed to load drivers'
        toastStore.error(this.error)
      } finally {
        this.isLoading = false
      }
    }
  }
}) 
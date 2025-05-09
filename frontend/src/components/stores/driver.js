import { defineStore } from 'pinia'

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
    ]
  }),
  actions: {
    approveDriver(id) {
      const driver = this.drivers.find(d => d.id === id)
      if (driver) driver.status = 'activate'
    },
    rejectDriver(id) {
      const driver = this.drivers.find(d => d.id === id)
      if (driver) driver.status = 'rejected'
    }
  }
}) 
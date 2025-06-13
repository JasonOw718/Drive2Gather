import { defineStore } from 'pinia'
import { io } from 'socket.io-client'
import { useUserStore } from './user'

export const useSocketStore = defineStore('socket', {
  state: () => ({
    socket: null,
    isConnected: false,
    rideUpdates: []
  }),

  actions: {
    initializeSocket() {
      if (this.socket) {
        console.log('Disconnecting existing socket connection')
        this.socket.disconnect()
      }

      const userStore = useUserStore()
      const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'
      console.log('Initializing socket connection to:', API_URL)

      // Connect to the WebSocket server
      this.socket = io(API_URL, {
        transports: ['websocket'],
        auth: {
          token: userStore.token
        }
      })

      // Socket event handlers
      this.socket.on('connect', () => {
        console.log('Connected to WebSocket server')
        this.isConnected = true
        this.joinRidesRoom()
      })

      this.socket.on('disconnect', () => {
        console.log('Disconnected from WebSocket server')
        this.isConnected = false
      })

      this.socket.on('connect_error', (error) => {
        console.error('Socket connection error:', error)
        this.isConnected = false
      })

      // Handle new ride updates
      this.socket.on('new_ride', (rideData) => {
        console.log('New ride received:', rideData)
        this.rideUpdates.push(rideData)
      })
    },

    joinRidesRoom() {
      if (this.socket && this.isConnected) {
        console.log('Joining rides room')
        this.socket.emit('join_rides')
      } else {
        console.warn('Cannot join rides room: socket not connected')
      }
    },

    leaveRidesRoom() {
      if (this.socket && this.isConnected) {
        console.log('Leaving rides room')
        this.socket.emit('leave_rides')
      }
    },

    disconnect() {
      if (this.socket) {
        console.log('Disconnecting socket')
        this.socket.disconnect()
        this.socket = null
        this.isConnected = false
      }
    }
  }
}) 
import { defineStore } from 'pinia'

export const usePassengerInputStore = defineStore('passengerInput', {
  state: () => ({
    from: '',
    to: '',
    time: '',
    seats: 1
  }),
  actions: {
    setInput({ from, to, time, seats }) {
      this.from = from
      this.to = to
      this.time = time
      this.seats = seats
    }
  }
}) 
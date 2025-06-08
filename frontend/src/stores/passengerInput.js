import { defineStore } from 'pinia'

export const usePassengerInputStore = defineStore('passengerInput', {
  state: () => ({
    from: '',
    to: '',
    seats: 1
  }),
  actions: {
    setInput({ from, to, seats }) {
      this.from = from
      this.to = to
      this.seats = seats
    }
  }
}) 
import { defineStore } from 'pinia'

export const usePassengerInputStore = defineStore('passengerInput', {
  state: () => ({
    from: '',
    to: '',
    date: '',
    time: '',
    seats: 1,
    dateTime: ''
  }),
  actions: {
    setInput({ from, to, date, time, seats, dateTime }) {
      this.from = from
      this.to = to
      this.date = date
      this.time = time
      this.seats = seats
      this.dateTime = dateTime || `${date}T${time}:00`
    }
  }
}) 
import { defineStore } from 'pinia'

export const useReportStore = defineStore('report', {
  state: () => ({
    reports: [
      {
        id: 1,
        driverName: 'Ali Khan',
        issue: 'Late arrival',
        date: '2024-06-01',
        status: 'pending',
        details: 'Driver arrived 20 minutes late to the pickup location.'
      },
      {
        id: 2,
        driverName: 'Sara Ahmed',
        issue: 'Rude behavior',
        date: '2024-06-02',
        status: 'resolved',
        details: 'Driver was rude to the passenger during the ride.'
      },
      {
        id: 3,
        driverName: 'Bilal Sheikh',
        issue: 'Unsafe driving',
        date: '2024-06-03',
        status: 'pending',
        details: 'Driver was speeding and ignored traffic signals.'
      }
    ]
  }),
  actions: {
    getReportById(id) {
      return this.reports.find(r => r.id === parseInt(id))
    }
  }
}) 
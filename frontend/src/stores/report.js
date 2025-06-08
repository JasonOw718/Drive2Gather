import { defineStore } from 'pinia'
import { useToastStore } from './toast'
import { useAdminAuthStore } from './adminAuth'
import { feedbackService } from '../services/api'

// API base URL - Make sure this matches your backend configuration
const API_BASE_URL = 'http://localhost:5000/api'

export const useReportStore = defineStore('report', {
  state: () => ({
    reports: [],
    isLoading: false,
    error: null
  }),
  actions: {
    async fetchReports() {
      this.isLoading = true;
      this.error = null;
      const toastStore = useToastStore();
      
      try {
        const response = await feedbackService.getAllFeedback();
        
        if (response.data && response.data.feedbacks) {
          // Transform the feedback data into the format expected by the frontend
          this.reports = response.data.feedbacks.map(feedback => ({
            id: feedback.feedback_id,
            rideId: feedback.ride_id,
            driverName: feedback.driver_name || `Driver ID: ${feedback.driver_id}`,
            passengerName: feedback.passenger_name || `User ID: ${feedback.user_id}`,
            issue: feedback.issue_type,
            comments: feedback.comments,
            date: new Date(feedback.comment_time).toLocaleDateString(),
            timestamp: feedback.comment_time,
            userId: feedback.user_id
          }));
        }
      } catch (error) {
        console.error('Failed to fetch reports:', error);
        this.error = error.response?.data?.error || 'Failed to load reports';
        toastStore.error(this.error);
      } finally {
        this.isLoading = false;
      }
    },
    
    getReportById(id) {
      return this.reports.find(r => r.id === parseInt(id));
    }
  }
}) 
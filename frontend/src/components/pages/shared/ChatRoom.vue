<template>
  <div class="min-h-screen bg-white px-6 pt-[max(2.5rem,env(safe-area-inset-top))] pb-[max(env(safe-area-inset-bottom),2.5rem)] flex flex-col" style="max-width: 420px; margin: 0 auto; font-family: 'Poppins', sans-serif;">
    <!-- Header -->
    <div class="flex items-center justify-between mt-4 mb-4">
      <button @click="$router.back()" class="mt-4 absolute top-4 left-4 w-10 h-10 flex items-center justify-center rounded-lg bg-[#F5F5F5] z-20 border border-gray-200">
        <font-awesome-icon icon="fa-arrow-left" class="text-[#C77DFF] text-2xl" />
      </button>
      <div class="text-2xl font-bold text-center flex-1 mt-8" style="font-family: 'Poppins', sans-serif; font-weight: 500;">Chat Room</div>
    </div>

    <!-- Ride Details Banner -->
    <div class="bg-gradient-to-r from-purple-100 to-pink-50 rounded-lg p-3 mb-6 shadow-sm">
      <div class="text-sm text-gray-700 font-medium text-center flex items-center justify-center">
        <span class="mr-2 text-[#C77DFF]">
          <font-awesome-icon icon="fa-route" />
        </span>
        {{ rideDetails.startingLocation }} 
        <span class="mx-2 text-[#C77DFF]">
          <font-awesome-icon icon="fa-arrow-right" />
        </span> 
        {{ rideDetails.dropoffLocation }}
      </div>
    </div>

    <!-- Loading state -->
    <div v-if="loading" class="flex justify-center items-center h-64">
      <svg class="animate-spin h-12 w-12 text-[#C77DFF]" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"></path>
      </svg>
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="text-center text-red-500 mt-10 p-4 bg-red-50 rounded-lg">
      <font-awesome-icon icon="fa-exclamation-circle" class="mr-2" />
      {{ error }}
      <button @click="loadChatData" class="block mx-auto mt-4 text-[#C77DFF] font-medium hover:underline px-4 py-2 rounded-lg hover:bg-purple-50 transition-colors">
        <font-awesome-icon icon="fa-sync" class="mr-2" />
        Try Again
      </button>
    </div>

    <div v-else class="flex flex-col flex-1">
      <!-- Chat messages -->
      <div class="flex-1 overflow-y-auto mb-4 px-1" ref="messagesContainer">
        <div v-if="messages.length === 0" class="text-center text-gray-500 mt-10 p-6 bg-gray-50 rounded-lg">
          <font-awesome-icon icon="fa-comments" class="text-3xl text-gray-300 mb-3" />
          <div>No messages yet. Start the conversation!</div>
        </div>
        <div v-else class="space-y-4 py-2">
          <div v-for="message in messages" :key="message.message_id" 
               :class="[
                 'max-w-[80%] p-3 rounded-lg shadow-sm transition-all duration-200 animate-fadeIn', 
                 message.user_id === currentUserId ? 
                   'ml-auto bg-gradient-to-br from-[#C77DFF] to-[#B266FF] text-white rounded-tr-none' : 
                   'mr-auto bg-gray-100 text-gray-800 rounded-tl-none'
               ]">
            <div class="text-xs mb-1 font-medium" :class="message.user_id === currentUserId ? 'text-white/90' : 'text-gray-500'">
              {{ message.username }}
            </div>
            <div class="text-sm leading-relaxed">{{ message.content }}</div>
            <div class="text-xs text-right mt-1 opacity-80" :class="message.user_id === currentUserId ? 'text-white/80' : 'text-gray-500'">
              {{ formatTime(message.send_time) }}
            </div>
          </div>
        </div>
      </div>

      <!-- Message input -->
      <div class="border-t border-gray-100 pt-4 pb-2 bg-white shadow-lg rounded-t-xl">
        <div v-if="sendError" class="text-red-500 text-sm mb-2 px-2 py-1 bg-red-50 rounded-lg flex items-center">
          <font-awesome-icon icon="fa-exclamation-circle" class="mr-2" />
          {{ sendError }}
          <button @click="sendError = null" class="text-red-700 ml-auto hover:underline">
            <font-awesome-icon icon="fa-times" />
          </button>
        </div>
        <div class="flex items-center">
          <input 
            v-model="newMessage" 
            type="text" 
            placeholder="Type a message..." 
            class="flex-1 border border-gray-200 bg-white rounded-full py-3 px-4 focus:outline-none focus:ring-2 focus:ring-[#C77DFF] shadow-sm text-gray-700"
            @keyup.enter="sendMessage"
          />
          <button 
            @click="sendMessage" 
            class="ml-2 w-12 h-12 rounded-full bg-gradient-to-r from-[#C77DFF] to-[#B266FF] flex items-center justify-center shadow-md hover:shadow-lg transition-all duration-200 transform hover:scale-105"
            :disabled="!newMessage.trim()"
            :class="{'opacity-50': !newMessage.trim()}"
          >
            <font-awesome-icon icon="fa-paper-plane" class="text-white" />
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, nextTick, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '../../../stores/user'
import { chatService, rideService } from '../../../services/api'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

// Get ride ID from route params
const rideId = computed(() => route.params.id)

// Reactive state
const loading = ref(true)
const error = ref(null)
const sendError = ref(null)
const chatId = ref(null)
const messages = ref([])
const newMessage = ref('')
const rideDetails = ref({})
const messagesContainer = ref(null)

// Get current user ID
const currentUserId = computed(() => {
  const user = JSON.parse(localStorage.getItem('user') || '{}')
  return user.id || user.user_id
})

// Load chat data
async function loadChatData() {
  loading.value = true
  error.value = null
  
  try {
    // Get ride details
    const rideResponse = await rideService.getRideById(rideId.value)
    rideDetails.value = rideResponse.data
    
    // Get or create chat for this ride
    const chatResponse = await chatService.getChatByRideId(rideId.value)
    chatId.value = chatResponse.data.chat_id
    
    // Get chat messages
    await loadMessages()
    
    // Set up polling for new messages
    startMessagePolling()
  } catch (err) {
    console.error('Error loading chat data:', err)
    error.value = 'Failed to load chat. Please try again.'
  } finally {
    loading.value = false
  }
}

// Load messages
async function loadMessages() {
  if (!chatId.value) return
  
  try {
    const response = await chatService.getMessages(chatId.value)
    messages.value = response.data.messages
    
    // Scroll to bottom after messages load
    await nextTick()
    scrollToBottom()
  } catch (err) {
    console.error('Error loading messages:', err)
  }
}

// Send a new message
async function sendMessage() {
  if (!newMessage.value.trim() || !chatId.value) return
  
  try {
    // Make sure we have a valid token
    const token = localStorage.getItem('token')
    if (!token) {
      sendError.value = 'You need to be logged in to send messages'
      return
    }
    
    const response = await chatService.sendMessage(chatId.value, newMessage.value)
    messages.value.push(response.data)
    newMessage.value = ''
    
    // Scroll to bottom after sending
    await nextTick()
    scrollToBottom()
  } catch (err) {
    console.error('Error sending message:', err)
    
    // Check if it's an authentication error
    if (err.response && err.response.status === 401) {
      sendError.value = 'Authentication error. Please refresh the page and try again.'
    } else {
      sendError.value = err.response?.data?.error || 'Failed to send message. Please try again.'
    }
  }
}

// Format time from ISO string (HH:MM)
function formatTime(isoTime) {
  if (!isoTime) return ''
  const date = new Date(isoTime)
  return `${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`
}

// Scroll to bottom of messages container
function scrollToBottom() {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

// Poll for new messages
let messagePollingInterval = null
function startMessagePolling() {
  // Clear any existing interval
  if (messagePollingInterval) {
    clearInterval(messagePollingInterval)
  }
  
  // Set up new interval to check for messages every 5 seconds
  messagePollingInterval = setInterval(async () => {
    if (!chatId.value) return
    
    try {
      const response = await chatService.getMessages(chatId.value)
      if (response.data.messages.length > messages.value.length) {
        messages.value = response.data.messages
        
        // Scroll to bottom if new messages
        await nextTick()
        scrollToBottom()
      }
    } catch (err) {
      console.error('Error polling messages:', err)
    }
  }, 5000)
}

// Clean up on component unmount
onMounted(() => {
  loadChatData()
})

// Watch for changes to messages and scroll to bottom
watch(messages, async () => {
  await nextTick()
  scrollToBottom()
})
</script>

<style scoped>
/* Add custom scrollbar styling */
.overflow-y-auto {
  scrollbar-width: thin;
  scrollbar-color: #C77DFF transparent;
  max-height: calc(100vh - 250px);
}

.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: transparent;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background-color: #C77DFF;
  border-radius: 20px;
}

/* Animation for new messages */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.animate-fadeIn {
  animation: fadeIn 0.3s ease-out;
}
</style> 
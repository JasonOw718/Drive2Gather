import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import './assets/main.css';
import router from './router' 
import { createPinia } from 'pinia'

import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { registerIcons } from './fontawesome'
import { useUserStore } from './stores/user'
import { useAdminAuthStore } from './stores/adminAuth'

registerIcons()

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

// Initialize authentication state before mounting the app
const userStore = useUserStore(pinia)
userStore.initializeAuth()

// Initialize admin authentication state
const adminAuthStore = useAdminAuthStore(pinia)
adminAuthStore.initializeAdminAuth()

app.component('font-awesome-icon', FontAwesomeIcon)
app.mount('#app')

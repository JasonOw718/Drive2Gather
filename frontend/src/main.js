import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import './assets/main.css';
import router from './router' 
import { createPinia } from 'pinia'

import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { registerIcons } from './fontawesome'

registerIcons()

const app = createApp(App)
app.use(createPinia()) 
app.use(router)
app.component('font-awesome-icon', FontAwesomeIcon)
app.mount('#app')

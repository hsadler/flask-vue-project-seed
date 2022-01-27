import { createApp } from 'vue'
import App from './App.vue'

import services from '@/services'
import httpService from '@/services/httpService'

import router from '@/router'

services.registerServices({
  httpService
})

const app = createApp(App)
app.use(router)
app.mount('#app')

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createHead } from '@vueuse/head'
import router from './router'
import App from './App.vue'
import './assets/styles/main.css'
import { useAuthStore } from './stores/auth'

const app = createApp(App)
const pinia = createPinia()
const head = createHead()

app.use(pinia)
app.use(router)
app.use(head)

const auth = useAuthStore()
auth.restoreSession().finally(() => {
  app.mount('#app')
})

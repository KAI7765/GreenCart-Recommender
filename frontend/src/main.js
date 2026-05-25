import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

console.log('main.js loaded')
const app = createApp(App)
console.log('App created')
app.use(router)
console.log('Router added')
app.mount('#app')
console.log('App mounted')
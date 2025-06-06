import { createRouter, createWebHistory } from 'vue-router'
import HomePage from './Home.vue'
import Customsimulation from './Customsimulation.vue'

const routes = [
  { path: '/', component: HomePage },
  { path: '/create', component: Customsimulation }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router

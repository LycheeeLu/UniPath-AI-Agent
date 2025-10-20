import { createRouter, createWebHistory } from 'vue-router'
import UploadView from '../views/UploadView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'upload', component: UploadView }
  ]
})

export default router

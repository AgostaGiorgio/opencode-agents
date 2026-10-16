import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '@/views/DashboardView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: DashboardView,
    },
    {
      path: '/about',
      name: 'about',
      // Non-initial views are lazy-loaded.
      component: () => import('@/views/AboutView.vue'),
    },
  ],
  scrollBehavior() {
    return { top: 0 }
  },
})

export default router

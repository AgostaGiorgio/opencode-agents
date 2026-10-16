<script setup>
import { useRoute } from 'vue-router'
import { Home, Info } from '@lucide/vue'

const route = useRoute()

const items = [
  { to: '/', label: 'Home', icon: Home },
  { to: '/about', label: 'About', icon: Info },
]

const isActive = (to) => (to === '/' ? route.path === '/' : route.path.startsWith(to))
</script>

<template>
  <!-- Mobile/tablet: horizontal bottom bar · Desktop: vertical rail on the left, centered -->
  <nav
    class="fixed z-50 bg-brand-surface/70 backdrop-blur-xl border border-white/10 shadow-app rounded-[24px]
           left-1/2 -translate-x-1/2 bottom-[calc(1rem+env(safe-area-inset-bottom))] w-[calc(100%-2rem)] max-w-md
           lg:left-6 lg:bottom-auto lg:top-1/2 lg:translate-x-0 lg:-translate-y-1/2 lg:w-auto lg:max-w-none"
  >
    <div class="flex justify-around items-center p-3 lg:flex-col lg:justify-center lg:gap-4 lg:px-2 lg:py-4">
      <RouterLink
        v-for="item in items"
        :key="item.to"
        :to="item.to"
        class="flex flex-col items-center gap-1 px-2 py-0.5 lg:py-2.5 transition-colors duration-200"
        :class="isActive(item.to) ? 'text-brand-primary' : 'text-brand-textMuted'"
      >
        <component :is="item.icon" :size="21" :stroke-width="isActive(item.to) ? 2.5 : 2" />
        <span class="text-[10px] font-medium tracking-wide">{{ item.label }}</span>
      </RouterLink>
    </div>
  </nav>
</template>

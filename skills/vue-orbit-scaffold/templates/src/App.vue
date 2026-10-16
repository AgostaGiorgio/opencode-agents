<script setup>
import AppHeader from '@/components/AppHeader.vue'
import AppNavbar from '@/components/AppNavbar.vue'
import ToastHost from '@/components/ui/ToastHost.vue'
</script>

<template>
  <div
    class="min-h-screen bg-brand-background flex flex-col items-center text-brand-textMain font-sans pb-36 lg:pb-8 selection:bg-brand-primary selection:text-white"
  >
    <AppHeader />

    <div class="w-full lg:pl-28">
      <RouterView v-slot="{ Component }">
        <component :is="Component" />
      </RouterView>
    </div>

    <AppNavbar />
    <ToastHost />
  </div>
</template>

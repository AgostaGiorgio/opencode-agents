<script setup>
import { Settings } from '@lucide/vue'
</script>

<template>
  <header class="w-full flex justify-between items-center mb-2 px-5 mt-8">
    <div class="text-2xl font-extrabold tracking-tighter cursor-default">
      <span class="text-brand-textMain">__APP_NAME__</span><span class="text-brand-primary">.</span>
    </div>

    <RouterLink
      to="/about"
      title="About"
      aria-label="About"
      class="w-10 h-10 rounded-full bg-brand-surface border border-white/10 flex items-center justify-center shadow-sm hover:bg-brand-surface/80 transition-colors text-brand-textMuted"
    >
      <Settings :size="18" />
    </RouterLink>
  </header>
</template>

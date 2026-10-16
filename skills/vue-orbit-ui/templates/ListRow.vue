<script setup>
import Money from './Money.vue'
import { stringToColor } from '@/utils/stringToColor'

const props = defineProps({
  title: { type: String, required: true },
  subtitle: { type: String, default: '' },
  value: { type: [Number, String], default: null },
  icon: { type: String, default: null },
})

const initial = () => (props.title || '?').charAt(0).toUpperCase()
const tint = stringToColor(props.title)
</script>

<template>
  <div class="flex items-center gap-3 px-3 py-3">
    <span
      class="w-10 h-10 rounded-full flex items-center justify-center shrink-0 overflow-hidden"
      :style="{ backgroundColor: tint + '22', color: tint }"
    >
      <img v-if="icon" :src="icon" :alt="title" class="w-full h-full object-cover" />
      <span v-else class="font-bold text-sm">{{ initial() }}</span>
    </span>

    <div class="flex-1 min-w-0">
      <p class="text-sm font-semibold text-brand-textMain truncate">{{ title }}</p>
      <p v-if="subtitle" class="text-xs text-brand-textMuted truncate">{{ subtitle }}</p>
    </div>

    <div v-if="value !== null" class="text-sm font-semibold text-brand-textMain shrink-0">
      <Money :value="value" />
    </div>
  </div>
</template>

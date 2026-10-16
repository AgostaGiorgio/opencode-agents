<script setup>
import { computed } from 'vue'
import Money from './Money.vue'
import PnLValue from './PnLValue.vue'
import { formatPct, toNumber } from '@/utils/format'
import { trendClass } from '@/utils/trend'

const props = defineProps({
  label: { type: String, default: '' },
  total: { type: [Number, String], default: 0 },
  changeEur: { type: [Number, String], default: null },
  changePct: { type: [Number, String], default: null },
  monthPct: { type: [Number, String], default: null },
})

const hasMonth = computed(() => toNumber(props.monthPct) !== null)
const monthClass = computed(() => trendClass(props.monthPct))
</script>

<template>
  <div class="flex flex-col gap-2">
    <p v-if="label" class="text-[11px] uppercase tracking-wider font-semibold text-brand-textMuted">
      {{ label }}
    </p>
    <div class="flex items-start justify-between gap-3">
      <div class="text-4xl font-extrabold tracking-tighter">
        <Money :value="total" />
      </div>
      <span
        v-if="hasMonth"
        class="text-xs font-semibold mt-1.5 shrink-0"
        :class="monthClass"
        title="vs last month"
      >
        {{ formatPct(monthPct) }}
      </span>
    </div>
    <PnLValue :pl-eur="changeEur" :pct="changePct" size="md" />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useSensitiveVisibility } from '@/composables/useSensitiveVisibility'
import { formatMoney, formatPct, toNumber } from '@/utils/format'
import { trendClass, trendIcon } from '@/utils/trend'

const props = defineProps({
  plEur: { type: [Number, String], default: null },
  pct: { type: [Number, String], default: null },
  showAmount: { type: Boolean, default: true },
  size: { type: String, default: 'sm' }, // sm | md
})

const { isSensitiveHidden } = useSensitiveVisibility()

const hasPct = computed(() => toNumber(props.pct) !== null)
const hasAmount = computed(() => toNumber(props.plEur) !== null)
const hasData = computed(() => hasPct.value || hasAmount.value)

const metric = computed(() => toNumber(props.plEur) ?? toNumber(props.pct) ?? null)
const colorClass = computed(() => trendClass(metric.value))
const icon = computed(() => trendIcon(metric.value))
const amountClass = computed(() => (props.size === 'md' ? 'text-base' : 'text-sm'))
</script>

<template>
  <span v-if="hasData" class="inline-flex items-center gap-1 font-semibold" :class="colorClass">
    <component :is="icon" v-if="icon" :size="props.size === 'md' ? 16 : 13" />
    <span :class="amountClass">
      <template v-if="hasPct">{{ formatPct(pct) }}</template>
      <template v-if="showAmount && hasAmount">
        <span class="text-brand-textMuted font-medium ml-1">
          {{ isSensitiveHidden ? '€ ••••' : formatMoney(plEur) }}
        </span>
      </template>
    </span>
  </span>
  <span v-else class="text-brand-textMuted text-sm">—</span>
</template>

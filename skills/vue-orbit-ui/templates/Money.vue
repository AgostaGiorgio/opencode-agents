<script setup>
import { computed } from 'vue'
import { useSensitiveVisibility } from '@/composables/useSensitiveVisibility'
import { formatMoney, formatMoneySigned } from '@/utils/format'

const props = defineProps({
  value: { type: [Number, String], default: null },
  decimals: { type: Number, default: 2 },
  signed: { type: Boolean, default: false },
  mask: { type: String, default: '€ ••••' },
})

const { isSensitiveHidden } = useSensitiveVisibility()
const display = computed(() =>
  isSensitiveHidden.value
    ? props.mask
    : props.signed
      ? formatMoneySigned(props.value, props.decimals)
      : formatMoney(props.value, props.decimals),
)
</script>

<template>
  <span>{{ display }}</span>
</template>

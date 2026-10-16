<script setup>
import { ref, computed } from 'vue'
import { Wallet } from '@lucide/vue'
import { useMediaQuery } from '@/composables/useMediaQuery'
import { useToast } from '@/composables/useToast'
import SegmentedControl from '@/components/ui/SegmentedControl.vue'
import EmptyState from '@/components/ui/EmptyState.vue'
import { formatMoney, formatPct } from '@/utils/format'
import { trendClass } from '@/utils/trend'

const isDesktop = useMediaQuery('(min-width: 1024px)')
const toast = useToast()

const period = ref('3m')
const periodOptions = [
  { value: '3m', label: '3M' },
  { value: '6m', label: '6M' },
  { value: '12m', label: '12M' },
  { value: 'all', label: 'All' },
]

// Static sample data — replace with real API calls (see src/services/api.js).
const summary = ref({ total: 12450.5, changePct: 3.42 })
const items = ref([
  { id: 1, name: 'Checking account', value: 8200, pct: 1.1 },
  { id: 2, name: 'Savings', value: 3050.5, pct: -0.4 },
  { id: 3, name: 'Investments', value: 1200, pct: 6.7 },
])

const empty = computed(() => items.value.length === 0)
</script>

<template>
  <main class="w-full px-4">
    <div class="py-3 flex flex-col gap-5 w-full">
      <div class="w-full lg:pr-28">
        <div class="w-full max-w-sm mx-auto">
          <SegmentedControl v-model="period" :options="periodOptions" />
        </div>
      </div>

      <!-- Mobile: stacked cards · Desktop: two cards side by side -->
      <div :class="isDesktop ? 'grid grid-cols-[2fr_1fr] gap-5' : 'flex flex-col gap-5'">
        <section class="app-card rounded-app p-5 flex flex-col gap-2">
          <p class="text-[11px] uppercase tracking-wider font-semibold text-brand-textMuted">Total</p>
          <div class="flex items-start justify-between gap-3">
            <div class="text-4xl font-extrabold tracking-tighter">{{ formatMoney(summary.total) }}</div>
            <span class="text-xs font-semibold mt-1.5 shrink-0" :class="trendClass(summary.changePct)">
              {{ formatPct(summary.changePct) }}
            </span>
          </div>
        </section>

        <section class="app-card rounded-app p-5 flex flex-col gap-3">
          <p class="text-[11px] uppercase tracking-wider font-semibold text-brand-textMuted">Breakdown</p>
          <button
            v-for="item in items"
            :key="item.id"
            type="button"
            class="flex items-center justify-between gap-3 text-left"
            @click="toast.info(`Selected ${item.name}`)"
          >
            <span class="text-sm text-brand-textMain">{{ item.name }}</span>
            <span class="text-sm font-semibold" :class="trendClass(item.pct)">{{
              formatMoney(item.value)
            }}</span>
          </button>
        </section>
      </div>

      <EmptyState
        v-if="empty"
        :icon="Wallet"
        title="No data yet"
        description="Connect the API and add your first entry."
      />
    </div>
  </main>
</template>

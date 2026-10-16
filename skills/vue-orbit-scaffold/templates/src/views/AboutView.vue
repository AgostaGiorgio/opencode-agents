<script setup>
import { ref } from 'vue'
import { useToast } from '@/composables/useToast'
import BottomSheet from '@/components/ui/BottomSheet.vue'
import Field from '@/components/ui/Field.vue'

const toast = useToast()
const sheetOpen = ref(false)
const name = ref('')

const save = () => {
  toast.success('Saved')
  sheetOpen.value = false
}
</script>

<template>
  <main class="w-full px-4">
    <div class="py-3 flex flex-col gap-5 w-full lg:pr-28">
      <section class="app-card rounded-app p-5 flex flex-col gap-3">
        <h1 class="text-xl font-bold">About __APP_NAME__</h1>
        <p class="text-sm text-brand-textMuted">
          Sample view showing the card + form-sheet pattern. Replace it with the real pages.
        </p>
        <button
          type="button"
          class="self-start h-10 px-4 rounded-full bg-brand-primary text-white text-xs font-bold shadow-lg shadow-brand-primary/20 hover:bg-brand-secondary active:scale-95 transition-all"
          @click="sheetOpen = true"
        >
          Open form
        </button>
      </section>
    </div>

    <BottomSheet :open="sheetOpen" title="Example form" @close="sheetOpen = false">
      <Field
        v-model="name"
        label="Name"
        placeholder="Type something"
        hint="Demonstrates the Field + BottomSheet pattern"
      />
      <template #footer>
        <button
          type="button"
          class="w-full h-11 rounded-app-sm bg-brand-primary text-white text-sm font-bold active:scale-[0.98] transition-all"
          @click="save"
        >
          Save
        </button>
      </template>
    </BottomSheet>
  </main>
</template>

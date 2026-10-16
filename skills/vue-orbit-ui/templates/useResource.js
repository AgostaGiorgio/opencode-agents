import { ref } from 'vue'

// Minimal async resource: data + loading + error, with a reload().
// Keeps every view consistent instead of hand-rolling flags.
export function useResource(fetcher, { immediate = false } = {}) {
  const data = ref(null)
  const loading = ref(false)
  const error = ref(null)

  const load = async (...args) => {
    loading.value = true
    error.value = null
    try {
      data.value = await fetcher(...args)
      return data.value
    } catch (e) {
      error.value = e
      throw e
    } finally {
      loading.value = false
    }
  }

  if (immediate) load()

  return { data, loading, error, load }
}

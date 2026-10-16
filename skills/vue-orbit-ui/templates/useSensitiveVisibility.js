import { ref } from 'vue'

// Global "hide sensitive values" toggle. Module-level ref => shared singleton,
// optionally persisted in localStorage.
const STORAGE_KEY = 'app_sensitive_hidden'

const isSensitiveHidden = ref(false)

try {
  const stored = localStorage.getItem(STORAGE_KEY)
  if (stored !== null) isSensitiveHidden.value = stored === 'true'
} catch {
  // localStorage unavailable (SSR, privacy mode): keep the in-memory default.
}

function toggleSensitiveHidden() {
  isSensitiveHidden.value = !isSensitiveHidden.value
  try {
    localStorage.setItem(STORAGE_KEY, String(isSensitiveHidden.value))
  } catch {
    // ignore persistence errors
  }
}

export function useSensitiveVisibility() {
  return { isSensitiveHidden, toggleSensitiveHidden }
}

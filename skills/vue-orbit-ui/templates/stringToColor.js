// Deterministic accent color from a string (names, categories, tags).
// Same input -> same color, stable across renders. Returns a hex string so it
// can be used directly with the Badge component (color + '22' alpha).

const PALETTE = [
  '#8b5cf6', // primary (violet)
  '#f59e0b', // amber
  '#10b981', // emerald
  '#3b82f6', // blue
  '#ef4444', // red
  '#ec4899', // pink
  '#14b8a6', // teal
  '#eab308', // yellow
  '#6366f1', // indigo
  '#f97316', // orange
]

export function stringToColor(str = '') {
  let hash = 0
  for (let i = 0; i < str.length; i++) {
    hash = (hash * 31 + str.charCodeAt(i)) | 0
  }
  return PALETTE[Math.abs(hash) % PALETTE.length]
}

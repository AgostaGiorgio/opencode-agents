# Stack & conventions

Deep detail behind `vue-orbit-scaffold`. Read when bootstrapping or when deciding
how to grow the generated frontend.

## File tree

```
<frontend>/
├── index.html                  # PWA head: manifest, theme-color, apple meta
├── package.json                # scripts (dev/build/preview/lint/format) + deps
├── vite.config.js              # vue + devtools plugins, '@' alias, assetsDir: static
├── tailwind.config.js          # presets: [orbitEcosystemPreset]
├── postcss.config.js
├── orbit-ecosystem-preset.js   # shared theme (identical in every project)
├── jsconfig.json               # '@/*' -> './src/*'
├── .editorconfig .prettierrc.json .oxlintrc.json eslint.config.js .gitignore
├── .env / .env.example / .env.development   # VITE_API_BASE_URL
├── Dockerfile                  # build (node) -> nginx
├── nginx.conf                  # SPA fallback + cache for /static/
├── public/
│   ├── manifest.json
│   ├── favicon.png icon-192.png icon-512.png
│   └── <app>-logo.png
└── src/
    ├── main.js
    ├── App.vue
    ├── style.css
    ├── router/index.js
    ├── services/api.js
    ├── composables/{useToast,useMediaQuery}.js
    ├── components/
    │   ├── AppHeader.vue
    │   ├── AppNavbar.vue
    │   └── ui/{BottomSheet,Field,SelectField,SegmentedControl,Badge,EmptyState,Skeleton,ToastHost}.vue
    └── views/{DashboardView,AboutView}.vue
```

## Design tokens (Orbit Ecosystem)

| Token | Value | Use |
| --- | --- | --- |
| `brand-background` | `#0f172a` | page background |
| `brand-surface` | `#1e293b` | cards, sheets, navbar |
| `brand-primary` | `#8b5cf6` | accents, active state, CTAs |
| `brand-secondary` | `#c084fc` | hover/accent |
| `brand-textMain` | `#f8fafc` | primary text |
| `brand-textMuted` | `#94a3b8` | secondary text |
| `rounded-app` | `24px` | cards, navbars, sheets (top) |
| `rounded-app-sm` | `12px` | inputs, badges, small surfaces |
| `shadow-app` | layered dark shadow | floating surfaces |
| `font-app-title` / `font-app-body` | 2rem/700 · 1rem/500 | display text |

Semantic colors (not in the preset, used directly as Tailwind classes):
positive `text-emerald-400`, negative `text-red-400`, neutral `text-brand-textMuted`.

## Layout shell

`App.vue` is a column: `min-h-screen bg-brand-background text-brand-textMain font-sans`
plus bottom padding to clear the navbar (`pb-24`/`pb-36 lg:pb-8`), then:

```
AppHeader        # brand (two-tone) + primary action + action buttons
RouterView       # page content (wrapped in lg:pl-28 when a left rail exists)
AppNavbar        # bottom bar (mobile) / left rail (desktop)
ToastHost        # global toasts (Teleport)
```

`AppNavbar` (myInves style, the recommended one):

- mobile: fixed bottom, centered, `w-[calc(100%-2rem)] max-w-md`, rounded `24px`,
  `bottom-[calc(1rem+env(safe-area-inset-bottom))]`;
- desktop (`lg:`): fixed left rail, vertically centered (`lg:left-6 lg:top-1/2
  lg:-translate-y-1/2`), column layout.

When using the left rail, wrap the page content with `lg:pl-28` so it does not sit
under the rail.

## Mobile → desktop adaptivity

The house pattern: **one card on mobile, split cards on desktop**. Use the
`useMediaQuery` composable and branch in the template:

```vue
<script setup>
import { useMediaQuery } from '@/composables/useMediaQuery'
const isDesktop = useMediaQuery('(min-width: 1024px)')
</script>

<template>
  <div v-if="isDesktop" class="grid grid-cols-[2fr_1fr] gap-5">
    <section class="app-card rounded-app p-5">...</section>
    <section class="app-card rounded-app p-5">...</section>
  </div>
  <section v-else class="app-card rounded-app p-5">
    <!-- tabs via SegmentedControl -->
  </section>
</template>
```

Equivalent pure-CSS approach: duplicate-free layouts with `hidden lg:grid` /
`lg:hidden`. Prefer `useMediaQuery` only when the DOM/behavior must differ, not
just the styling.

## UI kit (`components/ui/`)

| Component | Purpose |
| --- | --- |
| `Badge` | colored pill (`color` hex + optional dot) |
| `BottomSheet` | mobile modal from the bottom (Teleport + Transition, safe-area footer) |
| `Field` | labeled text/number input with error/hint/suffix |
| `SelectField` | labeled native select with custom chevron |
| `SegmentedControl` | pill tab switcher (`v-model`, `options: [{value,label}]`) |
| `EmptyState` | centered icon + title + description + slot action |
| `Skeleton` | pulse placeholder lines |
| `ToastHost` | renders the `useToast` singleton stack |

## State & composables

Cross-component state is a **module-level singleton**:

```js
// composables/useToast.js
import { ref } from 'vue'
const toasts = ref([])            // module scope => shared across all components
export function useToast() { /* push/success/error/info */ return { toasts, ... } }
```

Use this for UI-global concerns (toasts, visibility toggles, theme). For
server/domain state, prefer a composable that owns `ref` + `load()` and is called
per view (data is fetched on mount in the view).

## Services (API)

Single axios instance in `src/services/api.js`, one method per endpoint, grouped
as a plain object export:

```js
export const api = {
  async getItems() {
    const { data } = await apiClient.get('/api/v1/items')
    return data
  },
}
```

Base URL comes from `VITE_API_BASE_URL`. In Docker it is injected at build time
(`--build-arg VITE_API_BASE_URL=...`), because Vite inlines env vars at build.

## PWA

`index.html` sets `manifest.json`, `theme-color`, Apple web-app meta and the
touch icon. `manifest.json` uses `display: standalone` and the two icons.
Regenerate/patch the placeholder icons with the real logo before shipping.

## Verification

```sh
npm install
npm run dev        # http://localhost:5173 — check shell + sample views
npm run build      # must produce dist/ without errors
npm run lint       # oxlint + eslint
```

Manual checks: bottom navbar clears content on mobile; left rail does not overlap
content on desktop; cards use `.app-card`; toasts appear top-center; the app has
no console errors.

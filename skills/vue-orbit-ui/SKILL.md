---
name: Vue Orbit UI Conventions
description: Use when building or changing UI in an existing Vue 3 + Tailwind frontend that uses the Orbit Ecosystem theme (orbit-ecosystem-preset.js): cards, mobile-first layout, bottom-sheet forms, loading/empty/error states, toasts, money/percent formatting and sensitive-value masking, deterministic colors. Trigger on requests like "aggiungi una view", "nuovo componente Vue", "card", "bottom sheet", "form", "sistema la UI", "mobile-first", "tema Orbit", "stile", "pagina", "componente riutilizzabile".
---

# Vue Orbit UI conventions

How to build UI in the house style shared by myInves / MTrack / Orbit. For a brand
new project, bootstrap it with the companion skill **`vue-orbit-scaffold`** first.

**Every project belongs to the Orbit ecosystem.** The `orbit-ecosystem-preset.js`
theme is mandatory — never optional, never bypassed. Before writing any UI, confirm
the preset is present and wired into Tailwind; if it is not, add it (copy the file
from the `vue-orbit-scaffold` templates) and make sure `src/style.css` defines
`.app-card`. Do not style with ad-hoc CSS or hardcoded colors.

## The rules that define the style

1. **Theme via `brand-*` tokens only.** Never hardcode colors: use
   `bg-brand-background`, `bg-brand-surface`, `text-brand-textMain`,
   `text-brand-textMuted`, `bg-brand-primary`, `bg-brand-secondary`. Semantic
   states use `text-emerald-400` (positive) / `text-red-400` (negative).
2. **Cards** are `.app-card` + a radius utility + padding:
   `class="app-card rounded-app p-5"`. `.app-card` is defined in `src/style.css`
   (gradient border + backdrop blur).
3. **Mobile-first.** Style the base breakpoint for the phone, then enhance with
   `lg:`. Keep content clear of the bottom navbar (`pb-24`/`pb-36`) and respect
   `env(safe-area-inset-*)`.
4. **Reuse `components/ui/`** primitives instead of rewriting inputs, sheets,
   badges, empty/skeleton states.
5. **Data through `services/api.js`**; formatting through `utils/format.js`;
   feedback through `useToast()`.
6. **Design the four states** for every data view: loading (`Skeleton`), empty
   (`EmptyState`), error (`toast.error`), loaded (cards).

## When to use

Any UI work in an existing Orbit frontend: a new view/page, a new reusable
component, a form (usually in a `BottomSheet`), a list of cards, a chart, a
theming/consistency fix, or a mobile/desktop responsive adjustment.

## Workflow

1. **Apply the Orbit theme (mandatory).** Verify the project already uses it:
   - `orbit-ecosystem-preset.js` exists and is listed in
     `tailwind.config.js` under `presets`;
   - `src/style.css` (or `src/assets/main.css`) contains the `.app-card` class;
   - `postcss.config.js` loads `tailwindcss`.
   If anything is missing, add it first (copy the missing files from the
   `vue-orbit-scaffold` templates) before touching the UI. Never create a parallel
   ad-hoc stylesheet instead.
2. **Locate the shell**: `App.vue` (header/navbar/toasts) and `src/style.css`
   (`.app-card`). Match the existing page container (`px-4`, `lg:pr-28` when the
   desktop rail is used).
3. **Pick the primitives** from `components/ui/`; copy the house patterns from
   `templates/` when they are missing (Money, PnLValue, sensitive masking,
   deterministic color, hero card, list row, `useResource`).
4. **Compose the view** in `src/views/<Name>View.vue`: fetch with a composable /
   `useResource`, render cards, handle the four states, wire actions to
   `BottomSheet` + `Field` and confirm with `useToast`.
5. **Adapt mobile → desktop** with `useMediaQuery` only when behavior differs;
   otherwise do it in CSS (`hidden lg:grid`).
6. **Verify**: `npm run lint` + `npm run build`; check the four states, the
   mobile/desktop layout, and that the brand tokens are actually applied.

## Non-negotiable rules

- **Do not invent new theme colors.** If a color is needed, it is a `brand-*`
  token or a semantic Tailwind color (emerald/red/amber/…). Never write a custom
  stylesheet with hardcoded hex values.
- **Cards and spacing are fixed.** Cards are always `app-card rounded-app p-5`.
  Page container is `px-4`; vertical rhythm is `gap-5`. Do not invent
  per-component spacing or radii — reuse the canonical values.
- **The preset is the single source of theme.** If `orbit-ecosystem-preset.js`
  is missing or not wired, add it first; do not approximate the theme with
  inline utilities.
- **One component per file**, `<script setup>`, props via `defineProps`, events
  via `defineEmits`. Keep `ui/` primitives presentational (no API calls).
- **Formatting is centralized**: money/percent/date go through
  `utils/format.js` (and `Money`/`PnLValue`), never inline `toFixed`/string math.
- **Sensitive values** (`Money`, `PnLValue`) respect the global
  `useSensitiveVisibility()` mask; keep new value components consistent.
- **Toasts, not `alert()`**: use `useToast().success/error/info`.
- **Icon-only buttons** need a `title`/`aria-label`.
- **Lazy-load** non-initial routes; keep components small and composed.

## Reference & assets

- `references/conventions.md` — cards, spacing, adaptivity, forms/states, lists,
  charts, accessibility, end-to-end checklist.
- `templates/` — drop-in house patterns: `Money.vue`, `PnLValue.vue`,
  `StatHero.vue`, `ListRow.vue`, `useSensitiveVisibility.js`, `useResource.js`,
  `stringToColor.js`.

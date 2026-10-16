# UI conventions — detail

Deep detail behind `vue-orbit-ui`. Read when unsure about spacing, states,
adaptivity, or a component's shape.

## Page container & spacing

The page root is a `<main>` with horizontal padding and a vertical rhythm:

```vue
<main class="w-full px-4">
  <div class="py-3 flex flex-col gap-5 w-full">
    <!-- sections -->
  </div>
</main>
```

- Vertical rhythm: `gap-5` between cards, `flex flex-col gap-5`.
- When the desktop left rail exists, push content right with `lg:pl-28` on the
  shell (`App.vue`) or `lg:pr-28` on the section that must not sit under a
  centered control.
- Bottom clearance: the navbar floats, so the shell keeps `pb-24`/`pb-36`.

## Cards

Single container class: **`.app-card`** (gradient border + blur + shadow, in
`src/style.css`). Combine with a radius and padding:

```html
<section class="app-card rounded-app p-5 flex flex-col gap-3">…</section>
```

- `rounded-app` (24px) for large cards; `rounded-app-sm` (12px) for compact
  surfaces (inputs, tiles, badges containers).
- Nested rows do **not** get their own card; they are plain rows inside the card,
  separated by `gap`/`divide-y divide-white/5`.
- Interactive cards: `hover:-translate-y-1 hover:shadow-app transition-all`.

## Mobile → desktop adaptivity

Two tools, choose by need:

| Need | Use |
| --- | --- |
| Only styling differs | CSS: `grid lg:grid-cols-2`, `hidden lg:block` |
| DOM/behavior differs (e.g. tabs vs split cards) | `useMediaQuery('(min-width: 1024px)')` |

Canonical breakpoint is **1024px** (`lg`). The house pattern: one card with a
`SegmentedControl` on mobile, split cards on desktop (see myInves `PortfolioHero`).

## Forms (BottomSheet)

Forms are `BottomSheet` (Teleport + Transition, safe-area footer) + `Field` /
`SelectField`. The primary action lives in the `#footer` slot.

```vue
<BottomSheet :open="open" title="Add item" @close="open = false">
  <Field v-model="name" label="Name" :error="errors.name" />
  <template #footer>
    <button class="w-full h-11 rounded-app-sm bg-brand-primary text-white text-sm font-bold active:scale-[0.98] transition-all"
            @click="save">Save</button>
  </template>
</BottomSheet>
```

- Labels are `text-[11px] uppercase tracking-wider font-semibold text-brand-textMuted`.
- Errors render under the field in `text-[11px] text-red-400`.
- Primary buttons: `bg-brand-primary text-white` + `shadow-lg shadow-brand-primary/20`
  and `active:scale-95`.

## The four states

1. **Loading** → `<Skeleton :lines="3" />` inside the card.
2. **Empty** → `<EmptyState :icon="Wallet" title="…" description="…" />` with an
   optional action in the default slot.
3. **Error** → `toast.error('…')`; keep the last good data if any.
4. **Loaded** → the cards.

`useResource(fetcher)` (template) gives `{ data, loading, error, load }` so views
stay consistent.

## Lists

A list is one card containing rows (not a card per row). Row shape: leading
avatar/icon, title + muted subtitle, trailing value/badge.

```html
<div class="app-card rounded-app p-2">
  <ListRow v-for="item in items" :key="item.id" … />
</div>
```

Long lists: `overflow-y-auto hide-scrollbar` (`.hide-scrollbar` in `style.css`).

## Values, money & masking

- Always format via `utils/format.js` (`formatMoney`, `formatMoneySigned`,
  `formatPct`, `formatDate`). Locale/currency constants live at the top of the file.
- Use `Money` for amounts and `PnLValue` for deltas (value + percent + trend icon).
- Both respect `useSensitiveVisibility()` — the global "hide values" toggle. Any
  new value component should do the same (`€ ••••` mask).

## Feedback & state sharing

- `useToast()` for transient feedback; `success`/`error`/`info`, auto-dismiss.
- Cross-component UI state (toast, masking, theme) is a **module-level singleton
  composable** (a `ref` at module scope). Domain/server state lives in a
  per-view composable that owns `ref` + `load()`.

## Colors from names

Categories/tags/asset types get a deterministic accent from their name:
`stringToColor(name)` (template) → a stable hex, ideal for `Badge`. Never
randomize per render.

## Charts (optional)

Charts use `chart.js` + `vue-chartjs`. Wrap them in a small component and pass
`points`/`labels`; theme colors come from the `brand-*` palette. Keep them inside
an `.app-card`.

## Accessibility

- Icon-only buttons: `title` + `aria-label`.
- Active nav/segmented items: color + `stroke-width` (not color alone).
- Keep tap targets ≥ 40px (`h-10 w-10`).
- Interactive rows are `<button>`/`<RouterLink>`, not clickable `<div>`.

## End-to-end checklist

- [ ] Only `brand-*` tokens (no hardcoded theme colors).
- [ ] Cards use `app-card rounded-app p-5`.
- [ ] Content clears the navbar; safe-area respected.
- [ ] Four states handled.
- [ ] Formatting via `utils/format.js`; masking respected.
- [ ] Mobile and desktop both checked (1024px boundary).
- [ ] `npm run lint` + `npm run build` pass.

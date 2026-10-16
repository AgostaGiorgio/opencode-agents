---
name: Vue Orbit Frontend Scaffold
description: Use when creating a brand-new Vue 3 + Vite + Tailwind frontend in the house style (Orbit Ecosystem dark theme via orbit-ecosystem-preset.js, mobile-first shell with bottom navbar + desktop rail, card-based UI, components/ui kit, axios service layer, vue-router, PWA, Docker/nginx). Trigger on requests like "crea un nuovo frontend", "new Vue project", "scaffold frontend", "nuova app Vue", "bootstrap Vue + Tailwind", "frontend con tema Orbit", "app mobile-first", "nuovo frontend Vue".
---

# Vue Orbit frontend scaffold (house style)

Creates a new frontend that matches the UI of myInves / MTrack / Orbit.

- **Stack**: Vue 3 (`<script setup>`) + Vite + Vue Router + Tailwind **v3** + PostCSS
  + axios + lucide icons. Lint/format: oxlint + eslint + prettier.
- **Theme**: the shared `orbit-ecosystem-preset.js` (dark, `brand-*` tokens,
  `rounded-app`, `shadow-app`). Copy it verbatim — it is identical in every project.
- **Style**: mobile-first, card-based, bottom navbar on mobile + left rail on desktop.

```
src/
├── main.js                 # createApp + router
├── App.vue                 # shell: AppHeader + RouterView + AppNavbar + ToastHost
├── style.css               # Tailwind layers + .app-card + helpers
├── router/index.js         # routes (lazy for non-initial views)
├── services/api.js         # axios instance + endpoint methods (single entry point)
├── composables/            # useToast (singleton), useMediaQuery
├── components/
│   ├── AppHeader.vue       # brand + header actions
│   ├── AppNavbar.vue       # bottom navbar (mobile) / left rail (desktop)
│   └── ui/                 # reusable primitives (badge, field, bottom sheet, ...)
└── views/                  # one file per route
```

For the day-to-day UI conventions (cards, adaptivity, form sheets, states,
formatting, masking), use the companion skill **`vue-orbit-ui`**.

## When to use

Use this skill to bootstrap a **new** Vue frontend: a new app, a new frontend for
a backend, or a throwaway reference project. Do **not** use it to add features to
an existing frontend (use `vue-orbit-ui`).

## Workflow

1. **Collect the metadata** (ask if unknown):
   - `name` — app display name (e.g. `MyInves`).
   - `slug` — package/Docker slug, lowercase (e.g. `myinves`).
   - `description` — one line (used in `manifest.json`).
   - `api_url` — backend base URL (e.g. `http://localhost:8000`).
2. **Generate the tree** with the bundled script:
   ```sh
   python scripts/scaffold_frontend.py \
       --target ../<slug>-frontend \
       --name <Name> \
       --slug <slug> \
       --description "<description>" \
       --api-url http://localhost:8000
   ```
   Add `--force` to overwrite. Manual fallback: copy `templates/` and replace the
   placeholders below.
3. **Install & run**:
   ```sh
   cd <target>
   npm install
   cp .env.example .env          # or rely on .env.development
   npm run dev                   # http://localhost:5173
   ```
4. **Verify**:
   ```sh
   npm run build                 # produces dist/
   npm run lint                  # oxlint + eslint
    grep -rl '8b5cf6' dist/static/*.css   # confirm brand tokens made it into the build
   ```
5. **Make it yours**: rename the sample `DashboardView`/`AboutView`, set the navbar
   items and routes, replace the placeholder icons in `public/`, and add endpoints
   in `src/services/api.js`.

## Placeholders (used by the script)

| Placeholder | Meaning | Example |
| --- | --- | --- |
| `__APP_NAME__` | App display name | `MyInves` |
| `__APP_SLUG__` | Package/Docker slug | `myinves` |
| `__APP_DESCRIPTION__` | One-line description | `Personal investment tracker` |
| `__API_URL__` | Backend base URL | `http://localhost:8000` |

## Non-negotiable rules

- **Use the shared preset verbatim** (`orbit-ecosystem-preset.js`). Never redefine
  brand colors inline; always use the `brand-*` tokens (`bg-brand-background`,
  `bg-brand-surface`, `text-brand-textMain`, `text-brand-textMuted`,
  `bg-brand-primary`, `bg-brand-secondary`).
- **The preset is the single source of theme.** Do not add a parallel/ad-hoc
  stylesheet or hardcoded hex colors; `.app-card` and the `brand-*` utilities are
  the only way to style.
- **Tailwind v3** with `tailwind.config.js` `presets: [orbitEcosystemPreset]`
  (do not migrate to v4; the preset uses the v3 shape).
- **Cards** use the `.app-card` component class plus a radius utility, e.g.
  `class="app-card rounded-app p-5"`.
- **Mobile-first**: design at the base breakpoint and enhance with `lg:`; use
  `env(safe-area-inset-*)` and bottom padding (`pb-24`/`pb-36`) so content clears
  the navbar.
- **`components/ui/` for reusable primitives**; one component per file,
  `<script setup>` + `defineProps`/`defineEmits`. Views compose components; they
  do not re-implement fields, sheets, badges, etc.
- **Cross-component state = module-level singleton composable** (a `ref` declared
  at module scope, exposed by `useX()`), like `useToast`.
- **API only via `src/services/api.js`** (axios). Components never import axios or
  read `import.meta.env.VITE_API_BASE_URL` directly.
- **Router**: lazy-import non-initial views (`() => import(...)`); keep
  `scrollBehavior` returning to top.
- **PWA**: keep `manifest.json`, the `theme-color`/apple meta tags and the icons.
- **Logos/actions** stay accessible (`title`/`aria-label` on icon-only buttons).

## Reference & assets

- `references/stack.md` — full file tree, design tokens, layout shell, mobile→desktop
  adaptivity, verification.
- `templates/` — a complete, runnable frontend (project files, shell, `ui/` kit,
  sample views, Docker/nginx, PWA manifest).
- `scripts/scaffold_frontend.py` — copies `templates/`, fills placeholders, and
  generates placeholder PWA icons.

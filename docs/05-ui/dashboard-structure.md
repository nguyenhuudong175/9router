# Dashboard Structure

## App Router grouping
- Main authenticated UI is in `src/app/(dashboard)/dashboard/**`.
- Public pages include `src/app/login`, `src/app/landing`, and callback route.

## Main dashboard sections
- Endpoint, providers, combos, usage, quota, CLI tools, media providers, translator, MITM, profile, console log.

## Layout
- Dashboard routes use `src/app/(dashboard)/layout.js` which wraps with `DashboardLayout` from shared components.

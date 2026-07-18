# Frontend Architecture Compass

This document serves as the implementation guide and architectural standard for the Ascendrite frontend application.

---

## 1. Project Organization

All frontend code lives under `platform/client/` and is organized as follows:

```
platform/client/
├── src/
│   ├── assets/                # Styling, media, and static assets
│   ├── components/            # Reusable UI widgets and layout views
│   ├── api/                   # Decoupled REST client services
│   ├── store/                 # State management stores (Pinia/Redux)
│   ├── router/                # Vue/React routing guards and setups
│   └── views/                 # Top-level route pages
```

---

## 2. Interface Design Principles

*   **Decoupled State**: Views must read and update data using state stores. They should never invoke REST endpoints directly.
*   **Design System Rules**: Custom UI layouts must utilize variables from `index.css` for consistency. Avoid ad-hoc utility styling overrides.
*   **Responsive Integrity**: Design layouts prioritizing mobile usability, ensuring smooth display rendering across all display boundaries.

---

## 3. Navigation & Routing Guards

*   **Auth Gates**: Routes requiring authorization must use metadata flags, processed via router navigation guards.
*   **Lazy Loading**: Split route views dynamically to speed up loading times.

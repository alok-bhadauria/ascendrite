# Frontend Architecture: UI/UX Standards and Component Design

## Document Metadata
*   **Purpose**: Outlines the Single Page Application layout, global state synchronization, adaptive interfaces, and UI design standards.
*   **Scope**: Governs client-side React code structures, visualizer modules, and rendering styles.
*   **Intended Audience**: Frontend developers, UI engineers, accessibility specialists, and design managers.
*   **Related Documents**:
    *   [Platform Philosophy](../governance/platform-philosophy.md)
    *   [Product Philosophy](../governance/product-philosophy.md)
    *   [Backend Architecture](backend-architecture.md)
*   **Ownership**: Lead UX/UI Architect & Head of Platform Engineering

---

## 1. Single Page Application (SPA) Structure & Subdomain Readiness
The frontend is constructed using React, Vite, and Tailwind CSS. The project directory layout is structured to maintain clean component boundaries and isolate routes by subdomain zones:

```
platform/client/
├── src/
│   ├── config/             # Config hubs (env.js settings)
│   ├── components/         # Modular visual UI components
│   │   ├── ui/             # Dynamic overlays (CommandPalette, ToastProvider)
│   │   ├── layout/         # Shell containers (Sidebar, Header, AppLayout)
│   │   └── primitives/     # Core reusable components (Button, Modal, EmptyState)
│   ├── pages/              # Primary route containers (Dashboard, Profile)
│   ├── router/             # Route Guards and capability gates
│   ├── store/              # State management stores (Zustand)
│   └── utils/              # Parsers, navigators, and Axios clients
```

### Future-Proofing for V2 Subdomains
To support migrating routes to separate subdomains (e.g., `studio.ascendrite.com` or `admin.ascendrite.com`) in V2, client routing is decoupled:
1.  **Dynamic Navigation Helper (`src/utils/navigation.js`)**: All navigation links call `getAppUrl(appName, path)` or `navigateToApp(navigate, appName, path)`. In V1, this maps onto local path prefixes; in V2, it automatically resolves to cross-origin subdomain domains.
2.  **Environment Config Registry (`src/config/env.js`)**: Manages base API paths, Google OAuth URLs, cookie parameters, and hosts. Allows changing environments dynamically using `.env` configurations without modifying components code.
3.  **Modular Router Boundaries (`src/App.jsx`)**: Routes are separated using explicit layout zones, matching Public, Learner, Creator, and Admin capability limits. Each block can easily be extracted into its own SPA project repository in the future.

---

## 2. Reusable UI Components & Primitive Foundations
To enforce visual consistency and prevent duplicate ad-hoc styling hacks, developers must build pages strictly using reusable primitives from `src/components/primitives/`:

*   **Buttons (`Button.jsx`)**: Unified triggers handling primary, secondary, and disabled UI interaction patterns.
*   **Cards (`Card.jsx`)**: Standard containers for content blocks, supporting standard headers, content wrappers, and shadow elevations.
*   **Inputs & TextAreas (`Input.jsx`, `TextArea.jsx`)**: Accessible text boxes with custom focus outlines.
*   **Modals (`Modal.jsx`)**: Standard portals managing overlays backdrop clicks, ESC event listeners, and focus traps.
*   **Empty State (`EmptyState.jsx`)**: Placeholder panel with inline illustration icons and helper buttons.
*   **Error State (`ErrorState.jsx`)**: Connection failure fallbacks with optional "Retry" action hooks.
*   **Indicators (`Spinner.jsx`, `Badge.jsx`)**: Loading animations and status banners consuming standard design tokens.

---

## 3. Styling Token Foundation
The styling system uses unified design tokens declared in `src/styles/ascendrite-style.css`. Component styling consumes these variables to ensure changes to the design system propagate globally.

### Design Tokens Catalog
*   **Typography Scaling**: Fluid typography scales mapped to CSS variables (e.g. `--font-size-base`, `--font-size-2xl`) using CSS `clamp()` rules to scale naturally between mobile and ultrawide screens.
*   **Responsive Breakpoints**: Breakpoint rules align with Tailwind CSS (640px, 1024px, 1536px) and handle margins/paddings dynamically using `.page-container`.
*   **Accessibility Focus Outline (`.focus-ring`)**: Focusable elements declare custom ring styles using `--color-theme-accent` with a clear 2px offset.
*   **Reduced-Motion Override**: Media queries detect `prefers-reduced-motion: reduce` and disable long fade/scale animations globally.
*   **Layout Dimensions**: Central variables (Navbar height: `--header-height`, Sidebar width: `--sidebar-width`) coordinate layout margins to prevent component overlaps and collisions.

---

## 4. State Synchronization & Offline Resilience
*   **Hydration Sync Guards**: Component state variables loading from namespaced local storage (such as notes or study planner tasks) use `isHydrated` checks. This prevents React from overwriting stored user data with empty defaults during mount.
*   **Telemetry Integration**: User progress telemetries (completions, assessment scores, timeline milestones) retrieve data from backend APIs.
*   **Spaced Repetition Schedule**: Using client-side state engines, the dashboard calculates memory decay variables (based on diagnostic scores and study time gaps) to highlight review suggestions.

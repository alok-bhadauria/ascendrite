# Frontend Architecture: UI/UX Standards and Component Design

---

## 1. Single Page Application (SPA) Structure
The frontend client is built as a single-page application using **ReactJS** and compiled using **Vite**. The structure separates presentation logic, global state, and interactive visualizer sub-engines.

```
platform/client/
├── public/                 # Static public assets (icons, font assets)
├── src/
│   ├── components/         # Reusable global design components
│   │   ├── ui/             # Core primitives (Button, Card, Input)
│   │   ├── layout/         # Shell containers (Sidebar, Navbar)
│   │   └── visualizers/    # Polymorphic simulator components
│   ├── hooks/              # Global state and API hooks
│   ├── pages/              # Route views (Dashboard, TopicReader, Profile)
│   ├── store/              # State management modules (Zustand schemas)
│   ├── utils/              # Helper libraries (KaTeX wrappers, API clients)
│   ├── App.tsx             # Master Router mapping
│   └── main.tsx            # DOM hook and global styles entry
```

---

## 2. UI/UX Architecture Guidelines
Ascendrite utilizes a modern, sleek design system to maximize readability and reduce cognitive load.

### Visual Design System
*   **Color Palette:** Sleek dark-mode first configuration. Uses slate/zinc base scales with vibrant teal/violet indicators for achievements, math formulas, and code segments.
*   **Typography:** The platform uses **Inter** for UI layout controls and **Outfit** for structural headings. KaTeX math formulas are rendered using native KaTeX serifs.
*   **Micro-animations:** Interactive components leverage **Framer Motion** for smooth transition animations (hover states, progress bars sliding, dialog fade-ins).
*   **Accessibility (WAI-ARIA):** All interactive buttons and inputs require explicit `id` attributes, standard focus rings, and proper keyboard navigation bindings (tab indexing).

---

## 3. State Management Configuration
Global client state is managed via **Zustand**, providing lightweight, atomic state management without boilerplate overhead.

```
+-----------------------------------------------------------+
|                        Zustand Store                      |
+-----------------------------------------------------------+
  |-- AuthStore: Track active user data, tokens, and roles.
  |-- CourseStore: Cache syllabus index paths and topic meta.
  |-- TrackerStore: Logs active topic duration and quiz inputs.
```

State changes trigger re-renders only in affected leaf nodes, ensuring page frames remain smooth and run at 60 FPS.

---

## 4. Content Delivery Optimization
To maintain rapid initial page loads:
*   **Route-Based Code Splitting:** Code-split route boundaries using `React.lazy` to load pages dynamically as users navigate.
*   **Dynamic Visualizer Loading:** Since heavy Canvas/SVG rendering engines (like Mermaid.js) are only required on specific notes, they are imported dynamically (`import()`) only when mounting visualizer components.
*   **Tree Shaking:** Explicit configurations in compilation tools to strip unused icons and module helpers from the final client bundle.

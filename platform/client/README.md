# Ascendrite Client Application SPA

This directory houses the frontend Single Page Application (SPA) client workspace for the Ascendrite platform ecosystem.

---

## 1. Product Purpose & UX Philosophy

The Ascendrite client provides a structured, responsive, and visually refined interactive interface for all platform users:
*   **Visitor**: Discovers subjects and curriculum pathways, and authenticates via credential inputs.
*   **Learner**: Manages study planners, reads mathematical topic materials, derivation proofs, and logs masteries.
*   **Creator**: Authors, edits, validates, and publishes curriculum syllabuses and markdown/LaTeX content.
*   **Administrator**: Monitors system metrics, modifies configuration values, and handles content review queues.

UX boundaries enforce **clarity over clutter, textbook-grade typography, dynamic visual feedback, and handcrafted product identity**.

---

## 2. Frontend Architecture & Technology Stack

The application is built on a modern, high-performance web engineering stack:
*   **Core framework**: [React 19](https://react.dev/) using functional component patterns.
*   **Build Pipeline & Compiler**: [Vite 8](https://vite.dev/) offering fast Hot Module Replacement (HMR) and optimized rollup production bundles.
*   **Routing System**: [React Router 7](https://reactrouter.com/) configuring nested route mapping with protective middleware guards:
    - `ProtectedRoute`: Prevents unauthenticated actors from accessing internal pages.
    - `CapabilityGate`: Restricts paths to specific capability permissions (e.g. `creator:write` for authoring, `admin:write` for governance).
*   **Asynchronous Queries**: [TanStack React Query 5](https://tanstack.com/query) for caching, refetch limits, and automated server synchronization.
*   **State Management**: [Zustand](https://github.com/pmndrs/zustand) managing global authentication, capability maps, and visual theme states.
*   **Icons**: [Lucide React](https://lucide.dev/) for consistent vector iconography.
*   **Styling**: Vanilla CSS variables integrated with [Tailwind CSS 4](https://tailwindcss.com/) for layout systems and fluid spacing grids.

---

## 3. Directory & Component Organization

The client codebase maintains strict folder boundaries to guarantee component reuse:
```
platform/client/
├── src/
│   ├── components/
│   │   ├── layout/       # Shared structural wrappers (Navbar, Sidebar, Footer, Layouts)
│   │   ├── primitives/   # Pure atomic elements (Button, Card, Switch, TextArea, Spinner)
│   │   └── ui/           # Custom interactive components (Bubble Sort Visualizer, explorers)
│   ├── pages/            # Complete page channels (LearnPage, CreatorPage, AdminPage, etc.)
│   ├── router/           # Protected and capability-gated route middleware guards
│   ├── store/            # Zustand global state hooks (authStore.js)
│   ├── utils/            # Axios API wrappers and formatting utilities
│   ├── App.jsx           # Routing configuration registry and layout provider
│   ├── index.css         # Global design system tokens and Tailwind bindings
│   └── main.jsx          # DOM entry mounting anchor
├── package.json          # Dependency mappings and lifecycle scripts
└── vite.config.js        # Vite compilation and proxy configurations
```

---

## 4. HSL Variable Theme Engine

The visual design system maps HSL colors to CSS custom properties. It features **Monkeytype-inspired** themes loaded persistently to prevent Flash of Unstyled Content (FOUC):
*   Theme selections (`dark`, `light`, `nord`, `dracula`, `solarized`, `monokai`) apply visual modifications directly to the document root element.
*   Colors (accents, backgrounds, borders, active states) are calculated dynamically usingTailwind color bindings.

---

## 5. Development Workflow

Configure your local environment variables in `.env.local` at the repository root before booting:

### 5.1 Boot Development Server
Launches Vite HMR local server at `http://localhost:5173`:
```bash
npm run dev
```

### 5.2 Build Production Bundle
Compiles and packages the codebase into optimized, minified assets under `dist/`:
```bash
npm run build
```

### 5.3 Static Linter Checking
Runs ESLint check to audit formatting rules and unused import errors:
```bash
npm run lint
```

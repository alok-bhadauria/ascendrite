# Frontend Architecture: UI/UX Standards and Component Design

## Document Metadata
*   **Purpose**: Outlines the Single Page Application layout, global state synchronization, and UI design standards.
*   **Scope**: Governs client-side React code structures, visualizer modules, and rendering styles.
*   **Intended Audience**: Frontend developers, UI engineers, and style guide managers.
*   **Related Documents**:
    *   [Platform Philosophy](../governance/platform-philosophy.md)
    *   [Product Philosophy](../governance/product-philosophy.md)
    *   [Backend Architecture](backend-architecture.md)
*   **Ownership**: Lead UX/UI Architect & Head of Platform Engineering

---

## 1. Single Page Application (SPA) Structure
The frontend application shall be built using React and compiled via Vite. The project directory layout is structured to maintain clean component boundaries:

```
platform/client/
├── src/
│   ├── components/         # Modular visual UI components
│   │   ├── ui/             # Standard design primitives (Buttons, Inputs)
│   │   ├── layout/         # Shell containers (Sidebar, Header)
│   │   └── visualizers/    # Interactive simulator canvases
│   ├── hooks/              # Global state loaders and API fetch hooks
│   ├── pages/              # Primary route containers
│   ├── store/              # State management stores (Zustand)
│   └── utils/              # Parsers, KaTeX wrappers, and API clients
```

---

## 2. Workspace-First Experience & Component Composition
The frontend layout shall implement a single, unified workspace rather than independent, isolated pages:
*   **Navigation Shell (Left)**: Renders dynamic curriculum indexes and progress indicators from metadata configurations.
*   **Workspace Canvas (Center)**: Displays active lesson details, LaTeX math formulations, and code interfaces.
*   **Contextual Panel (Right)**: Slides open to present context-aware widgets (AI assistants, glossary words, code execution outputs) without reloading the main workspace.
*   **Persistent Context**: The persistent AI assistant and code compilation runtimes must remain mounted across topics, maintaining their state variables in memory.

---

## 3. Dynamic Theme Engine
The interface styling system must not use static, hardcoded stylesheets or simple dark/light modes.
*   **Metadata Integration**: The theme configurations shall be parsed dynamically from subject metadata files (`theme` containing `primary`, `secondary`, `accent`, `surface`, `text`, `graph`).
*   **Dynamic CSS Custom Properties**: Theme values must be injected into the root HTML context as CSS custom properties (e.g. `--color-primary`, `--color-graph`). Core components shall use these variables to dynamically adapt their accents.

---

## 4. Navigation & Universal Search
*   **Route Code Splitting**: All primary pages (Dashboard, Profile, Settings) must be lazy-loaded using `React.lazy` and `Suspense` to minimize the initial download footprint.
*   **Command Palette**: The client must bind `Ctrl+K` to mount a global Command Palette modal, allowing users to search concepts, jump to topics, and toggle AI assistants using keyboard shortcuts.

---

## 5. Offline-First Client Architecture
*   **Local Caching**: The application shall cache current progress updates and quiz inputs in local client stores.
*   **Status Indicators**: If network connectivity is lost, the client must display an offline warning in the header.
*   **State Syncing**: Progress updates must queue locally and synchronize with the backend automatically once connection is restored.
*   **Assets Fallback**: If dynamic rendering libraries (Mermaid.js, LaTeX packages) fail to load, the visualizers must degrade to render raw text codes within code blocks.

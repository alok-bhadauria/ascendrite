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

## 3. Context-Aware UI & Right-Panel Coordination
The right-side contextual panel must adapt dynamically to the active state of the center workspace:
*   **Active Node Binding**: The client routing controller shall maintain an active state object tracking the visible curriculum node ID.
*   **Context Extraction**: Custom hooks (`useActiveContext`) must listen to active node changes, load associated JSON metadata, and automatically instantiate corresponding tools:
    *   *Conceptual Note*: Mounts the Learning Assistant chatbot pre-primed with the topic's notes text.
    *   *Coding Exercise*: Mounts the Code Compiler widget and Execution Trace view.
    *   *Math Derivation*: Mounts step-by-step interactive sliders to trace calculations.

---

## 4. Adaptive Dashboard & Spaced Repetition
The User Dashboard shall adapt its visual cards and recommended next-steps using progress data:
*   **Telemetry Integration**: The dashboard retrieves user telemetry progress (score metrics, completions, durations) from backend endpoints.
*   **Spaced Repetition Schedule**: Using client-side state engines, the dashboard calculates memory decay variables (based on diagnostic scores and study time gaps) to highlight review suggestions.
*   **Adaptive Pathing**: The next-steps widget dynamically shows nodes matching prerequisites from `subject-map.json` that are unlocked but not completed.

---

## 5. Dynamic Theme Engine
The interface styling system must not use static, hardcoded stylesheets or simple dark/light modes.
*   **Metadata Integration**: The theme configurations shall be parsed dynamically from subject metadata files (`theme` containing `primary`, `secondary`, `accent`, `surface`, `text`, `graph`).
*   **Dynamic CSS Custom Properties**: Theme values must be injected into the root HTML context as CSS custom properties (e.g. `--color-primary`, `--color-graph`). Core components shall use these variables to dynamically adapt their accents.

---

## 6. Universal Search & Command Palette
*   **Route Code Splitting**: All primary pages (Dashboard, Profile, Settings) must be lazy-loaded using `React.lazy` and `Suspense` to minimize the initial download footprint.
*   **Command Palette**: The client must bind `Ctrl+K` to mount a global Command Palette modal, allowing users to search concepts, jump to topics, and toggle AI assistants using keyboard shortcuts.

---

## 7. Accessibility (WAI-ARIA) and Focus Governance
All user interfaces must comply with WCAG 2.1 Level AA accessibility criteria:
*   **Semantic Elements**: Layout definitions must utilize HTML5 semantic tags (`<header>`, `<main>`, `<nav>`, `<section>`).
*   **ARIA Attributes**: Interactive widgets must declare explicit ARIA roles (e.g., `role="dialog"`, `aria-expanded`, `aria-label`).
*   **Keyboard Navigation**: Viewports must support standard keyboard tab progression. Focus traps must be enforced on open modal layers (such as the Command Palette) to keep tab navigation restricted to the modal boundaries.
*   **Focus Ring Indicator**: All focusable inputs, selectors, and buttons must display high-contrast outline focus rings when active (`focus-visible:ring-2`).

---

## 8. Offline-First Client Architecture
*   **Local Caching**: The application shall cache current progress updates and quiz inputs in local client stores.
*   **Status Indicators**: If network connectivity is lost, the client must display an offline warning in the header.
*   **State Syncing**: Progress updates must queue locally and synchronize with the backend automatically once connection is restored.
*   **Assets Fallback**: If dynamic rendering libraries (Mermaid.js, LaTeX packages) fail to load, the visualizers must degrade to render raw text codes within code blocks.

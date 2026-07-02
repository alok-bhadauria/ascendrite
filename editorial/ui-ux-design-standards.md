# Ascendrite UI/UX Design Standards

This document defines the visual architecture, typography constraints, animation guidelines, accessibility parameters, and interactive component standards for all client-side web applications on the Ascendrite platform.

---

## 1. Document Purpose and Scope

Consistency in user interfaces directly impacts cognitive retention and workflow efficiency. This guide ensures all interfaces, components, color systems, and interactive visualizations maintain a cohesive, textbook-grade academic layout across screen dimensions and themes.

---

## 2. Core Design Philosophies

The platform enforces three fundamental design rules:
1.  **Technical Minimalism:** Focus visual hierarchy on information mappings. Reduce excessive borders, gradients, and secondary visual indicators that do not contribute to core concept retention.
2.  **Dual-Coding Alignment:** Place textual explanations (prose, LaTeX derivations) and interactive visualizers (execution scopes, node maps) in unified viewports or side-by-side structures. Never hide visualizations behind unnecessary navigation boundaries.
3.  **Predictable Interface States:** Ensure interactive elements provide immediate, deterministic visual feedback (active, hover, focus, loading, error, and transition states) within 200 milliseconds.

---

## 3. Typography and Layout Grid

### Typography System
To maintain clarity across mathematical derivations and code traces, the font scaling uses distinct displays:
*   **Headers and Titles:** Google Font **Outfit** (sans-serif) for high readability, modern appearance, and structural headings.
*   **Body Copy:** Google Font **Inter** (sans-serif) for neutral, technical body text.
*   **Monospace Code and LaTeX:** Browser-default monospace stack (`JetBrains Mono`, `Fira Code`, `SFMono-Regular`, `Consolas`, `monospace`) to ensure accurate alignment of indentation and characters.

| Type Classification | Font Family | Weight | Font Size | Line Height |
| :--- | :--- | :--- | :--- | :--- |
| **Hero Title** | Outfit | 800 (Extra Bold) | 3.75rem (60px) | 1.15 |
| **Page Heading (H1)** | Outfit | 700 (Bold) | 2.25rem (36px) | 1.25 |
| **Section Title (H2)** | Outfit | 700 (Bold) | 1.875rem (30px) | 1.3 |
| **Component Title (H3)** | Outfit | 600 (Semi-Bold) | 1.25rem (20px) | 1.4 |
| **Body Standard** | Inter | 400 (Regular) | 0.875rem (14px) | 1.6 |
| **Subtle Label** | Inter | 500 (Medium) | 0.75rem (12px) | 1.5 |
| **Monospace / Code** | Monospace | 400 (Regular) | 0.75rem (12px) | 1.5 |

### Layout Grid and Spacing
*   **Base Spacing Unit:** 4px incremental scale. Margins and paddings must align strictly to: 4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px, and 96px.
*   **Page Container:** Max-width set to `7xl` (1280px) for standard content folds.
*   **Grid System:** 12-column responsive grid on desktop resolutions, collapsing to 4-column grids on mobile resolutions.
*   **Mobile Padding Safety:** Standard horizontal margins on mobile screens must be a minimum of 16px (`px-4`) to ensure content is not clipped by physical device bezels.

---

## 4. Theme System and Color Palettes

The application implements a theme persistence layer that prevents flashes of unstyled content (FOUC). All colors must be mapped using theme-derived CSS variables. Hardcoded HEX values in components are prohibited.

### CSS Custom Properties
```css
:root {
  --color-bg: #151515;
  --color-surface: #1d1d1d;
  --color-border: #2d2d2d;
  --color-text: #f6f6f6;
  --color-subtle: #a0a0a0;
  --color-accent: #f44336;
}
```

### Supported Palettes

| Theme Name | Style Mode | Background | Surface Card | Foreground Text | Accent Color | Primary Border |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Carbon** | Dark | `#151515` | `#1d1d1d` | `#f6f6f6` | `#f44336` | `#2d2d2d` |
| **Dracula** | Dark | `#282a36` | `#343746` | `#f8f8f2` | `#bd93f9` | `#44475a` |
| **Matrix** | Dark | `#081008` | `#111a11` | `#c2ffc2` | `#00c800` | `#1b351b` |
| **Nord Light** | Light | `#eceff4` | `#f3f5f9` | `#2e3440` | `#5e81ac` | `#d8dee9` |
| **Sepia** | Light | `#f4edd8` | `#ebe3cc` | `#5b4636` | `#8d6e63` | `#e4d9bc` |
| **Milkshake** | Light | `#ffffff` | `#f5f5f5` | `#222222` | `#e91e63` | `#e5e5e5` |

---

## 5. Interactive Components

### Buttons
*   **Primary Button:** Solid `--color-accent` background, high contrast white text. Uses dynamic active scale transformation: `active:scale-95`.
*   **Secondary Button:** Transparent background, solid `1px` border using `--color-border`. Transitions to `--color-surface` background on hover.
*   **Sign In / Actions:** Must use explicit cursor indicators (`cursor-pointer`) and display interactive focus states when navigated via keyboard.

### Input Fields
*   **Default State:** Solid background mapping to `--color-bg`, border matching `--color-border`.
*   **Focus State:** Border changes to `--color-accent` with a subtle outline ring mapping to `--color-accent` at 15% opacity (`ring-2 ring-theme-accent/15`).
*   **Error State:** Border transitions to pure red (`#ef4444`) with immediate helper message rendering beneath the input boundary.

---

## 6. Animation and Transition Guidelines

To maintain cognitive comfort, avoid high-contrast blinking, rapid scaling, and distracting page-wide transitions.

*   **Standard Transition Curve:** All CSS variables (background, color, borders) must transition using a 200ms ease-in-out curve.
    ```css
    transition: all 200ms cubic-bezier(0.4, 0, 0.2, 1);
    ```
*   **Micro-Animations:** Hover states on roadmap nodes and interactive cards must scale by no more than 1.5% (`scale-[1.015]`).
*   **Keyframes for UI Highlights:**
    *   `fade-in`: Transitions opacity from 0 to 1 over 150ms.
    *   `pulse-soft`: Animates ambient glow layers between 5% and 15% opacity to avoid visual fatigue.
    *   `float`: Slowly shifts decorative badges or cards vertically by 6px using a sinusoidal curve over 3 seconds.

---

## 7. Accessibility (WCAG 2.1 Compliance)

All interface layouts must conform to international accessibility directives:
1.  **Touch Targets:** All interactive elements (buttons, links, menu selectors) must have a minimum clickable area of 44x44 pixels.
2.  **Color Contrast:** Text-to-background contrast ratio must satisfy a minimum threshold of 4.5:1 for standard body copy, and 3:1 for large display headers.
3.  **Keyboard Interoperability:** All interactive components must show visible focus indicator rings (`focus-visible:ring-2`) and support standard Tab-key progression.
4.  **Semantic HTML:** Use structural landmarks (`<header>`, `<main>`, `<nav>`, `<section>`, `<footer>`) instead of generic nested `<div>` structures to support screen readers.

---

## 8. Interactive Visualizer Framework

Simulators displaying arrays, code traces, and data models must conform to structural layout bounds:
*   **Canvas Containers:** Visualizer elements (bars, grid cells, pointers) must render within constrained canvas bounds. Horizontal scrolling within sorting grids is prohibited; array blocks must scale down dynamically to fit the viewport width.
*   **Code Trace Panels:** Place execution code trace structures side-by-side or stacked cleanly. Ensure the code panel content does not extend beyond its container border or push adjacent layouts out of horizontal alignment.
*   **Controls Layout:** Simulators must expose clear, semantic control interfaces:
    *   `Play/Pause` button to toggle automatic animation ticks.
    *   `Step Forward` button to execute operations one instruction at a time.
    *   `Speed Slider` to adjust delay rates between steps.
    *   `Reset` button to return datasets to their original unsorted state.

# Ascendrite Diagram Style Guide

## Document Metadata
*   **Purpose**: Standardizes visual design, color palettes, and markup formats (such as Mermaid.js) for all graphical illustrations.
*   **Scope**: Governs all diagram files (`diagrams/*.json`) and inline markdown illustrations.
*   **Intended Audience**: All curriculum authors, graphic designers, and automated prompt generators.
*   **Related Documents**:
    *   [Editorial Style Guide](editorial-style-guide.md)
    *   [Platform Philosophy](../docs/governance/platform-philosophy.md)
*   **Ownership**: Lead Educational Systems Designer & Head of Platform Engineering

---

## 1. Diagram Philosophy and Aesthetics
*   **Minimalist Detailing**: Decorative elements that do not convey system states or logical flows must not be included.
*   **Scalability**: All diagrams must be generated in scalable vector formats (SVG) or text-based markup (Mermaid.js) to support responsive scaling.

---

## 2. Diagram Archetypes and Formats

### 2.1 Flowcharts and Process Maps
*   **Flow Direction**: Process steps shall flow left-to-right (LR) or top-to-bottom (TD).
*   **Standard Shapes**:
    *   *Rectangle*: Represents processing nodes or calculation steps.
    *   *Rhombus/Diamond*: Represents decision branches.
    *   *Pill/Oval*: Represents start or end terminators.

### 2.2 Systems & Network Architecture Diagrams
*   **Component Representation**:
    *   *Double-walled box*: Represents system boundary separations (e.g. client vs server).
    *   *Cylinder*: Represents databases and persistent stores.
    *   *Arrows*: Must indicate data flow direction. Bidirectional arrows should be avoided unless describing synchronous handshakes.

### 2.3 Mathematical & Coordinate Plots
*   **Grid Scaling**: Must include labeled axes (e.g., $x, y$), explicit origin points, and clear scaling indices.
*   **Mathematical Markup**: Mathematical symbols in diagrams must align with [Mathematical Style Guide](mathematical-style-guide.md) and be rendered inside LaTeX tags where supported.

### 2.4 Entity-Relationship (ER) and UML Diagrams
*   **Table Modeling**: Must display the entity name in the header, followed by field listings (highlighting primary keys `PK` and foreign keys `FK`).
*   **Relationship Connections**: Use crow's foot notation (e.g. `one-to-many`, `one-to-one`) to explicitly define constraints.

---

## 3. Accessibility & Print Standards
*   **Color Contrast**: Labels in diagrams must maintain a minimum contrast ratio of 4.5:1 against the background canvas (WCAG AA).
*   **Line Styling**: Differentiate relationship types using distinct line styles (e.g., dashed for optional links, solid for required dependencies) rather than color alone to accommodate monochrome prints.

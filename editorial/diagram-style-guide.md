# Ascendrite Diagram Style Guide

This document defines the visual design standards, color palettes, typography, layout rules, and markup formats (like Mermaid, SVG) for all diagrams and graphical assets across the Ascendrite platform.

---

## 1. Document Purpose and Scope

Visual assets reduce cognitive load and enhance retention. This guide ensures that all diagrams have a uniform, premium look and feel, read clearly on various devices (desktop, mobile, tablet), render correctly in print/PDF formats, and meet accessibility standards.

---

## 2. Diagram Philosophy and Aesthetics

### Core Principles
*   **Clarity Over Complexity:** Keep diagrams minimal. Avoid decorative elements that do not convey structural or procedural information.
*   **Dynamic and Responsive:** Ensure diagrams use scalable formats (SVG, Mermaid.js) that adapt to dark and light modes.

---

## 3. Color Palettes and Typography

Standards for colors and fonts used in static and dynamic graphics.

*   **Primary Palette:** Neutral dark grays, slate, and off-white for backgrounds and primary nodes.
*   **Accent Palette:** Distinct HSL-based accents (e.g., specific shades of blue for inputs, green for outputs, orange for warnings) to represent specific states or functions.
*   **Typography:** Set clean sans-serif typefaces (e.g., Inter, Outfit, or system-native sans-serif) for all diagram labels.

---

## 4. Diagram Archetypes and Formats

Standards for specific diagram categories.

### Flowcharts and Process Maps
[Placeholder: Guidelines for rendering workflow steps, decision loops, and execution directions using standard shapes.]

### Architecture and Network Diagrams
[Placeholder: Visual representations of client-server systems, APIs, messaging queues, load balancers, and distributed server nodes.]

### Mathematical and Geometric Diagrams
[Placeholder: Standards for plotting coordinate systems, vector projections, functions, and multidimensional hyperplanes using SVG/TikZ/Mathplotlib structures.]

### UML, Database, and Entity-Relationship Diagrams
[Placeholder: Standard representations of class hierarchies, relational database tables, columns, constraints, and foreign key relations.]

---

## 5. Consistency, Accessibility, and Print Compatibility

*   **Consistency Rules:** Establish shapes (rectangles for nodes, diamonds for decisions, cylinders for databases) and connector types.
*   **Accessibility:** Ensure all diagrams maintain text labels with minimum color contrast ratios (WCAG AA standard) and include detailed `alt` text.
*   **Print Compatibility:** Define styles for black-and-white print output, ensuring gray scales are differentiable and line patterns (dashed, dotted, solid) are used to indicate relationships without relying solely on color.

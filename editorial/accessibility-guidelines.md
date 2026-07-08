# Accessibility Guidelines

## Document Metadata
*   **Purpose**: Defines visual contrast rules, keyboard controls, voice screen readers, and WCAG compatibility.
*   **Scope**: Governs all frontend interactive components and layout views.
*   **Intended Audience**: Frontend developers, UX designers, and quality assurance specialists.
*   **Related Documents**:
    *   [UI/UX Design System](ui-ux-design-system.md)
    *   [Testing Strategy](../docs/development/testing-strategy.md)
*   **Ownership**: Lead UX/UI Architect & QA Lead

---

## 1. Compliance Level

All user interfaces on the Ascendrite platform must achieve Web Content Accessibility Guidelines (WCAG) 2.1 Level AA compliance. System designs must accommodate users with visual, auditory, motor, or cognitive impairments.

---

## 2. Keyboard Navigation Standards

The platform must remain fully functional when operated exclusively via a keyboard:
*   **Logical Focus Order**: Interactive elements must receive focus in a natural sequence (generally top-to-bottom, left-to-right).
*   **Visible Focus Indicators**: Focused elements must display a high-contrast focus ring. Focus indicators must never be hidden or disabled.
*   **Keyboard Action Keys**: Users must be able to trigger buttons using `Enter` or `Space`, close modals using `Escape`, and navigate dropdown menus using arrow keys.

---

## 3. Screen Reader Integration

To support screen reader navigation:
*   **Semantic Landmarks**: Use standard HTML structural elements (e.g. `<main>`, `<nav>`, `<aside>`, `<header>`) rather than generic containers.
*   **Explicit Mappings**: Elements that do not have native labels (such as icon buttons or widgets) must include descriptive `aria-label` or `aria-labelledby` properties.
*   **Dynamic Announcements**: Dynamic updates (such as code evaluation results or popups) must be announced using screen reader live region attributes.

---

## 4. Visual Accessibility & Contrast

*   **Minimum Contrast**: Normal body text layers must maintain a minimum contrast ratio of 4.5:1 against the background canvas. Headings and large text elements must maintain a contrast ratio of at least 3:1.
*   **Color Redundancy**: Color must never be the sole indicator of state changes, links, or validation status. All status changes must be accompanied by explanatory icons or text labels.
*   **Reduced Motion Support**: Animations must honor browser configurations for reduced motion by disabling sliding and scaling transitions.

# UI/UX Design System

## Document Metadata
*   **Purpose**: Outlines the platform's visual design philosophy, layout constraints, typography guidelines, and user experience patterns.
*   **Scope**: Governs UI/UX designs, frontend visual layouts, and rendering behavior across client applications.
*   **Intended Audience**: UI/UX designers, frontend developers, and product reviewers.
*   **Related Documents**:
    *   [Platform Philosophy](../docs/governance/platform-philosophy.md)
    *   [Accessibility Guidelines](accessibility-guidelines.md)
*   **Ownership**: Head of Platform Engineering & Lead UX/UI Architect

---

## 1. Visual Hierarchy & Reading Behavior

The user interface of Ascendrite is designed to serve technical study. Layouts must guide the learner's attention through concepts systematically:

*   **F-Shaped Scanning**: Structure technical notes to support the natural F-shaped reading pattern. Place core principles, bold terms, and code definitions on the left margin, with detailed explanations expanding outward.
*   **Attention Management**: Limit decorative graphics, floating elements, or secondary visual borders. The user's focus must remain undivided on reading text, code examples, and active visualizations.
*   **Decoupled Viewports**: Place conceptual text and corresponding code or diagrams in side-by-side or dual-pane viewports. This visual continuity allows learners to reference derivations and code implementations simultaneously without switching contexts.

---

## 2. Typography & Spacing Philosophy

Typography and grid metrics are selected to balance high information density with visual comfort:

*   **Header Typography**: Use geometric, highly structured sans-serif typefaces (e.g., Outfit) for titles and section headings. This provides a modern, textbook-grade editorial feel.
*   **Body Typography**: Use highly readable, neutral sans-serif typefaces (e.g., Inter) for paragraphs and general labels, maintaining readability across standard and high-density screens.
*   **Monospace Stack**: Fall back to clean, tabular monospace fonts for code blocks and mathematical variables. Monospace ensures that indentation lines, braces, and math symbols align horizontally.
*   **Spacing Grid**: Enforce a strict 4px spacing unit across all margins, paddings, and components. Spacing should indicate relationships: tighter spacing for related labels, wider gaps for distinct sections.

---

## 3. Color Psychology & Themes

Color is used as a functional tool to convey state, hierarchy, and context rather than decoration:

*   **Theme Selection**: Provide dark modes (e.g., carbon, slate) to minimize eye strain during long coding sessions, sepia modes for long reading comfort, and high-contrast modes for accessibility.
*   **Semantic Color States**: Use standardized, desaturated colors to convey state changes:
    *   *Green*: Indicates passing tests, verified status, or correct answers.
    *   *Red*: Indicates execution errors, validation failures, or boundary limits.
    *   *Amber*: Indicates validation in progress, warning states, or processing delays.
*   **Visual Balance**: Mute card backgrounds and secondary borders, using strong primary colors exclusively to highlight active selection nodes or interactive buttons.

---

## 4. Component Interaction & Animation Philosophy

Transitions must guide the user's focus, providing instant feedback without causing distraction:

*   **Standard Latency Target**: Every interactive element must provide immediate visual feedback (such as active scaling or color shifting) within 200 milliseconds of user input.
*   **Micro-Animations**: Limit scaling animations to minor, subtle transformations. Examples include:
    *   *Button Feedback*: Direct click scaling transformations (`scale-95`).
    *   *Hover States*: Cards scaling slightly on mouse-over (`scale-[1.015]`).
    *   *Focus Indicators*: Outline rings shifting color upon keyboard tab focus.
    *   *Inline Validation*: Form labels turning red or green instantly.
*   **Macro-Animations**: Panel transitions, dashboard shifts, and routing views must slide smoothly, indicating spatial relationships:
    *   *Navigation Transitions*: Sidebars sliding out from the left margin.
    *   *Workspace Switching*: Smooth sliding of the center canvas.
    *   *Dashboard Changes*: Modular grid panels reflowing.
    *   *Theme Changes*: Color values changing using a 200ms ease-in-out curve.
*   **Functional Animation**: Only use motion to illustrate data flows, execution traces, or state transitions. Decorative animations that do not represent functional processes are prohibited.

---

## 5. Workspace & Dashboard Design Principles

### 5.1 Workspace First Experience
The primary workspace simulates a desktop operating system, keeping features contextually localized. Grid panels can be resized, collapsed, and nested. The workspace saves panel configurations, active file directories, scroll locations, and open tabs, restoring them exactly when the user returns.

### 5.2 Dynamic Personalized Dashboard
The landing dashboard aggregates essential learner information within a responsive modular grid:
*   **Mandatory Components**:
    *   *Learning Progress*: Interactive tracking charts mapping completed subjects.
    *   *Workspace Activity*: List of recently modified scratchpads or files.
    *   *Notifications*: Unified alerts registry dashboard.
*   **Personalization Components**:
    *   *Recommendations*: Algorithmic path prompts recommending next topics.
    *   *Achievements*: Earned badges and progress rankings.
    *   *Analytics*: Time-on-task metrics and score statistics.
*   **Layout Adaptability**: Future versions will use AI-driven dashboard adaptation to inject custom widget widgets dynamically based on behavior patterns, without breaking existing layout alignments.
*   **Empty States**: Empty files or lists must show descriptive text and a primary action trigger (e.g., "No projects initialized. Click 'New Project' to start.").

---

## 6. Loading Experience Philosophy

Loading states must reduce uncertainty and maintain layout stability. Ascendrite uses four distinct loading patterns:
*   **Skeleton Loading**: Used for predictable content structures (e.g., dashboard cards, profile layouts, and knowledge cards). Skeleton blocks mimic the dimensions of the final components to prevent layout shifts.
*   **Task-Based Loading**: Used for operations with measurable progress (e.g., AI content generation, file processing, and large asset uploads), displaying progress percentages.
*   **Descriptive Loading**: Used for long-running, variable-time operations (e.g., AI reasoning loops, vector database indexing, and recommendation compiles). Displays descriptive text explaining what system action is active.
*   **Optimistic UI**: Used for low-latency actions where success is highly likely (e.g., toggling preferences, saving code drafts, or liking community posts). The UI updates instantly, rolling back state only in the case of network failure.

---

## 7. Toasts vs. Notifications

The system keeps transient feedback separate from persistent announcements. These systems must never be combined:

### 7.1 Toast System
*   **Purpose**: Temporary, immediate visual feedback for direct user actions.
*   **Examples**: "Session established", "Draft saved", "File upload complete", "Validation failed".
*   **Characteristics**: Non-persistent (not stored in database), short-lived (disappears within 3 seconds), context-sensitive, and displayed on screen boundaries.

### 7.2 Notification System
*   **Purpose**: Stored, audit-logged announcements requiring long-term visibility.
*   **Examples**: Friend requests, direct messages, project feedback, deadline reminders, system announcements.
*   **Characteristics**: Stored in MongoDB, priority-based, time-based, supports read/unread state trackers, managed via a dedicated Notification Center, and governed by user delivery preferences.

---

## 8. Settings & User Control Center

The settings view functions as a unified dashboard separating configurations across five areas:

*   **Appearance**: Theme studio selections, custom styling adjustments, light/dark mode triggers, and visual density scaling.
*   **Accessibility**: Color contrast adjustments, screen reader enhancements, blue-light filters, reduced-motion triggers, and font size scaling.
*   **Privacy**: Visibility selectors for profile details, email addresses, study metrics, and community connections.
*   **Security**: Password rotation controls, two-factor authentication (2FA) status, session registries, and trusted device lists.
*   **Communication**: Notification frequency controls, email subscription toggles, and direct message scopes.

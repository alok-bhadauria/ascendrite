# UI/UX Design System & Product Experience Standards

## Document Metadata
*   **Purpose**: Outlines the platform's visual design philosophy, layout constraints, typography guidelines, semantic color theory, accessibility standards, and interaction states.
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
*   **Recognition over Recall**: Minimize cognitive load by making objects, actions, and options visible. Users must not have to remember information from one part of the workspace to another. Instructions for use must be easily retrievable or visible whenever appropriate.
*   **Progressive Disclosure**: Present complex information incrementally. Display essential metadata and primary content first, providing "Show More" expandable sections, hovering tooltips, or right-panel context slides for advanced derivations, telemetry stats, and secondary variables.

---

## 2. Typography, Layout, Grids & Spacing

Typography and grid metrics are selected to balance high information density with visual comfort:

*   **Header Typography**: Use geometric, highly structured sans-serif typefaces (e.g., Outfit) for titles and section headings. This provides a modern, textbook-grade editorial feel.
*   **Body Typography**: Use highly readable, neutral sans-serif typefaces (e.g., Inter) for paragraphs and general labels, maintaining readability across standard and high-density screens.
*   **Monospace Stack**: Fall back to clean, tabular monospace fonts for code blocks and mathematical variables. Monospace ensures that indentation lines, braces, and math symbols align horizontally.
*   **Spacing Grid**: Enforce a strict 4px spacing unit across all margins, paddings, and components. Spacing should indicate relationships: tighter spacing for related labels, wider gaps for distinct sections.
*   **Grids & Spacing Layout**: The workspace canvas utilizes an 8-column or 12-column responsive CSS Grid system. Spacing classes must use standard scale values:
    *   `4px` (xs): Tight margins between icons and text labels.
    *   `8px` (sm): Padding inside inputs, buttons, and badges.
    *   `16px` (md): Margin between cards and layout columns.
    *   `24px` (lg): Gaps between major workspace panels.
*   **Affordances & Signifiers**: Interactive components must provide clear visual signifiers of their function:
    *   *Buttons*: Convex bevel shading or subtle drop-shadows indicating pushability.
    *   *Resizers*: Distinct double-line cursor grab handles (`col-resize` / `row-resize`) at panel margins.
    *   *Links*: Dynamic underlines appearing on hover, paired with system accent colors.

---

## 3. Semantic Color Theory & Themes

Color is used as a functional tool to convey state, hierarchy, and context rather than decoration:

*   **Theme Selection**: Provide dark modes (e.g., carbon, slate) to minimize eye strain during long coding sessions, sepia modes for long reading comfort, and high-contrast modes for accessibility.
*   **Semantic Color States**: Use standardized, desaturated colors to convey state changes:
    *   *Green (Success)*: Indicates passing tests, verified status, or correct answers.
    *   *Red (Danger/Error)*: Indicates execution errors, validation failures, or boundary limits.
    *   *Amber (Warning)*: Indicates validation in progress, warning states, or processing delays.
    *   *Blue (Info)*: Indicates helper tips, metadata details, or non-blocking system parameters.
*   **Visual Balance**: Mute card backgrounds and secondary borders, using strong primary colors exclusively to highlight active selection nodes or interactive buttons.

---

## 4. Component Interaction, States & Animations

Transitions must guide the user's focus, providing instant feedback without causing distraction:

*   **Standard Latency Target**: Every interactive element must provide immediate visual feedback (such as active scaling or color shifting) within 200 milliseconds of user input.
*   **Micro-Animations**: Limit scaling animations to minor, subtle transformations. Examples include:
    *   *Button Feedback*: Direct click scaling transformations (`scale-95`).
    *   *Hover States*: Cards scaling slightly on mouse-over (`scale-[1.015]`).
    *   *Focus Indicators*: Outline rings shifting color upon keyboard tab focus.
    *   *Inline Validation*: Form labels turning red or green instantly.
*   **Macro-Animations**: Panel transitions, dashboard shifts, and routing views must slide smoothly, indicating spatial relationships:
    *   *Navigation Transitions*: Sidebars sliding out from the left margin.
    *   *Workspace Panel Slides*: Smooth sliding of the right panel context drawer.
    *   *Dashboard Changes*: Modular grid panels reflowing.
    *   *Theme Changes*: Color values changing using a 200ms ease-in-out curve.
*   **Functional Animation**: Only use motion to illustrate data flows, execution traces, or state transitions. Decorative animations that do not represent functional processes are prohibited.
*   **States Grid**:
    *   *Default*: Standard component styles.
    *   *Hover*: Subtle brightness shift (+5%) or scale transform.
    *   *Active/Focus*: Enforced high-contrast focus rings (`focus-visible:ring-2`).
    *   *Disabled*: Opacity set to 50%, cursor styled to `not-allowed`, click events bypassed.
    *   *Overlay States*: Modals or dropdowns must cast distinct drop shadows (`shadow-xl`) and mount a semi-transparent dark backdrop (`bg-black/50`) to isolate focus.

---

## 5. Form Behavior & Input Design

To prevent validation errors and streamline input operations:
*   **Form Validation States**: Input boundaries shift to semantic green (Success) or red (Error) dynamically as the user types. Error fields must display inline, descriptive text explaining the correction rule.
*   **Error Prevention**: Dropdowns, autocomplete filters, and smart switches are preferred over free-form text input fields where data constraints apply.
*   **Auto-Save Indicators**: Workspace settings and code drafts implement automatic debounced saves. A status indicator in the workspace header displays:
    *   `Saving...` (mutations queued).
    *   `Saved to Local Cache` (offline buffer active).
    *   `Changes Synced` (committed to Postgres).

---

## 6. AI Interaction, Uploads, & Generation States

*   **AI-Specific Interaction States**:
    *   *Thinking state*: The AI assistant panel renders a pulsing skeleton message container with descriptive text (e.g. `Tutor is analyzing your code trace...`) to manage performance perception.
    *   *Source Attribution*: LLM responses must display inline, clickable reference links pointing to the exact source documents or code examples used for RAG generation.
    *   *Step-up Prompts*: Operations triggered by AI proposals (like updating code configurations) must display a clear "Approve Proposal" action with step-up verification checks.
*   **Upload States**:
    *   *Quarantine Scanning state*: During malware and MIME validation loops, the file card displays a yellow spinner with status `Scanning for threats...`.
    *   *Progress state*: File transfers render a real-time progress bar displaying percentage and file size.
    *   *Error state*: Blocked files display a red card explaining the validation issue (e.g. `Invalid file type: expected PNG, got shell script`).
*   **Danger-Zone UX**:
    *   Destructive actions (such as account deletion or workspace purge) are grouped in a distinct, red-bordered "Danger Zone" container at the bottom of configurations.
    *   Triggers require typing confirmation strings (e.g. `DELETE WORKSPACE`) in addition to step-up password verification checks.

---

## 7. Loading Experience Philosophy

Loading states must reduce uncertainty and maintain layout stability. Ascendrite uses four distinct loading patterns:
*   **Skeleton Loading**: Used for predictable content structures (e.g., dashboard cards, profile layouts, and knowledge cards). Skeleton blocks mimic the dimensions of the final components to prevent layout shifts.
*   **Task-Based Loading**: Used for operations with measurable progress (e.g., AI content generation, file processing, and large asset uploads), displaying progress percentages.
*   **Descriptive Loading**: Used for long-running, variable-time operations (e.g., AI reasoning loops, vector database indexing, and recommendation compiles). Displays descriptive text explaining what system action is active.
*   **Optimistic UI**: Used for low-latency actions where success is highly likely (e.g., toggling preferences, saving code drafts, or liking community posts). The UI updates instantly, rolling back state only in the case of network failure.

---

## 8. Toasts vs. Notifications

The system keeps transient feedback separate from persistent announcements. These systems must never be combined:

### 8.1 Toast System
*   **Purpose**: Temporary, immediate visual feedback for direct user actions.
*   **Examples**: "Session established", "Draft saved", "File upload complete", "Validation failed".
*   **Characteristics**: Non-persistent (not stored in database), short-lived (disappears within 3 seconds), context-sensitive, and displayed on screen boundaries.

### 8.2 Notification System
*   **Purpose**: Stored, audit-logged announcements requiring long-term visibility.
*   **Examples**: Friend requests, direct messages, project feedback, deadline reminders, system announcements.
*   **Characteristics**: Stored in MongoDB, priority-based, time-based, supports read/unread state trackers, managed via a dedicated Notification Center, and governed by user delivery preferences.

---

## 9. Settings & User Control Center

The settings view functions as a unified dashboard separating configurations across five areas:

*   **Appearance**: Theme studio selections, custom styling adjustments, light/dark mode triggers, and visual density scaling.
*   **Accessibility**: Color contrast adjustments, screen reader enhancements, blue-light filters, reduced-motion triggers, and font size scaling.
*   **Privacy**: Visibility selectors for profile details, email addresses, study metrics, and community connections.
*   **Security**: Password rotation controls, two-factor authentication (2FA) status, session registries, and trusted device lists.
*   **Communication**: Notification frequency controls, email subscription toggles, and direct message scopes.

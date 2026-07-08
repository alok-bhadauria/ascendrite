# Product Philosophy

## Document Metadata
*   **Purpose**: Defines the architectural principles behind the product design, focusing on metadata-driven presentation.
*   **Scope**: Governs user interface design, backend API contract systems, and curriculum rendering loops.
*   **Intended Audience**: Frontend engineers, backend developers, and UI/UX designers.
*   **Related Documents**:
    *   [Project Vision](project-vision.md)
    *   [Platform Philosophy](platform-philosophy.md)
*   **Ownership**: Principal Software Architect & Lead Product Architect

---

## 1. Metadata-Driven Presentation
The presentation layer of Ascendrite is entirely dynamic. The frontend client does not hardcode folders, categories, or subject layouts. Instead, the user interface is rendered by consuming structural metadata indexes (`platform-structure.json`, `domain-taxonomy.json`, and `curriculum-map.json`). 

This decoupling ensures that:
*   Curriculum updates do not require client-side code deployments or database migrations.
*   The presentation layer remains agnostic of physical file paths or server-side directories.

---

## 2. Decoupled UI Rule
We enforce a strict separation between application code and learning content. The application is a generic container that parses structured JSON schemas and renders them. If the curriculum maps add a new subject, category, or progress pathway, the client automatically scales to display it based on standard layout definitions.

---

## 3. Adaptivity and Customization
Every learner experiences a personalized interface designed around their current progress state. The dashboard adapts dynamically based on progress metadata, rendering target nodes, locking/unlocking downstream modules, and displaying customized theme color codes defined in the subject configuration files.

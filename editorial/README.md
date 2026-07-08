# Ascendrite Editorial Division

## Document Metadata
*   **Purpose**: Introduces the publishing operations, guidebooks structure, and content review cycles of the platform.
*   **Scope**: Governs all files in the `editorial/` directory and educational JSON catalogs under `knowledge-base/`.
*   **Intended Audience**: Content authors, subject matter experts, editors, and AI generation agents.
*   **Related Documents**:
    *   [Ascendrite Master Blueprint](../blueprint/ascendrite-master-blueprint.md)
    *   [Repository Structure](../docs/development/repository-structure.md)
*   **Ownership**: Head of Editorial Division

---

## 1. Role & Objective

The Editorial Division is the publishing authority of the Ascendrite platform. It establishes the standards, validation criteria, and authoring guidelines required to produce educational materials. This ensures that every lesson, revision card, and coding exercise exhibits a unified voice, academic rigor, and instructional clarity, regardless of whether it is created by human writers or automated agents.

---

## 2. Directory Layout & Document Hierarchy

The guidebooks under `editorial/` are categorized into three areas:

```
editorial/
├── README.md                     # Directory map and publishing workflow overview
├── editorial-style-guide.md      # Core writing rules, voice, and grammar guidelines
├── educational-philosophy.md     # Pedagogical framework (Bloom's Taxonomy, Active Recall)
├── curriculum-framework.md       # Syllabus hierarchy rules and database metadata mapping
├── learning-flow.md              # Progression guidelines for subject content assets
│
├── Content Guides/               # Prescriptive guides for specific assets authoring
│   ├── content-authoring-guide.md   # Guidelines for writing core reading material
│   ├── revision-authoring-guide.md  # Rules for condensing knowledge into review cards
│   └── interview-authoring-guide.md # Standards for framing industry interview queries
│
├── Formatting Guides/            # Validation specifications for formatting
│   ├── assessment-style-guide.md    # Multiple-choice and coding assessments guidelines
│   ├── examples-style-guide.md      # Criteria for selecting and framing code examples
│   ├── diagram-style-guide.md       # Style parameters for Mermaid visualization scripts
│   ├── mathematical-style-guide.md  # Standard LaTeX templates and complexity notations
│   └── code-style-guide.md          # Naming and formatting conventions in example code
│
├── Interface & Access Guides/    # UX standards and visual design principles
│   ├── ui-ux-design-system.md       # Visual hierarchy, typography, and theme guidelines
│   └── accessibility-guidelines.md  # WCAG principles and keyboard navigation rules
│
└── Governance & Quality Guides/  # Quality assurance and AI integration rules
    ├── ai-content-governance.md     # Human-in-the-loop review rules for AI output
    ├── quality-assurance-framework.md # Review gates, acceptance rules, and validation runs
    ├── publishing-workflow.md       # Stages from draft proposal to platform publication
    ├── prompt-library.md            # Verified prompt templates for AI content agents
    └── quality-checklist.md         # Operational checklists for pre-commit checks
```

---

## 3. Reference Relationships

The documents in this directory act as the **Execution Standard** for content production:
*   **`blueprint/`**: Dictates the platform-wide architectural boundaries (the *Why*).
*   **`docs/`**: Outlines the platform system requirements and designs (the *What*).
*   **`editorial/`**: Defines the content generation guidelines and publishing workflows (the *How*).
*   **`knowledge-base/`**: Holds the metadata catalogs that power the learning application.

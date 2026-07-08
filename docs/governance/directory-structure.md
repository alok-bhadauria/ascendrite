# Documentation Scope & Directory Structure

To maintain structural clarity and operational efficiency across the Ascendrite project, a strict boundary is established between the **Editorial Division** (`editorial/`) and the **Systems Documentation** (`docs/`).

---

## 1. Editorial Division (`editorial/`)

### Operational Scope
The `editorial/` directory serves as the **Publishing Constitution** for Ascendrite. It defines the constraints, guidelines, style patterns, and quality gates for writing and formatting the educational curriculum (the notes, revision flashcards, quiz options, code examples, practice skeletons, and diagrams) inside the knowledge base.

### Files Governed
*   **[editorial-style-guide.md](../../editorial/editorial-style-guide.md)**: Master constitution defining tone, voice, structure, and structural standards.
*   **[mathematical-style-guide.md](../../editorial/mathematical-style-guide.md)**: Standard LaTeX notation matrices and KaTeX parameters.
*   **[code-style-guide.md](../../editorial/code-style-guide.md)**: Standards for coding style inside examples and practice exercises.
*   **[examples-style-guide.md](../../editorial/examples-style-guide.md)**: Architectural constraints for zero-dependency Python/JS executions.
*   **[diagram-style-guide.md](../../editorial/diagram-style-guide.md)**: Structural specs for formatting and nesting Mermaid visual layout scripts.
*   **[assessment-style-guide.md](../../editorial/assessment-style-guide.md)**: Rules for creating balanced multiple-choice diagnostic queries.
*   **[glossary-style-guide.md](../../editorial/glossary-style-guide.md)**: Constraints on keywords, tags, and technical references.
*   **[prompt-library.md](../../editorial/prompt-library.md)**: System prompt templates for LLM-based content generators.
*   **[quality-checklist.md](../../editorial/quality-checklist.md)**: Pre-commit quality assurance checklist for curriculum authors.

---

## 2. Systems Documentation (`docs/`)

### Operational Scope
The `docs/` directory serves as the **Technical Architecture Specification** for the platform. It documents the software engineering designs, high-level layouts, lower-level implementations, database schemas, API contracts, authorization models, and security principles required to build, deploy, run, and scale the Ascendrite web client, API server, and databases.

### Domain Reorganization Structure
The documentation is organized into logical engineering domains to reflect ownership boundaries:

#### 2.1 Governance Layer (`docs/governance/`)
Defines the organizational constitution, roadmap, philosophies, and processes:
*   **[project-overview.md](project-overview.md)**: General product overview and developer workflow foundations.
*   **[directory-structure.md](directory-structure.md)**: Scope definition between editorial guidebooks and technical system docs.
*   **[project-vision.md](project-vision.md)**: Core mission statement, open-access principles, and alignment.
*   **[product-philosophy.md](product-philosophy.md)**: Metadata-first presentation and client-decoupling principles.
*   **[learning-philosophy.md](learning-philosophy.md)**: The Dual-Loop Learning model (Conceptual vs. Practical loops).
*   **[engineering-principles.md](engineering-principles.md)**: Modularity, clean coding rules, SOLID adherence, and backward compatibility.
*   **[platform-philosophy.md](platform-philosophy.md)**: Workspace-first layout and dynamic theme engine rules.
*   **[ai-philosophy.md](ai-philosophy.md)**: Multi-agent boundaries and the non-replacement principle.
*   **[organizational-structure.md](organizational-structure.md)**: Ownership scopes across engineering departments.
*   **[product-evolution-strategy.md](product-evolution-strategy.md)**: Decoupled service boundaries and contract-first APIs.
*   **[version-roadmap.md](version-roadmap.md)**: Multi-phase technical roadmap and stack migration targets.
*   **[engineering-decision-process.md](engineering-decision-process.md)**: RFC proposal cycle and consensus guidelines.

#### 2.2 Systems Architecture (`docs/architecture/`)
Documents high-level system diagrams and cross-boundary integrations:
*   **[system-architecture-hld.md](../architecture/system-architecture-hld.md)**: Decoupled multi-tier system layout and scalability planning.
*   **[ai-architecture.md](../architecture/ai-architecture.md)**: RAG search flow pipelines and agent prompts configurations.

#### 2.3 Implementation & Engineering (`docs/engineering/`)
Lower-level implementations and framework-specific designs:
*   **[backend-architecture.md](../engineering/backend-architecture.md)**: FastAPI loops, logging settings, and router layers.
*   **[frontend-architecture.md](../engineering/frontend-architecture.md)**: React client views, component layout, and state stores.
*   **[database-schema.md](../engineering/database-schema.md)**: MongoDB collection models, Pydantic DTOs, and indexes.

#### 2.4 Knowledge Ingestion (`docs/knowledge/`)
Metadata schemas, parsers, caches, and validation suites:
*   **[knowledge-base-integration.md](../knowledge/knowledge-base-integration.md)**: Decentralized ingestion, JSON schemas, and content runners.

#### 2.5 Security, Operations & Development
Infrastructure rules, secure coding practices, and sandbox setups:
*   **[security-standards.md](../security/security-standards.md)**: JWT cookie bounds, network whitelists, and validation gates.

---

## 3. Knowledge Base Metadata Directory (`knowledge-base/`)

To support a completely metadata-driven knowledge architecture, several global structural indices reside at the root of `knowledge-base/`.

### Files Governed
*   **`platform-structure.json`**: Physical directory index mapping layout templates and directories. It decouples the application code from physical storage paths.
*   **`domain-taxonomy.json`**: Academic categorization tree detailing domains, disciplines, and subject groups. It organizes subjects in a generic classification structure.
*   **`knowledge-graph.json`**: Conceptual semantic graph modeling concepts and logical relationship edges (prerequisites, extensions, parts).
*   **`curriculum-map.json`**: Progression mapping relating subjects, modules, and topics to actual assets (notes, revision, example codes, diagrams) and semantic concepts.
*   **`schemas/`**: Folder containing the JSON Schema Draft 2020-12 specifications (`subject.schema.json`, `curriculum.schema.json`, `topic.schema.json`, `revision.schema.json`, `interview.schema.json`, `example.schema.json`, `practice.schema.json`, `quiz.schema.json`) for validation of all curriculum assets.

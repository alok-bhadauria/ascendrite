# Documentation Scope: Editorial vs. Systems Documentation

To maintain structural clarity and operational efficiency across the Ascendrite project, a strict boundary is established between the **Editorial Division** (`editorial/`) and the **Systems Documentation** (`docs/`).

---

## 1. Editorial Division (`editorial/`)

### Operational Scope
The `editorial/` directory serves as the **Publishing Constitution** for Ascendrite. It defines the constraints, guidelines, style patterns, and quality gates for writing and formatting the educational curriculum (the notes, revision flashcards, quiz options, code examples, practice skeletons, and diagrams) inside the knowledge base.

### Files Governed
*   **`editorial-style-guide.md`**: Master constitution defining tone, voice, structure, and structural standards.
*   **`mathematical-style-guide.md`**: Standard LaTeX notation matrices and KaTeX parameters.
*   **`code-style-guide.md`**: Standards for coding style inside examples and practice exercises.
*   **`examples-style-guide.md`**: Architectural constraints for zero-dependency Python/JS executions.
*   **`diagram-style-guide.md`**: Structural specs for formatting and nesting Mermaid visual layout scripts.
*   **`assessment-style-guide.md`**: Rules for creating balanced multiple-choice diagnostic queries.
*   **`glossary-style-guide.md`**: Constraints on keywords, tags, and technical references.
*   **`prompt-library.md`**: System prompt templates for LLM-based content generators.
*   **`quality-checklist.md`**: Pre-commit quality assurance checklist for curriculum authors.

---

## 2. Systems Documentation (`docs/`)

### Operational Scope
The `docs/` directory serves as the **Technical Architecture Specification** for the platform. It documents the software engineering designs, high-level layouts, lower-level implementations, database schemas, API contracts, authorization models, and security principles required to build, deploy, run, and scale the Ascendrite web client, API server, and databases.

### Files Governed
*   **`project-overview.md`**: Architectural overview, technical stack choices, and future roadmap phases.
*   **`system-architecture-hld.md`**: High-level decoupled multi-tier designs and scalability blueprints.
*   **`backend-architecture.md`**: Core API server setups, FastAPI loops, rate limiters, logging, and performance specs.
*   **`frontend-architecture.md`**: Single Page Application details, Zustand stores, UI styles, and accessibility rules.
*   **`database-schema.md`**: Collections modeling, validation patterns, and indexing strategies for MongoDB Atlas.
*   **`knowledge-base-integration.md`**: Parsers, caches, and validation runs for raw content ingestion.
*   **`ai-architecture.md`**: RAG pipelines, vector directories, search algorithms, and agent patterns.
*   **`security-standards.md`**: Zero Trust principles, JWT secure cookie parameters, injection blocks, and PR checks.

---

## 3. Knowledge Base Metadata Directory (`knowledge-base/`)

To support a completely metadata-driven knowledge architecture, several global structural indices reside at the root of `knowledge-base/`.

### Files Governed
*   **`platform-structure.json`**: Physical directory index mapping layout templates and directories. It decouples the application code from physical storage paths.
*   **`domain-taxonomy.json`**: Academic categorization tree detailing domains, disciplines, and subject groups. It organizes subjects in a generic classification structure.
*   **`knowledge-graph.json`**: Conceptual semantic graph modeling concepts and logical relationship edges (prerequisites, extensions, parts).
*   **`curriculum-map.json`**: Progression mapping relating subjects, modules, and topics to actual assets (notes, revision, example codes, diagrams) and semantic concepts.


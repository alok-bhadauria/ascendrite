# Ascendrite Platform Ecosystem

Ascendrite is an enterprise-grade, metadata-driven educational platform and curriculum infrastructure system. The platform translates traditional high-level technical syllabi into granular, code-driven learning roadmaps. 

This repository houses the platform's core architecture specifications, operational style guides, public database schemas, and validation pipelines, segregating the **Knowledge Infrastructure** from proprietary **Knowledge Assets**.

---

## 1. Project Vision & Governance

Ascendrite exists to democratize and accelerate advanced technical mastery. The system is designed around the locked Master Blueprint, which serves as the constitutional source of truth. All technical specs, operational pipelines, database tables, and client views derive from this blueprint's principles.

The platform separates the public framework codebase from the proprietary educational assets (Notes, Revision, Interview, Examples, Practice, Quizzes), routing all requests through the **Knowledge Service** layer:

$$\text{Platform} \longrightarrow \text{Knowledge Service} \longrightarrow \text{Knowledge Storage} \longrightarrow \text{Private Knowledge Assets}$$

---

## 2. Repository Directory Map

### 2.1 Constitutional Blueprints (`blueprint/`)
Contains locked, top-level architectural definitions and decisions:
*   **[Master Blueprint](blueprint/ascendrite-master-blueprint.md)**: Platform constitutional source of truth.
*   **[Architectural Decision Records (ADRs)](blueprint/architectural-decision-records.md)**: Record of core engineering decisions (ADR-001 through ADR-013).
*   **[Domain Reference](blueprint/domain-reference.md)**: Global business terminology reference catalog.
*   **[Engineering Checklists](blueprint/engineering-checklists.md)**: Commit checkpoints and validation criteria.

### 2.2 Technical Specifications (`docs/`)
Divided into five operational departments:
*   **Governance** (`docs/governance/`): Houses [Project Vision](docs/governance/project-vision.md), [Product Philosophy](docs/governance/product-philosophy.md), [Learning Philosophy](docs/governance/learning-philosophy.md), [Engineering Principles](docs/governance/engineering-principles.md), [Platform Philosophy](docs/governance/platform-philosophy.md), [AI Philosophy](docs/governance/ai-philosophy.md), and [Product Evolution Strategy](docs/governance/product-evolution-strategy.md).
*   **Architecture** (`docs/architecture/`): Specifies [System Architecture (HLD)](docs/architecture/system-architecture-hld.md), [Backend Architecture (LLD)](docs/architecture/backend-architecture.md), [API Architecture](docs/architecture/api-architecture.md), [Database Schema](docs/architecture/database-schema.md), [Event Architecture](docs/architecture/event-architecture.md), [State Machines](docs/architecture/state-machines.md), [Engineering Flows](docs/architecture/engineering-flows.md), and [AI Architecture](docs/architecture/ai-architecture.md).
*   **Operations** (`docs/operations/`): Details [Security Standards](docs/operations/security-standards.md), [Observability & Telemetry](docs/operations/observability-telemetry.md), [Deployment Architecture](docs/operations/deployment-architecture.md), [Monitoring](docs/operations/monitoring.md), [Backup & Recovery](docs/operations/backup-recovery.md), [Incident Response](docs/operations/incident-response.md), and [Operational Standards](docs/operations/operational-standards.md).
*   **Development** (`docs/development/`): Houses [Contribution Guide](docs/development/contribution-guide.md), [Coding Standards](docs/development/coding-standards.md), [Local Development](docs/development/local-development.md), [Environment Configuration](docs/development/environment-configuration.md), and [Testing Strategy](docs/development/testing-strategy.md).
*   **References** (`docs/references/`): Contains centralized lookup tables including [Glossary](docs/references/glossary.md), [Domain Map](docs/references/domain-map.md), [Actor Capability Matrix](docs/references/actor-capability-matrix.md), [Event Catalog](docs/references/event-catalog.md), and [Technology Decisions](docs/references/technology-decisions.md).

### 2.3 Editorial & Publishing guides (`editorial/`)
Defines the publishing department standards:
*   **[Style Guides](editorial/editorial-style-guide.md)**: Governs visual guidelines, writing voice, KaTeX mathematical conventions, and formatting constraints.
*   **[Pedagogical Frameworks](editorial/educational-philosophy.md)**: Structures Bloom's Taxonomy, Spaced Repetition flashcards, and Project-Based learning models.
*   **[Authoring Specifications](editorial/content-authoring-guide.md)**: Directs notes drafting, [Revision lists](editorial/revision-authoring-guide.md), [Interview mockups](editorial/interview-authoring-guide.md), and [MCQ formatting](editorial/assessment-style-guide.md).
*   **[Asset Guidelines](editorial/code-style-guide.md)**: Standardizes python/typescript code blocks, [Mermaid diagrams](editorial/diagram-style-guide.md), and [AI prompt templates](editorial/prompt-library.md).
*   **[QA & Review](editorial/quality-assurance-framework.md)**: Codifies pre-publication checklists, [moderation pipelines](editorial/publishing-workflow.md), and [pre-commit checklist indices](editorial/quality-checklist.md).

### 2.4 Knowledge Infrastructure (`knowledge-base/`)
Exposes metadata schema configurations and taxonomy trees:
*   **`schemas/`**: Draft 2020-12 validation schemas for subjects, modules, topics, and assets.
*   **`domain-taxonomy.json`**: Structural classification tree.
*   **`knowledge-graph.json`**: Graph relational map verifying concept prerequisite DAG boundaries.
*   **`curriculum-map.json`**: Flat index catalog relating syllabus paths to actual private assets.

---

## 3. Technology Stack & Persistence Architecture

Ascendrite prioritizes local-first execution as the primary development strategy. Database infrastructure is decoupled to allow isolated components:
*   **PostgreSQL**: Handles ACID transactions (users, permissions, settings).
*   **MongoDB**: Hosts metadata document catalogs (syllabi, concept taxonomy).
*   **Redis Cache**: In-memory transient cache layer warming data at startup.
*   **Vector Repository**: Abstracted interface engine storing embeddings (pgvector implementation default).
*   **MinIO**: Object storage housing binary files and private educational assets.

---

## 4. Ingestion & Content Validation

To ensure schema stability, contributions must pass the validation pipelines:
*   **Schema Linting**: Verifies curriculum files against JSON schemas.
*   **Graph Linting**: Validates that sitemaps contain no circular prerequisites.
*   **Audit Check**: Programmatically scans for Unicode emojis, missing citations, or unresolved identifiers.

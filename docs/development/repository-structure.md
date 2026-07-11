# Documentation Scope & Directory Structure

## Document Metadata
*   **Purpose**: Outlines the platform documentation layout, repository structure, and folder scopes.
*   **Scope**: Governs all docs/ systems files and editorial/ guidelines files.
*   **Intended Audience**: All core developers, system architects, and document contributors.
*   **Related Documents**:
    *   [Engineering Lifecycle](engineering-lifecycle.md)
*   **Ownership**: Engineering Governance Lead & Lead Product Architect

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

### Technical Documentation System Structure
The documentation is organized into five logical departments to reflect ownership boundaries:

#### 2.1 Governance (`docs/governance/`)
Defines the organizational constitution, roadmap, philosophies, and processes:
*   **[project-vision.md](project-vision.md)**: Core mission statement, open-access principles, and alignment.
*   **[product-philosophy.md](product-philosophy.md)**: Metadata-first presentation and client-decoupling principles.
*   **[platform-philosophy.md](platform-philosophy.md)**: Workspace-first layout and dynamic theme engine rules.
*   **[learning-philosophy.md](learning-philosophy.md)**: The Dual-Loop Learning model (Conceptual vs. Practical loops).
*   **[engineering-principles.md](engineering-principles.md)**: Modularity, clean coding rules, SOLID adherence, and backward compatibility.
*   **[ai-philosophy.md](ai-philosophy.md)**: Multi-agent boundaries and the non-replacement principle.
*   **[organizational-structure.md](organizational-structure.md)**: Ownership scopes across engineering departments.
*   **[product-evolution-strategy.md](product-evolution-strategy.md)**: Decoupled service boundaries and contract-first APIs.
*   **[version-roadmap.md](version-roadmap.md)**: Multi-phase technical roadmap and stack migration targets.
*   **[engineering-decision-process.md](engineering-decision-process.md)**: RFC proposal cycle and consensus guidelines.

#### 2.2 Architecture (`docs/architecture/`)
Documents high-level system diagrams and cross-boundary integrations:
*   **[system-architecture-hld.md](../architecture/system-architecture-hld.md)**: Decoupled multi-tier system layout and scalability planning.
*   **[ai-architecture.md](../architecture/ai-architecture.md)**: RAG search flow pipelines and agent prompts configurations.
*   **[backend-architecture.md](../architecture/backend-architecture.md)**: FastAPI loops, logging settings, and router layers.
*   **[frontend-architecture.md](../architecture/frontend-architecture.md)**: React client views, component layout, and state stores.
*   **[database-schema.md](../architecture/database-schema.md)**: MongoDB collection models, Pydantic DTOs, and indexes.
*   **[knowledge-base-integration.md](../architecture/knowledge-base-integration.md)**: Ingestion pipelines, JSON validation schemas, and pre-commit checks.
*   **[storage-architecture.md](../architecture/storage-architecture.md)**: Local directory layout structures, vector store index configuration, and cached assets.
*   **[api-architecture.md](../architecture/api-architecture.md)**: REST routing schemas, return payload schemas, and response validation rules.
*   **[event-architecture.md](../architecture/event-architecture.md)**: Inter-domain communication events, logging queues, and message integration rules.
*   **[state-machines.md](../architecture/state-machines.md)**: Workspace state transition validations and agent safety reviews logic.

#### 2.3 Operations (`docs/operations/`)
Infrastructure rules, server monitoring, backups, and security policies:
*   **[security-standards.md](../operations/security-standards.md)**: JWT cookie bounds, network whitelists, and validation gates.
*   **[observability-telemetry.md](../operations/observability-telemetry.md)**: Metrics collectors settings, tracing setups, and performance instrumentation.
*   **[deployment-architecture.md](../operations/deployment-architecture.md)**: Containerization rules, target environments staging-production alignment, and rollback protocols.
*   **[monitoring.md](../operations/monitoring.md)**: Active metrics alert thresholds and severity classification guidelines.
*   **[backup-recovery.md](../operations/backup-recovery.md)**: Database snapshot frequencies, retention rules, and recovery drill plans.
*   **[incident-response.md](../operations/incident-response.md)**: Escalation loops, on-call schedules, and post-mortem report templates.
*   **[operational-standards.md](../operations/operational-standards.md)**: System maintenance window rules, capacity scaling parameters, and logging retention cycles.

#### 2.4 Development (`docs/development/`)
Developer setup rules, lifecycle, and coding guides:
*   **[engineering-lifecycle.md](engineering-lifecycle.md)**: Development, staging, production loops and release pipelines.
*   **[repository-structure.md](repository-structure.md)**: Directory layout definitions across documentation and source code repositories.
*   **[contribution-guide.md](contribution-guide.md)**: Git branching naming rules, commit formatting guidelines, and PR validation steps.
*   **[coding-standards.md](coding-standards.md)**: Formatting rules, strict typing parameters, and complexity annotation rules.
*   **[local-development.md](local-development.md)**: Machine pre-requisites, dependencies installation, and local container running tools.
*   **[environment-configuration.md](environment-configuration.md)**: Environment variable naming keys, backend properties, and configuration settings.
*   **[testing-strategy.md](testing-strategy.md)**: Unit testing pyramids, integration testing targets, and CI verification pipelines.

#### 2.5 References (`docs/references/`)
Quick indexing lookups and terminology references:
*   **[glossary.md](../references/glossary.md)**: Alphabetical list of operational acronyms and term explanations.
*   **[domain-map.md](../references/domain-map.md)**: Inter-domain interfaces dependencies and package boundaries schemas.
*   **[actor-capability-matrix.md](../references/actor-capability-matrix.md)**: Role capability limits and security profiles access grids.
*   **[event-catalog.md](../references/event-catalog.md)**: Event definitions schemas and domain data properties catalogs.
*   **[technology-decisions.md](../references/technology-decisions.md)**: Framework selections, database engines, and migration roadmaps justification.
*   **[discoverability.md](../references/discoverability.md)**: Metadata schemas, crawler sitemap rules, and OpenAPI versioning standards.

---

## 3. Knowledge Base Infrastructure Directory (`knowledge-base/`)

To support a completely metadata-driven knowledge architecture, the public repository exposes only the **Knowledge Infrastructure**. Proprietary educational content represents valuable intellectual property and is managed privately via the **Knowledge Storage** system.

### Files Governed in Repository
*   **`platform-structure.json`**: Physical directory index mapping layout templates and directories. It decouples the application code from physical storage paths.
*   **`domain-taxonomy.json`**: Academic categorization tree detailing domains, disciplines, and subject groups. It organizes subjects in a generic classification structure.
*   **`knowledge-graph.json`**: Conceptual semantic graph modeling concepts and logical relationship edges (prerequisites, extensions, parts).
*   **`curriculum-map.json`**: Progression mapping relating subjects, modules, and topics to actual assets (notes, revision, example codes, diagrams) and semantic concepts.
*   **`schemas/`**: Folder containing the JSON Schema Draft 2020-12 specifications (`subject.schema.json`, `curriculum.schema.json`, `topic.schema.json`, `revision.schema.json`, `interview.schema.json`, `example.schema.json`, `practice.schema.json`, `quiz.schema.json`) for validation of all curriculum assets.

### Migration Status
The legacy educational content files residing under the domain subdirectories in the repository are migration candidates. They are scheduled for automated transfer into the private Knowledge Storage system, leaving the public `knowledge-base/` directory exclusively populated with schemas, indexes, and sample assets.

---

## 4. Repository Evolution Planning

To prepare the repository for active coding and infrastructure setup, the physical layout will evolve to include the following directories:

*   **`platform/`**: The core application server codebase:
    *   `src/`: Application source directory.
    *   `domain/`, `service/`, `repository/`, `infrastructure/`: Clear Clean Architecture subpackages.
    *   `routers/`, `middlewares/`, `dto/`: Presentation endpoints and DTO definitions.
*   **`database/`**: Persistent storage orchestration:
    *   `migrations/`: Relational schema updates and indices initialization scripts.
    *   `seeds/`: Standard bootstrap configurations and taxonomy data.
*   **`storage/`**: Object storage files:
    *   `configs/`: Object Storage (RustFS) server buckets and CORS configurations.
    *   `scripts/`: S3 sync tools to transfer Knowledge Assets from local staging folders to storage.
*   **`infrastructure/`**: Deployment configurations:
    *   `docker/`: Local development and staging Dockerfiles.
    *   `k8s/`: Kubernetes manifest deployment configurations.
    *   `monitoring/`: Prometheus alert definitions and Grafana dashboard templates.
*   **`scripts/`**: Development and validation tools:
    *   `validators/`: Pytest schema and graph integrity checkers.
    *   `loaders/`: Scripts converting raw curriculum notes into RAG vectors.



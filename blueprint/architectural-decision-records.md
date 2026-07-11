# Ascendrite Architectural Decision Records

**Version:** 1.0.0
**Status:** Approved
**Owner:** Architecture & Governance Division
**Last Updated:** 2026-07-09

### Reference Context
This document is derived directly from the constitutional source of truth, the [Ascendrite Master Blueprint](ascendrite-master-blueprint.md). For the phased implementation timeline, refer to the [Implementation Roadmap](implementation-roadmap.md). For operational checks and developer guidelines, see the [Engineering Checklists](engineering-checklists.md).

---

## Index

1. **ADR-001**: Architectural Pattern — Modular Monolith
2. **ADR-002**: Metadata-First Platform
3. **ADR-003**: Workspace-First Philosophy
4. **ADR-004**: Multi-Agent AI System
5. **ADR-005**: RAG-First Knowledge Retrieval
6. **ADR-006**: Modular Database Architecture
7. **ADR-007**: Theme Metadata System
8. **ADR-008**: Documentation as Product
9. **ADR-009**: Blueprint as Constitutional Source of Truth
10. **ADR-010**: Future Microservices Migration Strategy
11. **ADR-011**: Public Knowledge Infrastructure vs. Private Knowledge Assets
12. **ADR-012**: Knowledge Service Architecture & Hybrid Storage Model
13. **ADR-013**: Capability-Based, Inherited Permission Model
14. **ADR-014**: Object Storage Backend — Migration to RustFS

---

## ADR-001: Architectural Pattern — Modular Monolith

### Status
Approved

### Context
Ascendrite must scale effectively while minimizing operational complexity and development overhead during the initial development cycles. Deploying a distributed microservices architecture from the project's inception increases network latency, deployment complexity, and configuration overhead.

### Decision
Build the platform as a modular monolith. Enforce clean separation of domains at the code level, keeping business boundaries distinct through restricted interfaces, package imports, and module APIs.

### Alternatives Considered
- **Distributed Microservices**: Rejected due to premature operational overhead, network latency, and complexity in managing shared state during early stages.
- **Unstructured Monolith**: Rejected due to lack of scalability and risk of codebase entropy.

### Consequences
- **Positive**: Simplifies local deployment, testing, and debugging. Enforces domain boundaries.
- **Negative**: Requires strict static analysis and code reviews to prevent boundary leaks.

---

## ADR-002: Metadata-First Platform

### Status
Approved

### Context
Educational content must remain separate from presentation layers to enable continuous updates without client-side redeployments. hardcoding syllabus structures or layout instructions directly into frontend code increases code churn and restricts multi-platform support.

### Decision
Adopt a metadata-first system where every level of the knowledge graph (Domain, Discipline, Subject, Module, Topic, Concept, Asset) carries standardized metadata specifying its hierarchy, relations, and display configurations.

### Alternatives Considered
- **Code-Driven Hierarchy**: Rejected due to high maintenance overhead.
- **Relational-Only Tables**: Rejected as it complicates graph relationships and dynamic rendering.

### Consequences
- **Positive**: Frontend applications function as thin, dynamic renderers. Knowledge bases can evolve independently.
- **Negative**: Requires strict schema validation layers to enforce metadata integrity.

---

## ADR-003: Workspace-First Philosophy

### Status
Approved

### Context
Traditional learning management systems force learners to switch between disconnected pages for lessons, practice environments, projects, note-taking, and support channels, causing context switching and fragmented user sessions.

### Decision
Design the user experience around a stateful, persistent Workspace that unifies all learning modules, note scratchpads, project environments, and AI interactions within a single, continuous interface.

### Alternatives Considered
- **Standard Tabbed Navigation**: Rejected due to high context switching and loss of state during learning workflows.
- **Multi-App Layout**: Rejected due to fragmentation of the user journey.

### Consequences
- **Positive**: Eliminates workflow friction, improves user focus, and maintains session context.
- **Negative**: Increases frontend state complexity and browser resource management overhead.

---

## ADR-004: Multi-Agent AI System

### Status
Approved

### Context
Monolithic AI prompts are brittle, expensive to process, and struggle to perform diverse specialized operations such as navigation help, learning feedback, and code assessment within one set of instructions.

### Decision
Implement the AI layer as specialized independent agents managed by an orchestration registry. Each agent operates with a bounded scope, specific system instructions, and targeted tool access.

### Alternatives Considered
- **Monolithic Chatbot**: Rejected due to prompt engineering limits and context contamination.
- **Direct API Integrations**: Rejected due to lack of unified tracing and orchestration controls.

### Consequences
- **Positive**: Improves prompt maintainability, enables targeted optimization of individual agents, and limits context token costs.
- **Negative**: Requires a central orchestrator to manage agent lifecycles and state transitions.

---

## ADR-005: RAG-First Knowledge Retrieval

### Status
Approved

### Context
Generative AI models are prone to hallucinating factual errors and lack direct context about the platform's proprietary syllabus layout, subject maps, and educational metadata standards.

### Decision
Deploy Retrieval-Augmented Generation (RAG) as the default retrieval pipeline for all user-facing educational agents. The platform retrieves verified knowledge assets and context before sending prompts to the LLM.

### Alternatives Considered
- **Model Fine-Tuning**: Rejected due to high training cost and inability to easily deprecate outdated material.
- **Zero-Shot Prompting**: Rejected due to high rates of factual hallucination.

### Consequences
- **Positive**: Enforces accurate, syllabus-aligned AI responses and minimizes model hallucinations.
- **Negative**: Introduces query processing latencies and vector database storage requirements.

---

## ADR-006: Modular Database Architecture

### Status
Approved

### Context
A unified database schema with broad cross-domain joins leads to tight database coupling, preventing modular scaling and introducing single points of failure across unrelated domains.

### Decision
Implement a modular database architecture where each business domain owns its collection or tables. Inter-domain queries must occur through service layer APIs rather than direct database joins.

### Alternatives Considered
- **Shared Schema with Global Joins**: Rejected as it violates the boundary rules of the modular monolith.
- **Independent Database Instances**: Rejected due to excessive operational complexity in local environments.

### Consequences
- **Positive**: Domain storage remains decoupled, enabling independent indexing, query optimization, and future database migrations.
- **Negative**: Requires application-level data aggregation and resolution of distributed reads.

---

## ADR-007: Theme Metadata System

### Status
Approved

### Context
Personalization and accessibility requirements demand flexible UI adjustments (such as dark mode, high-contrast, or tailored fonts). Hardcoding styling variables in static sheets prevents runtime updates.

### Decision
Store and distribute visual configurations as dynamic theme metadata. Client applications read theme JSON schemas from the backend and map variables directly to UI element properties at runtime.

### Alternatives Considered
- **Static Compiled Stylesheets**: Rejected as they prevent user-level personalization and backend style injection.
- **Inline Style Rules**: Rejected due to performance implications and poor maintainability.

### Consequences
- **Positive**: Supports absolute styling control from the backend, custom themes, and dynamic accessibility overrides.
- **Negative**: Requires the client to parse theme metadata configurations before initial page renders.

---

## ADR-008: Documentation as Product

### Status
Approved

### Context
Unsynchronized documentation, architectural drift, and poor onboarding guides slow down development cycles and impact code quality across engineering contributors.

### Decision
Treat internal documentation, technical references, and architectural files as first-class product assets. Manage them via markdown in version control, and review them as part of the pull request lifecycle.

### Alternatives Considered
- **External Wiki Storage**: Rejected as documents drift from the current state of source code.
- **Implicit Knowledge (No Written Docs)**: Rejected due to onboarding bottlenecks.

### Consequences
- **Positive**: Maintains documentation accuracy and alignment with current implementation details.
- **Negative**: Increases pull request review time to ensure compliance with editorial standards.

---

## ADR-009: Blueprint as Constitutional Source of Truth

### Status
Approved

### Context
Large projects with diverse contributors (both humans and AI agents) are highly susceptible to feature creep, architectural drift, and philosophical inconsistency over time.

### Decision
Lock the Ascendrite Master Blueprint as the constitutional source of truth. All companion guidebooks, roadmaps, metadata schemas, and implementations must align with this blueprint's locked vision.

### Alternatives Considered
- **Evolutionary Architecture (No Locked Source)**: Rejected as it increases the risk of feature creep and system entropy.

### Consequences
- **Positive**: Prevents architectural drift and establishes a clear evaluation standard for new changes.
- **Negative**: Requires a formal review and approval process to introduce any blueprint revisions.

---

## ADR-010: Future Microservices Migration Strategy

### Status
Approved

### Context
Certain services (such as AI model inference or operational telemetry logging) will scale at vastly different rates than CRUD actions, eventually bottlenecking the modular monolith.

### Decision
Define a clear migration strategy to extract modular domains into independent microservices once monitoring and performance metrics indicate scaling bottlenecks.

### Alternatives Considered
- **Indefinite Monolithic Scaling**: Rejected due to resource consumption bottlenecks.
- **Premature Microservices Architecture**: Rejected via ADR-001.

### Consequences
- **Positive**: Prevents premature optimization while providing a logical pathway for system scaling.
- **Negative**: Requires careful design of API boundaries in the monolith to ensure services are clean-cut.

---

## ADR-011: Public Knowledge Infrastructure vs. Private Knowledge Assets

### Status
Approved

### Context
Educational content represents valuable, proprietary intellectual property (IP). Committing actual lessons, assessments, and mock interviews directly into a public source control repository risks IP exposure.

### Decision
Segregate the knowledge base into two systems:
1. **Knowledge Infrastructure (Public)**: Exposes schemas, templates, build indexing validators, and mock assets inside the repository.
2. **Knowledge Assets (Private)**: Stores actual, proprietary notes, revision flashcards, quizzes, and code exercises outside version control.

### Alternatives Considered
- **All-in-Git Strategy**: Rejected due to IP exposure risk.
- **Entirely Private Repo**: Rejected as it limits open-source framework contributions and public infrastructure validation.

### Consequences
- **Positive**: Protects proprietary curriculum assets while keeping framework code open-source.
- **Negative**: Requires a deployment workflow to compile and ingest Knowledge Assets into Knowledge Storage.

---

## ADR-012: Knowledge Service Architecture & Hybrid Storage Model

### Status
Approved

### Context
Direct filesystem reads of JSON assets introduce structural coupling, slowing database migrations and preventing independent component scaling.

### Decision
Establish a dedicated **Knowledge Service** layer. Client and backend services query the Knowledge Service, which mediates all access to the underlying storage engines:
*   Metadata and Relationships map to MongoDB.
*   Proprietary assets map to **Managed Knowledge Storage** buckets.
*   Binary assets (diagrams, images) map to S3-compatible object stores (locally backed by RustFS).
*   High-dimensional concept indexes map to a Vector Database.

### Alternatives Considered
- **Direct Database/Filesystem Access**: Rejected due to tight database coupling.

### Consequences
- **Positive**: Total storage engine independence. Layout and structural changes are fully abstracted.
- **Negative**: Increases network call routing steps between services.

---

## ADR-013: Capability-Based, Inherited Permission Model

### Status
Approved

### Context
Hardcoded organizational roles are inflexible, failing to support fine-grained scoping required by administrators, external organizations, classrooms, and AI agents.

### Decision
Implement a capability-based, permission-driven access control model. Permissions (Read, Write, Review, Approve, Publish, Archive, Delete, Configure, Manage) are assigned independently and inherit downward through the curriculum taxonomy:

$$\text{Platform} \longrightarrow \text{Domain} \longrightarrow \text{Subject} \longrightarrow \text{Module} \longrightarrow \text{Topic} \longrightarrow \text{Asset}$$

### Alternatives Considered
- **Flat RBAC Role Checks**: Rejected due to lack of scoping flexibility.

### Consequences
- **Positive**: Absolute granularity of access. AI agents can be restricted to targeted workspaces.
- **Negative**: Requires recursive authority checks during authorization evaluations.

---

## ADR-014: Object Storage Backend — Migration to RustFS

### Status
Approved

### Context
Initially, MinIO was planned as the S3-compatible local development object storage backend. However, to minimize the local footprint on Windows workstations, prevent Docker runtime dependencies, and ensure native performance via a statically compiled binary, a single-executable alternative was required.

### Decision
Migrate the local development object storage backend to **RustFS (1.0.0-beta.8)** running as an automatic Windows service (`AscendriteRustFS`). The application runtime continues to interact with S3 via standard S3 API client libraries, keeping the domain logic fully decoupled from the storage engine.

### Alternatives Considered
- **Local MinIO Service**: Rejected due to larger memory footprint and extra configuration overhead compared to a single static binary.
- **Local Filesystem Emulation**: Rejected because it prevents the application from utilizing authentic S3 bucket policy and versioning semantics during testing.

### Consequences
- **Positive**: Lightweight execution (compiled in Rust), zero external dependencies, robust S3 API compatibility validated via AWS CLI.
- **Negative**: Requires configuring a Windows service wrapper (WinSW) for background management.



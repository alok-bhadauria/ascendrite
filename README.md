# Ascendrite Platform Ecosystem

```
                            ASCENDRITE
-------------------------------------------------------------------
        Knowledge | Intelligence | Infrastructure | Learning

                   Learner / Educator / Developer / AI Agent
                                     |
                                     v
                            API Gateway (FastAPI)
                                     |
                     +---------------+---------------+
                     |                               |
                     v                               v
        Platform Infrastructure             Knowledge Services
      (RBAC, Workspace, Auditing)         (Syllabi, Graphs, RAG)
                     |                               |
    +----------------+----------------+--------------+----------------+
    |                |                |              |                |
    v                v                v              v                v
PostgreSQL        MongoDB          Memurai        pgvector         RustFS
(Relational)      (Metadata)     (Cache/Volatile) (Embeddings)    (Object/S3)
```

Ascendrite is an enterprise-grade, metadata-driven educational platform ecosystem and knowledge infrastructure system. The ecosystem translates technical curricula into granular, code-driven learning roadmaps, treating educational knowledge as structured, queryable, and mathematically validated resources.

This repository serves as the canonical source for the platform's core architecture specifications, governance guidelines, validation engines, and local platform orchestrators. It separates the public framework codebase from private, proprietary educational assets via clean service and storage abstractions.

---

## 1. Vision and Product Philosophy

Traditional educational content is frequently fragmented across disconnected tools, static formats, and isolated courses. Ascendrite resolves this challenge by treating knowledge as an interconnected Directed Acyclic Graph (DAG) of concepts, modules, and learning assets.

The platform provides:
*   **Structured Metadata Boundaries**: Content structure is decoupled from platform rendering logic, allowing the knowledge base to evolve independently.
*   **Segregated Content Lifecycle**: A strict division separates public platform infrastructure from proprietary knowledge assets, protecting intellectual property while ensuring developer flexibility.
*   **Role-Based & Capability-Based Access**: Multi-actor security models govern read, write, moderation, and administrative capability scopes.
*   **AI Agency & Retrieval-Augmented Generation**: Bounded AI workflows access validated platform schemas and semantic repositories prior to inference, ensuring high-fidelity, hallucination-resistant assistance.

---

## 2. Core Architectural Principles

The architecture is governed by the principles defined in the constitutional [Master Blueprint](blueprint/ascendrite-master-blueprint.md) and the [Architectural Decision Records](blueprint/architectural-decision-records.md).

### 2.1 Separation of Concerns
The core platform is structured as a modular monolith following Clean Architecture boundaries:
*   **Domain Layer**: Houses pure business entities, graph invariants, and domain definitions across Knowledge, Learning, and Assessment platforms.
*   **Service Layer**: Orchestrates database transactions, publishing workflows, team assignments, and operational administration capabilities.
*   **Repository Layer**: Abstracts storage implementations (PostgreSQL, MongoDB, vector registries, object storage).
*   **Infrastructure Layer**: Exposes FastAPI endpoints, handles authentication, and interfaces with external network utilities.

For details, refer to the [System Architecture HLD](docs/architecture/system-architecture-hld.md) and [Backend Architecture](docs/architecture/backend-architecture.md).

### 2.2 Security & Trust Boundary
*   **Deny-by-Default Authorization**: All API capabilities require explicit actor-role mappings defined in the [Actor Capability Matrix](docs/references/actor-capability-matrix.md).
*   **Opaque Session Management**: User session tokens are high-entropy identifiers stored in secure, server-managed cookies with `HttpOnly`, `Secure` (in HTTPS staging/production), and `SameSite=Lax` flags. LocalStorage storage of session identifiers is strictly prohibited.
*   **Step-Up Authentication**: Elevated-risk actions (modifying credentials) or destructive actions (purging data) require immediate confirmation or multi-factor signatures, as codified in the [Security Standards](docs/operations/security-standards.md).
*   **Adaptive CAPTCHA Challenge**: High-abuse candidate flows (signup, password recovery, verification resends) trigger adaptive challenges only when risk parameters require them. Safe operations remain exempt.
*   **API Key Management**: Integrations authenticate using public identifiers for database indexing and high-entropy API secrets validated server-side using SHA-256 and constant-time match blocks.

### 2.3 Storage & Persistence Boundaries
Rather than using a single database, storage responsibilities are strictly divided by access patterns:
*   **PostgreSQL 18.4**: Serves as the relational store for structured transactional metadata (user identities, workspace settings, capability assignments, and security audit logs). See the [Database Schema](docs/architecture/database-schema.md).
*   **MongoDB Community Server 8.0.26**: Serves as the document catalog for curriculum structures, taxonomy definitions, and knowledge graphs.
*   **Memurai / Redis compatibility**: Acts strictly as a transient caching layer. No primary write commits directly to the cache; it is warmed at startup or populated on-demand.
*   **Vector Repository (pgvector)**: Abstracted behind a provider-neutral interface to handle semantic embeddings query similarity checks.
*   **RustFS S3 API**: Handles binary objects and private knowledge assets through a validated secure file promotion and quarantine pipeline.

For detailed storage mechanics, see the [Storage Architecture](docs/architecture/storage-architecture.md).

---

## 3. Repository Directory Structure

The repository organizes specifications, schemas, guides, and codebase modules logically:

```
Ascendrite/
├── blueprint/                  # Constitutional blueprint & roadmap definitions
├── docs/                       # Comprehensive technical specifications
│   ├── architecture/           # System, LLD, Database, Storage, API, and AI designs
│   ├── development/            # Guides for setup, coding, lifecycle, and testing
│   ├── governance/             # Constitutional values, vision, and principles
│   ├── operations/             # Security, telemetry, backup, and deployment standards
│   └── references/             # Central lookup tables, glosssary, and maps
├── editorial/                  # Content layout, style, assessment, and UI specifications
├── knowledge-base/             # Structural JSON metadata files and taxonomy schemas
└── platform/                   # Core application codebase
    ├── assets/                 # Global styling variables and static assets
    ├── client/                 # Frontend SPA codebase (React / Vite)
    └── server/                 # API backend codebase (FastAPI / Python)
```

For more detailed structure mapping, refer to the [Repository Structure](docs/development/repository-structure.md) documentation.

---

## 4. Technology & Infrastructure Matrix

The current local development and persistence stack is verified to run natively on Windows 11:

| Component | Target Technology | Service / Command Name | Port / Protocol | Expected State |
| :--- | :--- | :--- | :--- | :--- |
| Database (ACID) | PostgreSQL 18.4 | `postgresql-x64-18` | `127.0.0.1:5432` | Windows Service |
| Database (Docs) | MongoDB Community 8.0.26 | `MongoDB` | `127.0.0.1:27017` | Windows Service |
| Transient Cache | Memurai Developer 4.2.3 | `Memurai` | `127.0.0.1:6379` | Windows Service |
| Object Storage | RustFS 1.0.0-beta.8 | `AscendriteRustFS` | `127.0.0.1:9000` (API) | Windows Service |
| Storage Console | RustFS Console | `AscendriteRustFS` | `127.0.0.1:9001` (HTTP) | Web Console |
| Backend API | Python 3.10.11 / FastAPI | Uvicorn Server | `127.0.0.1:8000` (HTTP) | Managed Process |
| Frontend SPA | React / Node.js / Vite | Dev Server | `localhost:5173` (HTTP) | Managed Process |

The API backend encapsulates operational platform modules under standardized v1 route prefixes: `/api/v1/creator` (workspaces & publishing), `/api/v1/collaboration` (teams & tasks), and `/api/v1/admin` (system configuration & telemetry).

---

## 5. Development & Operations

Local platform orchestration and operational workflows are managed via specialized utilities.

### 5.1 The Ascendrite Platform Manager
Developers launch the local stack using the Windows-native control script:

```cmd
E:\Projects\Ascendrite> run-ascendrite.bat
```

The script runs as a self-contained polyglot batch/PowerShell manager at the repository root that exposes:
*   **Unified Service Monitoring**: Reads Windows Service query APIs (`sc.exe`) alongside TCP port scans to verify services are active and reachable.
*   **Safe PID & Process-Tree Ownership**: Writes process coordinates to `E:\Projects\ascendrite-data\runtime\`. Before termination, it validates that active PIDs belong to the managed process tree, eliminating accidental port-based termination of unrelated developer tools.
*   **Isolated Redirections**: Pipes uvicorn/npm output to `logs/backend.log` and `logs/frontend.log` respectively, avoiding file-locking write contentions.

```
================================================================
                  ASCENDRITE PLATFORM MANAGER                   
================================================================
 Infrastructure Status:
   PostgreSQL:         [ONLINE]  (Service: postgresql-x64-18, Port: 5432)
   MongoDB:            [ONLINE]  (Service: MongoDB, Port: 27017)
   Memurai / Redis:    [ONLINE]  (Service: Memurai, Port: 6379)
   RustFS S3 API:      [ONLINE]  (Service: AscendriteRustFS, Port: 9000)
   RustFS Console:     [ONLINE]  (Service: AscendriteRustFS, Port: 9001)

 Application Status:
   Backend API:        [OFFLINE] (Port: 8000)
   Frontend:           [OFFLINE] (Port: 5173)
================================================================
  [1] Start Application Stack
  [2] Start Full Development Stack
  [3] Stop Application Stack
  [4] Manage Infrastructure
  [5] Manage Application
  [6] Health and Diagnostics
  [7] Open Service URLs
  [8] View Logs
  [9] Refresh Dashboard
  [0] Exit
================================================================
```

For configuration specifics, review [Local Development](docs/development/local-development.md) and [Environment Configuration](docs/development/environment-configuration.md). Note that configuration is unified around a single `.env.local` file at the repository root; nested backend environment files (like `platform/server/.env`) are prohibited.

### 5.2 Quality Gates & Validation Engines
All repository updates must pass validation scripts located in `scratch/` prior to version commits:
*   `validate_docs_standards.py`: Verifies link integrity, directory structures, and scans for prohibited unicode emojis or absolute path strings.
*   `validate_knowledge_integrity.py`: Validates taxonomic schemas, curriculum mappings, and prerequisites concept mapping DAG cycles.
*   `validate_ai_notes.py`: Evaluates content formatting, mathematical latex validation, and academic structure layout standards.

### 5.3 Automated Integration Test Suite
The platform backend features comprehensive integration and regression test suites powered by `pytest`. Run all verification suites using:

```cmd
python -m pytest -v platform/server/tests
```

---

## 6. Implementation Roadmap

Ascendrite operates on a phased rollout. The system is transitioning from architectural baseline validation into active platform codebase development.

```
+------------------------------------+
|  1. Architecture & Specs (LOCKED)  |
+------------------+-----------------+
                   |
                   v
+------------------------------------+
| 2. Infrastructure Setup (VERIFIED) |
+------------------+-----------------+
                   |
                   v
+------------------------------------+
| 3. Dev Tooling & Manager (COMPLETE)|
+------------------+-----------------+
                   |
                   v
+------------------------------------+
| 4. Core Backend Platform (COMPLETE)|
+------------------+-----------------+
                   |
                   v
+------------------------------------+
|  5. Active APIs & Release (ACTIVE) |
+------------------------------------+
```

*   **V1 Implementation Focus**: Initialization of FastAPI core repository modules, DB migrations, session token validation, and object promotion middlewares.
*   **V1 Direct API Specifications**: Developer endpoints `/api/v1/openapi.json`, Swagger UI (`/docs`), and ReDoc (`/redoc`) are core requirements to be exposed dynamically by the server.
*   **Deferred Items**: Production container orchestrators, external verification provider registrations (Cloudflare Turnstile token routing), and the public discoverability text surface `/llms.txt` remain deferred until Phase 8.

See the complete [Implementation Roadmap](blueprint/implementation-roadmap.md) for exit criteria.

---

## 7. Reference Entry Points

Select the appropriate document directory to begin development or review:

*   **System Architects**: Focus on the constitutional blueprint in the [Master Blueprint](blueprint/ascendrite-master-blueprint.md), the high-level architecture in the [System Architecture HLD](docs/architecture/system-architecture-hld.md), and the history of design choices in the [Architectural Decision Records](blueprint/architectural-decision-records.md).
*   **Backend Engineers**: Reference the LLD specifications in [Backend Architecture](docs/architecture/backend-architecture.md), table models in [Database Schema](docs/architecture/database-schema.md), and payload details in [API Architecture](docs/architecture/api-architecture.md).
*   **Security Reviewers**: Audit compliance rules in the [Security Standards](docs/operations/security-standards.md) and token models in [API Architecture](docs/architecture/api-architecture.md) (Section 6).
*   **Content Editors**: Review pedagogical guidelines in the [Educational Philosophy](editorial/educational-philosophy.md), visual styling in the [UI/UX Design System](editorial/ui-ux-design-system.md), and draft specs in [Content Authoring Guide](editorial/content-authoring-guide.md).
*   **System Operations**: Configure host properties via [Local Development](docs/development/local-development.md) and configure environment variables in [Environment Configuration](docs/development/environment-configuration.md).

---

## 8. Developer Contribution Policy

All backend contributions must adhere to clean architecture design principles, preserve the distinct domain ownership boundaries, and maintain 100% test coverage safety. Run validation scripts located in `scratch/` locally before staging commits.

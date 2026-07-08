# Backend Architecture: Low-Level Design (LLD) & Modules Boundaries

## Document Metadata
*   **Purpose**: Outlines the low-level design structures, packages, dependency directions, module boundaries, and coding standards.
*   **Scope**: Governs backend directory layouts, library code dependencies, and server-side software boundaries.
*   **Intended Audience**: Backend developers, systems integrators, and engineering coordinators.
*   **Related Documents**:
    *   [System Architecture (HLD)](system-architecture-hld.md)
    *   [Repository Structure](../development/repository-structure.md)
*   **Ownership**: Head of Platform Engineering

---

## 1. Low-Level Design (LLD) & Package Topology

The backend uses a clean architecture layout. All software elements are grouped into distinct layers, ensuring isolation of business logic from infrastructure databases:

```
+-----------------------------------------------------------------+
|                      Infrastructure Layer                       |
|  - FastAPI Routers & Middleware    - MongoDB/Redis Drivers      |
|  - Vector Store Client             - MinIO S3 API Adapters      |
+-----------------------------------------------------------------+
                               |
                               v
+-----------------------------------------------------------------+
|                       Repository Layer                          |
|  - Database collection adapters    - Query executors            |
|  - Transaction coordinators                                     |
+-----------------------------------------------------------------+
                               |
                               v
+-----------------------------------------------------------------+
|                       Service Layer                             |
|  - Business transaction logic      - Validation middlewares     |
|  - DTO mapping converters                                       |
+-----------------------------------------------------------------+
                               |
                               v
+-----------------------------------------------------------------+
|                         Domain Layer                            |
|  - Domain entities                 - State machine engines      |
|  - Core invariant rules                                         |
+-----------------------------------------------------------------+
```

### 1.1 Package Responsibilities
*   `domain/`: Contains pure business objects, core validations, and state machine configurations. It has zero dependencies on external databases, frameworks, or libraries.
*   `service/`: Orchestrates transaction flows, translates query structures, maps validation errors, and handles third-party APIs.
*   `repository/`: Implements raw database read/write actions, connection configurations, and schema migrations.
*   `infrastructure/`: Houses entry web routes, FastAPI application servers, request handlers, telemetry instrumentation, and configurations.
*   `shared/`: Reusable, utility helper libraries (e.g. date arithmetic, crypto checks, string conversions) that have no references to service structures.

### 1.2 Dependency Direction Rules
*   **Core Independence**: The Domain layer lies at the center. It must never import packages from the Service, Repository, or Infrastructure layers.
*   **Inward Dependency**: Dependency references must flow strictly inward:
    $$\text{Infrastructure} \longrightarrow \text{Repository} \longrightarrow \text{Service} \longrightarrow \text{Domain}$$
*   **DTO Ownership**: Data Transfer Objects (DTOs) representing API request payloads or response envelopes are owned by the Service layer. The presentation layer (FastAPI routers) parses and returns DTO models, preventing database domain entities from leaking to clients.

---

## 2. Platform Module Boundaries & Responsibilities

The backend is partitioned into fourteen distinct modules. Each module enforces strict boundary definitions to ensure decouple-ability:

### 2.1 Authentication
*   **Ownership**: Identity Domain
*   **Responsibilities**: Manages credentials verification, refresh token rotation, and JWT signing.
*   **Boundaries**: Exposes public login, logout, and token refresh endpoints.
*   **Dependencies**: User Management (to retrieve actor profiles).
*   **Extension Points**: Webhooks for login events (`identity.session.created`).

### 2.2 User Management
*   **Ownership**: Identity Domain
*   **Responsibilities**: Governs user profile schemas, registration states, and actor roles.
*   **Boundaries**: Isolated user database collections. No direct access by external services.
*   **Dependencies**: None.
*   **Extension Points**: Registration event triggers (`identity.user.registered`).

### 2.3 Workspace
*   **Ownership**: Workspace Domain
*   **Responsibilities**: Persists client layout properties, active tab indexes, and sync logs.
*   **Boundaries**: Coordinates the Workspace state machine.
*   **Dependencies**: Authentication, User Management.
*   **Extension Points**: Sync completion hooks (`workspace.sync.completed`).

### 2.4 Knowledge
*   **Ownership**: Knowledge Domain
*   **Responsibilities**: Ingests curriculum data, validates metadata schemas, and handles RAG chunking.
*   **Boundaries**: Wraps all access to private files via the Knowledge Service interface.
*   **Dependencies**: None.
*   **Extension Points**: Index compilation event hooks (`knowledge.catalog.indexed`).

### 2.5 Search
*   **Ownership**: Platform Domain
*   **Responsibilities**: Tokenizes and indexes curriculum nodes for fast query responses.
*   **Boundaries**: Evaluates user credentials prior to returning matches.
*   **Dependencies**: Knowledge (to retrieve index data).
*   **Extension Points**: Custom search query preprocessors.

### 2.6 Recommendation
*   **Ownership**: Intelligence Domain
*   **Responsibilities**: Generates personal progression logs and schedules review tracks.
*   **Boundaries**: Exposes recommendations DTO payloads via the API router.
*   **Dependencies**: Knowledge, Telemetry.
*   **Extension Points**: Custom path calculation strategies.

### 2.7 AI
*   **Ownership**: Intelligence Domain
*   **Responsibilities**: Generates high-dimensional vectors and routes proxy LLM queries.
*   **Boundaries**: Enforces input/output validation guardrails.
*   **Dependencies**: Knowledge (for RAG context), Telemetry.
*   **Extension Points**: Custom guardrail filter configurations.

### 2.8 Notifications
*   **Ownership**: Platform Domain
*   **Responsibilities**: Triggers toast notifications and handles persistent alert queues.
*   **Boundaries**: Directs dispatches through WebSockets or mail gateways.
*   **Dependencies**: User Management.
*   **Extension Points**: Custom notification delivery channels (e.g. SMTP, Push).

### 2.9 Telemetry
*   **Ownership**: Operations Domain
*   **Responsibilities**: Ingests performance metrics and records application traces.
*   **Boundaries**: Restricts metrics collection route access to authorized scraper scrapers.
*   **Dependencies**: None.
*   **Extension Points**: Custom metrics exporters.

### 2.10 Administration
*   **Ownership**: Operations Domain
*   **Responsibilities**: Manages system environment variables, permission changes, and audit logs.
*   **Boundaries**: Restricts endpoint access strictly to Admin actors.
*   **Dependencies**: User Management.
*   **Extension Points**: Audit log output writers.

### 2.11 Settings
*   **Ownership**: Platform Domain
*   **Responsibilities**: Persists theme selections, accessibility preferences, and privacy tags.
*   **Boundaries**: Settings data collections are isolated per user.
*   **Dependencies**: User Management.
*   **Extension Points**: Custom theme loading hooks.

### 2.12 Media
*   **Ownership**: Platform Domain
*   **Responsibilities**: Manages binary image assets and scans file uploads.
*   **Boundaries**: Restricts uploads strictly to sandboxed workspace folders.
*   **Dependencies**: Authentication.
*   **Extension Points**: Custom anti-virus scanner adapters.

### 2.13 Organizations
*   **Ownership**: Workspace Domain
*   **Responsibilities**: Coordinates classrooms, assignments, and group projects.
*   **Boundaries**: Restricts access based on organizational authorization tokens.
*   **Dependencies**: User Management, Workspace.
*   **Extension Points**: Assignment creation hooks.

### 2.14 Communication
*   **Ownership**: Platform Domain
*   **Responsibilities**: Handles direct messages, connection links, and announcements.
*   **Boundaries**: Syncs messages securely through WebSocket handlers.
*   **Dependencies**: User Management.
*   **Extension Points**: External chat client adapters.

---

## 3. Engineering & Design Standards

*   **No Cross-Domain Database Joins**: Database collections belonging to one module must not be joined or directly queried by other modules. Cross-domain queries must query the target module's Service layer API.
*   **Transaction Boundaries**: Services manage transactional units. Operations that cross database collections must run within unit-of-work transactions.
*   **Backward Compatibility**: Metadata schema changes must use optional fields and default values, allowing legacy client versions to parse new response payloads without crashing.
*   **Extension Hooks**: Module actions must publish events to the event bus, allowing other systems to extend behavior without modifying the core service files.

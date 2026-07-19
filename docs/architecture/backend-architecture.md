# Backend Architecture: Low-Level Design (LLD) & Modules Boundaries

## Document Metadata
*   **Purpose**: Outlines the low-level design structures, clean architecture layers, dependency directions, module boundaries, error standards, and coding constraints.
*   **Scope**: Governs backend directory layouts, library code dependencies, and server-side software boundaries.
*   **Intended Audience**: Backend developers, systems integrators, and engineering coordinators.
*   **Related Documents**:
    *   [System Architecture (HLD)](system-architecture-hld.md)
    *   [Repository Structure](../development/repository-structure.md)
    *   [Security Standards](../operations/security-standards.md)
*   **Ownership**: Head of Platform Engineering

---

## 1. Low-Level Design (LLD) & Package Topology

The backend uses a clean architecture layout. All software elements are grouped into distinct layers, ensuring isolation of business logic from infrastructure databases:

```
+-----------------------------------------------------------------+
|                      Infrastructure Layer                       |
|  - FastAPI Routers & Middleware    - MongoDB/Redis Drivers      |
|  - Vector Store Client             - RustFS S3 API Adapters     |
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
*   `domain/`: Contains pure business objects, core validation models, and state machine configurations. It has zero dependencies on external databases, frameworks, or libraries.
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

The backend is partitioned into distinct modules. Each module enforces strict boundary definitions to ensure decouple-ability:

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

### 2.13 Organizations (V2 Future Concept)
*   **Ownership**: Workspace Domain
*   **Responsibilities**: Coordinates classrooms, assignments, and group projects. (Deferred in V1).
*   **Boundaries**: Restricts access based on organizational authorization tokens.
*   **Dependencies**: User Management, Workspace.
*   **Extension Points**: Assignment creation hooks.

### 2.14 Communication (V1-Ready / Deferred)
*   **Ownership**: Platform Domain
*   **Responsibilities**: Handles direct messages, connection links, and announcements.
*   **Boundaries**: Syncs messages securely through WebSocket handlers.
*   **Dependencies**: User Management.
*   **Extension Points**: External chat client adapters.

---

## 3. Background Jobs, Retries & Correlation IDs

The backend platform handles long-running processing tasks and telemetry logs using structured, stateless asynchronous routines:
*   **Background Jobs Queue**: Tasks (such as RAG embedding generation, PDF textbook compilation, and email dispatches) are pushed to an in-memory queue (Redis-backed Celery/rq tasks). In V1, the server falls back to FastAPI's background tasks for local execution.
*   **Retry Policy with Exponential Backoff**: Outgoing third-party requests (e.g. OpenAI API tutor queries) implement retry loops with exponential backoff and jitter constraints:
    *   *Retry Count*: 3 attempts.
    *   *Wait Interval*: $2^n \text{ seconds} + \text{jitter}$ (where $n$ is the retry attempt).
*   **Correlation & Request Tracking**: Every incoming request is intercepted by the `CorrelationIDMiddleware`.
    1.  The middleware checks for the `X-Correlation-ID` header. If absent, a new UUIDv4 is generated.
    2.  The correlation ID is attached to the thread-local logger context and injected into all transaction logs.
    3.  The ID is returned in the API success or error payload envelope to assist developers in debugging issues.

---

## 4. Engineering & Design Standards

*   **No Cross-Domain Database Joins**: Database collections belonging to one module must not be joined or directly queried by other modules. Cross-domain queries must query the target module's Service layer API.
*   **Transaction Boundaries**: Services manage transactional units. Operations that cross database collections must run within unit-of-work transactions.
*   **Backward Compatibility**: Metadata schema changes must use optional fields and default values, allowing legacy client versions to parse new response payloads without crashing.
*   **Extension Hooks**: Module actions must publish events to the event bus, allowing other systems to extend behavior without modifying the core service files.

---

## 5. Learning Platform Foundation

The platform introduces the foundational elements of the Learning Domain under `app/modules/learning/`.

### A. Domain Separation & Knowledge Decoupling
*   **Knowledge vs. Learning Boundary**: The Learning module is decoupled from the Knowledge module. It stores no content structures (such as syllabus titles or content notes). It references curriculum nodes (Topics, Contents) strictly by their string IDs.
*   **Ownership Model**: Every learning record is owned by a specific student account. Access is restricted using capability authorization guards (`learning:read`, `learning:write`).

### B. Lightweight Learning Sessions
*   **Temporal Container**: A `LearningSessionModel` represents a contiguous period of learner activity. It is lightweight and carries no business workflows.
*   **Decoupled Hooking**: Future learning experiences participate in active sessions to record timeline threads rather than sessions orchestrating experiences.

### C. Resource-Agnostic Learning Attempts
*   **Activity Evidence**: A `LearningAttemptModel` tracks a single student interaction with any learning resource.
*   **Generic References**: Attempts reference resources generically via `resource_id` and open-ended `resource_type` (e.g. topic, content, quiz, practice, note, challenge), future-proofing the schema.

### D. Derived Learning Progress
*   **Summary Representation**: `ProgressModel` is a derived representation of attempts. It summarizes confidence levels, status progressions (`not_started` -> `in_progress` -> `completed` -> `reviewed` -> `mastered`), review counts, and active times. It does not act as a learner event database.

---

## 6. Learning Experience Platform

Stage 4.2 introduces the Learning Experience Platform layer. It orchestrates learner-facing educational workflows (Reading Notes, Revision, Practice, Quiz, and Interview Preparation) utilizing the foundational abstractions of Stage 4.1.

### A. Unified Experience Orchestration
*   **Agnostic Interaction Model**: The platform defines a single `LearningExperienceModel` to represent a student's active engagement with an educational resource.
*   **Workflow State Containment**: The experience model retains lightweight runtime parameters (e.g. current question indices, submitted choices, scroll positions) inside an open-ended `state` schema, keeping sessions and attempt records free of transient workflow state.
*   **Automatic Lifespans**: Starting an experience automatically deactivates any existing active experience of the same type and hooks into the active temporal `LearningSession` if present.

### B. Progress & Evidence Pipeline
*   **Attempt Logging**: Upon completion or abandonment of an experience, the orchestrator triggers the `LearningAttemptService` to log corresponding learner attempt evidence.
*   **Derived Progress updates**: This attempt evidence is then picked up by the `ProgressService` to calculate topic-level status progressions (up to `mastered`) and increment confidence scores.

---

## 7. Learning Insights Platform

Stage 4.3 introduces the Learning Insights Platform layer. It provides deterministic, evidence-based aggregations and educational metrics that prepare the codebase for future personalization and intelligent layers.

### A. Information Architecture & Aggregations
*   **Learner Dashboard**: Computes dynamic statistics (total sessions, attempts, mastered topics, and concepts requiring review) along with the active temporal container state.
*   **Chronological Timeline**: Merges sessions, attempts, and experience events into a single unified timeline representation sorted descending.
*   **Rule-Based Recommendations**: Deterministically suggests next study options, including resuming open experiences, continuing incomplete topics, and retrying failed assessments (scores < 70%).
*   **Weak Area Tracking**: Evaluates attempt histories and marks subjects/topics as weak if their latest or average assessment score falls below 70%.

---

## 8. Education & Assessment Platform (Phase 5)

Phase 5 introduces the Education & Assessment Platform, establishing end-to-end evaluation capabilities alongside learner workspace organization and content discovery.

### A. Assessment Foundation
*   **Assessment Content**: Manages the modular `QuestionModel` bank (supporting multiple types like MCQ, FillBlank, TrueFalse) and reusable `AssessmentModel` definitions containing ordered, weighted `AssessmentQuestionRef` items.
*   **Assessment Runtime**: Executes lightweight active temporal `AssessmentSessionModel` instances capturing user responses, with built-in time-limit boundary enforcement.
*   **Deterministic Evaluation**: Grades finalized `AssessmentSubmissionModel` payloads against correct answers, generating strengths/weaknesses and logging completed attempt evidence to update Progress.

### B. Educational Experience
*   **Learning Utilities**: Manages learner study bookmarks/favorites (`LearningCollectionModel`), study planning (`LearningGoalModel`), and dynamic timelines for recently accessed/completed items.
*   **Discovery Platform**: Exposes global text search, advanced filtering, and related resource lookups across all platform models mapped to a unified `DiscoverableResource` projection.

---

## 9. Creator Platform (Phase 6 · Milestone 6.1)

Milestone 6.1 introduces the Creator Platform, providing the authoring environment and publication workflow management for educational resources.

### A. Content Workspace
*   **Unified Draft Model**: Manages editing lifecycles via `DraftResourceModel`, featuring an open-ended payload dictionary storing unsanitized fields for topics, content, questions, and assessments.
*   **Structural Verification**: Executes validation routines on draft objects, checking reference integrity and mandatory metadata fields before allowing progression to review stages.

### B. Asset Attachment
*   **Coordination Links**: Links existing `AssetModel` records to draft entities through `AssetAttachmentModel` records, querying the core Asset Platform to confirm existence without duplicating binary storage.

### C. Publishing Pipeline
*   **Deterministic Transitions**: Orchestrates lifecycle transitions (`draft` -> `ready_for_review` -> `approved` -> `published`) through `PublishingPipelineService`.
*   **Domain-Specific Insertion**: Upon final approval and publication, the pipeline invokes the target domain services (Knowledge or Assessments) to insert or update production records, maintaining clear domain boundaries.

---

## 10. Collaboration Platform (Phase 6 · Milestone 6.2)

Milestone 6.2 introduces the Collaboration Platform, coordinating organizational team dynamics, task assignments, contextual discussions, and recipient user notification systems.

### A. Teams & Membership
*   **Team Container**: Encapsulates collaborative spaces through `TeamModel` referencing the owner actor.
*   **Membership Lifecycle**: Manages user invitation status (`TeamMembershipModel`) mapped directly to existing identity user identifiers, preserving identity and auth scopes.

### B. Collaboration Workflows
*   **Assignments Mapping**: Tracks work allocation through `CollaborationAssignmentModel` linking workspace drafts to explicit assignee users.
*   **Discussions Threading**: Enables contextual comment trees through `CollaborationCommentModel` logs.

### C. Activity Tracking & Alerts
*   **Timeline History**: Records immutable operations history timeline streams (`CollaborationActivityModel`).
*   **Notifications Dispatch**: Distributes real-time collaborative alerts (`CollaborationNotificationModel`) to keep team members informed.

---

## 11. Administration Platform (Phase 6 · Milestone 6.3)

Milestone 6.3 introduces the Administration Platform, establishing system management operations and global feature configurations.

### A. Platform Configuration
*   **Global Config**: Persists key configurations (`PlatformConfigModel`) governing maintenance modes, CORS origin structures, and global feature toggles.
*   **Admin Guardianship**: Restricts edit/update and view access exclusively to users authenticated under the role `Admin`.

### B. Administrative Visibility
*   **Composition Dashboards**: Aggregates document footprint sizes and backlogs across topics, knowledge contents, assessments, draft review items, and uploaded assets collections, providing comprehensive operational visibility without duplicating data ownership.








# Backend Architecture Compass

This document serves as the authoritative implementation guide and architectural reference for the Ascendrite backend server.

---

## 1. Modular Organization

All backend server modules live under `platform/server/app/` and follow strict modular monolith and clean architecture decoupling rules:

```
platform/server/app/
├── api/                       # API Controllers and endpoints routing (v1)
├── core/                      # Constants, error models, settings, and password/JWT security
├── infrastructure/            # Technical adapters to external systems
│   ├── database/              # PostgreSQL and MongoDB connection drivers
│   └── storage/               # RustFS external object storage interfaces
├── modules/                   # Self-contained domain-bounded contexts
│   ├── users/                 # Profile and role repository models and schemas
│   ├── authentication/        # User session lifecycle and authorization flows
│   ├── knowledge/             # Subject, Syllabus, Topic, Asset documents repositories
│   ├── learning/              # Enrollment tracks, topic completion, bookmarks services
│   ├── assessments/           # Quiz evaluation rules and submission scores
│   └── analytics/             # System activity telemetry audits
├── middleware/                # Custom HTTP interceptors (exceptions)
└── utils/                     # Shared general utilities
```

### Rules of Dependency Flow
1.  **Strict Upward Imports Only**: A lower module must never import from a higher module.
2.  **Service Isolation**: Controllers can only import from `services/` or Pydantic `schemas/`. They must never access repositories or models directly.
3.  **Repository Isolation**: Services access databases strictly through interface-decoupled repository objects.

---

## 2. Implemented Foundation Status

*   **FastAPI application bootstrap**: Centralized application factory patterns inside `app/main.py` with async lifespan context hooks.
*   **Database access layer**: Ready-to-use engine connection configurations for PostgreSQL (`postgres.py` using SQLAlchemy sessionmakers) and MongoDB (`mongodb.py` using MotorClient).
*   **Decoupled storage layers**: Storage bucket abstractions mapped under `app/infrastructure/storage/rustfs.py`.
*   **Security Foundation**: Hashing algorithms and JWT signing helpers mapped under `app/core/security.py`.
*   **API Response Standards**: Exception interceptor middleware (`app/middleware/exceptions.py`) converting custom core errors (`app/core/errors.py`) to unified JSON outputs.

## 3. Configuration & Provider Architecture

### A. Configuration Precedence & Profile Helpers
Configurations are strongly typed and resolved from:
1.  **Environment Variables**: Overrides local configurations in production.
2.  **Root `.env.local`**: Custom developer configuration values.
3.  **Application Defaults**: Preconfigured fallback settings.

The active runtime profile (`APP_ENV`) exposes helper query properties:
*   `is_development`: Development environment.
*   `is_testing`: Pytest sandbox context.
*   `is_production`: Production container runtime environment.
*   `is_feature_enabled(name)`: Operations check for feature toggles.

### B. Feature Flags Classification
Feature flags are structured configurations prefixing operational and developer rules:
*   **Operational Flags**: `FEATURE_ENABLE_AI`, `FEATURE_ENABLE_BACKGROUND_WORKERS`, `FEATURE_ENABLE_EMAIL`.
*   **Development Flags**: `FEATURE_ENABLE_SEARCH`, `FEATURE_ENABLE_REGISTRATION`, `FEATURE_ENABLE_ANALYTICS`.

### C. Provider Interfaces Abstraction
External infrastructure drivers are decoupled behind abstract provider interfaces:
*   **`StorageProvider`**: Decouples binary payload interactions. Swaps implementations (Local `RustFS` $\rightarrow$ AWS S3 $\rightarrow$ Azure Blob) without editing business modules.
*   **`AIProvider`**: Decouples Generative model queries. Swaps implementations (OpenAI $\rightarrow$ Gemini $\rightarrow$ Ollama) for RAG curriculum processing.

Provider concrete implementations are bound to API endpoints dynamically using FastAPI native dependency injection (`Depends`), preventing service locator anti-patterns.

---

## 4. Operational Foundation

### A. Endpoint Responsibilities
*   `GET /api/v1/health`: Consolidates overall system health contract (timestamp, uptime, version, dependencies).
*   `GET /api/v1/health/liveness`: Fast process check returning simple status (used by load balancers and orchestrators).
*   `GET /api/v1/health/readiness`: Validates active database connection reachability (PostgreSQL, MongoDB).
*   `GET /api/v1/system/metadata`: Consolidates non-sensitive runtime attributes (Python version, build channel, startup timestamp).

### B. Security Classification
*   **PUBLIC**: `/api/v1/health/liveness` & `/api/v1/system/metadata`. Open to public telemetry services. No sensitive system variables or connection settings are exposed.
*   **INTERNAL**: `/api/v1/health` & `/api/v1/health/readiness`. Restricted to cloud network clusters or internal VPC access to protect detailed system health metrics and latency records.
*   **AUTHENTICATED / ADMIN**: Diagnostic tracing endpoints (future) require bearer tokens and admin capabilities.

### C. Request Lifecycle & Correlation
1.  **Ingress**: The request interceptor middleware retrieves or generates a unique correlation UUID (`X-Correlation-ID`).
2.  **Propagation**: The correlation ID is stored in a thread-safe `contextvars` context local.
3.  **Logging**: Every system log printed during request processing automatically references the request's correlation ID.
4.  **Egress**: The middleware appends `X-Correlation-ID` and `X-Process-Time` to response headers, mapping the correlation tracker into the response payload on exceptions.

### D. Structured Logging
In production, standard logging formats logs as JSON records containing:
*   `timestamp` (ISO 8601 UTC)
*   `level` (Severity level)
*   `request_id` (Correlation tracker)
*   `route` (Called path)
*   `duration_ms` (Time elapsed)
*   `message` (Log body)

---

## 5. Development Commands

### Running unit and config tests
Run pytest from the backend workspace root directory:
```powershell
python-venv-3.10.11\Scripts\python.exe -m pytest -v tests
```

### Running uvicorn local development server
```powershell
python-venv-3.10.11\Scripts\uvicorn main:app --host 127.0.0.1 --port 8000
```

---

## 6. Capability-Based Authorization Platform

### A. Authorization Philosophy
The platform employs a fine-grained **capability-based authorization model** instead of checking static application roles directly inside logic endpoints.
1.  **Capabilities as Contracts**: Permissions represent the sole authorization contracts (`domain:action`).
2.  **Roles as Bundles**: Roles (`Student`, `Contributor`, `Admin`) are reusable collections of these capabilities, serving as configurations rather than hardcoded logic boundaries.
3.  **FastAPI Route Guards**: Endpoints declare capability constraints using the `RequireCapability` dependency class, keeping access validation out of service business modules.

### B. Authenticated Principal Abstraction
To support non-human access (such as AI agents, service accounts, background workers, and API keys) without code changes:
*   **`AuthenticatedPrincipal`**: Represents a generic authenticated context resolving an `id`, `identity_type`, `role`, and active `capabilities` list.
*   **Principal Resolution**: The active JWT access token resolves into this generic principal context, decoupling authorization evaluations from the specific `UserModel` profile.

---

## 7. Platform Runtime Infrastructure

The platform provides a suite of decoupled, provider-agnostic runtime infrastructure engines under `app/core/runtime/`:

### A. Execution Metadata & Runtime Context
*   **`RuntimeContext`**: Consolidates correlation tracking and principal variables into a unified, request-scoped payload passed across all platform engines.

### B. Internal Event Dispatcher
*   **`LocalEventDispatcher`**: Handles internal application pub/sub flows synchronously in-memory, preserving the request's correlation metadata in the event contract.

### C. Auditing & User Activity Boundaries
*   **`MongoAuditService`**: Persists system-facing security logs (containing actor references, actions, targets, status codes) to the `audit_logs` collection.
*   **`MongoActivityService`**: Persists user-facing timeline feeds (actions completed by human accounts) to the `activity_logs` collection.

### D. Pluggable Notifications Dispatcher
*   **`NotificationDispatcher`**: Distributes notification deliveries across active channels (`InAppChannel` to `in_app_notifications` MongoDB collection, `MockEmailChannel`, `MockSMSChannel`, `MockPushChannel`) without coupling routing logic to the sender.

### E. Provider-Agnostic Tasks Scheduler
*   **`BackgroundTaskScheduler`**: Dequeues and processes tasks in the background. Operates provider-agnostically, wrapping either the request-scoped `FastAPIBackgroundTaskProvider` or the asynchronous `AsyncioBackgroundTaskProvider` loop runner.

---

## 8. Asset & Media Platform

The platform defines a clean boundary separating logical asset ownership and metadata persistence from physical storage details:

### A. Intermediate Storage Management Layer
*   **`StorageManager`**: Acts as an intermediate boundary isolating business services from raw storage operations (`StorageProvider`). Resolves standardized bucket names and directory keys (`assets/{owner_id}/{asset_id}/{filename}`) dynamically.

### B. Asset Domain & Strongly Typed Lifecycle Enums
*   **`AssetModel`**: Defines the metadata schema for persistent documents. Includes checksum validation (`checksum_algorithm`), logical storage location properties, and reserved slots for media dimensions, durations, and processing triggers.
*   **`AssetStatus`**: Strongly typed enumeration (`uploaded`, `active`, `archived`, `deleted`). soft-deletions transition status to `DELETED` instead of calling physical removal.

### C. Security boundaries & Principal Ownership
*   **Ownership Validation**: All service transactions verify `principal.id == asset.owner_id`. Admin roles automatically bypass ownership barriers.
*   **Platform Runtime Hooks**: Uploads/deletions trigger internal event publication (`AssetUploaded`, `AssetDeleted`), security auditing, and user timeline events.

---

## 9. Academic Structures, Knowledge Content & Platform Search

The platform implements an institutional-independent academic syllabus hierarchy, publication workflows, and unified search discovery:

### A. Academic Syllabus Semantics
*   **Subject**: Canonical discipline independent of any specific university or course provider (e.g. Operating Systems).
*   **Syllabus**: Institution/university-specific curriculum structure (e.g. GLA University B.Tech CSE 2025).
*   **Module**: Logically grouped divisions within a syllabus (e.g. Process Synchronization).
*   **Topic**: Actionable instructional node within a module (e.g. Dining Philosophers).
*   *Validation Constraints*: Strict parent-child resolution is enforced on CRUD. Parent deletion is blocked if any active child nodes reference it (non-cascading deletion).

### B. Knowledge Content & Publishing Lifecycle
*   **Content Types**: Notes, Revision Summaries, and Interview Preparation materials linked directly to specific topics.
*   **Publication States**: Managed through a state machine: `Draft` $\rightarrow$ `Published` $\rightarrow$ `Archived` $\rightarrow$ `Deleted`.
*   **Visibility Guards**: Enforce access controls. Students can only retrieve `Published` content. Contributors and authors can access `Draft` versions.
*   **Asset Association**: Reusable media attachments (from the Asset platform) are verified for ownership and active status.

---

## 10. Learning Platform Foundation

The platform introduces the foundational elements of the Learning Domain, designed to track student engagement, progression, and evidence of mastery without coupling to specific content types or hardcoding learning experiences.

### A. Domain Separation & Knowledge Decoupling
*   **Knowledge vs. Learning Boundary**: The Learning module (`app/modules/learning`) remains strictly decoupled from the Knowledge module. It stores no content properties (such as title, description, or body). It refers to curriculum nodes (Topics, Contents) strictly via their ID string keys.
*   **Ownership Model**: Every learning record is tied directly to an owner `principal.id`. Access is governed by capability checks (`learning:read`, `learning:write`) rather than static roles.

### B. Lightweight Learning Sessions
*   **Temporal Container**: A `LearningSessionModel` represents a contiguous period of learner activity. It is lightweight and intentionally carries no business workflows.
*   **Participating Abstraction**: Future learning experiences participate in the session container to provide a chronological thread of learning rather than having the session orchestrate the experiences.

### C. Resource-Agnostic Learning Attempts
*   **Activity Evidence**: A `LearningAttemptModel` tracks a single learner interaction with any resource (e.g. topic, content, quiz, practice, note, challenge).
*   **Generic References**: Attempts reference resources generically via `resource_id` and open-ended `resource_type`, future-proofing the schema against new curriculum content types.

### D. Derived Learning Progress
*   **Derived Summary State**: `ProgressModel` acts as a derived summary of student achievement rather than a persistence layer for learning events.
*   **Backward Compatibility**: The progress schemas default new lifecycle states and confidence metrics upon parsing legacy documents, preserving compatibility.

---

## 11. Learning Experience Platform

Stage 4.2 introduces the Learning Experience Platform layer. It orchestrates learner-facing educational workflows (Reading Notes, Revision, Practice, Quiz, and Interview Preparation) utilizing the foundational abstractions of Stage 4.1.

### A. Unified Experience Orchestration
*   **Agnostic Interaction Model**: The platform defines a single `LearningExperienceModel` to represent a student's active engagement with an educational resource.
*   **Workflow State Containment**: The experience model retains lightweight runtime parameters (e.g. current question indices, submitted choices, scroll positions) inside an open-ended `state` schema, keeping sessions and attempt records free of transient workflow state.
*   **Automatic Lifespans**: Starting an experience automatically deactivates any existing active experience of the same type and hooks into the active temporal `LearningSession` if present.

### B. Progress & Evidence Pipeline
*   **Attempt Logging**: Upon completion or abandonment of an experience, the orchestrator triggers the `LearningAttemptService` to log corresponding learner attempt evidence.
*   **Derived Progress updates**: This attempt evidence is then picked up by the `ProgressService` to calculate topic-level status progressions (up to `mastered`) and increment confidence scores.

---

## 12. Learning Insights Platform

Stage 4.3 introduces the Learning Insights Platform layer. It provides deterministic, evidence-based aggregations and educational metrics that prepare the codebase for future personalization and intelligent layers.

### A. Information Architecture & Aggregations
*   **Learner Dashboard**: Computes dynamic statistics (total sessions, attempts, mastered topics, and concepts requiring review) along with the active temporal container state.
*   **Chronological Timeline**: Merges sessions, attempts, and experience events into a single unified timeline representation sorted descending.
*   **Rule-Based Recommendations**: Deterministically suggests next study options, including resuming open experiences, continuing incomplete topics, and retrying failed assessments (scores < 70%).
*   **Weak Area Tracking**: Evaluates attempt histories and marks subjects/topics as weak if their latest or average assessment score falls below 70%.








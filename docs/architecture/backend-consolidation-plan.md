# Phase 1 Stage 1.5 Backend Architecture Consolidation Plan

This document serves as the architectural blueprint for consolidating and hardening the Ascendrite backend layout into a domain-driven Modular Monolith structure.

---

## 1. Current Architecture Analysis

### A. Found Duplications & Technical Debt
*   **Parallel Hierarchies**: Pre-existing folders at `platform/server/` (`api/`, `core/`, `models/`, `repositories/`, `schemas/`, `services/`) exist alongside their new counterparts inside `platform/server/app/`. This creates ambiguity in code searches, imports resolutions, and editor tooling indexing.
*   **Generic Layering over Domain Focus**: Files are organized by technical layers (every model lives in `/models/`, every service in `/services/`) rather than by business contexts. This requires engineers to touch up to six directories to add a single feature (e.g. adding a field in progress tracking).
*   **Infrastructure Pollution**: Database engines (`core/database.py` or `app/database/`) are mixed alongside core configuration environments instead of being cleanly separated as infrastructural adapters.

---

## 2. Bounded Context Modular Monolith Architecture

To solve these issues, the backend will be reorganized around **Domain Bounded Contexts**.

### Target Folder Layout (`platform/server/app/`)
```
platform/server/app/
├── core/                      # Application primitives (Env, Config, Security, JWT, Logging)
│   ├── config.py
│   ├── security.py
│   ├── logging.py
│   ├── constants.py
│   └── errors.py
│
├── infrastructure/            # Adapters to external stores/services (No domain logic)
│   ├── database/
│   │   ├── postgres.py
│   │   ├── mongodb.py
│   │   └── redis.py
│   └── storage/
│       └── rustfs.py
│
├── modules/                   # Domain-bounded contexts (Self-contained)
│   ├── users/                 # Domain, Repos, Services for Profiles & Preferences
│   ├── authentication/        # Session logic, login workflows, JWT verification
│   ├── knowledge/             # Subject, Syllabus, Topic, Asset documents (Read-only)
│   ├── learning/              # Enrollments, Topic progress tracking, Bookmarks
│   ├── assessments/           # Quiz submissions, Attempt histories, Scores
│   └── analytics/             # System telemetry, activity logs
│
├── api/                       # HTTP API Layer (Maps routes to modules)
│   └── v1/
│       ├── endpoints/
│       │   ├── health.py
│       │   ├── auth.py
│       │   ├── curriculum.py
│       │   ├── progress.py
│       │   └── assessments.py
│       └── router.py
│
├── middleware/                # App-level HTTP handlers (CORS, Exceptions)
└── main.py                    # App factory initializer
```

### Dependency Rules & Direction Flow
*   **Core (`app/core/`)** is a leaf dependency; it must never import from any other directory.
*   **Infrastructure (`app/infrastructure/`)** depends only on `core/`.
*   **Modules (`app/modules/<name>/`)** are self-contained. A module can only import from its own folders, `app/core/`, or interfaces in `app/infrastructure/`. Inter-module communications should occur via service boundaries.
*   **API Layer (`app/api/`)** depends only on `app/modules/` services and schemas, orchestrating inputs and mapping status codes.

---

## 3. Data & Domain Ownership

### Entity Ownership Model
*   **`users`**: Profiles, access roles, active token claims.
*   **`knowledge`**: Subjects, syllabuses, topics, and assets. Read-only at runtime for students.
*   **`learning`**: Enrollments, topic completions, and bookmarks.
*   **`assessments`**: Quiz attempts, scores, and submissions history.

### Storage Split Boundaries
*   **MongoDB (Document Store)**: Houses the `knowledge` models. Well-suited for complex curriculum trees and media metadata.
*   **PostgreSQL (Relational Store)**: Houses transactional user authentication data (`users`, `sessions`, `roles`), `learning` tracking records, and `assessments` attempts. Keep operations indexed.
*   **Redis (Cache)**: Caches high-frequency read requests like topic completion statistics and user session verification profiles.
*   **RustFS (Object Store)**: Houses static PDF manuals, video assets, and user upload storage blocks.

---

## 4. Security & Future Scalability

### Security Architecture
*   **Password Hashing**: Uses `passlib` with Argon2 or Bcrypt.
*   **Access vs Refresh Lifecycle**: Access JWT tokens (HMAC-SHA256) expire in 15 minutes. Refresh tokens are HTTP-Only, Lax SameSite cookies with a 7-day lifespan.
*   **Inputs Safety**: Pydantic v2 schemas sanitize and validate all payload keys before executing database writes.

### Future Scalability
*   **Service Extraction**: Since each module under `app/modules/` is bounded and self-contained, any context (e.g., `assessments` or `search`) can be extracted into an independent microservice later without modifying core client APIs.
*   **AI Integration Isolation**: AI agents or RAG pipelines query curriculum models using read-only API connectors, ensuring core transactional databases remain isolated.

---

## 5. Clean-Up & Consolidation Strategy

### Files to Move
1.  Move files inside `app/core/` to their final layout:
    - `app/core/config.py`, `app/core/security.py`, `app/core/constants.py`, `app/core/errors.py`.
2.  Move files under `app/database/` into `app/infrastructure/database/`.
3.  Move files under `app/storage/` into `app/infrastructure/storage/`.
4.  Consolidate models, schemas, repositories, and services into their bounded context modules:
    - **Authentication**: `services/auth.py` $ightarrow$ `modules/authentication/services/auth.py`
    - **Users**: `models/user.py`, `repositories/user.py`, `schemas/user.py` $ightarrow$ `modules/users/`
    - **Knowledge**: `services/curriculum.py` $ightarrow$ `modules/knowledge/services/curriculum.py`
    - **Learning**: `models/progress.py`, `repositories/progress.py`, `schemas/progress.py`, `services/progress.py` $ightarrow$ `modules/learning/`
    - **Assessments**: `models/quiz_submission.py`, `repositories/quiz_submission.py`, `schemas/quiz_submission.py` $ightarrow$ `modules/assessments/`

### Files to Delete
*   Remove all duplicate files and folders remaining at the root level of `platform/server/` (`api/`, `core/`, `models/`, `repositories/`, `schemas/`, `services/`).

### Rollback Strategy
*   Before refactoring, verify local git commits are clean. If errors occur, discard changes via `git checkout -- .` and restore status.

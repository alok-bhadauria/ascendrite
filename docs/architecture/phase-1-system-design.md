# Ascendrite Phase 1 System Design Specifications

This document defines the comprehensive roadmap, domain model, API design, and AI integration boundaries for Phase 1.

---

## 1. Phase 1 Execution Roadmap

```
Stage 0 (Design) ──► Stage 1 (Domain Model) ──► Stage 2 (APIs) ──► Stage 3 (Backend Core) ──► Stage 4 (Frontend Integration)
```

*   **Stage 0: System Design & Architecture**: Finalize system boundaries and structural compass documents.
*   **Stage 1: Domain Entities & Repositories**: Define data layer interfaces and schemas for Users, Knowledge, and Learning.
*   **Stage 2: API Contract Specification**: Specify standard JSON response frameworks, route contracts, and exception mappings.
*   **Stage 3: Core API Services Ingestion**: Code backend logic modules, repositories implementations, and token authorization.
*   **Stage 4: Frontend UI Components**: Implement Pinia/Redux state store hooks, routing guards, and clean components mapping.
*   **Stage 5: Final Verification Integration**: Verify end-to-end integration and run full suite regression tests.

---

## 2. Backend Architecture Design & Directory Layout

### Component Architecture
Ascendrite follows a decoupled architecture pattern:
```
[Client App] ──► [API Controllers] ──► [App Services] ──► [Repositories] ──► [MongoDB/PostgreSQL]
```

### Module Responsibilities
*   **API Layer (`app/api/`)**: Exposes FastAPI endpoints. Responsible only for route handling, status mapping, and Pydantic request deserialization.
*   **Application Services Layer (`app/services/`)**: Executes business rules. Interacts with repositories to compile aggregates and triggers domain events.
*   **Repository Layer (`app/repositories/`)**: Abstracts persistent storage mechanisms, keeping SQL queries or MongoDB aggregation operators isolated.
*   **Domain Models Layer (`app/domain/`)**: Pure domain logic and validation rules, independent of databases or external API routers.
*   **Infrastructure (`app/core/` / `app/database/`)**: Manages configuration loading, database engine initializations, and dependencies injection.

---

## 3. Database Boundary Review

To prevent duplicated sources of truth, storage responsibilities are strictly separated:

| Storage Engine | Collections / Tables | Responsibilities |
| :--- | :--- | :--- |
| **MongoDB** | `subjects`, `syllabuses`, `topics`, `assets` | Hierarchical, content-rich knowledge graphs & local files imports |
| **PostgreSQL** | `users`, `roles`, `permissions`, `sessions`, `progress`, `attempts` | Transactional authentication records, learning states, & relational indexes |

### Relational Mapping
Any document in MongoDB matches its PostgreSQL progress mapping using the canonical `id` field as a non-volatile foreign key string, keeping Mongo decoupled from user progress.

---

## 4. Domain Modeling & Boundaries

### User Aggregate (PostgreSQL Owned)
*   **Entities**: `User` (profile, preferences, hashed credentials), `Role`, `Permission`, `Session`.
*   **Lifecycle**: Handled during register, login, credential updates, and session expiration.

### Knowledge Aggregate (MongoDB Owned)
*   **Entities**: `Subject`, `Syllabus`, `Topic`, `Asset`.
*   **Lifecycle**: Managed by the dry-run/apply migration toolkit. Read-only at runtime for client students.

### Learning Aggregate (PostgreSQL Owned)
*   **Entities**: `ProgressRecord` (topic completions, bookmark state), `AssessmentAttempt` (quiz answers score).
*   **Lifecycle**: Mutated via API application services on user interaction endpoints.

---

## 5. API Architecture Specification

### Request & Response Standards
All endpoints conform to a standardized JSON response envelope:
```json
{
  "status": "success",
  "data": {},
  "meta": {
    "pagination": null
  }
}
```

### Error Standardization
Exceptions map to HTTP status codes following RFC 7807 problem details:
```json
{
  "status": "error",
  "error": {
    "code": "ENTITY_NOT_FOUND",
    "message": "The requested topic resource could not be found.",
    "details": []
  }
}
```

### Token-Based Authentication Flow
1.  **Login**: User sends credentials to `/api/v1/auth/login`. Returns a JWT access token (15 mins lifespan) and a secure HTTP-only refresh token (7 days lifespan).
2.  **Access Guard**: API requests include the access token inside `Authorization: Bearer <token>`.
3.  **Refresh**: Client requests new access token using refresh tokens via `/api/v1/auth/refresh`.

---

## 6. AI Integration Boundary

AI features remain decoupled from the core application layer:
*   **Isolation**: Core database collections must never be modified by AI scripts directly.
*   **Integration Pointers**: AI features hook into App Services via REST APIs, leveraging retrieved read-only knowledge vectors.
*   **Auditing**: AI interaction logs are captured under independent learning analytics collections.

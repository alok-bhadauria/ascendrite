# Backend Architecture: API Design, Security, and Performance Engineering

## Document Metadata
*   **Purpose**: Outlines the server routing, dependency injection models, security filters, and caching strategies.
*   **Scope**: Governs backend FastAPI codebase layouts, API router endpoints, and authentication scopes.
*   **Intended Audience**: Backend engineers, database administrators, and security coordinators.
*   **Related Documents**:
    *   [Engineering Principles](../governance/engineering-principles.md)
    *   [Security Standards](../security/security-standards.md)
    *   [Database Schema](database-schema.md)
*   **Ownership**: Head of Platform Engineering

---

## 1. Core API Server Architecture
The backend application shall be constructed using FastAPI. It must leverage asynchronous execution loops (`async`/`await`) to manage I/O-bound requests concurrently.

### 1.1 Dependency Injection Policy
All runtime resources (database connections, authentication helper tools, user sessions) must be injected using FastAPI’s dependency injection system (`Depends`). 
*   **Resource Lifetimes**: Injected dependencies shall govern their own scopes, guaranteeing connection cleanup and preventing resource leaks.
*   **Testing Hooks**: Real database drivers should be swappable with mock implementations in test suites via dependency overrides.

---

## 2. Authentication & Session Management
The platform shall enforce a stateless authentication workflow using JSON Web Tokens (JWT) signed with `HS256` keys.

### 2.1 Login & Token Issuance Flow
1.  The client sends authentication requests to `POST /api/v1/auth/login`.
2.  The server must query the user record. Password verification shall compare inputs using **bcrypt** (minimum work factor of 12) or **Argon2id**.
3.  Upon verification, the server shall generate a short-lived access token (expiration limit: 15 minutes) containing role claims in its payload.
4.  The access token must be returned to the client inside a secure, `HttpOnly`, `SameSite=Strict`, `Secure` cookie. It must not be returned in JSON response bodies to protect against XSS.

---

## 3. Role-Based Access Control (RBAC)
The server must validate permissions on every protected endpoint using dependency filters mapping to user actors:

| Actor | Permitted API Scopes |
| :--- | :--- |
| **Guest** | `/api/v1/health`, `/api/v1/subject-indexes` (public read only) |
| **Learner** | `/api/v1/progress/*`, `/api/v1/quiz/submit` |
| **Moderator** | `/api/v1/moderation/*`, `/api/v1/curriculum/drafts/*` |
| **Admin** | Full access to `/api/v1/admin/*` and configuration endpoints |

---

## 4. API Input Validation and Sanitization
*   **Strict Type Constraints**: All request payloads must be defined using Pydantic V2 models.
*   **Input Sanitization**: Strings containing HTML or JS content must be escaped before processing to prevent scripting injections.
*   **NoSQL Injection Prevention**: Database queries shall utilize parameterized driver parameters rather than direct string building.

---

## 5. Performance and Caching Strategies
*   **Curriculum Memory Cache**: Raw JSON assets (notes, syllabi, metadata) must be parsed once during server startup and stored in a read-only memory cache. Endpoints querying curriculum data shall fetch from this cache to achieve $O(1)$ response times.
*   **Redis Progress Caching**: Active user progress records and sessions should be stored in a Redis cache using a time-to-live (TTL) parameter of 1 hour to reduce direct datastore reads.

---

## 6. Observability & Logging
*   **Structured Logging**: App servers shall generate logs in JSON format, capturing correlation IDs, execution durations, request paths, and HTTP statuses.
*   **Audit Trail Logs**: Crucial actions (role changes, system locks) must be output to a write-once audit log file.
*   **Metrics Ingestion**: App instances should expose standard metrics tracking memory footprints, error counts, and response latency.

# API Architecture

## Document Metadata
*   **Purpose**: Standardizes API routing, public/private/AI interfaces, parameters validation, error responses, pagination, filtering, search, and idempotency interfaces.
*   **Scope**: Governs all backend RESTful interfaces and routing middleware.
*   **Intended Audience**: Backend software engineers, frontend developers, and security auditors.
*   **Related Documents**:
    *   [Backend Architecture](backend-architecture.md)
    *   [Security Standards](../operations/security-standards.md)
*   **Ownership**: Principal API Architect & Head of Platform Engineering

---

## 1. API Surface Categorization

To maintain strict least privilege and isolate operational paths, the platform categorizes all RESTful endpoints into dedicated API surfaces:

*   **Public APIs**:
    *   *Path Prefix*: `/api/v1/public/`
    *   *Audience*: Anonymous guest users, educational index crawlers.
    *   *Scope*: Read-only access to syllabus structures, subject metadata catalogues, and public search.
    *   *Authentication*: None required. Strictly protected by aggressive rate limiters.
*   **Internal / Client APIs**:
    *   *Path Prefix*: `/api/v1/workspace/` and `/api/v1/users/`
    *   *Audience*: Registered human learners, authors, and moderators using the client SPA.
    *   *Scope*: Read/write access to personal profiles, workspaces, attachments, and progress syncing.
    *   *Authentication*: Enforced opaque session cookie checks (`HttpOnly`, `Secure`, `SameSite=Lax`).
*   **AI Service APIs**:
    *   *Path Prefix*: `/api/v1/ai/`
    *   *Audience*: Autonomous AI agents, automated content generators.
    *   *Scope*: Read-only access to taxonomy graphs, write-only access to progress evaluations.
    *   *Authentication*: Secure header-based client keys (HMAC-based signature verification).
*   **Knowledge Platform APIs**:
    *   *Path Prefix*: `/api/v1/knowledge/`
    *   *Audience*: Local content ingestion pipelines, publisher tools.
    *   *Scope*: Compile and ingest raw markdown/JSON syllabus objects, trigger indexing loops.
    *   *Authentication*: Short-lived authorization tokens bound to localhost/internal IPs.
*   **Administrative APIs**:
    *   *Path Prefix*: `/api/v1/admin/`
    *   *Audience*: System administrators and platform supervisors.
    *   *Scope*: Revoke sessions, reassign user roles, manage system configurations, rotate S3 credentials, purge quarantine folders.
    *   *Authentication*: Session cookie authentication with mandatory active step-up verification ($\le 10\text{ min}$ freshness).

---

## 2. Path, Query, Body, Header, and Cookie Semantics

All API transactions conform to strict HTTP verb and parameter mappings:
*   **GET Requests**:
    *   *Purpose*: Retrieve resources. Must be safe and idempotent.
    *   *Parameters*: Scoped in path coordinate slugs (e.g. `/subjects/{subject_id}`) and query parameters (e.g. `?limit=20`).
*   **POST Requests**:
    *   *Purpose*: Create resources or execute non-CRUD actions (e.g. `POST /auth/login`).
    *   *Parameters*: Transmitted inside JSON-formatted request bodies.
*   **PUT/PATCH Requests**:
    *   *Purpose*: Update resources. `PUT` replaces the entire resource; `PATCH` updates fields partially.
    *   *Parameters*: JSON request body.
*   **DELETE Requests**:
    *   *Purpose*: Soft-delete or archive resources.
    *   *Parameters*: Target ID passed in the path.
*   **Cookies**: Authenticated browser requests must transmit opaque session IDs inside cookies using properties `HttpOnly`, `Secure`, and `SameSite=Lax`.
*   **Headers**:
    *   `X-Correlation-ID`: Enforced UUID mapping across logs and responses to track requests.
    *   `Idempotency-Key`: Enforced for POST/PATCH state mutations to prevent double commits.
    *   `X-Requested-With`: Set to `XMLHttpRequest` to defend against CSRF attempts.

---

## 3. Query Parameter Validation & Complexity Controls

To protect database instances against denial-of-service attempts via complex queries:
*   **Pydantic Schema Checking**: All query parameters must be parsed and validated against strictly defined Pydantic input models. Excess or unmapped parameters trigger instant HTTP 422 errors.
*   **Input Limits (Pagination)**: Enforce cursor pagination for collections:
    *   `limit`: Integer defining max records returned (default: 20, max: 100).
    *   `cursor`: String token returned in `meta` marking the last item coordinate.
*   **Filtering Limits**: Filters are restricted to a whitelist of indexed database fields (e.g., `filter[difficulty]`, `filter[category]`). Unindexed fields are rejected.
*   **Sorting Bounds**: Standardize string parsing parameters using a minus (`-`) prefix to represent descending order (e.g., `GET /api/v1/subjects?sort=-created_at`). Max sorting fields limit is 2.
*   **Search Limits**: Text search strings are trimmed to a maximum length of 128 characters to prevent regex backtracking attacks.

---

## 4. Authoritative OpenAPI Contracts & Versioning

*   **API Versioning**: Enforced via the URI namespace (e.g., `/api/v1/`). Major updates increment the path variable, keeping legacy code bases isolated.
*   **Authoritative OpenAPI Specification**: The backend FastAPI engine automatically generates the OpenAPI schema JSON at `/api/v1/openapi.json`. This schema serves as the single source of truth for:
    *   Client API client code generation.
    *   AI agent routing configurations (agent-readable API schemas).
    *   Contract testing validation suites.
*   **Documentation URLs**: Accessible by human developers at `/docs` (Swagger UI) and `/redoc` (ReDoc) for clear, interactive exploration.

---

## 5. API Error Standards

API endpoints must return a predictable response envelope. The JSON structure enforces strict data contracts:

*   **Success Payload Envelope**:
    ```json
    {
      "status": "success",
      "data": {},
      "meta": {
        "timestamp": "2026-07-09T03:15:00Z",
        "correlation_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d"
      }
    }
    ```
*   **Error Payload Envelope**:
    ```json
    {
      "status": "error",
      "error": {
        "code": "INVALID_PARAMETERS",
        "message": "The request payload did not pass validation checks.",
        "details": [
          {
            "field": "email",
            "issue": "must be a valid email address"
          }
        ],
        "correlation_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d"
      }
    }
    ```
*   **Standardized Error Codes**:
    *   `UNAUTHORIZED`: Session token is missing, expired, or invalid.
    *   `FORBIDDEN`: Actor lacks the capability required for this resource.
    *   `NOT_FOUND`: Target resource path does not exist.
    *   `RATE_LIMIT_EXCEEDED`: API call threshold breached.
    *   `INTERNAL_ERROR`: Unhandled exception intercepted (hides database stack traces).

---

## 6. API Credential & Key Lifecycle (Developer Applications)

External developer integrations and AI agents authenticate using API credentials managed under `Settings -> Developer Applications` (V1-Ready / Deferred):
*   **Credential Creation**:
    1.  The user requests a developer application key.
    2.  The backend generates a client ID (plain text) and an API key secret.
*   **One-Time Reveal**: The API key secret is shown to the user **exactly once** upon creation. It is never rendered in cleartext again.
*   **Hashing & Fingerprinting**: The backend hashes the secret key using SHA-256 before storing it in PostgreSQL (`hashed_secret`). Authenticated requests present the key, which is hashed and matched.
*   **Rotation & Revocation**: Keys can be manually rotated or revoked instantly. Revoked keys update status to `Revoked` in Postgres, blocking subsequent access.
*   **Expiry Bounds**: Keys are issued with configured expirations (e.g. 90 days, 180 days, or permanent). Expired keys automatically return HTTP 403.
*   **Audit Tracking**: Creation, rotation, and revocation events write to `security_audit_logs`.

---

## 7. Mutation Idempotency

Any mutation API route (POST, PUT, PATCH) that modifies system states must enforce idempotency checks:
*   **Headers**: Clients must transmit a unique, client-generated UUID in the `Idempotency-Key` header.
*   **Processing Rules**:
    1.  The server checks if the key exists in the cache (Redis).
    2.  If the key exists and matches a completed transaction, the cached response is returned.
    3.  If the key is locked (processing in progress), the server returns an HTTP status `409 Conflict`.
    4.  If the key is new, the server processes the request, caching the output using a TTL of 24 hours.

---

## 8. Webhook Readiness (V2 Future Concept)

To support future real-time integrations, the API architecture is designed to support webhooks without implementing them in V1:
*   **Webhook Registration Models**: PostgreSQL schemas support registration tables (`webhook_subscriptions` containing `url`, `event_types`, `hashed_secret_token`).
*   **Dispatch Architecture**: The event dispatcher pipeline checks this table and queues tasks for dispatch. In V1, this step is skipped.

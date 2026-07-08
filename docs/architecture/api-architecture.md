# API Architecture

## Document Metadata
*   **Purpose**: Standardizes API routing, payloads, error responses, pagination, filtering, and idempotency interfaces.
*   **Scope**: Governs all backend RESTful interfaces and routing middleware.
*   **Intended Audience**: Backend software engineers, frontend developers, and security auditors.
*   **Related Documents**:
    *   [Backend Architecture](backend-architecture.md)
    *   [Security Standards](../operations/security-standards.md)
*   **Ownership**: Principal API Architect & Head of Platform Engineering

---

## 1. Routing Standards

All platform APIs conform to RESTful design patterns and are versioned via the URI namespace.
*   The canonical root path for version one APIs is `/api/v1/`.
*   Routes correspond to business domains (e.g., `/api/v1/identity`, `/api/v1/workspace`, `/api/v1/knowledge`).
*   Path parameters must be lowercase and use kebab-case formats (e.g., `/api/v1/knowledge/subjects/{subject-id}`).

---

## 2. Naming Conventions

*   **Resource Names**: Use plural nouns for resource paths (e.g., `/api/v1/subjects`, `/api/v1/topics`).
*   **Sub-resources**: Nest sub-resources logically (e.g., `/api/v1/subjects/{subject-id}/modules`).
*   **Actions**: Non-CRUD operations use post actions at the end of paths (e.g., `POST /api/v1/auth/login`, `POST /api/v1/workspace/sync`).

---

## 3. Response Envelopes

API endpoints must return a predictable response envelope. The JSON structure enforces strict data contracts:

*   **Success Payload Envelope**:
    ```json
    {
      "status": "success",
      "data": {},
      "meta": {
        "timestamp": "2026-07-09T03:15:00Z"
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
            "field": "username",
            "issue": "must be a valid email address"
          }
        ]
      }
    }
    ```

---

## 4. Query Parameter Standards

To search, sort, and paginate collections:

*   **Pagination (Cursor-Based)**: Enforce cursor pagination to support real-time data flow without offset lag:
    *   `limit`: Integer defining max records returned (default: 20, max: 100).
    *   `cursor`: String token returned in `meta` marking the last item coordinate.
    *   *Metadata Envelope*: Returns `next_cursor` within `meta`.
*   **Filtering**: Group filters using a structured parameter mapping (e.g., `GET /api/v1/subjects?filter[difficulty]=Hard&filter[category]=ai`).
*   **Sorting**: Standardize string parsing parameters using a minus (`-`) prefix to represent descending order (e.g., `GET /api/v1/subjects?sort=-created_at`).

---

## 5. Mutation Idempotency

Any mutation API route (POST, PUT, PATCH) that modifies system states must enforce idempotency checks:
*   **Headers**: Clients must transmit a unique, client-generated UUID in the `Idempotency-Key` header.
*   **Processing Rules**:
    1.  The server checks if the key exists in the cache.
    2.  If the key exists and matches a completed transaction, the cached response is returned.
    3.  If the key is locked (processing in progress), the server returns an HTTP status `409 Conflict`.
    4.  If the key is new, the server processes the request, caching the output using a TTL of 24 hours.

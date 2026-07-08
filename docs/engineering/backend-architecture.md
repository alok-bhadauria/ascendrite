# Backend Architecture: API Design, Security, and Performance Engineering

---

## 1. Core API Server Design
The backend is built using **FastAPI** to leverage asynchronous execution loops (`async`/`await`), automatic OpenAPI documentation generation, and strict data parsing using **Pydantic**.

### Dependency Injection
FastAPI's dependency injection system manages lifetime scopes (e.g. database connections, user sessions). All database sessions are injected via dependencies, ensuring clean connection closures and preventing resource leaks.

---

## 2. Authentication & Authorization
Ascendrite utilizes stateless **JSON Web Tokens (JWT)** for secure, decentralized user sessions.

### Execution Flow
1.  **Login:** The client sends credentials via `POST /api/v1/auth/login`.
2.  **Verification:** The server verifies credentials against the database user record (passwords hashed using **bcrypt** with a work factor of 12).
3.  **Token Generation:** If verified, the server generates an access token containing the user identity and roles in the payload, signed with a secret key using the `HS256` signature algorithm.
4.  **Client Storage:** The token is returned in a secure, `HttpOnly`, `SameSite=Strict`, `Secure` cookie to mitigate Cross-Site Scripting (XSS) and Cross-Site Request Forgery (CSRF) vulnerabilities.

---

## 3. User & Permission Management
The system enforces **Role-Based Access Control (RBAC)** across three distinct role hierarchies:

| Role | Permissions | API Constraints |
| :--- | :--- | :--- |
| **Student** | Read curriculum content, submit progress logs, take quizzes. | `/api/v1/progress/*`, `/api/v1/assessments/*` |
| **Contributor** | Edit subject JSON configurations, write curriculum data. | Access to staging content generation folders. |
| **Admin** | Manage users, alter system configurations, view platform logs. | Full access to all API routes. |

Authorization is enforced at the router layer using FastAPI dependencies:
```python
def require_role(allowed_roles: List[str]):
    def dependency(current_user: User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Operation forbidden")
        return current_user
    return dependency
```

---

## 4. Security Architecture
*   **Input Validation:** Pydantic schemas validate all payload inputs, converting types and rejecting malformed requests before execution reaches business logic layers.
*   **NoSQL/SQL Injection Prevention:** Avoid raw document queries or string concatenations. Utilize the driver parameterization structures to query MongoDB Atlas safely.
*   **CORS Configuration:** Enforce strict Origin boundaries. Only allow explicit frontend client domains to resolve API responses.

---

## 5. Caching Strategy
To minimize database I/O latency:
*   **Static Asset Caching:** All notes, syllabus maps, and diagrams are loaded once at startup and cached in server memory.
*   **Dynamic State Caching:** User progress records are cached in a **Redis** instance using a time-to-live (TTL) expiration of 1 hour, reducing read loads on MongoDB Atlas.

---

## 6. Logging & Monitoring
*   **Structured Logging:** Outputs logs in JSON format containing timestamps, log levels, request paths, execution times, and correlation IDs (to track requests across asynchronous boundaries).
*   **Application Performance Monitoring (APM):** Exposes Prometheus metrics tracking request durations, latency bounds, and CPU/memory allocations.

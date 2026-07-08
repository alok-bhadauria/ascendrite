# Ascendrite Security Standards

## Document Metadata
*   **Purpose**: Outlines the official platform security requirements, authentication specifications, and compliance rules.
*   **Scope**: Applies to all software engineering, database design, AI services, and infrastructure deployment pipelines.
*   **Intended Audience**: All security leads, software engineers, DevOps specialists, and content auditors.
*   **Related Documents**:
    *   [Backend Architecture](../engineering/backend-architecture.md)
    *   [Engineering Principles](../governance/engineering-principles.md)
*   **Ownership**: Security, Operations & QA Division Lead

---

## 1. Security-First Architecture
Security is a foundational design constraint. The platform shall operate on the assumption that all external endpoints are hostile.

### 1.1 Zero Trust & Least Privilege
*   **Zero Trust**: The application must validate credentials and authorization scopes on every API request. No request shall be trusted implicitly based on origin or internal network boundaries.
*   **Least Privilege (PoLP)**: System tasks, background agents, and database configurations must execute with the absolute minimum set of privileges required to perform their operations.
*   **Defense in Depth**: Security controls must be implemented across multiple decoupled layers (reverse proxy boundaries, application routers, DB credentials).

---

## 2. Authentication and Session Security

### 2.1 Password Hashing Policy
*   Passwords must never be stored in plain text or using weak hashing algorithms.
*   **Hashing Standard**: Passwords shall be salted and hashed using **bcrypt** (minimum work factor of 12) or **Argon2id** (configured matching RFC 9106 standards: $m=65536$ memory, $t=3$ iterations, $p=4$ parallel threads).

### 2.2 JWT Session Configuration
User authentication states shall be managed using stateless JSON Web Tokens (JWT):
*   **Token Signatures**: Access tokens must be signed using secure keys with algorithm `HS256` or `RS256` (keys $\ge 2048$ bits).
*   **Lifetime Boundaries**: Access tokens must expire within 15 minutes. Refresh tokens must expire within 7 days.
*   **Cookie Delivery Guidelines**: Access tokens must be transmitted to clients inside cookies using these secure parameters:
    *   `HttpOnly`: Prevents client-side scripts from reading the cookie value (XSS mitigation).
    *   `Secure`: Restricts transmissions strictly to encrypted HTTPS channels.
    *   `SameSite=Strict`: Restricts cookie transmissions on cross-site requests, mitigating CSRF vectors.

---

## 3. Data Validation and Injection Defense

### 3.1 Input Validation
*   All request payloads must validate against strict Pydantic V2 schemas.
*   The server must reject inputs containing extra or unmapped properties to prevent parameter-binding attacks.
*   Strings must be constrained using regular expressions, length parameters, and range limits.

### 3.2 Output Sanitization & XSS Prevention
*   Any data loaded from external databases must be sanitized before output.
*   The client application must use context-aware HTML entity escaping when rendering variables in the UI.
*   All page headers should inject strict **Content Security Policies (CSP)**.

### 3.3 Database Query Parameterization
*   **SQL Queries**: Applications must use parameterized queries or Object-Relational Mappings (ORM). Raw SQL string concatenation is strictly prohibited.
*   **NoSQL Queries**: MongoDB queries shall utilize driver-native parameters to sanitize query filters.

---

## 4. API and Transport Security
*   **Transport Encryption**: The API gateway and reverse proxy must enforce HTTPS (TLS 1.3 preferred, TLS 1.2 minimum). Port 80 traffic must return a `301 Moved Permanently` redirect to HTTPS.
*   **Security Response Headers**: Every server response must contain these security headers:
    ```http
    Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
    X-Content-Type-Options: nosniff
    X-Frame-Options: DENY
    Content-Security-Policy: default-src 'self'; frame-ancestors 'none';
    Referrer-Policy: strict-origin-when-cross-origin
    ```
*   **CORS Configuration**: CORS configurations shall be restricted to whitelisted domain lists. Wildcard origins (`*`) are prohibited on endpoints handling cookies.
*   **Rate Limiting**: Rate-limiting rules must be applied to all endpoints, with strict limits on auth/login paths.

---

## 5. Audit Logging and Security Monitoring
*   **PII Sanitization**: Logs must not write passwords, credit card numbers, JWT tokens, or database connection strings.
*   **Structured Logs**: Logging output shall be generated in JSON format.
*   **Audit Trail Log**: Critical operations (privilege elevations, account updates, rate-limiting violations) must be directed to a separate, write-once audit log file.
*   **Error Masking**: API error responses in production must hide stack traces, database schema logs, and path traces, returning generic error codes instead.

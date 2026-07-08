# Ascendrite Security Standards

This document establishes the official engineering security standards, architectural policies, and development rules for the Ascendrite platform. All backend, frontend, AI, and infrastructure components must comply with these guidelines.

---

## 1. Core Security Philosophy

### Security-First Development
Security is a first-class architectural concern, not an overlay implemented near release. We build with the assumption that all external entry points are hostile.

### Zero Trust & Defense in Depth
*   **Zero Trust:** Never trust, always verify. Every API request, internal RPC call, database operation, and file read must authenticate and authorize the entity performing the action.
*   **Defense in Depth:** Implement redundant security controls at multiple layers (network, gateway, application runtime, database access controls) so that a failure in one tier does not compromise the system.

### Principle of Least Privilege (PoLP)
Every system module, database credential, API client, user, and background execution runner must operate with the absolute minimum set of privileges required to perform its task.

---

## 2. Secure Software Development Lifecycle (SSDLC)

*   **Design Phase:** Conduct threat modeling on all new API architectures and database access paths.
*   **Implementation Phase:** Enforce static code analysis (SAST) linting, write strict input validation schemas, and restrict direct execution of raw commands or strings.
*   **Testing Phase:** Run automated security regression tests, dependency vulnerability scanners, and execute schema validation scripts.
*   **Deployment Phase:** Ensure environment variables are injected using vault/secret managers, and bind container runtimes to non-privileged OS user profiles.

---

## 3. OWASP Top 10 Mitigations

Contributors must evaluate every code change against the OWASP Top 10 vectors, focusing on these controls:

*   **A01: Broken Access Control:** Enforce server-side role validations on all protected route groups. Never rely on frontend UI components to hide controls for safety.
*   **A03: Injection:** Validate inputs using strict type-cast parsing and parameterize database queries.
*   **A05: Security Misconfiguration:** Restrict CORS endpoints to strict origin boundaries, disable debug/development stack-traces in production builds, and bind cookies to secure properties.
*   **A08: Software and Data Integrity Failures:** Lock dependencies in lockfiles (`package-lock.json`, strict python version tags) and verify package checksums.

---

## 4. Authentication, Authorization & Session Management

### Password Hashing Policy
*   Passwords must never be stored in plain text or using weak hashing algorithms (e.g. MD5, SHA-1, SHA-256).
*   **Hashing Standard:** Passwords must be salted and hashed using **bcrypt** (minimum work factor of 12) or **Argon2id** (configured as per RFC 9106 specs: $m=65536$ memory, $t=3$ iterations, $p=4$ parallelism).

### JWT & Session Management
The platform utilizes stateless JWT tokens for active user sessions:
*   **Access Tokens:** Short-lived tokens (expiration limit: 15 minutes) signed using secure algorithms (`HS256` or `RS256` keys with key lengths $\ge 2048$ bits).
*   **Refresh Tokens:** Long-lived tokens (expiration limit: 7 days) stored securely in the database to manage session rotations.
*   **Cookie Security:** Tokens must be stored in cookies using these parameters:
    *   `HttpOnly`: Prevents client-side scripts from reading the cookie value (XSS mitigation).
    *   `Secure`: Ensures the cookie is only transmitted over encrypted HTTPS channels.
    *   `SameSite=Strict`: Restricts cookie transmissions on cross-site requests, mitigating CSRF vectors.

### Authorization Design
*   **Role-Based Access Control (RBAC):** Users must be assigned explicit roles (Student, Contributor, Admin) validated on the server for each endpoint.
*   **Attribute-Based Access Control (ABAC) Compatibility:** Design auth logic to accept contextual properties (e.g. owner IDs, resource tags) to support future dynamic policies.

---

## 5. Input Validation, Output Sanitization & Injection Prevention

### Input Validation
*   All API request payloads must validate against strict structures (e.g., Pydantic schemas in Python, JSON Schema parsers).
*   Reject requests containing extra or unmapped parameters.
*   Enforce string length constraints, regex character boundaries, and strict numeric ranges.

### Output Sanitization & XSS Prevention
*   Sanitize data loaded from the database or external APIs before outputting it.
*   Use context-aware HTML entity escaping when rendering variables in the UI.
*   Enforce strict **Content Security Policies (CSP)** headers to prevent unauthorized script injections.

### Injection Prevention (SQL / NoSQL)
*   **SQL Queries:** Use parameterized queries or Object-Relational Mappings (ORM) to run searches. Never concatenate variables directly into SQL queries.
*   **NoSQL Queries:** Do not construct raw dictionary queries using unvalidated user inputs. Use driver-native parameters to sanitize query filters.

---

## 6. API and Middleware Security

### Middleware Responsibilities
*   **Transport Security:** Enforce HTTPS. Strip unencrypted traffic at the gateway or return a `301 Moved Permanently` redirect to HTTPS.
*   **Security Headers:** Inject security headers on every response:
    ```http
    Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
    X-Content-Type-Options: nosniff
    X-Frame-Options: DENY
    Content-Security-Policy: default-src 'self'; frame-ancestors 'none';
    Referrer-Policy: strict-origin-when-cross-origin
    ```
*   **CORS (Cross-Origin Resource Sharing):** Define explicit origin limits. Do not use wildcards (`*`) on endpoints handling user credentials or cookies.

### Rate Limiting and Brute-Force Protection
*   All endpoints must be protected by rate-limiting rules.
*   Enforce strict limits on authentication endpoints (e.g. maximum of 5 login attempts per email address per 15-minute window).
*   Implement adaptive delays (IP backoffs) to protect endpoints from brute-force scripts.

### File Upload Security
If the platform implements file uploads:
*   Validate file sizes and MIME types on the server against an explicit allowlist.
*   Store uploaded files outside the public web root.
*   Rename files using random UUID tokens to prevent directory traversal or remote code execution (RCE) attacks.

---

## 7. Secrets and Key Management

*   **No Hardcoded Secrets:** Passwords, API tokens, encryption keys, and private keys must never exist inside the repository source code or commits.
*   **Inject via Environment:** Load secrets from the server environment at runtime (`.env` files ignored by git, or injected via runtime keys).
*   **Encryption-at-Rest:** Databases storing sensitive details must use storage-level encryption (e.g., MongoDB Atlas Automated Encryption).

---

## 8. Logging, Monitoring & Audit Policies

*   **Sanitized Logging:** Logs must never write sensitive personal data, passwords, JWT tokens, credit card numbers, or database connection strings.
*   **Structured Logs:** Output logs in structured JSON format to simplify querying.
*   **Audit Logging:** Changes to user accounts, permission elevations, billing actions, or security threshold violations must be logged to a separate, write-once audit log file.

---

## 9. Exception and Error Handling

*   **No Stack-Traces in Production:** API responses must return structured error schemas (e.g., status codes, clean message strings). Internal database errors, file routes, and debug stack-traces must only exist in system log files.
*   **Graceful Degrades:** Return clear status codes (e.g., `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`, `429 Too Many Requests`).

---

## 10. Compliance Readiness

Design modules to align with the core security rules of global standards:
*   **GDPR:** Support the right to be forgotten (cascading user deletion from databases), and document all PII locations.
*   **SOC 2 / ISO 27001:** Establish trace paths for access controls, system logs, and security incident reporting.

---

## 11. Security Checklist for Contributors

Before submitting a Pull Request, verify compliance with this checklist:

- [ ] Zero hardcoded passwords, tokens, or private keys exist in the diff.
- [ ] Every input field is validated using a structured schema (Pydantic/JSON Schema).
- [ ] No raw SQL/NoSQL queries or string concatenations exist.
- [ ] No console logs or print statements outputting sensitive credentials are left in the code.
- [ ] Dependency lockfiles (`package-lock.json`, `requirements.txt`) are updated.
- [ ] Code passes all linting, static analysis, and validation checks.
- [ ] All new APIs return clean error codes with no stack-traces exposed.
- [ ] User role validations (RBAC) are verified on the server.
- [ ] No emojis exist in any of the modified documentation or source files.

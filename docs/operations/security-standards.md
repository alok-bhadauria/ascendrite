# Ascendrite Security Standards

## Document Metadata
*   **Purpose**: Outlines the official platform security requirements, authentication specifications, and compliance rules.
*   **Scope**: Applies to all software engineering, database design, AI services, and infrastructure deployment pipelines.
*   **Intended Audience**: All security leads, software engineers, DevOps specialists, and content auditors.
*   **Related Documents**:
    *   [Backend Architecture](../architecture/backend-architecture.md)
    *   [Engineering Principles](../governance/engineering-principles.md)
*   **Ownership**: Security, Operations & QA Division Lead

---

## 1. Security-First Architecture
Security is a foundational design constraint. The platform operates on the assumption that all external endpoints are hostile.

### 1.1 Zero Trust & Least Privilege
*   **Zero Trust**: The application must validate credentials and authorization scopes on every API request. No request is trusted implicitly based on origin or internal network boundaries.
*   **Least Privilege (PoLP)**: System tasks, background agents, and database configurations must execute with the absolute minimum set of privileges required to perform their operations.
*   **Defense in Depth**: Security controls must be implemented across multiple decoupled layers (reverse proxy boundaries, application routers, DB credentials).

---

## 2. Identity & Session Security

### 2.1 Password Hashing Policy
*   Passwords must never be stored in plain text or using weak hashing algorithms.
*   **Hashing Standard**: Passwords shall be salted and hashed using **bcrypt** (minimum work factor of 12) or **Argon2id** (configured matching RFC 9106 standards: $m=65536$ memory, $t=3$ iterations, $p=4$ parallel threads).

### 2.2 JWT Session Configuration
User sessions are managed using stateless JSON Web Tokens (JWT):
*   **Token Signatures**: Access tokens must be signed using secure keys with algorithm `HS256` or `RS256` (keys $\ge 2048$ bits).
*   **Session Lifecycle**: Access tokens must expire within 15 minutes. Refresh tokens must expire within 7 days.
*   **Refresh Token Rotation**: Refresh tokens must follow a single-use rotation strategy. Once a refresh token is used to issue a new access token, it is revoked, and a new refresh token is issued.
*   **Cookie Delivery Guidelines**: Access tokens must be transmitted to clients inside cookies using `HttpOnly`, `Secure`, and `SameSite=Strict` flags.

### 2.3 Verification & SSO Readiness
*   **Trusted Devices**: The system registers device finger-prints during login. Multi-device logins are tracked, allowing users to revoke active sessions remotely.
*   **Multi-Factor Authentication (MFA)**: Schema parameters must accommodate future Totp-based MFA configurations.
*   **Enterprise SSO**: Architecture supports future SAML/OIDC configuration keys to integrate with external identity systems.
*   **Account Recovery**: Out-of-band email validation links generated via cryptographically signed short-lived tokens. Account recovery processes must never disclose username existence.

---

## 3. Application Security & Injection Defense

The platform enforces systematic defenses against common application vulnerabilities:
*   **SQL Injection**: Applications must use parameterized queries or ORMs. Raw SQL concatenation is prohibited.
*   **NoSQL Injection**: MongoDB queries must utilize driver-native parameters rather than raw strings to sanitize query filters.
*   **Cross-Site Scripting (XSS)**: Data loaded from databases must be escaped before outputting to the DOM. The client application must use context-aware HTML entity escaping when rendering variables.
*   **Cross-Site Request Forgery (CSRF)**: Cookies are restricted via `SameSite=Strict` flags, and mutations require custom request headers (e.g. `X-Requested-With`).
*   **Server-Side Request Forgery (SSRF)**: Any outgoing request triggered by user input must be restricted to a whitelist of verified domains, blocking internal loopback IPs (`127.0.0.1`, `localhost`) and metadata endpoints.
*   **Clickjacking**: Frame-ancestor options must be configured to deny rendering of the platform within external iframes.
*   **Path Traversal**: File upload and reading routes must validate target paths against sandboxed workspace directories, rejecting sequences containing directory traversals (`..`).
*   **Open Redirects**: Navigation redirects must be restricted to local paths, checking that target URLs match the platform's host domain.

---

## 4. API Security & Transport Controls

API routes must implement standardized security layers at the gateway and middleware boundaries:
*   **Authentication Middleware**: Validates incoming JWT tokens and extracts active actor credentials.
*   **Authorization Middleware**: Verifies client credentials against the resource path parameters and evaluates permissions.
*   **Capability Validation**: Verifies that the actor holds the specific capability required for the target method.
*   **Input Validation & Output Sanitization**: Inputs validate against Pydantic schemas, rejecting unmapped properties. Outputs are sanitized to filter out system errors or PII records.
*   **API Versioning**: Enforces version routes (e.g., `/api/v1/`) to ensure changes do not break legacy integrations.
*   **Rate Limiting**: Limits requests per IP address, with strict bounds on auth and search endpoints.
*   **Request Size Limits**: Max payload size limits must be enforced on uploads to block denial-of-service attempts.

---

## 5. Audit Logging, Monitoring & Security Telemetry

Structured telemetry gathers security events without exposing personal data:
*   **Structured Logs**: Logging output shall be generated in JSON format.
*   **PII Sanitization**: Logs must not write passwords, credit card numbers, JWT tokens, or database connection strings.
*   **Immutable Audit Logs**: Operational adjustments (permissions, ownership transfers, deletions) are directed to a cryptographically sealed, read-only audit log.
*   **Suspicious Activity Detection**: Automated alerts monitor rate-limiting violations, high token burn rates, or simultaneous logins from distant geo-coordinates.
*   **Failed Login Monitoring**: Repeated credential validation failures must trigger temporal IP bans on auth routes.
*   **Permission Change Auditing**: Every authorization modification or capability change is logged with matching moderator IDs and timestamps.

---

## 6. Infrastructure Security

Operational hosting environments must enforce strict boundaries:
*   **HTTPS Everywhere**: Gateway routers redirect Port 80 requests to encrypted TLS 1.3 channels.
*   **Secure Secrets Management**: Database passwords, API credentials, and JWT keys are loaded from secure vault stores at runtime, never committed to version control.
*   **Environment Isolation**: Development, staging, and production clusters run on completely isolated network subnets.
*   **Reverse Proxy Readiness**: All web requests route through a reverse proxy (e.g. Nginx or Cloudflare) handling load balancing and SSL termination.
*   **DDoS Mitigation Readiness**: Traffic rate limits and web application firewalls (WAF) protect the entry gateways.
*   **Container Isolation**: Services run in non-root Docker container contexts with limited host resource access.
*   **Backup Protection**: Database snapshots are encrypted at rest and stored in secure, read-only backup locations.

---

## 7. AI Security & Guardrails

To prevent compromise through AI pipelines:
*   **Prompt Injection Awareness**: Input sanitization filters inspect user prompts for execution instructions before forwarding queries to the LLM.
*   **Retrieval Validation**: The Knowledge Service verifies that retrieved RAG context chunks map strictly to the active topic ID, preventing data leakage.
*   **Agent Capability Restrictions**: AI agents are assigned scoped permissions matching their specific tasks, conforming to PoLP rules.
*   **Human Approval**: Sensitive operations (such as committing curriculum draft updates or altering system indexes) require manual verification and approval by a moderator.
*   **Auditability of AI Actions**: Every decision, prompt token weight, similarity score, and LLM output is recorded in the security logging database.

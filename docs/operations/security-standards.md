# Ascendrite Security Standards

## Document Metadata
*   **Purpose**: Outlines the official platform security requirements, authentication specifications, session lifecycles, file uploads safety, and compliance rules.
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

## 2. Identity, Sessions & Device Security

### 2.1 Password Hashing Policy
*   Passwords must never be stored in plain text or using weak hashing algorithms.
*   **Hashing Standard**: Passwords shall be salted and hashed using **Argon2id** (configured matching RFC 9106 standards: $m=65536$ memory, $t=3$ iterations, $p=4$ parallel threads) as the canonical KDF for new passwords. Legacy bcrypt hashes (minimum work factor of 12) are supported only for migration compatibility, and successful logins using legacy hashes must trigger an automatic upgrade to the Argon2id standard.

### 2.2 Secure Session Management
User sessions are managed using secure, server-side session contexts identified by opaque browser session tokens:
*   **Session Token Storage**: Browser clients receive an opaque, high-entropy session identifier. The token must be transmitted to the browser inside cookies with these properties:
    *   `HttpOnly = true` (blocks client-side JavaScript access, defending against XSS leaks).
    *   `Secure = true` (enforced in HTTPS staging/production settings).
    *   `SameSite = Lax` by default (prevents cross-site request forgery while maintaining navigation usability).
    *   `Path = /` (scoped to the application domain).
*   **LocalStorage Ban**: Sensitive credentials, access keys, or long-lived authentication secrets must never be stored in browser `localStorage` or `sessionStorage`. Non-sensitive UI variables (e.g. theme preference) may be stored in local storage.

### 2.3 Configurable Security Default Timeouts
*   **Normal Session Idle Timeout**: 7 days.
*   **Remember-Login Idle Timeout**: 30 days.
*   **Absolute Session Lifetime**: 90 days (forces complete re-authentication).
*   **Step-Up Verification Freshness**: 10 minutes (determines expiration of elevated authorization context).
*   **Password Reset Token**: 15 to 30 minutes (short-lived cryptographically signed token).
*   **Email-Change Verification**: 15 to 30 minutes.
*   **One-Time Verification Code (MFA)**: 10 minutes.

### 2.4 Device & Session Management
The platform provides users with visual oversight and self-service revocation of active session locations under `Settings -> Security -> Devices & Sessions`:
*   **Session Metadata Table**: The backend tracks active session contexts including:
    *   `session_id` (UUIDv4 primary key)
    *   `user_id` (UUIDv4 referencing the actor)
    *   `hashed_session_secret` (SHA-256 hash of the opaque session token)
    *   `created_at` (UTC timestamp)
    *   `last_active_at` (updated on request validations)
    *   `client_agent` (normalized browser/OS device classification)
    *   `ip_address` (used for geo-coordinate lookup context)
*   **Revocation Flow**:
    1.  The user selects a remote target session from the device list.
    2.  The backend validates the request, updates the target's status to `Revoked` in the session database table, and invalidates the cached session key in Redis.
    3.  The next request from the revoked client fails token validation and redirects the user to the login screen.
*   **Session Epoch / Epoch Invalidations**: Major account events (password reset, emergency lockdown, or account suspension) trigger a session epoch increment, automatically invalidating all previously issued sessions and token hashes associated with that user ID.

---

## 3. Step-Up Authentication

High-impact operations are protected by step-up verification rules. Actions are classified by risk levels:

*   **Risk Classifications**:
    *   *Routine*: Viewing progress, editing dashboard card layouts, reading notes. (No step-up required).
    *   *Sensitive*: Modifying account email, editing notifications preferences, reviewing logs. (Requires active verification freshness $\le 10\text{ minutes}$).
    *   *Critical*: Banning users, changing roles, assigning system capabilities, or rotating S3 access keys. (Requires step-up confirmation immediately prior to write commit).
    *   *Destructive*: Deleting an account, purging workspace files, clearing database collections. (Requires password check and active MFA signature).
*   **Verification Loop**:
    1.  The API router catches a request classified as Sensitive/Critical.
    2.  The server checks the session's `last_step_up_time`. If the time has expired or is absent, the backend responds with HTTP 401 requesting re-verification.
    3.  Upon verification validation, the backend issues an elevated authorization token (stored securely and bound to the session) expiring in 10 minutes, allowing the user to complete the task.
    4.  All step-up events are recorded in `security_audit_logs`.

---

## 4. Secure File Upload Ingestion Pipeline

To prevent malicious uploads from corrupting storage systems or attacking web clients, all uploads undergo a strict validation pipeline:

```
[Incoming File Upload]
       │
       ▼
[Size/Extension Verification] (Verifies byte size and checks extension allowlist)
       │
       ▼
[Quarantine Area] (Writes file stream to bucket temporary-assets)
       │
       ▼
[MIME & Magic-Byte Scanner] (Inspects file headers for actual content signatures)
       │
       ▼
[Security & Malware Scan] (Executes security/antivirus checks on temporary files)
       │
       ├─► [Failure] ──► Auto-purge from quarantine & log security threat
       │
       ▼
[Metadata Sanitization] (Strips metadata tags from images, escapes characters)
       │
       ▼
[Promotion to Trusted Bucket] (Moves validated asset to knowledge-assets or user-media)
```

*   **Quarantine Staging**: Files must never write to permanent buckets directly. Uploads write to `temporary-assets` first, using random object keys to block path traversal attempts.
*   **Automatic Cleanup**: An hourly cron task deletes files remaining in the `temporary-assets` quarantine bucket for more than 24 hours.

---

## 5. Secure Generated Downloads & Exports

The platform secures the delivery of system-generated books, sitemaps, resumes, and study progress reports:
*   **Entitlement Auditing**: Every export request evaluates the caller's capability scopes and ownership credentials before launching background tasks.
*   **Storage Isolation**: Generated files write to the private bucket `generated-assets` with an active expiration rule.
*   **Secure Delivery**: Files must never be exposed via static public URLs. Delivery is handled via short-lived, pre-signed URLs expiring in 15 minutes.
*   **Download Logging**: Successful download events write to log databases, tracking user ID and document type.
*   **Lifecycle Purge**: An automated object retention policy purges objects from `generated-assets` after 7 days.

---

## 6. Application Security & Injection Defense

The platform enforces systematic defenses against common application vulnerabilities:
*   **SQL Injection**: Applications must use parameterized queries or ORMs. Raw SQL concatenation is prohibited.
*   **NoSQL Injection**: MongoDB queries must utilize driver-native parameters rather than raw strings to sanitize query filters.
*   **Cross-Site Scripting (XSS)**: Data loaded from databases must be escaped before outputting to the DOM. The client application must use context-aware HTML entity escaping when rendering variables.
*   **Cross-Site Request Forgery (CSRF)**: Cookies are restricted via `SameSite=Lax` flags, and mutations require custom request headers (e.g. `X-Requested-With`).
*   **Server-Side Request Forgery (SSRF)**: Any outgoing request triggered by user input must be restricted to a whitelist of verified domains, blocking internal loopback IPs (`127.0.0.1`, `localhost`) and metadata endpoints.
*   **Clickjacking**: Frame-ancestor options must be configured to deny rendering of the platform within external iframes.
*   **Path Traversal**: File upload and reading routes must validate target paths against sandboxed workspace directories, rejecting sequences containing directory traversals (`..`).
*   **Open Redirects**: Navigation redirects must be restricted to local paths, checking that target URLs match the platform's host domain.

---

## 7. API Security & Transport Controls

API routes must implement standardized security layers at the gateway and middleware boundaries:
*   **Authentication Middleware**: Validates incoming JWT tokens and extracts active actor credentials.
*   **Authorization Middleware**: Verifies client credentials against the resource path parameters and evaluates permissions.
*   **Capability Validation**: Verifies that the actor holds the specific capability required for the target method.
*   **Input Validation & Output Sanitization**: Inputs validate against Pydantic schemas, rejecting unmapped properties. Outputs are sanitized to filter out system errors or PII records.
*   **API Versioning**: Enforces version routes (e.g., `/api/v1/`) to ensure changes do not break legacy integrations.
*   **Rate Limiting**: Limits requests per IP address, with strict bounds on auth and search endpoints.
*   **Request Size Limits**: Max payload size limits must be enforced on uploads to block denial-of-service attempts.

---

## 8. Audit Logging, Monitoring & Security Telemetry

Structured telemetry gathers security events without exposing personal data:
*   **Structured Logs**: Logging output shall be generated in JSON format.
*   **PII Sanitization**: Logs must not write passwords, credit card numbers, JWT tokens, or database connection strings.
*   **Immutable Audit Logs**: Operational adjustments (permissions, ownership transfers, deletions) are directed to a cryptographically sealed, read-only audit log.
*   **Suspicious Activity Detection**: Automated alerts monitor rate-limiting violations, high token burn rates, or simultaneous logins from distant geo-coordinates.
*   **Failed Login Monitoring**: Repeated credential validation failures must trigger temporal IP bans on auth routes.
*   **Permission Change Auditing**: Every authorization modification or capability change is logged with matching moderator IDs and timestamps.

---

## 9. Infrastructure Security

Operational hosting environments must enforce strict boundaries:
*   **HTTPS Everywhere**: Gateway routers redirect Port 80 requests to encrypted TLS 1.3 channels.
*   **Secure Secrets Management**: Database passwords, API credentials, and JWT keys are loaded from secure vault stores at runtime, never committed to version control.
*   **Environment Isolation**: Development, staging, and production subnets run on completely isolated network segments.
*   **Reverse Proxy Readiness**: All web requests route through a reverse proxy (e.g. Nginx or Cloudflare) handling load balancing and SSL termination.
*   **DDoS Mitigation Readiness**: Traffic rate limits and web application firewalls (WAF) protect the entry gateways.
*   **Container Isolation**: Services run in non-root Docker container contexts with limited host resource access.
*   **Backup Protection**: Database snapshots are encrypted at rest and stored in secure, read-only backup locations.

---

## 10. AI Security & Guardrails

To prevent compromise through AI pipelines:
*   **Prompt Injection Awareness**: Input sanitization filters inspect user prompts for execution instructions before forwarding queries to the LLM.

---

## 11. Adaptive Human-Challenge Abuse Protection

To protect the platform against automated abuse, denial-of-service attempts, and credential-stuffing attacks, the platform employs a provider-neutral adaptive human-challenge (CAPTCHA) model:

### 11.1 Core Abuse Prevention Principles
*   **Defense-in-Depth**: Human challenges are not a substitute for authentication or authorization. They serve as one layer of abuse prevention alongside:
    *   IP-based and route-based rate limiting.
    *   Failed-login cooldown timers.
    *   Request complexity restrictions.
    *   Usage quotas and token budgets.
    *   Audit and security logging.
*   **Risk-Based Enforcement**: CAPTCHAs are not presented indiscriminately. The security gateway evaluates request risk parameters dynamically:
    *   *Low Risk*: No challenge is presented; requests proceed subject to standard rate limits.
    *   *Elevated Risk*: A lightweight, passive, or interactive human challenge is required.
    *   *High-Confidence Abuse*: Requests are blocked or rejected directly, rather than presenting endless challenge loops.
*   **Privacy & Accessibility**: Human-challenge components must remain keyboard-navigable and screen-reader compatible. Standard image-selection grids are prohibited; passive background checks (e.g. cryptographic puzzle tokens) are preferred. User data collection must follow data minimization principles.

### 11.2 Flow Enforcement Matrix
*   **Candidate Flows for Challenge Verification**:
    *   User registration/signup under anomalous geo-coordinates or network indicators.
    *   User login attempts following repeated credential validation failures.
    *   Account recovery or password reset requests to block enumeration attempts.
    *   Email verification code resend triggers to prevent mail server abuse.
    *   Public anonymous search or AI tutor endpoints (if exposed in public spaces).
*   **Normally Exempt Flows**:
    *   Routine workspace operations and note reading by authenticated users.
    *   Profile updates and configuration adjustments within active, validated sessions.
    *   Developer application API-key generation requests (which must use **Step-Up Authentication** instead).
    *   Administrative actions and moderator approvals (which require password confirmations or MFA step-up authentication).

### 11.3 Verification & Integration Flow
*   **Provider-Neutral Design**: Core business logic interacts with a generic verification adapter interface. While Cloudflare Turnstile is documented as the preferred initial implementation candidate, the integration boundary must remain fully replacable without altering backend controllers.
*   **Conceptual Challenge Verification Flow**:
    ```
    Client Request ──► Gateway Checks ──► Elevated Risk: Return challenge payload
    Client Solves Challenge ──► Submit Token with Action ──► Server Authoritative Verification
    ```
*   **Authoritative Server Verification**:
    *   Frontend solution tokens are never trusted on their own. The backend must query the challenge provider API to authoritatively verify the token.
    *   Verification must validate token freshness and expiry according to the selected provider's authoritative guarantees and Ascendrite's configured security policy. Ascendrite must never extend provider-issued validity or accept a token outside the provider's valid verification window.
    *   Where supported by the selected provider, authoritative server-side verification must validate the provider-returned hostname, site identity, or equivalent environment context against Ascendrite's configured allowlist for the active deployment environment. (Incoming raw HTTP request headers are request inputs and must not independently establish trusted challenge context; provider-returned verification metadata must be checked against trusted server-side configuration; and development, staging, and production environments may have different configured allowed hostnames or site identities.)
    *   Challenge tokens are not reusable. Storing raw tokens in logs is prohibited.

### 11.4 Failure & Outage Recovery (Fail-Closed Policy)
In the event of a challenge provider outage or API network failure, the platform enforces risk-dependent fallback rules:
*   *Low-risk operations* (e.g., public search) degrade to basic rate-limiting limits.
*   *Elevated-risk operations* (e.g., signup, recovery) must fail closed, rejecting requests with HTTP 503 until verification reachability is restored.

### 11.5 Implementation & Deployment Classification
*   **V1 Direct Requirement**: Provide a provider-neutral human-challenge verification adapter interface class in the backend code and a verification middleware schema.
*   **Endpoint Activation**: Challenge verification must be enforced on signup, login, recovery, verification-code resend, public/anonymous AI operations, and other applicable abuse-sensitive endpoints only when the risk engine, endpoint policy, or prior challenge state requires a human challenge. Low-risk requests must be allowed to proceed without CAPTCHA subject to ordinary security controls.
*   **Provider Status**: Not currently implemented. The physical Cloudflare Turnstile client is deferred until active deployment.


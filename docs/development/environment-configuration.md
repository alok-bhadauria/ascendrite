# Environment Configuration

## Document Metadata
*   **Purpose**: Outlines configuration parameters, required environments, and secret injection guidelines.
*   **Scope**: Governs `.env` configurations, staging properties, and cloud vault profiles.
*   **Intended Audience**: Software developers, DevOps engineers, and security compliance auditors.
*   **Related Documents**:
    *   [Local Development](local-development.md)
    *   [Security Standards](../operations/security-standards.md)
*   **Ownership**: Lead DevOps Engineer & Site Reliability Operations Lead

---

## 1. Config Variable Standards

Ascendrite manages runtime variables using strict naming and loading rules:
*   All environment variables must use uppercase letters and snake-case formats (e.g., `DATABASE_URL`).
*   Default configurations must be loaded using typed structures (e.g., Pydantic settings models) to validate parameters before startup.
*   Production environments must never fall back to default development settings. Missing required variables must halt startup.

---

## 2. Required Backend Environment Variables

The backend API server requires the following configuration keys:

*   `DATABASE_URL`: Connection string for the database instance.
*   `REDIS_URL`: Connection parameters for the memory cache tier.
*   `JWT_SECRET`: Secret key used for cryptographic token signing.
*   `JWT_EXPIRATION_MINUTES`: Session token expiration limit.
*   `AI_MODEL_PROVIDER`: Target LLM provider connector name.
*   `AI_MODEL_API_KEY`: API credential key for the model client.

---

## 3. Required Frontend Environment Variables

The React user interface requires the following public properties:

*   `REACT_APP_API_URL`: Target URL endpoint for the REST API server.
*   `REACT_APP_ENV`: Deployment context indicator (`development`, `staging`, or `production`).

---

## 4. Secret Management Rules

To protect credentials:
*   **No Secrets in Git**: Committing `.env` files, password strings, or API key values to version control repositories is prohibited.
*   **Local Emulation**: Developers use `.env.local` files for sandbox parameters.
*   **Production Deployment**: Staging and production credentials are dynamically injected into container memory from secure secret vaults during the release phase.

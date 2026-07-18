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

The backend API server requires the following configuration keys (non-secret default templates for local development):

*   **MongoDB Connection**:
    *   `MONGODB_URI`: Local connection parameters pointing to the MongoDB Community Server instance (e.g. `mongodb://ascendrite_app:Alok@Mongodb#AscendriteApplication@127.0.0.1:27017/ascendrite`).
    *   `MONGODB_DB_NAME`: Database name (defaults to `ascendrite`).
*   **PostgreSQL Connection**:
    *   `POSTGRES_URL`: Relational connection string pointing to the PostgreSQL instance (e.g. `postgresql://ascendrite_app:Alok@Postgresql#AscendriteApplication@127.0.0.1:5432/ascendrite`).
*   **Redis Connection**:
    *   `REDIS_URL`: Connection parameters for caching and event queues (e.g. `redis://ascendrite_app:Alok@Memurai#AscendriteApplication@127.0.0.1:6379/0`).
*   **RustFS / S3 Object Storage**:
    *   `RUSTFS_ENDPOINT`: Local S3 endpoint address (`127.0.0.1:9000`).
    *   `RUSTFS_ACCESS_KEY_ID`: Client application key identity (local default: `ascendrite_runtime`).
    *   `RUSTFS_SECRET_ACCESS_KEY`: Cryptographic signing key (reconciled dynamically at runtime).
    *   `RUSTFS_REGION`: Bucket storage region (local default: `ap-south-1`).
*   **JWT Security Configuration**:
    *   `JWT_SECRET`: Cryptographic signing secret key.
    *   `JWT_ALGORITHM`: Signature hash algorithm (default: `HS256`).
    *   `JWT_EXPIRE_MINUTES`: Access duration (default: `15`).
    *   `JWT_REFRESH_TOKEN_EXPIRE_DAYS`: Refresh duration (default: `7`).
*   **AI Tutoring Integration**:
    *   `OPENAI_API_KEY`: API credential key for LLM calls.
    *   `OPENAI_EMBEDDING_MODEL`: Target vector embedding model (default: `text-embedding-3-small`).
    *   `OPENAI_CHAT_MODEL`: Target tutor LLM model (default: `gpt-4o`).

---

## 3. Required Frontend Environment Variables

The React user interface requires the following public properties:

*   `REACT_APP_API_URL`: Target endpoint for the REST API server (local default: `http://127.0.0.1:8000/api/v1`).
*   `REACT_APP_ENV`: Deployment context indicator (`development`, `staging`, or `production`).

---

## 4. Environment Precedence Contract

To ensure portability and avoid configuration inconsistencies, the application does not maintain nested environment files (e.g. `platform/server/.env` is prohibited). Configuration resolves using a strict priority hierarchy:

1.  **System / Container Environment**: Variables injected directly in shell or container memory (e.g., via Docker Compose env mappings, Kubernetes ConfigMaps, or CI/CD runner secrets). Take absolute top precedence.
2.  **Local Sandbox File (`.env.local`)**: A developer-created, untracked configuration file located at the repository root (`/`). Read during local development to emulate environment-specific credentials.
3.  **Default Config Models**: Embedded in PydanticSettings class attributes (`platform/server/core/config.py`) as developer fallback variables.

---

## 5. Secret Management Rules

To protect credentials:
*   **No Secrets in Git**: Committing `.env` files containing raw passwords, API secret keys, or access keys to version control is strictly prohibited.
*   **Local Emulation**: Developers use `.env.local` files at the repository root for sandbox parameters.
*   **Production Deployment**: Staging and production credentials must be injected dynamically into container memory from secure secret vaults during the release phase. No deployment-specific parameters are committed to source files.
*   **Local Secrets Management**: All development secrets, API keys, credentials, and certificates are fully decoupled from source code, residing in the untracked private directory `E:\Projects\ascendrite-private\`:
    *   `credentials.txt`: A private, owner-only local credential registry containing local infrastructure connection details, identities, roles, purposes, and credentials for PostgreSQL 18.4, MongoDB Community Server 8.0.26, Memurai Developer Edition 4.2.3 / Redis API 7.4.9, and RustFS 1.0.0-beta.8. It is a current local single-owner development convention, not the intended production secret-management architecture. No credential values are exposed or reproduced in the repository code.
    *   `api-keys.txt`: Currently empty reserved local file for future API-key storage if required. Its concrete purpose must be established before active use. No active credentials exist in this file.
    *   `rustfs-access-key.txt`: Machine-readable RustFS access-key file consumed by the current RustFS service startup configuration.
    *   `rustfs-secret-key.txt`: Machine-readable RustFS secret-key file consumed by the current RustFS service startup configuration.
    *   `rustfs-credentials.exported.json`: Sensitive RustFS credential export artifact. It must remain private, untracked, and outside the source repository.

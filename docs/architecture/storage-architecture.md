# Storage Architecture

## Document Metadata
*   **Purpose**: Defines the platform storage architecture, local directory specs, S3 storage buckets, and layout boundaries.
*   **Scope**: Governs local directory structures, S3 object storage layouts, database persistence paths, and caching directories.
*   **Intended Audience**: Backend software engineers, database administrators, and operations engineers.
*   **Related Documents**:
    *   [Backend Architecture](backend-architecture.md)
    *   [Database Schema](database-schema.md)
*   **Ownership**: Lead Storage Architect & Head of Platform Engineering

---

## 1. Storage Boundaries & Local Directory Layout

Ascendrite separates storage into logical layers, ensuring separation between third-party binaries, application source code, and persistent runtime state.

Local storage paths in the development environment follow a strict Windows layout configuration:

### 1.1 Binaries & SDKs Directory (`E:\Softwares\`)
Third-party binaries, database runtimes, and local service utilities are installed under `E:\Softwares\`:
*   `E:\Softwares\RustFS\`: Houses the S3-compatible Object Storage service binaries.
*   `E:\Softwares\Amazon\AWSCLIV2\`: Contains the AWS CLI executables for S3 testing.

### 1.2 Application Source Repository (`E:\Projects\Ascendrite\`)
Houses the active Git repository, schemas, scripts, and modular service codes:
*   `platform/client/`: React client code.
*   `platform/server/`: FastAPI backend logic.
*   `knowledge-base/`: Public curriculum schemas and metadata taxonomy files.

### 1.3 Persistent Infrastructure Data (`E:\Projects\ascendrite-data\`)
Contains persistent state, runtime logs, backups, and active data. It must never be committed to Git:
*   `mongodb/`: MongoDB active collections and lock files.
*   `postgres/`: PostgreSQL transactional records.
*   `redis/`: Ephemeral Memurai database caches.
*   `rustfs/`:
    *   `data/`: Persistent bucket directories and object binaries.
    *   `logs/`: S3 console and access event outputs.
*   `knowledge-base/`: Generated runtime exports of the curriculum catalogs.
*   `migration-toolkit/`: Operational utilities for data migration (containing import/export scripts and logs under `reports/`).
*   `backups/`: Unified backups directory containing folders for `knowledge`, `mongodb`, `postgres`, and `rustfs`.

### 1.4 Private Assets Directory (`E:\Projects\ascendrite-private\`)
Contains untracked credential keys, certificates, and historical snapshots:
*   `secrets/`:
    *   `credentials.txt`: A private, owner-only local credential registry containing local infrastructure connection details.
    *   `api-keys.txt`: Reserved file for future API-key storage.
    *   `rustfs-access-key.txt` & `rustfs-secret-key.txt`: Machine-readable S3 credentials.
    *   `rustfs-credentials.exported.json`: Sensitive RustFS credential export artifact.
*   `certificates/`: SSL and TLS certificates for secure local domain endpoints.
*   `snapshots/`: Historical snapshots of raw content directories.

---

## 2. Object Storage Configuration & Buckets

The platform interfaces with S3-compatible object storage (locally backed by the **RustFS** service on `127.0.0.1:9000`).

### 2.1 Buckets Lifecycle
To protect proprietary data and manage cache expirations, files are structured into separate buckets:

*   **`knowledge-assets`**:
    *   *Purpose*: Houses compiled topic notes, exercises, and revision cards.
    *   *Versioning*: Enabled to track asset edits.
    *   *Security*: Restricted strictly to the `Knowledge Service` runtime user.
*   **`user-media`**:
    *   *Purpose*: Stores user avatars and images.
    *   *Lifecycle*: Retained for 30 days after account archival events.
    *   *Access*: Public read access via pre-signed S3 URLs.
*   **`workspace-files`**:
    *   *Purpose*: Caches code scratchpads and layout assets.
    *   *Lifecycle*: Retained during active session lifecycle.
*   **`generated-assets`**:
    *   *Purpose*: Holds exported PDFs, ZIP packages, and textbook compilations.
    *   *Lifecycle*: Expired and deleted automatically after 7 days to conserve space.
*   **`temporary-assets`**:
    *   *Purpose*: Quarantine area for incoming uploads during scanning.
    *   *Lifecycle*: Auto-purged every 24 hours.
*   **`system-backups`**:
    *   *Purpose*: Monthly encrypted database snapshots.
    *   *Access*: Restrictive consoleAdmin policies (write-access denied to standard app keys).

---

## 3. Cache Persistence Rules

To minimize database read latencies, Redis is deployed as a high-speed volatile cache:
*   Session validation tokens are stored with an explicit Time-to-Live (TTL) expiration boundary.
*   Frequently queried catalog indices are cached in memory and invalidated automatically upon content publication.

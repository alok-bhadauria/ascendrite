# Data Architecture & Persistence Engineering Specification

## Document Metadata
*   **Purpose**: Details the multi-tier persistence schemas, datastore parameters, caches, object storage configurations, and database abstractions.
*   **Scope**: Governs all databases, caches, vector indexers, and file storage instances across the platform.
*   **Intended Audience**: Database architects, backend developers, security engineers, and DevOps leads.
*   **Related Documents**:
    *   [Backend Architecture](backend-architecture.md)
    *   [API Architecture](api-architecture.md)
    *   [Security Standards](../operations/security-standards.md)
*   **Ownership**: Head of Platform Engineering & Principal Database Architect

---

## 1. Overall Persistence Architecture

The platform uses a hybrid storage topology, separating relational operations, document-based metadata maps, low-latency caching, vector index coordinates, and large binary media. Storage engines are completely abstracted from application code, communicating exclusively through repository classes.

```
                  +-----------------------------------+
                  |         Platform Services         |
                  +-----------------------------------+
                                    |
                                    v
                  +-----------------------------------+
                  |         Knowledge Service         |
                  +-----------------------------------+
                                    |
            +-----------------------+-----------------------+
            |                       |                       |
            v                       v                       v
+-----------------------+ +-----------------------+ +-----------------------+
|  PostgreSQL Database  | |   MongoDB Database    | |    Vector Database    |
|  - Users, sessions    | |  - Course metadata  | |  - Vector indexes   |
|  - Permissions, logs  | |  - Syllabus graph   | |  - RAG embeddings   |
+-----------------------+ +-----------------------+ +-----------------------+
            |                       |                       |
            +-----------------------+-----------------------+
                                    |
            +-----------------------+-----------------------+
            |                                               |
            v                                               v
+-----------------------+                       +-----------------------+
|  Redis Memory Cache   |                       |  S3 Object Storage    |
|  - Active session cache|                       |  - Knowledge Assets   |
|  - Rate-limit flags   |                       |  - User media uploads |
+-----------------------+ +-----------------------+-----------------------+
```

### 1.1 Storage Technology Responsibilities
*   **PostgreSQL**: System of record for transactional user identities, sessions, capability mappings, activity feeds, audit logs, and settings configurations. Chosen for strict ACID enforcement and foreign key constraints.
*   **MongoDB**: Document-based metadata engine hosting curriculum taxonomies (domains, subjects, modules, topics). Handles fast, hierarchical JSON schema validations.
*   **Redis**: In-memory data structures layer optimizing hot-path reads, rate limits, session caches, and WebSocket notifications queue tracking.
*   **Vector Database**: High-dimensional index store mapping curriculum notes into embeddings to resolve real-time RAG similarity queries.
*   **S3-Compatible Object Storage**: S3-compatible storage service (locally backed by RustFS) housing system backups, temporary exports, static files, and media.
*   **Managed Knowledge Storage**: Private bucket directory containing the raw proprietary Knowledge Assets, isolated from the public repository.

### 1.2 Universal Resource Abstraction (V1 Requirement)
To ensure trace-ability and consistent permission enforcement without excessive coupling, core system resources inherit parameters from a common Resource model:
*   **Resource Identity**: Assigned an immutable, prefix-based identifier (e.g. `res_01823a0f` where prefix indicates the domain: `usr_` for users, `sub_` for subjects, `doc_` for documents, `pkg_` for packages, `con_` for conversations).
*   **Resource Ownership**: Binds the resource to an owner ID or an organization token, defining administrative control.
*   **Resource Versioning**: Tracks state modifications via an incrementing integer `resource_version` incremented on every database transaction, independent of the Git code commit history.
*   **Resource Permissions**: Bound to capability scopes checked by the authorization middleware.
*   **Resource Lifecycle**: Tracks FSM states (`Draft`, `Review`, `Approved`, `Published`, `Archived`, `Deleted`).

---

## 2. PostgreSQL Engineering Design

PostgreSQL acts as the transactional storage engine. The database is organized into modular relational domains:

### 2.1 Domain Entity Specifications

#### 2.1.1 Authentication & Users (Current Verified Reality)
*   **Purpose**: Manages actor login credentials, registration times, and account status.
*   **Ownership**: Identity Domain
*   **Primary Key**: `user_id` (UUIDv4)
*   **Unique Constraints**: `email` (case-insensitive unique index)
*   **Indexes**: BTREE on `email`, hash index on `user_status`.
*   **Archival Strategy**: Suspended accounts remain online for 90 days. Archived accounts trigger soft-deletion, masking PII fields.
*   **Concurrency**: Optimistic locking via `version_id` (incrementing integer).

#### 2.1.2 Sessions & Refresh Tokens (V1 Requirement)
*   **Purpose**: Manages JWT lifecycle and refresh token rotation tokens.
*   **Ownership**: Identity Domain
*   **Primary Key**: `session_id` (UUIDv4)
*   **Foreign Keys**: `user_id` references `users.user_id` (ON DELETE CASCADE)
*   **Unique Constraints**: `refresh_token_hash` (unique)
*   **Indexes**: BTREE on `refresh_token_hash`, BTREE on `expires_at`.
*   **Archival Strategy**: Expired and revoked sessions are purged daily via cron processes.
*   **Concurrency**: Single-use token rotation forces immediate lock acquisition.

#### 2.1.3 Actor, Capability & Scope Model (V1 Requirement)
To prevent complex over-engineering during initial stages, Ascendrite avoids complex wildcard systems, adopting an explicit Actor-Role-Capability-Scope framework:
*   **Actor Types**:
    *   *Human Actors*: Learners, authors, moderators, and administrators.
    *   *AI Actors*: Scoped agents (tutors, validators, generators) running under programmatic contexts.
    *   *Organization Actors (V2 Future Concept)*: Business or educational groups mapped to shared capability rules. (Not implemented in v1).
*   **Role**: Groups permissions into identities (Guest, Learner, Moderator, Admin).
*   **Capability**: Individual capabilities (Read, Write, Review, Approve, Publish, Archive, Delete, Configure, Manage).
*   **Scope**: Path coordinates limiting a capability to a specific taxonomy level:
    $$\text{Platform} \longrightarrow \text{Domain} \longrightarrow \text{Subject} \longrightarrow \text{Module} \longrightarrow \text{Topic} \longrightarrow \text{Asset}$$
*   **Inheritance & Overrides**: Permissions propagate down the taxonomy. Higher-level allowances (e.g. `Read` at Subject level) apply to all children unless an explicit override or an **Explicit Deny** is set at a lower scope node (e.g., a specific topic). Explicit Deny overrides all allow grants.
*   **AI Restrictions**: AI agents are assigned scoped capabilities, blocking dangerous actions (such as publishing changes or changing permissions).
*   **Auditing**: Access grants and privilege evaluations are logged to `security_audit_logs`.

#### 2.1.4 Ownership Architecture (V1 Requirement)
Every resource maintains a clear ownership matrix defining administrative authority:
*   **Owner**: Full management rights (delegation, transfer, deletion).
*   **Maintainer**: Edit and revision review permissions.
*   **Reviewer**: Staging queue view and review logging capabilities.
*   **Approver**: Verification and sign-off privileges.
*   **Publisher**: Merge and production deployment permissions.
*   **Observer**: Read-only capability.
*   **Ownership Transfer**: Supports transferring ownership, which automatically regenerates target permission inheritance branches.
*   **Audit History**: Ownership updates write to `ownership_audit_logs`.

#### 2.1.5 Communication Data Model (V1-Ready / Deferred)
*   **Domain Definitions**:
    *   *Events*: Ephemeral backend messages tracking state changes. Never committed to conversation tables.
    *   *Notifications*: Persistent alert feeds. Stored in `notifications`.
    *   *Toasts*: Short-lived UI banners. Managed entirely on the client, never written to databases.
    *   *Messages*: Persistent direct or group chat logs. Stored in `messages`.
    *   *Announcements*: Broadcast logs. Stored in `announcements`.
*   **Database Tables**:
    *   `conversations`: Tracks conversation threads (`conversation_id` PK, unique participants list).
    *   `messages`: Tracks message payloads (`message_id` PK, `conversation_id` FK, author, text, timestamp).
    *   `attachments`: Tracks file attachment URLs (`attachment_id` PK, `message_id` FK, Object Storage S3 URL).
    *   `notification_preferences`: Stores user delivery channels (e.g., WebSocket, email).
    *   `notification_delivery`: Tracks notification states (Unread, Read, Archived).
    *   `broadcasts`: Tracks broad alerts issued to classrooms or organizations.

#### 2.1.6 Settings Data Model (V1 Requirement)
Settings configuration fields are grouped by responsibility domain. The database model supports dynamic schema additions to prevent schema locks when third-party integrations or features are added:
*   **Appearance**: Theme selections, dark/light modes, layout panel configurations.
*   **Accessibility**: High-contrast, screen reader formatting, font sizes, and reduced motion states.
*   **Privacy**: Visibility variables for profiles, metrics, and search crawling.
*   **Security**: Password logs, 2FA settings, session parameters, and trusted device lists.
*   **Communication**: Notification frequencies and direct message filter permissions.
*   **Extensibility**: Supported via a JSON schema field `plugin_settings` mapping configuration objects.

#### 2.1.7 Workspaces & Projects (V1 Requirement)
*   **Purpose**: Tracks user workspace panels, sync logs, and offline metrics.
*   **Ownership**: Workspace Domain
*   **Primary Key**: `workspace_id` (UUIDv4)
*   **Foreign Keys**: `owner_id` references `users.user_id`
*   **Indexes**: BTREE on `owner_id`, GIN index on `workspace_layout_json`.
*   **Concurrency**: Row-level locking (`SELECT FOR UPDATE`) during synchronization.

#### 2.1.8 Audit & Telemetry Log (Current Verified Reality)
*   **Purpose**: Stores security logs and telemetry metrics.
*   **Ownership**: Operations Domain
*   **Primary Key**: `log_id` (UUIDv4)
*   **Indexes**: GIN index on `payload_json`, BTREE on `created_at`.
*   **Archival Strategy**: Tables are partitioned monthly by `created_at`. Partitions older than 6 months are archived to read-only cold stores.

---

## 3. MongoDB Engineering Design

MongoDB operates as the document datastore, organizing the platform's metadata indexes and structural graph relations:

```
[Domain Document]
  └── [Discipline Reference]
        └── [Subject Document]
              ├── Theme configuration colors
              └── [Module Array]
                    └── [Topic Reference]
                          ├── Concept validation rules
                          └── [Asset Array]
```

### 3.1 Collection Schema Definitions (Current Verified Reality)

#### 3.1.1 `domain_taxonomy`
*   **Document Ownership**: Knowledge Domain
*   **Document Hierarchy**: Houses the structural classification of Domains and Disciplines.
*   **Reference Strategy**: Embedded subdocuments for static domains, referencing external Subject document IDs.
*   **Indexes**: Unique index on `domain_id` and compound index on `(category, classification_slug)`.
*   **Sharding Readiness**: Sharded by hash key on `domain_id`.

#### 3.1.2 `subjects`
*   **Document Ownership**: Knowledge Domain
*   **Document Hierarchy**: Contains metadata tags, estimated hours, category tags, and theme variables.
*   **Reference Strategy**: References parent Discipline ID, embeds Module sequence maps.
*   **Validation Expectations**: Enforces validation schemas matching the `subject.schema.json` specifications.
*   **Indexes**: Unique index on `subject_id`, text index on `display_name`.

#### 3.1.3 `topics`
*   **Document Ownership**: Knowledge Domain
*   **Document Hierarchy**: Contains topic objectives, difficulty tags, concept lists, and asset associations.
*   **Reference Strategy**: References parent Subject and Module IDs.
*   **Validation Expectations**: Conforms to `topic.schema.json` rules.
*   **Indexes**: Compound unique index on `(subject_id, topic_id)`.

#### 3.1.4 `knowledge_graph`
*   **Document Ownership**: Knowledge Domain
*   **Document Hierarchy**: Captures the relational semantic edges (prerequisites, recommended progression) between concepts.
*   **Validation Expectations**: Verified via Pytest scripts to confirm the graph forms a DAG.
*   **Indexes**: Unique index on `concept_id`, multi-key index on `prerequisites_array`.

---

## 4. Knowledge Storage & Versioning Design (V1 Requirement)

Knowledge educational notes, quizzes, and diagrams are stored securely outside public git version control. Versioning is managed independently by the Knowledge Service:
*   **`asset_version`**: An incrementing revision integer tracking content changes in database records (e.g. `asset_version: 12`).
*   **`schema_version`**: A SemVer string (e.g. `2.0.1`) tracking validation structure compatibility.
*   **`publication_version`**: A global deployment identifier indicating the active catalog build instance.
*   **`approval_history`**: A list of moderator signatures validating technical reviews.
*   **`checksum`**: A SHA-256 fingerprint generated during compilation.
*   **`rollback_reference`**: A unique Object Storage (RustFS) version token, allowing the service to roll back content instantaneously in case of errors.

---

## 5. Redis Cache Principles (Current Verified Reality)

**Redis is never the source of truth.** All data stored in Redis is transient. If Redis crashes, the platform can rebuild all cached records from PostgreSQL, MongoDB, or object storage databases:
*   **Database Ownership**: The database is the system of record. Writes must commit to PostgreSQL/MongoDB/Object Storage before the cache is updated.
*   **Cache Warming**: During application startup, a background initialization script runs, pre-loading global indexes, sitemaps, and sitemap settings into Redis.
*   **Cache Invalidation**: Event-driven pipelines invalidate caches. Mutations trigger a clean command on matching Redis keys (e.g., updating a topic notes file clears `knowledge:subject:{id}`).
*   **Expiration**: Caches utilize explicit TTL thresholds to prevent stale data.

---

## 6. Vector Storage Abstraction (V1 Requirement)

To prevent coupling retrieval pipelines to specific database engines, the AI subsystem communicates via a **Vector Repository Abstraction** interface:
*   **Abstraction Contract**: The interface defines methods: `upsert_embeddings()`, `query_similarity()`, and `delete_embeddings()`.
*   **Default pgvector Adapter**: The default adapter translates these requests into SQL operations using pgvector inside PostgreSQL.
*   **Future Adaptation (V2)**: Switching to a dedicated vector store (e.g. Milvus or Qdrant) requires writing a new adapter class conforming to the Vector Repository interface, leaving core AI services untouched.

---

## 7. Object Storage Design (Current Verified Reality)

Object storage is managed via standard S3 API interfaces (locally backed by **RustFS 1.0.0-beta.8**):

*   **`knowledge-assets` Bucket**:
    *   *Purpose*: Houses Knowledge Assets.
    *   *Lifecycle*: Infinite retention. Bucket versioning enabled.
    *   *Access*: Restricted to Knowledge Service credentials.
*   **`user-media` Bucket**:
    *   *Purpose*: Stores user avatar images and workspace attachments.
    *   *Retention*: Deleted 30 days after account archive events.
    *   *Access*: Public read access via pre-signed HTTP URLs.
*   **`system-backups` Bucket**:
    *   *Purpose*: Houses monthly database backups.
    *   *Retention*: Retained for 1 year, then auto-purged.
    *   *Access*: Private. Restricted to Admin S3 roles.

---

## 8. Cross-Database Relationship Model

To maintain modularity and avoid circular dependencies, data flows across storage technologies systematically:

```
[PostgreSQL: Users]
       │
       ▼
[PostgreSQL: Settings]
       │
       ▼
[PostgreSQL: Workspace]
       │
       ▼
[MongoDB: Curriculum Map] ──► [Redis: Cache Check]
       │
       ▼
[Object Storage: Knowledge Assets] ──► [Vector Repository Search]
```

*   **Rule 1**: PostgreSQL user accounts act as the anchor. All user settings, workspaces, and telemetry events refer to the Postgres `user_id`.
*   **Rule 2**: Progress trackers reference Subject and Topic IDs in MongoDB.
*   **Rule 3**: Concept IDs link MongoDB documents to corresponding Vector Repository indexes and Object Storage assets.

---

## 9. Data Lifecycle & Ingestion

### 9.1 General Lifecycle
Entities progress through a managed lifecycle:

$$\text{Draft} \longrightarrow \text{Review} \longrightarrow \text{Approved} \longrightarrow \text{Published} \longrightarrow \text{Archived} \longrightarrow \text{Deleted}$$

*   **Draft**: Asset content is edited or modified locally.
*   **Review**: Asset is submitted to moderation queues for validation.
*   **Approved**: Asset passes schema and technical checks.
*   **Published**: Asset is compiled and deployed to active user viewports.
*   **Archived**: Legacy asset is soft-deprecated, preserving IDs.
*   **Deleted**: Asset is completely removed, masking PII and purging files.

### 9.2 Knowledge Migration Pipeline
Knowledge educational assets follow a strict ingestion sequence to ensure integrity before publication:

```
[Knowledge Assets] (Draft notes, flashcards, etc.)
       │
       ▼
[Validation] (Checks JSON schemas and KaTeX syntax)
       │
       ▼
[Metadata Extraction] (Extracts concept tags and prerequisite IDs)
       │
       ▼
[Database Ingestion] (Writes metadata to MongoDB and assets to Object Storage)
       │
       ▼
[Embedding Generation] (Computes high-dimensional vectors)
       │
       ▼
[Indexing] (Upserts coordinates to Vector Repository)
       │
       ▼
[Publishing] (Sets asset status to Published, dispatches event)
       │
       ▼
[Cache Preparation] (Pre-loads active indexes to Redis cache)
```

During this migration pipeline, existing educational assets in the legacy folders remain fully preserved as migration candidates.

---

## 10. Data Versioning Strategy

To support platform scalability and prevent schema mismatch crashes:
*   **Schema Versioning**: API payloads and database tables track schema variations using Semantic Versioning (SemVer) tags in metadata.
*   **Content Versioning**: Knowledge Assets use independent content version numbers (`asset_version`) managed via the database and object storage buckets.
*   **Migration Isolation**: Migration scripts run sequentially. Databases must support dual-version reads during deployment windows (blue-green deployments).

---

## 11. Security Strategy

*   **Encryption at Rest**: Databases and S3 directories must use AES-256 encryption.
*   **Encryption in Transit**: TLS 1.3 is enforced on all network connections, including database drivers and internal cache queries.
*   **Least Privilege**: The Knowledge Service, API servers, and backup scripts are assigned scoped database users with access restricted to specific tables.
*   **Tamper Detection**: Database audit log records are signed cryptographically to prevent log modification.

---

## 12. Scalability Strategy

Local-first deployment remains the primary development strategy. Cloud infrastructure scaling options are treated as optional deployment optimizations:
*   **PostgreSQL Partitioning**: Audit and telemetry tables are partitioned by month.
*   **MongoDB Sharding**: The metadata database is sharded using `subject_id` as the shard key, ensuring course data scales horizontally.
*   **Optional Object Storage Edge Caching**: Web servers can cache large media assets on CDN edge nodes to reduce dynamic server traffic in distributed production clouds.

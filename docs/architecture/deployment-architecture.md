# Deployment Architecture

## Document Metadata
*   **Purpose**: Defines the platform deployment architecture, database provisionings, network topology, backup policies, and environment structures.
*   **Scope**: Governs local dev/testing infrastructure, self-hosted Linux production setups, database initialization, and backup strategies.
*   **Intended Audience**: DevOps engineers, system administrators, and security officers.
*   **Related Documents**:
    *   [System HLD](system-architecture-hld.md)
    *   [Storage Architecture](storage-architecture.md)
    *   [Database Schema](database-schema.md)
*   **Ownership**: Lead DevOps Architect & Head of Platform Engineering

---

## 1. Deployment Philosophy & Environment Separation

The platform utilizes a self-hosted, bare-metal or virtualized Linux instance strategy to minimize third-party provider dependencies and ensure absolute control over the data lifecycle.

The platform distinguishes three environment states:

### 1.1 Development Environment
*   **Current State**: Fully operational locally on Windows-based development setups.
*   **Configuration**: Runs development databases (MongoDB, PostgreSQL, Redis) and object storage (RustFS) bound to localhost (`127.0.0.1`) interfaces with debug logging enabled.

### 1.2 Testing Environment
*   **Current State**: Executed in automated pipelines using Pytest in-memory/isolated MongoDB database fixtures.
*   **Configuration**: Instantiated dynamically to run integration test suites before production deployments.

### 1.3 Production Environment
*   **Current State**: Intentionally deferred until official release deployment.
*   **Configuration**: Locked down behind private virtual networks with transport layer security (TLS) enforcement and automated backup cron tasks.

---

## 2. Infrastructure Topology & Linux Server Strategy

The target production infrastructure runs on a hardened Linux distribution (specifically Ubuntu Server LTS) configured as a single-node or clustered self-hosted system.

```
                  +-----------------------------------+
                  |          Public Internet          |
                  +-----------------------------------+
                                    |
                            HTTPS (Port 443)
                                    |
                                    v
                  +-----------------------------------+
                  |        Nginx Reverse Proxy        |
                  |     - SSL/TLS Termination         |
                  |     - Static Assets Web Server    |
                  +-----------------------------------+
                                    |
                  +-----------------+-----------------+
                  |  Internal Private Network Bridge  |
                  +-----------------+-----------------+
                                    |
            +-----------------------+-----------------------+
            |                       |                       |
            v                       v                       v
+-----------------------+ +-----------------------+ +-----------------------+
|  FastAPI App Server   | |  PostgreSQL Instance  | |   MongoDB Instance    |
| - Stateless API       | | - User accounts       | | - Progress & evidence |
| - Port 8000           | | - Port 5432           | | - Port 27017          |
+-----------------------+ +-----------------------+ +-----------------------+
            |                       |                       |
            +-----------+-----------+                       |
                        |                                   |
                        v                                   v
            +-----------------------+           +-----------------------+
            |    Redis Cache/DB     |           | RustFS Object Storage |
            | - Ephemeral state     |           | - Media & PDF files   |
            | - Port 6379           |           | - Port 9000           |
            +-----------------------+           +-----------------------+
```

### 2.1 Networking & Security Boundaries
*   **Internal Network Bridge**: All datastores and app runtimes bind exclusively to an internal private network adapter interface. They are unreachable directly from the public internet.
*   **Port Closures**: Public ingress is restricted strictly to TCP ports `80` (HTTP, redirected to HTTPS) and `443` (HTTPS) on the Nginx front-end. Administrative SSH access (port `22`) is restricted to specific VPN gateways.

---

## 3. Backend Services & Datastores

### 3.1 Nginx Reverse Proxy
*   **Role**: Handles public incoming connections, serves pre-built static client assets, routes `/api/v1/*` requests to the app server, and enforces rate-limiting configurations.
*   **HTTPS and Certificates**: Manages SSL handshake termination using Let's Encrypt certificates managed automatically via Certbot.
*   **Rate Limiting**: Enforces server-side rate limits using a leaky bucket algorithm on incoming `/api/v1/auth/` connections to prevent brute-force exploitation.

### 3.2 FastAPI Application Server
*   **Role**: Executes stateless Python service logic. It runs locally on port `8000` via Uvicorn process workers, scaling horizontally behind the Nginx load balancer.

### 3.3 PostgreSQL Database
*   **Role**: Stores structured core identity records, active user sessions, and permission schemas.
*   **Constraints**: Enforces foreign key constraints and transactional consistency across authentication entities.

### 3.4 MongoDB Database
*   **Role**: Persists educational knowledge metadata, student progress attempts evidence logs, creator workspace drafts, and collaboration timeline streams.
*   **Indexing**: Indexes are compiled automatically during repository startup calls to optimize read queries.

### 3.5 Redis Cache
*   **Role**: Provides low-latency volatile storage for session lock tokens, security lockouts, and compiled taxonomy maps.

### 3.6 RustFS Object Storage
*   **Role**: Implements S3-compatible file storage on port `9000` for hosting curriculum PDFs, user assets, and system backup archives.

### 3.7 Centralized Telemetry & Log Rotation
*   **Role**: Application and infrastructure server logs are forwarded to systemd journald log streams. A native logrotate job runs nightly to compress and archive application log files, keeping disk usage bounded.

---

## 4. Initialization & Migration Strategy

Database initialization and upgrades are handled as dedicated deployment tasks to prevent database corruption during application updates.

### 4.1 Database Provisioning
*   During initial deployment, a bootstrap utility creates system schemas, seeds default admin roles, and establishes configuration scopes.
*   Application runtime services automatically verify database connectivity and confirm the presence of required indices on startup.

### 4.2 Database Migrations
*   **Relational Migrations**: Schema alterations in PostgreSQL are managed using Alembic migration scripts.
*   **Document Migrations**: Structural changes in MongoDB are handled dynamically through model version flags in the application code, avoiding long-running database lockups.

---

## 5. Storage, Backups & Recovery Strategy

### 5.1 Persistent Storage Volumes
Production state directories are mounted to dedicated persistent block storage volumes to protect data against instance failures.

### 5.2 Backup Schedule & Rotation
A daily cron utility automates backup creation, storing encrypted archives in the `system-backups` RustFS object bucket:
*   **MongoDB & Postgres**: Complete database dumps are generated nightly, retaining a rolling history of 30 days.
*   **Object Storage**: S3 bucket data is replicated daily to a secondary off-site backup directory.

### 5.3 Recovery Strategy
Disaster recovery procedures verify database restoration procedures monthly using automated staging server rebuild pipelines.

---

## 6. Future Scalability Considerations

*   **Stateless Scaling**: FastAPI app processes can be deployed across multiple physical nodes with Nginx acting as the central load balancer.
*   **Database Clustering**: MongoDB replica sets and PostgreSQL master-replica read pools can be configured dynamically when request volume matches database thread capacities, with zero modifications required for the underlying repository layer.

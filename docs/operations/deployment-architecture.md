# Deployment Architecture

## Document Metadata
*   **Purpose**: Outlines containerization specifications, deployment target environments, and release pipeline patterns.
*   **Scope**: Governs container builds, deployment environments, and infrastructure management pipelines.
*   **Intended Audience**: DevOps specialists, operations leads, and software engineers.
*   **Related Documents**:
    *   [Security Standards](security-standards.md)
    *   [Version Roadmap](../governance/version-roadmap.md)
*   **Ownership**: Lead DevOps Engineer & Site Reliability Operations Lead

---

## 1. Containerization Specifications

All platform service instances are packed and executed inside isolated container environments:
*   **Base Images**: Services must run on minimal, officially verified base images to limit vulnerability footprints.
*   **Layer Optimization**: Dockerfiles must utilize multi-stage build patterns to isolate compilation libraries from runtime images.
*   **Security Restrictions**: Containers must execute processes as non-root users, utilizing system profiles with limited privileges.

---

## 2. Target Environments & Deployment Roadmap

Ascendrite defines an evolutionary deployment sequence, moving from local environments to containerized self-hosted VM setups:

$$\text{Local Development} \longrightarrow \text{Containerized Local Development} \longrightarrow \text{Self-hosted Production (VM)} \longrightarrow \text{Cloud-hosted Production (VM)} \longrightarrow \text{Container Orchestration (when justified)}$$

*   **Development (Local)**: Local developer machines running native Windows/Unix services. Emulates credentials using `.env.local` and database collections via local runtimes.
*   **Containerized Local Stack**: Docker Compose environment replicating all backend, database, cache, and frontend services for integration tests.
*   **Staging**: Run on a dedicated self-hosted staging VM mirroring the production topology to verify database schema migrations and run integration validation checks.
*   **Production**: The active, user-facing production environment deployed on secure virtual machine instances running production databases.

> [!IMPORTANT]
> **Environment Isolation & Synchronization Rules**:
> Development and Production operate as fully isolated environments. There is no automatic synchronization of database records, curriculum metadata, or schemas. Knowledge moves between local development and production environments exclusively via explicit export and import operations orchestrated through the Migration Toolkit.

---

## 3. Self-Hosted Production Stack & Backup Philosophy

The target production infrastructure is built on a resilient, self-hosted container framework:

*   **Host Operating System**: Ubuntu Server LTS.
*   **Container Platform**: Docker Engine with Docker Compose to coordinate service structures.
*   **Reverse Proxy / SSL**: Caddy Reverse Proxy, providing automated TLS 1.3 termination and secure routing to frontend/backend containers.
*   **Storage Volumes**: Docker persistent named data volumes mapped to databases (PostgreSQL, MongoDB) and RustFS object stores.
*   **Backup and Archival Philosophy**:
    *   *Runtime Backups*: Cron-based periodic encrypted database snapshots and raw logs are written to the persistent runtime storage folder `ascendrite-data/backups/`.
    *   *Historical Archiving*: High-fidelity versioned knowledge exports are generated from MongoDB and written to `ascendrite-data/knowledge-base/`, while master snapshots and certifications are preserved separately in `ascendrite-private/snapshots/`. Runtime backups and historical snapshots serve different operational recovery purposes.
*   **Telemetry & Monitoring**: Prometheus and log scrapers checking ports health and API throughput latencies.
*   **Security Layers**: Host firewalls (UFW), SSH key logins, IP tables rate-limiting, and constant-time API key comparisons.

---

## 4. Release Sequencing

Deployment actions are managed through automated CI/CD systems, following a defined execution sequence:
*   A push to release branches triggers compilation, testing, and container compilation.
*   Automated lint, security scan, and test scripts must complete successfully before release artifacts are pushed to registries.
*   Staging deployments are triggered automatically upon test completion.
*   Production releases require administrator confirmation following successful staging validation.

---

## 5. Rollback Protocols

In the event of a deployment failure:
*   Deployment pipelines must support automated, zero-downtime rollback to the previous version registry image.
*   Database schema migrations must be written with corresponding down scripts to reverse structural changes cleanly.

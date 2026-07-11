# Version Roadmap

## Document Metadata
*   **Purpose**: Details the multi-phase technical roadmaps, target tech changes, and infrastructure transitions.
*   **Scope**: Governs future sprint planning, architecture targets, and deployment upgrades.
*   **Intended Audience**: All software engineers, DevOps leads, and operations coordinators.
*   **Related Documents**:
    *   [Project Vision](project-vision.md)
    *   [Product Evolution Strategy](product-evolution-strategy.md)
*   **Ownership**: Principal Software Architect & Operations Coordinator

---

## 1. Phase 1: Local Infrastructure Setup (Current Verified Reality)
*   **Focus**: Configure and validate the native Windows services environment on the developer machine to minimize virtualization overhead and enable local-first compilation.
*   **Configured Engines**:
    *   **PostgreSQL 18.4** (Port 5432) for transactional and identity storage.
    *   **MongoDB Community Server 8.0.26** (Port 27017) for dynamic curriculum indexes.
    *   **Memurai Developer Edition 4.2.3** (Redis API 7.4.9, Port 6379) for caching and rate limiting.
    *   **RustFS 1.0.0-beta.8** (S3 API Port 9000, Console Port 9001) for object storage.
*   **Deliverables**: Baseline validation scripts, S3 credential rotations, local batch launchers, and directory layout definitions completed.

---

## 2. Phase 2: V1 Core Backend & Client Implementation (Direct Requirement)
*   **Focus**: Construct the FastAPI backend service code and React single-page frontend application under the `platform/` namespace.
*   **Deliverables**:
    *   *Backend*: Implement Clean Architecture package layers (`domain`, `service`, `repository`, `infrastructure`), write opaque cookie-session validation middlewares, and define the generic Vector Repository abstraction.
    *   *Frontend*: Build the workspace-first panel layouts, mount the contextual right panels, and integrate the dynamic CSS theme engine.
    *   *Ingestion*: Complete metadata linting rules and load subjects into MongoDB database instances.

---

## 3. Phase 3: Client Migration & High-Performance Rendering (V2 Evolution)
*   **Target Stack**: Next.js App Router App, Cloud Managed Services (MongoDB Atlas, AWS RDS).
*   **Focus**: Migrate the React frontend client to Next.js to leverage server-side rendering (SSR) and static site generation (SSG) for public subject curriculum views. Reconcile database drivers to connect to secure cloud database instances during deployment staging.
*   **Deliverables**: Next.js route codes splitting, global edge CDN distribution setups for static schemas, and migration scripts to sync S3 objects to public cloud buckets.

---

## 4. Phase 4: Enterprise Scale, Queueing & Containerization (Long-Term Possibilities)
*   **Target Stack**: Docker, Kubernetes (container orchestration), RabbitMQ (message broker).
*   **Focus**: Scale the stateless API services horizontally using container pods. Introduce an asynchronous message broker to coordinate logging telemetry, spaced repetition calculations, and notifications dispatches.
*   **Deliverables**: Create standard Dockerfiles, build Kubernetes deployment manifests, and write RabbitMQ consumer workers.

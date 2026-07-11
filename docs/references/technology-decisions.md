# Technology Decisions

## Document Metadata
*   **Purpose**: Records system framework choices, tooling validations, and future database migrations paths.
*   **Scope**: Governs all language selections, database software, and deployment tools.
*   **Intended Audience**: Core software developers, DevOps leads, and integration architects.
*   **Related Documents**:
    *   [System Architecture (HLD)](../architecture/system-architecture-hld.md)
    *   [Version Roadmap](../governance/version-roadmap.md)
*   **Ownership**: Principal Software Architect & Head of Platform Engineering

---

## 1. Selected Stack & Justification

The core platform technology stack is locked for Version One to ensure rapid iteration and baseline reliability:

*   **API Framework (FastAPI)**: Selected for its asynchronous capabilities, native Pydantic schema validation, automatic OpenAPI generation, and performant request lifecycle handling.
*   **User Interface (ReactJS)**: Chosen for its responsive component lifecycle, component reuse standards, and extensive ecosystem supporting animated, interactive data structures.
*   **Primary Database (MongoDB Atlas)**: Selected due to its natural alignment with dynamic, hierarchical JSON metadata representing syllabus structures and state objects.
*   **Cache Tier (Redis)**: Implemented for session state storage, database rate-limiting locks, and configuration overrides caching.

---

## 2. Infrastructure & Operations Stack

*   **Containerization (Docker)**: Deployed to standardize packaging across local workspaces and staging clusters.
*   **Telemetry (Prometheus & Log Collectors)**: Used to gather performance metrics, trace API latencies, and output structured operational events.
*   **Vector Search Engine**: Integrated to index and rank concept coordinates for RAG retrieval logic.
*   **Object Storage (S3-compatible API)**: Implemented (locally backed by RustFS) to handle large binary files, diagrams, and static assets, keeping the main database query paths lightweight.

---

## 3. Hybrid Storage & Database Evolution Path

To ensure absolute storage independence and accommodate scaling limits, the database architecture follows a hybrid design model managed by the **Knowledge Service**:

*   **Metadata & Relationships**: Stored in MongoDB to support dynamic, multi-layered document indexing and graph relations validation.
*   **Proprietary Educational Assets**: Reside in a private **Managed Knowledge Storage** bucket, keeping intellectual property separated from the public code repository.
*   **Binary & Large Assets**: Delegated to S3-compatible (locally backed by RustFS) object stores to keep the transactional databases clean of raw data sizes.
*   **High-Dimensional Vector Embeddings**: Stored in a vector database to power prompt retrieval in RAG workflows.
*   **Search & Caching**: Search queries are routed through the Knowledge Service, caching frequent hits in Redis to minimize backend reads.

### Future Transitions
*   **Database Transition**: In later horizons, the relational metadata layer will migrate to PostgreSQL to enforce schema validation at the database layer.
*   **Frontend Evolution**: Move to Next.js (utilizing Server Components) to improve page load times and search indexing capabilities.
*   **Service Extraction**: Transition the modular API monolith into independent microservices container clusters coordinated via Message Queues.

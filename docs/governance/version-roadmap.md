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

## 1. Phase 1: Metadata Foundation & Validation (Current)
*   **Focus**: Establish a standardized metadata mapping system (Platform Structure, Taxonomy tree, Knowledge Graph, and Curriculum Map) and decouple it from codebase routes.
*   **Deliverables**: Created validation schemas (JSON Schema Draft 2020-12) and cross-repository verification scripts.

---

## 2. Phase 2: Client Migration & High-Performance Rendering
*   **Target Stack**: React/Vite migration to Next.js framework.
*   **Focus**: Migrate the React frontend to Next.js to support server-side rendering (SSR) and static site generation (SSG) for public subject curriculum paths. This improves initial load performance and SEO indexes.
*   **Deliverables**: Restructure page routing using the Next.js App Router, implement layout caching, and optimize client hydration weights.

---

## 3. Phase 3: Relational Persistence & State Cache Layers
*   **Target Stack**: PostgreSQL (relational database), Redis (in-memory database).
*   **Focus**: Supplement or migrate Beanie/MongoDB progress stores to a PostgreSQL schema to enforce relational integrity constraint checks on multi-course logs. Integrate Redis as a caching layer to accelerate auth token lookups and in-memory syllabus indexes.
*   **Deliverables**: Design SQL relational schemas, configure migration run loops, and implement Redis cache-invalidation adapters.

---

## 4. Phase 4: Enterprise Scale, Queueing & Containerization
*   **Target Stack**: Docker, Kubernetes (container orchestration), RabbitMQ (message broker).
*   **Focus**: Scale the platform to support concurrent users. Standardize system configurations into Docker containers, deploy Kubernetes pods for elastic service scalability, and introduce RabbitMQ to handle asynchronous processing tasks (such as telemetry aggregation or email dispatches).
*   **Deliverables**: Create Helm charts, construct Kubernetes deployment files, and configure RabbitMQ exchange queues.

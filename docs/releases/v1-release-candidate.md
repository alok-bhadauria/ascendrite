# V1 Release Candidate Specification

This document details the V1 Release Candidate architecture, completed platforms integrations, security standards, and local development configurations for Ascendrite.

---

## 1. Permanent vs. Release Documentation Scope

To maintain modularity and clarity, Ascendrite keeps permanent technical designs separated from active release-specific states:

*   **Permanent Documentation (`docs/architecture/` & `docs/governance/`)**: Holds immutable design principles, editorial guidelines, styling configurations, HSL color tokens, and structural system boundary definitions.
*   **V1 Release Documentation (This document & `docs/releases/`)**: Summarizes the specific features, database models, testing matrices, and operational limitations active in the V1 candidate. Future V2 concepts are excluded from V1 release scopes.

---

## 2. V1 Release Scope & Achievements

*   **Integrated Client ↔ Server Monolith**: All views in the React SPA communicate directly with active Python FastAPI endpoint routers via Axios, syncing states dynamically instead of using client mock array fallbacks.
*   **Decentralized Datastore Ready**: PostgreSQL is configured as the relational transaction storage engine for identity management. MongoDB operates as the curriculum schema document store. Redis manages active caches and telemetry logging events.
*   **Interactive Visualizer Demo**: Textbook-rigorous learning loops featuring play/pause/step code traces (e.g. bubble sort algorithms) side-by-side with mathematical LaTeX proofs.
*   **Dynamic Learning Journeys**: Dynamic category explorers retrieving modules, estimated hours, and topic progression maps with state-persistent bookmark notes.
*   **Active Authoring Workspace**: Creator dashboards supporting draft creation, debounced auto-saving (via PUT), schema validations, and publication approval pipelines.
*   **Collaboration & Discussions**: Threaded discussion boards on topic read channels backing post/retrieve comments via dynamic endpoints.
*   **System Governance (Admin OS)**: Control panel managing maintenance toggles, telemetry telemetry logging, and metadata curation statistics.

---

## 3. Active Architecture State & Local Services

The V1 system is engineered for local VM self-hosting (no cloud SaaS dependencies):
*   **PostgreSQL 18.4** (Port `5432`): Houses transactional user data, credentials identities, refresh tokens, settings configurations, and comments.
*   **MongoDB Community Server 8.0.26** (Port `27017`): Houses curriculum taxonomy subjects, syllabuses, modules, topics, and markdown notes.
*   **Memurai / Redis** (Port `6379`): Manages local token caches, session caching, and diagnostic telemetry logging.
*   **RustFS 1.0.0-beta.8** (Port `9000`): Local S3 emulation storage housing document pdfs and media assets.

---

## 4. Release Validation & Integrity Metrics

The V1 release candidate has been audited using static and dynamic checkers:
*   **Backend Pytest Suite**: `PASS` (38 test assertions completed with 100% success rate).
*   **Client SPA Bundle Compilation**: `PASS` (Vite build compiles optimized static chunks in 299ms).
*   **Linter Rules Quality**: `PASS` (ESLint checks return zero errors and warnings).
*   **Relational Schema Verification**: Checked and created PostgreSQL schemas matching [init_postgres.sql](file:///g:/Projects/ascendrite/scripts/init_postgres.sql).
*   **Curriculum Catalog Verification**: Validated and ingested syllabus maps for disciplines (`ai`, `core-cs`, `software-engineering`, `web-development`).

---

## 5. V1 Known Limitations & Postponed Ideas

1.  **Local-First Authentication**: Google OAuth SSO parameters are supported in schema configs but fall back to secure local credentials registries for VM deployments.
2.  **No Advanced AI Automation**: AI tutoring systems, LLM copilot agents, and advanced intelligence layers are deferred to V2 stages to protect architectural simplicity and self-hosted boundaries.
3.  **Local Backup Schedule**: Nightly database dump logs are currently triggered manually or via cron. Automatic daemon background backups will deploy in VM stages.


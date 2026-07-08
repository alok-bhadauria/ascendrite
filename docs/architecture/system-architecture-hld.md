# High-Level Design (HLD): Software Architecture and Scalability Planning

## Document Metadata
*   **Purpose**: Details the high-level system components, client interaction models, actor structures, and scalability blueprints.
*   **Scope**: Governs overall frontend presentation configurations, backend API services, and infrastructure deployments.
*   **Intended Audience**: All platform developers, systems engineers, and DevOps specialists.
*   **Related Documents**:
    *   [Project Vision](../governance/project-vision.md)
    *   [Platform Philosophy](../governance/platform-philosophy.md)
    *   [Engineering Principles](../governance/engineering-principles.md)
*   **Ownership**: Principal Software Architect & Head of Platform Engineering

---

## 1. High-Level Architecture Overview
The platform shall be built using a highly decoupled multi-tier architecture to isolate concerns. The core design splits presentation logic, API coordination, and database storage to ensure each layer scales independently.

```
+-------------------------------------------------------------+
|                     User Browser / Client                   |
|  - ReactJS Single Page Application (SPA)                    |
|  - Dynamic Workspace-first visualizers & components         |
+-------------------------------------------------------------+
                              |
                     REST API Calls (HTTPS)
                              |
                              v
+-------------------------------------------------------------+
|                      API Gateway / Reverse Proxy            |
|  - SSL termination, load balancing, rate limiting           |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|                      FastAPI App Servers                    |
|  - Stateless execution instances                            |
|  - In-memory curriculum cache (ingested metadata indices)    |
+-------------------------------------------------------------+
                |                              |
         Database Queries                 Local Disk Reads
                |                              |
                v                              v
+------------------------------+ +----------------------------+
|         Data Store           | |  JSON Knowledge Base Files |
|  - Users, progress, quizzes  | |  - Notes, revision, etc.   |
+------------------------------+ +----------------------------+
```

---

## 2. Platform Interaction & Presentation Architecture

### 2.1 Workspace-First Layout
The client application must render as a single-page interactive workspace, avoiding traditional multi-page navigation styles. The interface shall consist of three primary zones:
*   **Navigation Shell (Left)**: Renders the active category and subject curriculum index dynamically from metadata maps.
*   **Interactive Workspace Canvas (Center)**: Renders LaTeX mathematics, rich text, and interactive coding canvases.
*   **Contextual Panel (Right)**: Renders secondary contextual widgets, including persistent AI assistants, math derivations, execution traces, or vocabulary glossaries without taking focus off the main content block.

### 2.2 Living Platform Composition
The frontend shall utilize component composition rather than static page composition. Persistent components (such as global state adapters, active code execution containers, and the persistent AI assistant) must remain mounted across navigation transitions. State shall survive panel folds or topic switching to ensure zero friction for the user.

### 2.3 Progressive Enhancement & Graceful Degradation
*   **Progressive Enhancement**: When browser runtime supports advanced features (such as hardware-accelerated WebGL or WebGPU contexts), client components should render dynamic 3D concept topologies and transitions.
*   **Graceful Degradation**: If specific layout visualizers (like Mermaid.js scripts) or database connections fail:
    *   The platform must catch exceptions locally.
    *   It shall degrade gracefully to standard SVG fallbacks or static text representations.
    *   It must not crash the surrounding page container or lock the reader viewport.

---

## 3. Core Actor & Permissions Architecture
The system shall enforce Role-Based Access Control (RBAC) across four baseline actors, while maintaining schema flexibility to support future organizational actor extensions.

### 3.1 Version 1 Core Actors
*   **Guest**: Unauthenticated users. Permitted to read public subject metadata indexes and check health indicators.
*   **Learner**: Authenticated users. Permitted to query detailed notes, submit code solutions, track study time, and record quiz results.
*   **Moderator**: Authenticated administrative users. Permitted to review submitted practice tests, edit course metadata drafts, and modify content flags.
*   **Admin**: Platform owners. Full read and write privileges over all routing networks, database tables, and autonomous AI system settings.

### 3.2 Reserved Future Actors
To support enterprise scalability, the database schema design and middleware code must reserve and accommodate:
*   **Recruiter**: Permitted to view authorized student achievement portfolios and verified code evaluations.
*   **Organization**: Permitted to manage custom subject mapping tracks and group access tokens.
*   **Organization Member**: Learners operating under corporate boundaries.

---

## 4. Scalability & Deployment Architecture

### 4.1 Stateless App Scale
The API application instances must remain completely stateless. They shall maintain no local user session states. Session storage is handled via signed JWT cookies, and state tracking is managed by the datastore. This ensures servers can scale horizontally behind load balancers.

### 4.2 Edge Distribution
Static JSON files (curriculum maps, notes, templates) should be cached on Content Delivery Networks (CDNs) at the network edge, minimizing API request loads to dynamic operations.

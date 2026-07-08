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

The platform uses a highly decoupled multi-tier architecture to isolate concerns. The Platform communicates exclusively with the **Knowledge Service**, which abstracts all file storage layouts and physical data pools.

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
|                      FastAPI App Servers (Platform)         |
|  - Stateless execution instances                            |
|  - In-memory metadata indexes                               |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|                      Knowledge Service                      |
|  - Retrieval, validation, versioning, indexing, caching     |
|  - Authorization check gates & audit logging                |
+-------------------------------------------------------------+
                 |                              |
         Database Queries                 Storage Requests
                 |                              |
                 v                              v
+------------------------------+ +----------------------------+
|         Data Store           | |     Knowledge Storage      |
|  - Users, progress, logs     | |  - Private Knowledge Assets |
|  - Metadata & Relationships  | |  - Notes, quizzes, code    |
+------------------------------+ +----------------------------+
```

---

## 2. Platform Interaction & Presentation Architecture

### 2.1 Workspace-First Layout
The client application renders as a single-page interactive workspace, avoiding traditional multi-page navigation styles. The interface consists of three primary zones:
*   **Navigation Shell (Left)**: Renders the active category and subject curriculum index dynamically from metadata maps.
*   **Interactive Workspace Canvas (Center)**: Renders LaTeX mathematics, rich text, and interactive coding canvases.
*   **Contextual Panel (Right)**: Renders secondary contextual widgets, including persistent AI assistants, math derivations, execution traces, or vocabulary glossaries without taking focus off the main content block.

### 2.2 Living Platform Composition
The frontend utilizes component composition rather than static page composition. Persistent components (such as global state adapters, active code execution containers, and the persistent AI assistant) remain mounted across navigation transitions. State survives panel folds or topic switching to ensure zero friction for the user.

### 2.3 Progressive Enhancement & Graceful Degradation
*   **Progressive Enhancement**: When browser runtime supports advanced features (such as hardware-accelerated WebGL or WebGPU contexts), client components render dynamic 3D concept topologies and transitions.
*   **Graceful Degradation**: If specific layout visualizers (like Mermaid.js scripts) or database connections fail:
    *   The platform catches exceptions locally.
    *   It degrades gracefully to standard SVG fallbacks or static text representations.
    *   It does not crash the surrounding page container or lock the reader viewport.

---

## 3. Core Permissions & Ownership Architecture

Ascendrite uses a capability-based, permission-driven access control model. While roles exist as organizational identities, individual capabilities determine specific system actions.

### 3.1 Permission Classifications
Capabilities are assigned independently and include:
*   `Read`: Access to view notes, examples, and metadata indexes.
*   `Write`: Access to draft and update workspace files and Knowledge Assets.
*   `Review`: Ability to evaluate proposed changes in the moderation queues.
*   `Approve`: Authority to sign off on technical reviews and curriculum changes.
*   `Publish`: Permission to merge drafts to master and rebuild global metadata maps.
*   `Archive`: Ability to soft-deprecate legacy assets, preserving IDs.
*   `Delete`: Permanent removal rights of system components.
*   `Configure`: Access to alter system environment flags and configuration parameters.
*   `Manage`: Full administrative capabilities over users, permissions, and audit logs.

### 3.2 Permission Inheritance Flow
Permissions inherit downward through the taxonomy hierarchy unless explicitly overridden at a lower node:

$$\text{Platform} \longrightarrow \text{Domain} \longrightarrow \text{Subject} \longrightarrow \text{Module} \longrightarrow \text{Topic} \longrightarrow \text{Asset}$$

*   Granting a permission (e.g., `Review`) at the **Subject** level automatically grants that permission for all modules, topics, and assets within that subject.
*   Explicit overrides at lower levels (e.g., a specific **Topic**) can restrict or expand access for targeted actors.

### 3.3 AI Agent Scoping
Autonomous AI systems and agents are treated as actors under this matrix. They are never granted unrestricted system roles. Instead, they receive scoped permissions matching their specific operational utility (e.g., the Learning Agent receives read-only access to concepts and write-only access to progress logs).

### 3.4 Administrative Operations
The administrative control plane is capability-based:
*   **Delegation**: Administrators can delegate subject or module ownership to moderators.
*   **Auditing**: Every permission check, assignment, and revocation is recorded securely in the system audit log.
*   **Transfer**: Ownership of subjects or domains can be transferred cleanly between actors, automatically updating the inheritance pathways.

---

## 4. Scalability & Deployment Architecture

### 4.1 Stateless App Scale
The API application instances must remain completely stateless. They maintain no local user session states. Session storage is handled via signed JWT cookies, and state tracking is managed by the datastore. This ensures servers can scale horizontally behind load balancers.

### 4.2 Edge Distribution
Local-first deployment remains the primary development strategy. In distributed environments, static JSON infrastructure (schemas, templates, public taxonomy indexes) can optionally be cached on Content Delivery Networks (CDNs) at the network edge as a deployment optimization to minimize request loads.

---

## 5. Public Platform Features

To ensure discoverability while protecting user assets and private knowledge files, the platform implements dedicated public endpoints:

### 5.1 Public Search
*   **Global Availability**: Guests can run text searches across public subject lists and the global curriculum index.
*   **Indexing Strategy**: Public indexes are compiled during main branch publication builds and stored in Elastic/Meilisearch.
*   **Permission-Aware Results**: The search service checks user capabilities at request time. Knowledge Assets, student profiles, and internal discussions are filtered out of guest results automatically.

### 5.2 SEO Architecture
*   **Dynamic Metadata**: Public marketing pages and catalog views inject dynamic meta tags (title, description, Open Graph variables) using serverside template parsing.
*   **Engine Crawling**: A static `robots.txt` governs crawler paths. Private routes (e.g., `/workspace`, `/admin`, `/api/v1/auth`) are blocked from search engine indexing.
*   **Sitemap Generation**: The build system compiles a daily, automated `sitemap.xml` mapping active public subjects and topic categories.
*   **Optimization**: Public catalog landing views are optimized for speed, leveraging server-side rendering (SSR) to ensure maximum indexing indexing scores.


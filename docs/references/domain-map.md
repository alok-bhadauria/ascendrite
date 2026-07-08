# Domain Map

## Document Metadata
*   **Purpose**: Outlines the system boundaries, module dependencies, and inter-domain interfaces.
*   **Scope**: Governs backend packages and logical domain communications.
*   **Intended Audience**: All platform engineers, system designers, and code reviewers.
*   **Related Documents**:
    *   [System Architecture (HLD)](../architecture/system-architecture-hld.md)
    *   [Repository Structure](../development/repository-structure.md)
*   **Ownership**: Principal Platform Architect & Head of Platform Engineering

---

## 1. Domain Directory Mapping

To prevent architectural drift and dependency leaks, components are organized under seven core business domains:

*   **Identity Domain**: Manages credentials, sessions, and role permissions.
*   **Knowledge Domain**: Houses the course syllabus graph structures and content metadata indices.
*   **Practice Domain**: Governs study assessments, code execution tools, and progress evaluations.
*   **Workspace Domain**: Handles state preservation for personal user work zones, files, and tools.
*   **Intelligence Domain**: Contains agent configurations, RAG retrieval services, and orchestrations.
*   **Platform Domain**: Coordinates core notifications, indexing registries, and UI visual theme metadata.
*   **Operations Domain**: Aggregates application metrics, telemetry exports, and data audits.

---

## 2. Dependency Hierarchy

Domains are isolated and must interact only using defined interface protocols:
```
[Identity] ──────► [Workspace] ◄────── [Platform (Themes, Search)]
     │                  │                      ▲
     ▼                  ▼                      │
[Knowledge] ◄──── [Practice] ◄─────────────────┘
     ▲                  ▲
     │                  │
     └───── [Intelligence (RAG)]
```

---

## 3. Communication Standards

Inter-domain communication must strictly adhere to the modular monolith guidelines:
*   **Synchronous Checks**: Executed using clean service API classes.
*   **Asynchronous Tasks**: Triggered by dispatching events over the internal event bus.
*   **Direct Access Blocked**: Modules of one domain (e.g., identity) must never import internal services or direct database collectors of another domain (e.g., workspace).

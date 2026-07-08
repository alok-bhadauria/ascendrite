# Organizational Structure

## Document Metadata
*   **Purpose**: Outlines the division of responsibilities, team ownership boundaries, and operational scopes.
*   **Scope**: Governs internal team collaboration, pull request review scopes, and repository file ownership.
*   **Intended Audience**: All active contributors, coordinators, and engineering managers.
*   **Related Documents**:
    *   [Project Vision](project-vision.md)
    *   [Engineering Decision Process](engineering-decision-process.md)
*   **Ownership**: Engineering Governance Lead & Operations Coordinator

---

## 1. Ownership Divisions
The Ascendrite repository is divided into specific structural domains. Each domain is owned exclusively by its corresponding engineering division to maintain modularity and prevent logic leaks:

```
                  [Governance / Operations / DX]
                                 |
         +-----------------------+-----------------------+
         |                       |                       |
  [Editorial & KB]       [Platform & Dev]         [AI Systems]
  - curriculum-map.json  - client code            - vector store
  - domain-taxonomy.json - server code            - agent prompts
```

---

## 2. Engineering Departments and Responsibilities

### 2.1 Knowledge Engineering & Editorial Division
*   **Ownership**: `knowledge-base/` directories (excluding schema files).
*   **Responsibilities**: Designing subject curriculum trees, writing educational notes, formatting LaTeX equations, and organizing syllabus layouts.

### 2.2 Platform Engineering
*   **Ownership**: `platform/` directories (client, server).
*   **Responsibilities**: Designing API routing contracts, rendering UI modules, optimization database queries, and implementing dynamic themes.

### 2.3 AI Engineering
*   **Ownership**: AI agent configurations, prompt directories, and semantic vector models.
*   **Responsibilities**: Scaling learning assistant systems, fine-tuning retrieval prompts, and managing conceptual graph routing.

### 2.4 Developer Experience (DX)
*   **Ownership**: `scratch/` validation scripts, schema definitions, and automation hooks.
*   **Responsibilities**: Providing fast verification runtimes, managing local linters, and updating sandbox tools.

### 2.5 Security, Operations & QA
*   **Ownership**: Security rules, network policies, deployment maps, and test suites.
*   **Responsibilities**: Ensuring JWT cookie safety, whitelisting IP endpoints, verifying test cases, and monitoring production builds.

# Actor Capability Matrix

## Document Metadata
*   **Purpose**: Outlines platform roles, permission hierarchies, and actor authorization boundaries.
*   **Scope**: Governs backend authorization checks, middleware permission validations, and client view access control.
*   **Intended Audience**: Software developers, security engineers, and database coordinators.
*   **Related Documents**:
    *   [Security Standards](../operations/security-standards.md)
    *   [Domain Map](domain-map.md)
*   **Ownership**: Principal Security Architect & Head of Identity Engineering

---

## 1. Permission-Driven Access Model

Ascendrite uses a capability-based, permission-driven access model. Under this architecture:
*   **Permissions Define Capabilities**: Roles serve only as organizational group identities. Middleware checks enforce individual, discrete permissions.
*   **Independent Assignment**: Permissions (e.g., `Review`, `Publish`) are assigned independently to actors.
*   **Fine-Grained Scopes**: Permissions apply to specific paths or resources rather than acting as global flags.

---

## 2. Permission Classifications

The system validates the following core permissions:
*   `Read`: View metadata indexes, syllabus structures, and public resources.
*   `Write`: Create, update, or draft personal files and workspace logs.
*   `Review`: Inspect proposed changes in moderation queues.
*   `Approve`: Validate accuracy of mathematical derivations, diagrams, and code snippets.
*   `Publish`: Merge validated content drafts to the active database catalog.
*   `Archive`: Soft-deprecate legacy concepts, preserving their identifiers.
*   `Delete`: Permanent removal of users or configurations.
*   `Configure`: Alter system environment flags and variables.
*   `Manage`: Read audit trails, assign permissions, and revoke actor privileges.

---

## 3. Hierarchical Permission Inheritance

Permissions follow a downward inheritance flow through the curriculum taxonomy:

$$\text{Platform} \longrightarrow \text{Domain} \longrightarrow \text{Subject} \longrightarrow \text{Module} \longrightarrow \text{Topic} \longrightarrow \text{Asset}$$

*   **Higher-Level Grants**: Assigning a permission (e.g., `Write`) at the **Subject** level automatically inherits down to all child modules, topics, and assets within that subject.
*   **Explicit Overrides**: Higher-level permissions can be overridden at lower nodes. For instance, an actor may hold `Read` access across a Subject, but be granted `Write` access for a specific Topic sandbox.

---

## 4. AI Agent Scoping

To prevent security risks and unvalidated actions:
*   Autonomous AI agents are assigned explicit, scoped permissions exactly like human actors.
*   Agents never receive global admin or wildcard (`*`) role permissions.
*   An AI agent's credentials must restrict it to specific tasks (e.g., the Auditor Agent holds `Read` permissions on draft queues and `Write` permissions only on review log metrics).

---

## 5. Matrix Table

The following matrix illustrates default capabilities mapped to standard roles before inheritance evaluation:

| Capability | Guest | Learner | Author | Moderator | Administrator | AI Agent |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **`Read` Public Index** | Yes | Yes | Yes | Yes | Yes | Yes |
| **`Write` Workspace** | No | Yes | Yes | Yes | Yes | Scoped |
| **`Review` Queue** | No | No | No | Yes | Yes | Scoped |
| **`Approve` Drafts** | No | No | No | Yes | Yes | No |
| **`Publish` Catalog** | No | No | No | Yes | Yes | No |
| **`Manage` Permissions**| No | No | No | No | Yes | No |
| **`Configure` System** | No | No | No | No | Yes | No |

# Event Catalog

## Document Metadata
*   **Purpose**: Indexes all core platform events, listing payload specifications and domain routing paths.
*   **Scope**: Applies to all synchronous and asynchronous events dispatched across system domains.
*   **Intended Audience**: Backend platform developers, SRE leads, and test engineers.
*   **Related Documents**:
    *   [Event Architecture](../architecture/event-architecture.md)
    *   [Observability & Telemetry](../operations/observability-telemetry.md)
*   **Ownership**: Principal Platform Architect & Head of Platform Engineering

---

## 1. Identity Domain Events

### `identity.actor.registered`
*   **Description**: Dispatched immediately after a new guest successfully registers an account.
*   **Publisher**: Identity Domain
*   **Subscribers**: Workspace Domain (triggers initialization of a new Personal Workspace)
*   **Payload Example**:
    ```json
    {
      "actorId": "usr_90218340",
      "email": "learner@ascendrite.org",
      "registrationTime": "2026-07-09T01:34:00Z"
    }
    ```

---

## 2. Workspace Domain Events

### `workspace.state.updated`
*   **Description**: Published when a user modifies workspace files, scratchpads, or logs progress.
*   **Publisher**: Workspace Domain
*   **Subscribers**: Operations Domain (updates telemetry queues), Intelligence Domain (updates recommendation context)
*   **Payload Example**:
    ```json
    {
      "workspaceId": "wsp_10283402",
      "actorId": "usr_90218340",
      "lastModifiedTime": "2026-07-09T01:34:15Z"
    }
    ```

---

## 3. Knowledge Domain Events

### `knowledge.graph.rebuilt`
*   **Description**: Published after new metadata validations complete and the active curriculum graph is rebuilt.
*   **Publisher**: Knowledge Domain
*   **Subscribers**: Intelligence Domain (triggers vector database indexing updates), Platform Domain (invalidates search registry caches)
*   **Payload Example**:
    ```json
    {
      "version": "1.2.0",
      "updatedConceptsCount": 42,
      "rebuildDurationSeconds": 4.5
    }
    ```

---

## 4. Practice Domain Events

### `practice.assessment.completed`
*   **Description**: Triggered when a learner completes a course quiz, code challenge, or project assessment.
*   **Publisher**: Practice Domain
*   **Subscribers**: Workspace Domain (persists progress metrics), Intelligence Domain (adjusts future path recommendations)
*   **Payload Example**:
    ```json
    {
      "assessmentId": "asm_502183",
      "actorId": "usr_90218340",
      "scorePercent": 95.0,
      "passed": true
    }
    ```

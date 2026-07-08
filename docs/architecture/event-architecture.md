# Event Architecture

## Document Metadata
*   **Purpose**: Outlines the event-driven system design, payload structures, message-driven routing boundaries, and retry conventions.
*   **Scope**: Governs inter-domain notifications, telemetry events, and audit logging pipelines.
*   **Intended Audience**: Backend platform developers, system integration engineers, and DevOps leads.
*   **Related Documents**:
    *   [Backend Architecture](backend-architecture.md)
    *   [Observability & Telemetry](../operations/observability-telemetry.md)
*   **Ownership**: Principal Platform Architect & Head of Platform Engineering

---

## 1. System Communication Boundaries

To preserve domain isolation in the modular monolith, direct method invocations across domains are restricted. Instead, the platform leverages synchronous and asynchronous event buses:
*   **Synchronous Event Dispatching**: Used for transactional workflows that must execute within the current request thread (e.g., identity verification triggers).
*   **Asynchronous Event Dispatching**: Used for long-running or non-blocking workflows (e.g., telemetry indexing, notification dispatches, and audit trail archiving).

---

## 2. Event Naming & Versioning

*   **Dot-Notation Formatting**: Events must be named using a domain-driven, dot-notated format representing state changes:
    
    $$\text{domain} \cdot \text{subdomain} \cdot \text{action}$$
    
    *   *Examples*: `identity.actor.registered`, `workspace.editor.saved`, `ai.guardrail.failed`.
*   **Event Versioning**: The event payload must contain a semantic version key (`event_version`) tracking schema changes. Consumer handlers must route payloads based on this version, allowing backward compatibility.

---

## 3. Producer & Consumer Responsibilities

*   **Producer Responsibilities**:
    1.  Generate and validate event payloads against schemas before dispatching.
    2.  Ensure transactional consistency: dispatch events only after corresponding database changes commit successfully.
    3.  Inject a unique `eventId` (UUIDv4) and UTC timestamp (`eventTime`) into all event metadata blocks.
*   **Consumer Responsibilities**:
    1.  Perform idempotency checks: verify that the `eventId` has not been processed previously.
    2.  Process handlers asynchronously without blocking downstream message queues.
    3.  Acknowledge message consumption only after execution completes, preventing data loss.

---

## 4. Retry Philosophy & Failure Handling

To survive network splits and API downtime:
*   **Exponential Backoff**: When event handlers fail, the consumer must retry processing using an exponential backoff sequence with randomized jitter:
    
    $$t_{\text{retry}} = 2^{\text{attempt}} \times 1\text{s} + \text{jitter}$$
    
*   **Dead Letter Queue (DLQ)**: If a message fails consecutive delivery attempts (max limit: 5), it is routed to the DLQ.
*   **SLA & Alerts**: DLQ additions must trigger administrator alerts, ensuring operations teams inspect and manually resolve failures.

---

## 5. Platform Event Classifications

The system event catalog is organized into ten distinct event classifications, driving core application loops:

*   **Authentication Events**: Fired upon user register, login, session termination, or trusted device validation.
*   **Learning Events**: Fired when concepts are read, progress indicators tick, or curriculum nodes are unlocked.
*   **Workspace Events**: Fired on workspace creation, panel layout configurations, or active tab swaps.
*   **File Events**: Fired when changes are written to coding scratchpads, files compile, or tests execute.
*   **AI Events**: Fired when RAG contexts generate embeddings, agents initialize, or guardrails reject LLM outputs.
*   **Communication Events**: Fired on friend relations updates, direct message logs, or community broadcasts.
*   **Notification Events**: Fired when announcements trigger, toasts display, or offline alerts archive.
*   **Recommendation Events**: Fired during offline inference schedules or active dashboard updates.
*   **Administrative Events**: Fired on permission changes, ownership transfer processes, or maintenance toggles.
*   **Analytics Events**: Fired during background telemetry aggregations or user study-time updates.

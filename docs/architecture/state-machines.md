# State Machines

## Document Metadata
*   **Purpose**: Defines the deterministic state machine configurations, session lifecycles, and transition validation constraints.
*   **Scope**: Governs workspace states, AI processing execution lifecycles, user accounts, and content publication stages.
*   **Intended Audience**: Backend developers, frontend engineers, and quality assurance specialists.
*   **Related Documents**:
    *   [System Architecture (HLD)](system-architecture-hld.md)
    *   [Backend Architecture](backend-architecture.md)
*   **Ownership**: Principal Software Architect & QA Lead

---

## 1. Architectural Pattern

Ascendrite uses finite state machine (FSM) models to govern entity lifecycles. State transitions must be deterministic, validating inputs against transition rules.
*   Entities must exist in exactly one state at any given runtime instant.
*   State changes are initiated exclusively by dispatching a validated action event to the corresponding state manager.
*   Transitions are protected by execution guards verifying user authorization, validation, and system conditions.
*   Transition logs must record: `sourceState`, `targetState`, `triggerEvent`, `actorId`, and `timestamp`.

---

## 2. Platform State Machines & Transition Events

### 2.1 User Account Lifecycle
Controls account registration and compliance states:
*   **States**:
    *   `Pending`: Account created, waiting for email activation.
    *   `Active`: Verified account permitted full platform access.
    *   `Suspended`: Access blocked due to violations.
    *   `Archived`: Account soft-deleted, data hidden.
*   **Transitions & Events**:
    *   `Pending` ──( Verify Email )──► `Active` (event: `identity.user.activated`)
    *   `Active` ──( Suspend Account )──► `Suspended` (event: `identity.user.suspended`)
    *   `Active` ──( Delete Account )──► `Archived` (event: `identity.user.deleted`)

### 2.2 Session Lifecycle
Tracks active tokens and session validity:
*   **States**:
    *   `Active`: Valid access token, active user requests.
    *   `Idle`: No requests received within the session threshold.
    *   `Expired`: Exceeded the 15-minute access token limit.
    *   `Revoked`: Explicitly terminated by user logout or rotation detection.
*   **Transitions & Events**:
    *   `Active` ──( User Logout )──► `Revoked` (event: `identity.session.revoked`)
    *   `Active` ──( Token Expires )──► `Expired` (event: `identity.session.expired`)
    *   `Expired` ──( Token Rotation )──► `Active` (event: `identity.session.refreshed`)

### 2.3 Notification Lifecycle
Governs alerts in the user dashboard:
*   **States**:
    *   `Unread`: Fresh notification, pending action.
    *   `Read`: Reviewed by user, remains in active list.
    *   `Archived`: Soft-deleted, hidden from main view.
*   **Transitions & Events**:
    *   `Unread` ──( Mark Read )──► `Read` (event: `notification.alert.read`)
    *   `Read` ──( Mark Archive )──► `Archived` (event: `notification.alert.archived`)

### 2.4 AI Job Lifecycle
Manages background reasoning, retrieval, and guardrail runs:
*   **States**:
    *   `Queued`: Task added to the execution queue.
    *   `Processing`: LLM calls or retrieval actions active.
    *   `Review`: Output checks and guardrails active.
    *   `Completed`: Verified content returned to the client.
    *   `Failed`: Execution error or guardrail rejection occurred.
*   **Transitions & Events**:
    *   `Queued` ──( Start Job )──► `Processing` (event: `ai.job.started`)
    *   `Processing` ──( Finish LLM Runs )──► `Review` (event: `ai.job.reviewing`)
    *   `Review` ──( Guardrail Pass )──► `Completed` (event: `ai.job.completed`)
    *   `Review` ──( Guardrail Reject )──► `Failed` (event: `ai.job.failed`)

### 2.5 Knowledge Asset Lifecycle
Tracks subject curriculum modifications and publishing:
*   **States**:
    *   `Draft`: Edited local content changes.
    *   `InReview`: Proposed pull request submitted, waiting for moderation.
    *   `Published`: Merged to the main branch, index compilation active.
    *   `Deprecated`: Outdated nodes preserved for backward compatibility.
*   **Transitions & Events**:
    *   `Draft` ──( Submit PR )──► `InReview` (event: `knowledge.asset.proposed`)
    *   `InReview` ──( Merge PR )──► `Published` (event: `knowledge.asset.published`)
    *   `Published` ──( Archive Node )──► `Deprecated` (event: `knowledge.asset.deprecated`)

### 2.6 Personal Workspace Lifecycle
Tracks client configuration, sync logs, and offline support:
*   **States**:
    *   `Uninitialized`: Client app loaded, waiting for authentication.
    *   `Initializing`: Downloading configuration maps and telemetry cache.
    *   `Active`: Workspace open and responsive.
    *   `Syncing`: Writing offline logs and files to the server.
*   **Transitions & Events**:
    *   `Uninitialized` ──( Authenticate )──► `Initializing` (event: `workspace.session.initialized`)
    *   `Initializing` ──( Config Loaded )──► `Active` (event: `workspace.setup.completed`)
    *   `Active` ──( Sync Start )──► `Syncing` (event: `workspace.sync.started`)
    *   `Syncing` ──( Sync Finish )──► `Active` (event: `workspace.sync.completed`)

### 2.7 File Upload Lifecycle
Controls binary and markdown uploads:
*   **States**:
    *   `Pending`: Target upload token generated.
    *   `Uploading`: Data stream written to MinIO.
    *   `Scanning`: Malware checks and security scan active.
    *   `Completed`: Asset validated and URL returned.
    *   `Failed`: Stream interrupted or scan failed.
*   **Transitions & Events**:
    *   `Pending` ──( Stream Start )──► `Uploading` (event: `media.upload.started`)
    *   `Uploading` ──( Stream Finish )──► `Scanning` (event: `media.scan.queued`)
    *   `Scanning` ──( Scan Pass )──► `Completed` (event: `media.upload.completed`)
    *   `Scanning` ──( Scan Fail )──► `Failed` (event: `media.upload.failed`)

### 2.8 Recommendation Task Lifecycle
Governs background personalization calculations:
*   **States**:
    *   `Scheduled`: Triggered by batch progression metrics.
    *   `Processing`: Offline inference calculating path nodes.
    *   `Calculated`: Suggested elements written to recommendations cache.
    *   `Expired`: Replaced by fresh calculations.
*   **Transitions & Events**:
    *   `Scheduled` ──( Trigger Inference )──► `Processing` (event: `recommendation.task.started`)
    *   `Processing` ──( Finish Calculations )──► `Calculated` (event: `recommendation.task.completed`)
    *   `Calculated` ──( Evict Cache )──► `Expired` (event: `recommendation.task.expired`)

# Engineering Flows

## Document Metadata
*   **Purpose**: Outlines the platform's primary end-to-end service interaction sequences, data paths, and state machine transitions.
*   **Scope**: Governs backend call execution sequences, domain boundary transitions, and entity lifecycle triggers.
*   **Intended Audience**: Software developers, database architects, and quality assurance specialists.
*   **Related Documents**:
    *   [Backend Architecture](backend-architecture.md)
    *   [API Architecture](api-architecture.md)
    *   [State Machines](state-machines.md)
*   **Ownership**: Principal Platform Architect & Head of Platform Engineering

---

## 1. Authentication Flow

This flow maps credential checks, JWT cookie generation, session caching, and transitions the **Session FSM**:

```
[Browser Client] ──( POST /auth/login )──► [API Gateway] ──► [Auth Service]
                                                                 │
                                                       ( Salt & bcrypt checks )
                                                                 │
                                                                 ▼
[Redis Cache] ◄──( Session active DTO )─── [Auth Service] ◄── [User Database]
      │                                                          │
      ▼                                                          ▼
( Transitions Session FSM to Active )                  ( Verify User FSM = Active )
      │
      ▼
[Browser Client] ◄──( Set-Cookie: HttpOnly Access JWT ) (Dispatched: identity.session.created)
```

---

## 2. Knowledge Retrieval Flow

This flow handles retrieving concepts from MongoDB and Knowledge Asset stores through the **Knowledge Service** boundary:

```
[Browser Client] ──( GET /subjects/{id} )──► [Platform API]
                                                 │
                                                 ▼
[MongoDB Datastore] ◄──( Find Metadata )─── [Knowledge Service]
                                                 │
                                                 ▼
[Managed Storage] ◄──( Load notes JSON )── [Knowledge Service]
                                                 │
                                   ( Verifies Asset FSM = Published )
                                                 │
                                                 ▼
[Browser Client] ◄──( JSON Asset DTO ) ◄───── [Platform API]
```

---

## 3. Search Flow

This flow routes text queries, applies permission filters, and returns ranked concepts:

```
[Browser Client] ──( GET /search?q=ml )──► [Search Router]
                                               │
                                               ▼
[Authz Middleware] ◄──( Verify Scopes )─── [Search Service]
                                               │
                                               ▼
[Elasticsearch] ◄──( Query & Match )────── [Search Service]
                                               │
                                   ( Filters only Published assets )
                                               │
                                               ▼
[Browser Client] ◄──( Filtered Results ) ◄── [Search Router]
```

---

## 4. Recommendation Flow

This flow maps online real-time inference and offline batch path generation, transitioning the **Recommendation Task FSM**:

*   **Online Path**:
    ```
    [Workspace Engine] ──► [Recs Service] ──► [In-Memory Cache] ──► [User DTO]
    ```
*   **Offline Path**:
    ```
    [Scheduler] ──► [Inference Engine] ──► [Telemetry DB]
                           │
                 ( Transitions Rec Task )
                 ( FSM: Scheduled -> Processing -> Calculated )
                 ( Dispatched: recommendation.task.completed )
                           │
                           ▼
    [Redis / Mongo] ◄──( Cache Path Array )
    ```

---

## 5. Notification Delivery Flow

This flow maps persistent notifications vs. transient toast routing, transitioning the **Notification FSM**:

```
[Event Bus] ──► [Notification Service]
                     │
                     ├─► ( Type = Toast ) ──► [WebSocket Gateway] ──► [Browser]
                     │
                     └─► ( Type = Persist ) ─► [MongoDB]
                                                   │
                                     ( Transitions Notification FSM to Unread )
                                                   │
                                                   ▼
                                         [Notification Center]
```

---

## 6. File Upload Flow

This flow handles object storage streaming, malware scans, validation, and transitions the **File Upload FSM**:

```
[Browser Client] ──( POST /media/upload )──► [Media Service]
                                                 │
                                                 ▼
[S3 Object Store (RustFS)] ◄──( Stream )───── [Media Service]
                                                 │
                                     ( FSM: Pending -> Uploading )
                                                 │
                                                 ▼
                                           [Malware Scanner]
                                                 │
                                     ( FSM: Uploading -> Scanning )
                                                 │
                                                 ├─► ( Pass ) ──► FSM: Completed (event: media.upload.completed)
                                                 │
                                                 └─► ( Fail ) ──► FSM: Failed (event: media.upload.failed)
                                                 │
                                                 ▼
[Browser Client] ◄──( Verified S3 URL ) ◄─── [Media Service]
```

---

## 7. AI Request Flow

This flow directs prompts, similarity matching, guardrail middleware, retries, and transitions the **AI Job FSM**:

```
[Workspace UI] ──( Prompt Query )──► [AI Router] ──► [AI Service]
                                                         │
                                               ( FSM: Queued -> Processing )
                                               ( Dispatched: ai.job.started )
                                                         │
                                                         ▼
[LLM Endpoint] ◄──( Grounded Prompt ) ◄────────────── [Vector Repository]
      │
      ▼
[Guardrail Validator] ──( FSM: Processing -> Review )
      │
      ├─► ( Pass ) ──► FSM: Completed (event: ai.job.completed) ──► [Workspace UI]
      │
      └─► ( Fail ) ──► FSM: Failed (event: ai.job.failed) ──► [Retry Queue]
```

---

## 8. Dashboard Rendering Flow

This flow coordinates user configurations, widget selections, and edge cache distributions:

```
[Browser Client] ──( Get Dashboard Config )──► [API Gateway]
                                                   │
                                                   ▼
[CDN Cache] ◄──( Load Template Schema )───── [Workspace Service]
                                                   │
                                                   ▼
[MongoDB datastore] ◄──( Load User Config )── [Workspace Service]
                                                   │
                                     ( Verify Workspace FSM = Active )
                                                   │
                                                   ▼
[Browser Client] ◄──( Composite JSON DTO ) ◄── [API Gateway]
```

---

## 9. Permission Evaluation Flow

This flow evaluates authorization checks through the inheritance hierarchy:

```
[API Endpoint Router] ──► [Authorization Middleware]
                               │
                               ▼
[MongoDB Datastore] ◄──( Load User Permissions )
                               │
                               ▼
                      [Evaluation Engine]
                               │
            ( Inherit: Platform -> Domain -> Subject )
                               │
                               ▼
                      ( Checks overrides )
                               │
                               ├─► ( Permitted ) ──► Execute Route
                               │
                               └─► ( Denied ) ─────► Return HTTP 403
```

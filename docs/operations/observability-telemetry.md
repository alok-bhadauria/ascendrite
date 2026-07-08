# Observability and Telemetry: Monitoring, Logging, and Performance Metrics

## Document Metadata
*   **Purpose**: Standardizes the system telemetry architecture, logging structures, application metrics, and user event monitoring systems.
*   **Scope**: Governs backend FastAPI monitoring instrumentation, Prometheus metrics scraping endpoints, and client telemetry events tracking.
*   **Intended Audience**: Operations engineers, DevOps leads, system security leads, and backend engineers.
*   **Related Documents**:
    *   [Backend Architecture](../engineering/backend-architecture.md)
    *   [Security Standards](../security/security-standards.md)
*   **Ownership**: Head of Platform Engineering & Site Reliability Operations Lead

---

## 1. System Observability Standards
The platform must implement structured logging and request correlation to track errors and performance drops across distributed boundaries.

### 1.1 Structured Logging Layout
All application logs shall be formatted and written as structured JSON payloads. This simplifies automated indexing in centralized log repositories.
*   **Mandatory Attributes**: Every log line must contain:
    *   `timestamp`: ISO-8601 formatted timestamp in UTC.
    *   `level`: System log severity (DEBUG, INFO, WARNING, ERROR, CRITICAL).
    *   `correlation_id`: Unique identifier injected at the API gateway layer to correlate requests.
    *   `component`: The specific microservice or application module.
    *   `duration_ms`: Execution time (if applicable) for transaction profiling.
*   **Sanitization Rules**: Log serialization routines must strip passwords, security tokens, and personal credentials.

### 1.2 Correlation ID Propagation
Every HTTP request passing through gateway layers must be assigned a unique trace ID. This correlation token shall be propagated:
1.  From the client request header (`X-Correlation-ID`).
2.  Into downstream API middleware contexts.
3.  Into database search queries and external API calls.
4.  In all logs printed during the request transaction scope.

---

## 2. Infrastructure & Application Metrics
To ensure operational stability, the platform must expose metrics tracking API performance, database health, and server memory allocations.

### 2.1 Prometheus Scraping Interface
All app servers must expose a `/metrics` route restricted to internal monitoring systems:
*   **API Latency Metrics**: Histogram vectors tracking HTTP request duration by route and status code.
*   **Active Sessions**: Gauge metrics monitoring currently authenticated sessions.
*   **Resource Footprints**: Gauges tracking memory consumption, active thread allocations, and CPU utilization.
*   **Database Metrics**: Counter metrics monitoring database transaction failures and connection pool states.

---

## 3. Telemetry Event Tracking
To support adaptive dashboards and personalized learning paths, the system must collect anonymous progression telemetry from the client workspace.

### 3.1 Event Schemas
Client actions shall trigger telemetry payloads sent to `/api/v1/telemetry/events`. All events must align with a strict validation schema:
*   `event_type`: Mapped string identifying the action. Supported values include:
    *   `topic_viewed`: User starts reading a note node.
    *   `quiz_submitted`: Diagnostic quiz completed.
    *   `practice_compiled`: Workspace code submitted for execution.
*   `event_metadata`: Dynamic nested objects capturing duration, correctness percentage, and node complexity ratings.
*   `timestamp`: Unix timestamp representing event occurrence.

### 3.2 Telemetry Privacy Controls
Telemetry collections must not include personally identifying information (PII). All user identity references in telemetry databases must be obfuscated using cryptographic tokens.

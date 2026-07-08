# Monitoring Standards

## Document Metadata
*   **Purpose**: Standardizes system monitoring metrics, alerting thresholds, and performance monitoring triggers.
*   **Scope**: Governs service runtime metrics, database connections, and dashboard alert notifications.
*   **Intended Audience**: DevOps engineers, operations leads, and site reliability specialists.
*   **Related Documents**:
    *   [Observability & Telemetry](observability-telemetry.md)
    *   [Incident Response](incident-response.md)
*   **Ownership**: Head of Platform Engineering & Site Reliability Operations Lead

---

## 1. Metrics Collection Architecture

Ascendrite monitors system health using metric collection agents scraping runtime stats:
*   **Scraping Endpoints**: Services expose standard `/metrics` endpoints returning Prometheus-formatted text metrics.
*   **Scraping Frequency**: Systems collect stats at a standard interval (e.g., every 15 seconds) to balance system metrics detail with collection overhead.
*   **Metric Instrumentation**: Custom performance metrics use unique, namespace-prefixed names to distinguish domain contexts (e.g., `ascendrite_identity_login_duration_seconds`).

---

## 2. Core Alert Metrics (SLA/SLO)

The platform evaluates operational health using Service Level Indicators (SLIs) aligned with system performance targets:

*   **API Latency**: $99\%$ of requests must complete in $\le 200\text{ms}$ ($p99 \le 200\text{ms}$).
*   **Error Rate**: System error HTTP status codes ($5xx$ errors) must represent less than $0.1\%$ of total weekly traffic.
*   **Database Capacity**: Database CPU usage must remain below $70\%$, and open connections must not exceed $80\%$ of pool capacity.

---

## 3. Severity Categorization

Operational alerts are classified to determine response priorities:

*   **Severity 1 (Critical)**: Platform is unresponsive or core database transactions fail. Triggers instant pager calls to on-duty operations personnel.
*   **Severity 2 (Warning)**: High API response latency ($p99 > 500\text{ms}$) or elevated error rates ($> 1\%$). Triggers warnings to operational dashboards and chat channels.
*   **Severity 3 (Info)**: Non-critical anomalies, disk utilization anomalies, or test pipeline failures. Logged to reporting dashboards for daily review.

---

## 4. Alert Routing Configurations

Operational notifications route directly to on-call schedules. Alert payloads contain specific context:
*   Failing service identify.
*   The triggered alert metric boundary.
*   A link to the operational debugging runbook.

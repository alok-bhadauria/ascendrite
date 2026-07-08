# Operational Standards

## Document Metadata
*   **Purpose**: Outlines system maintenance policies, Infrastructure as Code standards, and capacity management guidelines.
*   **Scope**: Applies to all production nodes, database clusters, config variables, and operations tools.
*   **Intended Audience**: System administrators, operations leads, and DevOps engineers.
*   **Related Documents**:
    *   [Deployment Architecture](deployment-architecture.md)
    *   [Incident Response](incident-response.md)
*   **Ownership**: Head of Platform Engineering & Site Reliability Operations Lead

---

## 1. Maintenance Windows

System maintenance tasks (such as database upgrades, node patching, or configuration rollouts) must occur during low-traffic windows:
*   **Scheduled Window**: Sundays between 02:00 UTC and 04:00 UTC.
*   **Notifications**: Maintenance schedules must be broadcast to the platform announcements board 48 hours in advance.
*   **Approval**: Production maintenance requires sign-off from the operations coordinator.

---

## 2. Infrastructure as Code (IaC)

All deployment architecture configurations must be managed via declarative code templates:
*   **No Manual Changes**: Modifying container configs, routing rules, or security permissions directly in server consoles is prohibited.
*   **State Locking**: Remote state storage files are locked cryptographically to prevent concurrent run conflicts.
*   **Version Control**: IaC templates reside in version control repositories, adhering to standard PR review procedures before deployment.

---

## 3. Capacity Scaling Rules

The system scales infrastructure resources automatically based on utilization metrics:
*   **Compute Instances**: Scale out when CPU utilization averages $\ge 70\%$ for 10 consecutive minutes.
*   **Database Capacity**: Storage volumes are configured with automated storage growth enabled.
*   **Bandwidth Controls**: Rate limits are set globally to protect backend databases from request spikes.

---

## 4. Operational Logging Audits

To verify system operational standards:
*   Telemetry configurations and access tokens are audited quarterly.
*   Application log files must be kept in search pools for 30 days, then archived to cold storage for long-term retention.

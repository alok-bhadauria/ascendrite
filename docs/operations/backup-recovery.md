# Backup & Recovery

## Document Metadata
*   **Purpose**: Defines database backup schedules, data retention rules, and disaster recovery validation steps.
*   **Scope**: Covers database collections, local storage configurations, and backup archiving scripts.
*   **Intended Audience**: Database administrators, DevOps engineers, and compliance leads.
*   **Related Documents**:
    *   [Database Schema](../architecture/database-schema.md)
    *   [Storage Architecture](../architecture/storage-architecture.md)
*   **Ownership**: Head of Platform Engineering & Lead Storage Architect

---

## 1. Backup Frequencies

To protect the integrity of workspace sessions and learning files, the database backup routines operate at defined frequencies:
*   **Transaction Logs**: Archived every 15 minutes to support Point-in-Time Recovery (PITR) configurations.
*   **Daily Snapshots**: Automated snapshot backup jobs execute during low-traffic windows (e.g., daily at 02:00 UTC).
*   **Weekly Backups**: Permanent structural database snapshots are captured weekly.

---

## 2. Retention Schedules

Backup archives are managed to optimize costs while satisfying compliance obligations:
*   **Hourly Transaction Logs**: Retained for a rolling 14-day window.
*   **Daily Snapshots**: Kept active for 30 calendar days.
*   **Weekly Snapshots**: Stored in cold storage archives for a minimum of 180 days before automated deletion routines.

---

## 3. Cryptographic Storage

Backup security is integrated directly into archiving routines:
*   **Encryption Standards**: All backup payloads must be encrypted using AES-256 keys prior to transferring to remote vault systems.
*   **Access Control**: Backup directories use strict IAM policies, preventing write/delete actions by application containers.

---

## 4. Disaster Recovery Drills

Verification of recovery capabilities must occur through routine simulation tests:
*   **Restore Validation**: Automated recovery checks execute monthly, restoring snapshots onto isolation staging instances.
*   **Drill Metric Target**: Recovery Time Objective (RTO) must remain $\le 2\text{ hours}$. Recovery Point Objective (RPO) must remain $\le 15\text{ minutes}$.
*   **Drill Log**: Every simulation logs restoring steps, encountered errors, and target restore speeds.

# Contribution Guide

## Document Metadata
*   **Purpose**: Standardizes the codebase contribution lifecycle, pull request workflows, and code review criteria.
*   **Scope**: Governs all commits, branch naming rules, and pull requests submitted by developers or AI agents.
*   **Intended Audience**: Core repository contributors, software engineers, and automated subagents.
*   **Related Documents**:
    *   [Engineering Lifecycle](engineering-lifecycle.md)
    *   [Repository Structure](repository-structure.md)
*   **Ownership**: Engineering Governance Lead & Operations Coordinator

---

## 1. Branch Naming Conventions

All Git branches must be named to match the nature of the change:
*   **Feature Branches**: `feature/[issue-number]-short-description` (e.g., `feature/412-jwt-token-refresh`).
*   **Bug Fixes**: `bugfix/[issue-number]-short-description` (e.g., `bugfix/102-workspace-scroll-flicker`).
*   **Hotfixes**: `hotfix/[issue-number]-short-description` (reserved for production patch changes).

---

## 2. Commit Message Standards

Ascendrite uses structured commit messages. The message format is:
```
[domain-prefix]: Short, imperative-mood description of the change

Detailed explanation of why the change is necessary, including references to 
related issues or ADRs.
```
*   **Valid Domain Prefixes**: `identity`, `workspace`, `knowledge`, `practice`, `platform`, `operations`, `docs`.
*   **Imperative Mood**: Use "add feature" instead of "added feature" or "adds feature".

---

## 3. Pull Request Submission

PR submissions must follow a structured validation sequence:
*   **Checklists**: PR descriptions must indicate completion of all relevant checks in the [Engineering Checklists](file:///E:/Projects/Ascendrite/blueprint/engineering-checklists.md).
*   **Documentation**: Code changes modifying API endpoints, database structures, or configs must include updates to matching documentation.
*   **CI Checks**: All automated lint, type check, and test jobs must pass successfully in the PR pipeline prior to merge.

---

## 4. Review Process

To maintain platform standards:
*   **Peer Approval**: Every PR requires review and approval from at least one core engineer or domain moderator.
*   **Domain Ownership**: Changes modifying a specific domain (e.g., identity) require approval from the designated owner.
*   **No Self-Merges**: Merging one's own PR without review is blocked, except during critical incident recovery operations.

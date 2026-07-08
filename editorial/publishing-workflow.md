# Publishing Workflow

## Document Metadata
*   **Purpose**: Outlines publishing stages, moderation processes, and content lifecycle phases.
*   **Scope**: Governs content creation, edit proposals, metadata rebuild triggers, and deprecation.
*   **Intended Audience**: Content authors, editors, moderators, and database administrators.
*   **Related Documents**:
    *   [Contribution Guide](../docs/development/contribution-guide.md)
    *   [Quality Assurance Framework](quality-assurance-framework.md)
*   **Ownership**: Head of Editorial Division & Operations Coordinator

---

## 1. Core Workflow Lifecycle

Syllabus content progresses through a series of review gates to ensure it meets platform standards before publication:

```
Idea
  │
  ▼
Draft
  │
  ▼
Technical Review
  │
  ▼
Editorial Review
  │
  ▼
Subject Review
  │
  ▼
AI Validation
  │
  ▼
Publishing
  │
  ▼
Maintenance
  │
  ▼
Deprecation
```

---

## 2. Explanation of Workflow Stages

*   **Idea**: A content contribution request is registered in the tracker, defining the target subject module and learning outcomes.
*   **Draft**: The author drafts notes, coding challenges, and assessments on a local branch.
*   **Technical Review**: Technical reviewers compile the code blocks and check derivations to verify correctness.
*   **Editorial Review**: Editors verify that the draft conforms to tone, voice, and grammar guidelines.
*   **Subject Review**: The designated subject coordinator signs off on the syllabus and pedagogical flow.
*   **AI Validation**: Automated pipelines validate the files against their schemas and check that prerequisite IDs resolve.
*   **Publishing**: The branch is merged to the main branch, triggering a build pipeline that compiles the global metadata indices.
*   **Maintenance**: Content is monitored and updated based on feedback and error logs.
*   **Deprecation**: Outdated content is soft-deprecated, preserving IDs for backward compatibility before removal.

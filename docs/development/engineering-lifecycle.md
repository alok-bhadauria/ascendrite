# Engineering Lifecycle and Release Governance

## Document Metadata
*   **Purpose**: Outlines the software development pipeline, CI/CD code validation, release processes, version management, and human-in-the-loop review workflows.
*   **Scope**: Applies to all software modules, platform client resources, database schemas, and knowledge-base content additions.
*   **Intended Audience**: All platform developers, content authors, peer reviewers, and QA automation leads.
*   **Related Documents**:
    *   [Engineering Principles](../governance/engineering-principles.md)
    *   [Engineering Decision Process](../governance/engineering-decision-process.md)
    *   [Knowledge Base Integration](../architecture/knowledge-base-integration.md)
*   **Ownership**: Head of Platform Engineering & Lead Release Coordinator

---

## 1. The Engineering Lifecycle
The development pipeline is split into separate workflows for software changes and knowledge-base updates to ensure curriculum stability and continuous platform deployment.

### 1.1 Software Development Lifecycle
1.  **Issue & Design**: Code changes must begin with a corresponding issue tracking task and, where required, an RFC outlining architectural changes.
2.  **Implementation**: Developers write clean, modular, and typed implementations, adding unit tests.
3.  **Local Checks**: Prior to commit, changes should pass local syntax checkers and unit test validations.
4.  **Pull Request Validation**: All PRs must undergo a peer review and pass all continuous integration build tests.
5.  **Staging Deployment**: Merges to `main` must automatically deploy to a sandbox staging environment for testing.
6.  **Production Release**: Staged versions must be promoted to production only after automated QA verification passes.

---

## 2. Release & Versioning Governance
To prevent breaking client-side trackers or user progression logs, both data APIs and knowledge bases follow version rules.

### 2.1 Content Versioning Policy
Knowledge base updates follow semantic versioning rules (`MAJOR.MINOR.PATCH`):
*   **MAJOR updates**: Structural modifications, subject removals, or module reorganizations.
*   **MINOR updates**: Subject profile changes, new topics, or syllabus expansion.
*   **PATCH updates**: Grammar fixes, code optimizations, formatting changes, or diagram updates.
Versions must be explicitly annotated in the `subject-metadata.json` configurations.

### 2.2 API Versioning and Deprecation Strategy
API router paths must be versioned (e.g. `/api/v1/`).
*   **Backward Compatibility Scopes**: Core APIs shall support previous endpoints for a minimum loop of one minor release cycle.
*   **Formal Deprecation Rules**: When a route changes:
    *   It must be marked as deprecated in OpenAPI documents.
    *   System warning logs should flag access calls.
    *   A formal deprecation announcement must outline the migration timeline.

---

## 3. Human Review and Pull Request Merging Workflow
Educational contents inside `knowledge-base/` are subject to a strict human-in-the-loop review pipeline:

```
[Author Drafts JSON Content]
             |
             v
[Local Checks: validate_ai_notes.py]
             |
             v
[Open Git Pull Request (PR)]
             |
             v
[Automated CI Validation]
- JSON Schema Draft 2020-12 checks
- validate_knowledge_integrity.py (orphans, duplicates, links)
             |
             v
[Knowledge Review Agent Validation]
- Cognitive complexity check
- Reference terminology check
             |
             v
[Human Editorial Peer Review]
- Tone, accuracy, and code walkthroughs
             |
             v
[Human Moderator Approves & Merges]
```

### 3.1 Content Validation Checklist
PR validation checkers must execute in sandbox boundaries:
*   **Syntax Check**: Deserialization validation to catch trailing commas or syntax leaks.
*   **Broken References**: Verification that all subject, concept, and link mappings exist in the branch.
*   **Peer Review Rule**: At least one human Moderator or Subject Editor must approve the content before merge.

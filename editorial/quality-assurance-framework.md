# Quality Assurance Framework

## Document Metadata
*   **Purpose**: Outlines quality checks, review gates, and acceptance criteria for publishing curriculum content.
*   **Scope**: Governs the pre-publication validation pipelines and PR review processes for all knowledge base updates.
*   **Intended Audience**: QA analysts, subject matter reviewers, content editors, and automated lint agents.
*   **Related Documents**:
    *   [Testing Strategy](../docs/development/testing-strategy.md)
    *   [AI Content Governance](ai-content-governance.md)
*   **Ownership**: Quality Assurance Lead & Head of Editorial Division

---

## 1. Quality Assurance Tiers

Ascendrite verifies content quality across four distinct tiers before publication:

### 1.1 Educational QA
*   **Target**: Verifies that learning outcomes align with Bloom's Taxonomy.
*   **Checks**: Ensures progression matches the designated difficulty level and confirms active recall check gates are embedded correctly.

### 1.2 Technical QA
*   **Target**: Verifies mathematical proofs and code examples.
*   **Checks**: Enforces that code samples compile and execute without errors within sandbox environments.

### 1.3 Editorial QA
*   **Target**: Ensures compliance with tone, voice, and grammar guidelines.
*   **Checks**: Verifies that the writing style remains objective, uses no emojis, and conforms to formatting rules.

### 1.4 Publishing QA
*   **Target**: Validates JSON metadata structures and semantic graph mappings.
*   **Checks**: Ensures files validate against designated schemas and confirms that the curriculum map has no broken links or circular paths.

---

## 2. Review Gates and Acceptance Criteria

Every content contribution must pass through three sequential review gates:

```
[Draft Submission]
       │
       ▼
[Gate 1: Automated Validation] (Checks JSON schemas, compiles code, runs lint tools)
       │
       ▼
[Gate 2: Subject Matter Review] (Manual check of derivations, diagrams, and logic)
       │
       ▼
[Gate 3: Editorial Sign-Off] (Confirm style guide compliance and merge PR)
```

---

## 3. Automated Validation Pipelines

*   **Schema Linting**: Pre-commit hooks validate modified JSON assets against the schema templates.
*   **Code Compilation**: Testing pipelines compile all code examples and run practice skeleton tests.
*   **Link Verification**: Relational tests confirm that all prerequisite topic IDs resolve to existing nodes.

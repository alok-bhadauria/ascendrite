# Testing Strategy

## Document Metadata
*   **Purpose**: Outlines test structures, test tool requirements, coverage targets, and pipeline checks.
*   **Scope**: Applies to all unit, integration, contract, and end-to-end tests across the repository.
*   **Intended Audience**: Quality assurance specialists, software engineers, and DevOps leads.
*   **Related Documents**:
    *   [Coding Standards](coding-standards.md)
    *   [Engineering Lifecycle](engineering-lifecycle.md)
*   **Ownership**: Security, Operations & QA Division Lead

---

## 1. Testing Pyramid

Ascendrite validates codebase integrity using a structured testing pyramid:

*   **Unit Tests**: Validate isolated functions, algorithms, and models. Execution speed must be optimized to run instantly.
*   **Integration Tests**: Check operations across domain boundaries and database connectors.
*   **Contract Tests**: Ensure backend Pydantic models align with frontend fetch models.
*   **End-to-End Tests**: Simulate real learner sessions navigating workspaces, scratchpads, and AI dialog flows.

---

## 2. Test Tool Stack

The test suites use the following core tools:
*   **Backend Testing**: Run using `pytest`. HTTP endpoints are emulated using `httpx.AsyncClient`.
*   **Frontend Testing**: Component checks use Jest and React Testing Library.
*   **Mock Services**: External services are mocked out using dedicated mock endpoints or library mocks during testing to prevent network-dependent failures.

---

## 3. Target Coverage Goals

All platform PR submissions must maintain or exceed target code coverage metrics:
*   **Overall Codebase Coverage**: Minimum $80\%$ test coverage.
*   **Critical Domains**: Identity, security, and knowledge validation layers must maintain $\ge 90\%$ coverage.
*   **Untested Code**: The addition of new features without corresponding test coverage is blocked.

---

## 4. Continuous Integration Checks

Tests execute automatically inside pull request pipelines:
*   Pipelines must build containers, run unit tests, and check contract mappings.
*   Test failure events block code merge actions.

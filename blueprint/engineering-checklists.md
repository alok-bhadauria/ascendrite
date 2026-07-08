# Ascendrite Engineering Checklists

**Version:** 1.0.0
**Status:** Approved
**Owner:** Architecture & Governance Division
**Last Updated:** 2026-07-09

### Reference Context
This document is derived directly from the constitutional source of truth, the [Ascendrite Master Blueprint](file:///E:/Projects/Ascendrite/blueprint/ascendrite-master-blueprint.md). For domain concepts ownership, refer to the [Domain Reference](file:///E:/Projects/Ascendrite/blueprint/domain-reference.md). For phase requirements and dependencies, see the [Implementation Roadmap](file:///E:/Projects/Ascendrite/blueprint/implementation-roadmap.md).

---

## New API Endpoint Checklist
- [ ] **Domain Placement**: Verify the endpoint is placed inside the correct business domain folder.
- [ ] **Input Validation**: Enforce request parameter validation using JSON Schema structures.
- [ ] **Authorization Check**: Enforce actor authentication filters and verify Role-Based Access Control (RBAC) permission scopes.
- [ ] **Telemetry Hooks**: Integrate logging middleware to track endpoint latency, status codes, and user types.
- [ ] **Contract Verification**: Write contract tests checking success, validation failure, and permission violation cases.
- [ ] **Documentation**: Document routes, arguments, and return types in the OpenAPI specifications.

---

## New Database Collection Checklist
- [ ] **Domain Separation**: Ensure the database access logic is isolated within the owning domain storage layer.
- [ ] **Schema Definition**: Apply JSON Schema Draft 2020-12 validation structures to database inputs.
- [ ] **Indexes**: Configure indexes for search paths and establish unique constraint index patterns.
- [ ] **No Cross-Domain Joins**: Enforce database queries to resolve relations programmatically via service APIs (no database joins across domains).
- [ ] **Migrations**: Write and test migration files for local, staging, and production database environments.
- [ ] **Backup Configuration**: Register the new collections with system data retention policies.

---

## New React Component Checklist
- [ ] **Component Sizing**: Store the file under the appropriate path (`/platform` primitives, widgets, or features).
- [ ] **Token Compliance**: Reference visual styling tokens (spacing, palette, typography) exclusively from the core theme metadata definitions.
- [ ] **Accessibility Attributes**: Assign correct keyboard focus landmarks and ARIA descriptors to interactive nodes.
- [ ] **Responsive Sizing**: Test component grids on mobile, tablet, and widescreen view resolutions.
- [ ] **State Machine Testing**: Write unit tests validating visual state changes and prop updates.
- [ ] **Component Sandbox**: Add component properties and usage guides to internal style interfaces.

---

## New Feature Integration Checklist
- [ ] **Architectural Integrity**: Answer the four architectural questions:
  1. Why does this feature exist?
  2. How does it align with the product vision?
  3. How does it integrate with the platform?
  4. Can it scale without architectural changes?
- [ ] **Interface Isolation**: Establish clean API boundaries between the new feature and existing domains.
- [ ] **Analytics & Tracking**: Embed audit logs and usage tracking telemetry hooks.
- [ ] **Review Verification**: Complete peer engineering review and architecture verification.
- [ ] **Feature Flags**: Deploy behind conditional configuration flags to isolate production deployment.

---

## AI Agent Integration Checklist
- [ ] **Registry Entry**: Register the agent instance within the central Orchestrator Registry.
- [ ] **System Prompt**: Write a restricted prompt definition with clear instructions, domain boundaries, and error recovery policies.
- [ ] **RAG Configuration**: Define the vector search collection inputs and RAG assembly formats.
- [ ] **Human-in-the-Loop**: Implement confirmation flags for agent actions affecting public databases.
- [ ] **Provider Configuration**: Set model parameters, max tokens, temperature, and usage safety thresholds.
- [ ] **Agent Simulation**: Implement unit validation tests validating agent outputs and formatting.

---

## Knowledge Asset Publication Checklist
- [ ] **Schema Compliance**: Validate metadata structures against JSON Schema guidelines.
- [ ] **Graph Verification**: Verify the knowledge asset has valid relations and contains no circular graph paths.
- [ ] **Assessment Matching**: Ensure modules include corresponding quizzes, code exercise assets, or projects.
- [ ] **Editorial Validation**: Review text content against editorial language standards.
- [ ] **Queue Submission**: Submit metadata adjustments to the moderator queue for platform validation.

---

## Accessibility Checklist
- [ ] **Color Contrast**: Maintain a minimum contrast ratio of 4.5:1 for normal text layers (3:1 for large display layers).
- [ ] **Interaction Hooks**: Add key event listeners to ensure all visual elements are keyboard navigable.
- [ ] **Focus Tracking**: Style active states with clear focus rings.
- [ ] **HTML Semantics**: Use structural tags (`<nav>`, `<header>`, `<main>`, `<article>`, `<section>`).
- [ ] **Screen Readers**: Test workspace elements using voice accessibility screen readers.

---

## Security Review Checklist
- [ ] **Input Sanitization**: Escape and validate all parameters prior to runtime execution.
- [ ] **CORS Restrictions**: Limit CORS setups to approved system domains.
- [ ] **Token Validation**: Rotate JWT security tokens and verify signature validation pipelines.
- [ ] **PII Masking**: Ensure no personally identifiable information (PII) is exported to log files or telemetry databases.
- [ ] **Dependencies Scanner**: Check libraries for vulnerabilities and audit package updates.

---

## Testing Checklist
- [ ] **Unit Tests**: Code coverage must cover state logic, helper functions, and error cases.
- [ ] **Integration Tests**: Verify database operations, local file systems, and domain communication modules.
- [ ] **Contract Tests**: Validate API schema compliance between client queries and server inputs.
- [ ] **Test Execution**: Ensure tests pass in local container environments and remote CI pipelines.

---

## Documentation Checklist
- [ ] **Domain Update**: Revise domain docs to match architectural and implementation modifications.
- [ ] **Markdown Compliance**: Conform to editorial style guides and formatting rules.
- [ ] **Database & Config Docs**: Document new database collections, API routes, and config flags.
- [ ] **Relative Links**: Ensure relative file links resolve correctly in version control directories.

---

## Pull Request Checklist
- [ ] **PR Description**: Describe structural changes, matching issues, and related decisions.
- [ ] **ADR Links**: Reference related Architectural Decision Records.
- [ ] **CI Passing**: Verify all automated checks and tests run successfully.
- [ ] **Review Resolution**: Enforce review approval and resolve comments.
- [ ] **Git Hygiene**: Clean test files, logs, or debug artifacts from the commit history.

---

## Release Readiness Checklist
- [ ] **Staging Execution**: Run data migrations and functional smoke tests in staging environments.
- [ ] **Variables Validation**: Verify all environmental keys and production settings are loaded.
- [ ] **Backup Checks**: Confirm database backup tasks are active and tested.
- [ ] **Rollback Plan**: Verify deployment rollback strategies for staging/production failure.
- [ ] **Ops Notification**: Coordinate with operational teams on deployment windows and maintenance notifications.

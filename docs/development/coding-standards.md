# Coding Standards

## Document Metadata
*   **Purpose**: Defines codebase style rules, language formatting constraints, complexity annotations, and coding principles.
*   **Scope**: Governs all Python, TypeScript/React, and JSON files inside the repository.
*   **Intended Audience**: All software developers, code reviewers, and automated writing agents.
*   **Related Documents**:
    *   [Repository Structure](repository-structure.md)
    *   [Testing Strategy](testing-strategy.md)
*   **Ownership**: Principal Software Architect & Head of Platform Engineering

---

## 1. Style & Linting Enforcement

To maintain a consistent codebase:
*   **Python (Backend)**: Follow PEP 8 style guidelines. Code formatting and lint checks are enforced via Ruff.
*   **TypeScript/React (Frontend)**: Standardized via ESLint and Prettier configuration sets.
*   **JSON Files**: Schemas must match designated schemas and use 2-space indentation.

---

## 2. Type Safety & Annotations

Strict typing is required to reduce runtime errors:
*   **Python Type Hints**: All function parameters, return values, and variables must be explicitly typed. Use Pydantic schemas for endpoint request and response validation.
*   **TypeScript Standards**: Explicitly declare interfaces or types for all component props, state hooks, and API responses. The use of `any` is prohibited.

---

## 3. Complexity Annotations

To ensure performant implementations:
*   **Algorithmic Complexity**: Every major data-processing function or lookup method must document its time and space complexity using Big-O notation within its docstring.
*   **Database Queries**: Query execution paths must include indexed search fields. Do not use unindexed lookups in key workflow paths.

---

## 4. Architectural Separation Rules

Developers must isolate business operations from implementation libraries:
*   **Dependency Inversion**: Access database connectors, external APIs, and local resources via interfaces rather than direct module imports.
*   **Data Transfer Objects (DTOs)**: Service operations must pass structured DTO models instead of raw database models to prevent schema leaks.
*   **Zero Placeholders**: Implementations must contain no incomplete code blocks, `TODO` comments, or blank default overrides.

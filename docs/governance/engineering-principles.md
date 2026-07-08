# Engineering Principles

## Document Metadata
*   **Purpose**: Outlines the core engineering design constraints, software patterns, and architecture philosophies.
*   **Scope**: Governs all backend codebase, frontend codebase, and database designs.
*   **Intended Audience**: Software engineers, database architects, and system integrators.
*   **Related Documents**:
    *   [Product Philosophy](product-philosophy.md)
    *   [Product Evolution Strategy](product-evolution-strategy.md)
*   **Ownership**: Principal Software Architect & Head of Platform Engineering

---

## 1. Modularity & Clean Architecture
We adhere to a decoupled, modular design pattern. Implementation code must follow Clean Architecture rules:
*   **Decoupled Layers**: Presentation, application, and data infrastructure layers must remain strictly isolated. 
*   **Dependency Inversion**: High-level business logics must never depend on low-level database drivers or frame APIs. Instead, components interact through abstraction interfaces.
*   **Single Responsibility**: Every service module, repository class, and client component should serve exactly one clear responsibility.

---

## 2. Core Code Design Standards
*   **SOLID**: Design classes and interfaces to be open for extension but closed for modification. Interface segregation must be strictly followed.
*   **DRY (Don't Repeat Yourself)**: Avoid code duplication. If shared logics exist, extract them to generic modules.
*   **YAGNI (You Aren't Gonna Need It)**: Do not write preemptive abstractions or features. Build only what is required by current specifications.
*   **Strict kebab-case**: All files, directories, JSON properties, and routing paths must follow `kebab-case`.

---

## 3. Backward Compatibility Strategy
API endpoints, data schemas, and metadata files must prioritize backward compatibility. When evolving metadata schemas:
*   Mark legacy or redundant fields as deprecated in documentation.
*   Retain legacy parameters temporarily to prevent breaking operational API clients or parsing runners.
*   Schedule formal migrations and deprecation removals in explicit version boundaries.

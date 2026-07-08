# Project Overview: Product Architecture and Development Standards

---

## 1. Product Vision & Architecture
Ascendrite is a premium, open-access knowledge platform designed to bridge the gap between academic theory, engineering practice, and professional readiness. The platform transitions traditional, high-level technical syllabi into granular, code-driven learning roadmaps.

### The Dual-Loop Learning Philosophy
Ascendrite structures its pedagogical progression around two core execution loops:
1.  **Conceptual Loop:** Translates abstract intuition into formal mathematical derivations and system designs.
2.  **Practical Loop:** Translates mathematical and design formulations into runnable, production-grade source code, performance benchmarks, and execution plans.

### Decoupled Subsystems
To ensure scalability, the platform is divided into three decoupled boundaries:
*   **Knowledge Base Repository:** A portable, offline-first database storing curriculum files strictly in JSON format.
*   **Core API Server (FastAPI):** A high-performance Python API server that ingests JSON curricula and orchestrates user state, progress, and authentication.
*   **Interactive Web Client (ReactJS):** A responsive, animated frontend that compiles data structures, arrays, and algorithms dynamically on the client canvas.

---

## 2. Documentation Standards
Ascendrite enforces a modular, single-source-of-truth (SSOT) documentation architecture. Design documents reside under `docs/` and adhere to these guidelines:
*   **File Naming:** Must follow strict `kebab-case.md` naming conventions.
*   **Zero Emojis:** The use of emojis is strictly prohibited in all documentation, source code, and JSON metadata files to maintain a professional, academic aesthetic.
*   **Academic and Engineering Neutrality:** Maintain objective styling. Present system limits, tradeoffs, and metrics rather than generic framework opinions.
*   **KaTeX/LaTeX Notation:** Math expressions must use standard KaTeX syntax. Wrap inline math in single dollar signs (e.g. $x \in \mathbb{R}$) and block equations in double dollar signs (e.g. $$\mathbf{A}\mathbf{x} = \lambda\mathbf{x}$$).

---

## 3. Development Standards
Contributors and code modules must adhere to the following development lifecycle constraints:
*   **Modularity:** Decouple business logic from framework-specific execution layers. Databases, routing layers, and third-party APIs must be accessed via defined abstraction interfaces (Dependency Inversion).
*   **Strict Typing:** Maintain typing definitions across Python (Pydantic, type hints) and JavaScript/TypeScript codebases.
*   **No Placeholders:** Source code implementations must not contain `// TODO`, `pass`, or placeholder parameters. All code blocks must be syntactically valid and executable.
*   **Complexity Annotation:** Every major algorithmic execution block or query must document its Big-O time and space complexity in its docstrings.

---

## 4. Maintainability & Extensibility Framework
To support future growth without requiring core system refactoring:
*   **Open-Closed Design:** Modules must be open for extensions (e.g., adding a new database engine or authentication provider) but closed for modifications.
*   **Standard Interface Protocols:** Services must expose clean API contracts and communicate via structured DTOs (Data Transfer Objects).
*   **Backward Compatibility:** Changes to API contracts must support legacy JSON schemas through version mappings (e.g., `/api/v1/` routes).

---

## 5. Future Expansion Roadmap
The system is designed to scale from the initial technology stack to enterprise topologies:
*   **Frontend Evolution:** Migration from client-side ReactJS rendering to Next.js (Server Components / SSR) and React Native (for mobile platform compatibility).
*   **Data Tier Migration:** Transitioning the database from MongoDB Atlas to PostgreSQL (relational schemas) and Redis (caching and session locks).
*   **Orchestration & Deployments:** Containerizing services with Docker and deploying onto Kubernetes clusters, managed by automated CI/CD pipeline pipelines.
*   **Distributed Architectures:** Transitioning the monolithic backend into modular microservices communicating via event-driven queues (e.g., RabbitMQ or Kafka).

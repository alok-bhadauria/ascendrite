# External Discoverability & Machine Legibility Standards

## Document Metadata
*   **Purpose**: Outlines terminology, indexing policies, SEO architecture, sitemap rules, and machine-legible standards (OpenAPI, structured metadata) for the platform.
*   **Scope**: Governs public website pages, API metadata outputs, crawler rules, and repository professionalism templates.
*   **Intended Audience**: Front-end developers, SEO specialists, technical writers, and AI integration engineers.
*   **Related Documents**:
    *   [System Architecture (HLD)](../architecture/system-architecture-hld.md)
    *   [API Architecture](../architecture/api-architecture.md)
*   **Ownership**: Head of Platform Engineering & Technical Documentation Architect

---

## 1. Multi-Audience Accessibility & Discoverability

Ascendrite must remain accessible, discoverable, and easily understandable across four primary groups:

*   **Human Learners**: Search and navigate dynamic curriculum views easily, utilizing clean, responsive components and consistent, academic typography.
*   **Educators & Content Managers**: Review syllabus maps, track course trajectories, and verify mathematical style notation standards.
*   **Search Engine Crawlers**: Automatically index public subjects, domains, and lesson catalogs without exposing workspace partitions or user records.
*   **AI Assistants, LLMs & Autonomous Agents**: Scan machine-legible API contracts and structured curriculum notes to provide real-time learning assistance.

---

## 2. Canonical Terminology

To ensure consistency across documents and search indexes, the system enforces a strict canonical terminology directory:
*   **Domain**: Top-level academic subject groups (e.g. `Computer Science`, `Mathematics`).
*   **Discipline**: Major academic departments (e.g. `Artificial Intelligence`, `Database Systems`).
*   **Subject**: A structured course study plan containing modules (e.g. `Deep Learning`, `SQL Basics`).
*   **Module**: A logical partition within a Subject containing topics (e.g. `Neural Networks`, `Backpropagation`).
*   **Topic**: An individual lesson node mapped to learning objectives.
*   **Asset**: A physical file containing text, flashcards, exercises, quizzes, or diagrams (e.g., `deep-learning-m1-t1-quiz.json`).
*   **Concept**: A semantic node in the global knowledge graph used to rank search results.

---

## 3. SEO Architecture & Web Crawling Rules

Public-facing catalog pages implement standardized optimization rules:
*   **Semantic HTML**: All public pages must be structured using semantic HTML5 tags (e.g. `<header>`, `<main>`, `<article>`, `<nav>`). Page layouts must limit nesting to prevent layout shifts (CLS) and ensure fast mobile rendering speeds.
*   **Dynamic Meta Tags**: Public routes (such as subject landing cards and lesson profiles) must inject metadata tags dynamically on the server side:
    *   `<title>`: Structured as `[Topic Title] | [Subject Name] | Ascendrite`.
    *   `<meta name="description">`: A short, compelling text summary ($\le 160\text{ characters}$) describing the lesson objectives.
    *   *Open Graph / Twitter Cards*: Standardized keys (`og:title`, `og:description`, `og:image`) configured for social sharing.
*   **Canonical URLs**: Every public page must declare a canonical link element to prevent search engine index dilution from duplicate parameters (e.g. `<link rel="canonical" href="https://ascendrite.org/subjects/deep-learning" />`).
*   **Robots Policy (`robots.txt`)**: A static robots file controls search engine scrapers:
    *   *Allowed Paths*: `/`, `/subjects/`, `/catalog/`.
    *   *Disallowed Paths*: `/workspace/`, `/admin/`, `/api/v1/auth/`, `/api/v1/admin/`.
*   **Sitemap Generation (`sitemap.xml`)**: An automated script runs daily, scanning MongoDB subjects and topics to generate a standardized XML sitemap index stored in the public folder.

---

## 4. Machine-Legible API Contracts & Structured Data

To allow developer tools, AI assistants, and integration agents to interact with the platform programmatically:
*   **OpenAPI authority**:
    *   **V1 Direct Requirement**: The FastAPI backend must expose the authoritative OpenAPI schema at `/api/v1/openapi.json` when the v1 application server is implemented, containing full endpoint definitions, input parameter models, DTO schemas, and response validation rules.
*   **Structured Metadata**: Public subject and topic cards inject **JSON-LD** schema metadata structured according to Schema.org specifications (e.g. `Course` and `EducationalOccupationalCredential` types) to support rich snippets in search results.
*   **Structured Notes Examples**: Coding exercises and math examples must expose structured JSON templates defining inputs, expected outputs, and execution parameters.
*   **llms.txt**:
    *   **V1-Ready / Deferred Until Public Documentation Activation**: A static `llms.txt` file is not created or served currently. It must be activated only when Ascendrite has sufficient stable public documentation to make it genuinely useful and maintainable. When activated, it will map stable canonical public documentation resources for AI assistants and agents.

---

## 5. Repository Professionalism & Version Control Semantics

The public facing repository maintains a clean, industry-grade layout to ensure developer trust:
*   **No Dummy/Fake Commits**: Commit messages must be clear, human-written, and describe the functional change (e.g. `feat: implement cursor-based pagination middleware`).
*   **Changelog**: Changes are tracked systematically in `CHANGELOG.md` using Keep a Changelog semantic versioning rules (`Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`).
*   **Documentation Link Stability**: Relative links within the repository documentation use relative file links (e.g. `[Local Development](../development/local-development.md)`). Avoid linking to local files using absolute host paths.

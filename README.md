# Ascendrite

Ascendrite is an enterprise-grade, metadata-driven learning platform and technical curriculum infrastructure. It translates traditional, high-level technical syllabi into granular, code-driven learning roadmaps. Designed for scalability, high information density, and modularity, the platform separates educational content from application logic.

---

## 1. Project Vision & Governance

Ascendrite exists to democratize and accelerate advanced technical mastery. We structure our platform around a decoupled architecture where curriculum databases, interactive clients, and AI-assisted workflows scale independently.

For detailed guidelines on our mission, learning model, and organizational boundaries, refer to the **Governance** layer:
*   **[Project Vision](docs/governance/project-vision.md)**: Core mission statement, values, and open-access principles.
*   **[Product Philosophy](docs/governance/product-philosophy.md)**: Metadata-first rendering rules and client-decoupling guidelines.
*   **[Learning Philosophy](docs/governance/learning-philosophy.md)**: The Dual-Loop Learning model (Conceptual vs. Practical loops).
*   **[Engineering Principles](docs/governance/engineering-principles.md)**: SOLID design guidelines, DRY/YAGNI, and backward compatibility.
*   **[Platform Philosophy](docs/governance/platform-philosophy.md)**: Workspace-first layout and dynamic theme engine tokens.
*   **[AI Philosophy](docs/governance/ai-philosophy.md)**: Multi-agent boundaries and the Non-Replacement Principle.
*   **[Organizational Structure](docs/governance/organizational-structure.md)**: Team boundaries and ownership scopes across engineering departments.
*   **[Product Evolution Strategy](docs/governance/product-evolution-strategy.md)**: Boundary decoupling guidelines and contract-first API design.
*   **[Version Roadmap](docs/governance/version-roadmap.md)**: Technology migrations and scalability roadmap.
*   **[Engineering Decision Process](docs/governance/engineering-decision-process.md)**: RFC proposal lifecycles and consensus guidelines.

---

## 2. Repository Directory Structure

```
ascendrite/
├── docs/                               # Systems design and platform specifications
│   ├── governance/                     # Roadmaps, philosophies, and processes
│   ├── architecture/                   # Decoupled system blueprints and RAG pipelines
│   ├── engineering/                    # Backend, frontend, and database specifications
│   ├── knowledge/                      # Ingestion parsing pipelines and validation rules
│   └── security/                       # Zero Trust parameters and secure cookie policies
├── editorial/                          # Operational Publishing Constitution
│   ├── editorial-style-guide.md        # Master editorial guide and tone specifications
│   ├── mathematical-style-guide.md     # LaTeX syntax standards and notation matrices
│   ├── code-style-guide.md             # Python/TypeScript code and script standards
│   ├── examples-style-guide.md         # Coding examples architecture rules
│   ├── diagram-style-guide.md          # Visual asset and Mermaid specification rules
│   ├── assessment-style-guide.md       # Quiz validation and adaptive metadata tagging rules
│   ├── glossary-style-guide.md         # Technical terminology and keyword rules
│   ├── prompt-library.md               # Actionable prompt templates for AI agents
│   └── quality-checklist.md            # Editorial QA check vectors
├── knowledge-base/                     # Decentralized, portable subject metadata
│   ├── schemas/                        # Draft 2020-12 JSON Schema files
│   ├── ai/                             # Artificial Intelligence subject files
│   ├── core-cs/                        # Core Computer Science subject files
│   ├── software-engineering/           # Software Engineering subject files
│   ├── web-development/                # Web Development subject files
│   └── aptitude/                       # General Aptitude subject files
├── platform/                           # Web application codebase
│   ├── client/                         # Interactive React SPA frontend
│   └── server/                         # FastAPI backend and database drivers
└── scratch/                            # Validation scripts and automation utilities
```

---

## 3. Technology Stack & Platform Overview

The platform uses a decoupled stack to guarantee high concurrency, secure session management, and sub-millisecond database queries:
*   **Backend Server**: Built using **FastAPI** utilizing stateless asynchronous execution loops and role-based access control.
*   **Frontend Client**: React Single Page Application (SPA) utilizing dynamic **Zustand** state stores, **Framer Motion** micro-animations, and a dynamic Theme Engine.
*   **Database Tier**: Document-oriented data storage (**MongoDB Atlas** / **Beanie ODM** / **Motor driver**) mapping nested user progress and quiz history. Swappable with relational databases (SQL) via the Repository Pattern.
*   **In-Memory Caching**: Redis instances cache active session parameters, while the server maintains an in-memory cache of the curriculum indexes for $O(1)$ lesson routing.
*   **AI Subsystem**: Stateless RAG search pipelines utilizing cosine similarity matches on a vector store, coupled with specialized multi-agent domains.

---

## 4. Ingestion & Content Validation

Curriculum assets are completely decoupled from application routing. Content is parsed from JSON files at server startup using standard configurations.

### Ingestion Validation Checks
To ensure database integrity and schema stability, all commits must pass two validation suites:

1.  **JSON Schema Validation**: Validates all curriculum assets against the JSON Schema Draft 2020-12 files under `knowledge-base/schemas/`.
2.  **Cross-Repository Verification**: Runs reference checking to find orphaned identifiers or duplicate keys:
    ```bash
    python scratch/validate_knowledge_integrity.py
    ```
3.  **Sanitization Check**: Verifies JSON syntax correctness and rejects Unicode emojis:
    ```bash
    python scratch/validate_ai_notes.py
    ```

---

## 5. Getting Started

### Prerequisites
*   Python 3.10+
*   Node.js 18+
*   MongoDB Instance (or whitelisted access to Atlas cluster)

### Running Backend
```bash
cd platform/server
pip install -r requirements.txt
python main.py
```

### Running Frontend
```bash
cd platform/client
npm install
npm run dev
```

---

## 6. Contribution & Licensing

We welcome contributions from human developers, content creators, and autonomous AI agents. All contributors must follow the guidelines detailed in the **[Editorial Style Guide](editorial/editorial-style-guide.md)** and the **[Quality Checklist](editorial/quality-checklist.md)**.

### Licensing
All code blocks are licensed under the Apache 2.0 License. All educational materials inside the `knowledge-base/` are licensed under the Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0).

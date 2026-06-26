# Ascendrite: Advanced Curriculum and Interactive Knowledge Infrastructure

Ascendrite is an enterprise-grade curriculum management and interactive learning platform designed to transform rigid, high-level course structures into granular, animated learning roadmaps, prioritizing content depth, mathematical rigor, and progress-tracking analytics.

---

## Codebase Architecture

The codebase is organized under a decoupled multi-tier architecture to maintain separation of concerns. This allows content databases, visualization systems, and backend services to evolve independently.

```
ascendrite/
├── README.md                           # Core system documentation
├── editorial/                          # Ascendrite Publishing Constitution and Style Guides
│   ├── editorial-style-guide.md        # Master editorial guide and tone specifications
│   ├── mathematical-style-guide.md     # LaTeX syntax standards and notation matrices
│   ├── code-style-guide.md             # Python/TypeScript code and script standards
│   ├── examples-style-guide.md         # Coding examples architecture rules
│   ├── diagram-style-guide.md          # Visual asset and Mermaid specification rules
│   ├── assessment-style-guide.md       # Quiz validation rules and option design guidelines
│   ├── glossary-style-guide.md         # Technical terminology and keyword rules
│   ├── prompt-library.md               # LLM prompt templates for content authors
│   └── quality-checklist.md            # Editorial compliance checks
├── knowledge-base/                     # Decentralized, portable subject repositories
│   └── ai/                             # Artificial Intelligence Subject curricula
│       ├── machine-learning/           # Canonical reference implementation (ML)
│       ├── deep-learning/              # Deep Learning Subject
│       ├── nlp/                        # Natural Language Processing Subject
│       ├── genai/                      # Generative AI Subject
│       └── ai-agents/                  # AI Agents and Orchestration Subject
├── platform/                           # Tracking platform code
│   ├── client/                         # Next.js/React interactive tracking frontend
│   └── server/                         # Python Flask/FastAPI API server and venv environment
└── scratch/                            # Helper scripts, validation tools, and temporary assets
```

---

## Core Subsystems

### 1. Decentralized Knowledge Base
Curriculum content is fully decentralized and parsed offline. Each subject folder under `knowledge-base/ai/` contains:
*   **`syllabus.json`**: The academic source of truth defining Modules -> Topics -> Subtopics.
*   **`subject-metadata.json`**: Theme colors, difficulty flags, and estimated learning times.
*   **`subject-map.json`**: Topic-level dependency trees and prerequisite resolution maps.
*   **`knowledge-assets.json`**: Curated bibliographies, glossary terms, and external citations.
*   **`book-metadata.json`**: Textbook-specific frontmatter, publisher details, and copyright licenses.

For every topic defined in the syllabus, a standardized six-layer asset suite is generated:
1.  **Notes (`notes/`)**: Highly detailed textbook-grade lessons stored as JSON containing LaTeX-formatted mathematical equations and callout blocks (e.g., "Student Trap", "Engineering Note").
2.  **Revision (`revision/`)**: High-density markdown study cards summarizing key equations, algorithms, and concepts.
3.  **Interview (`interview/`)**: Staff-engineer level mock interview guides containing targeted questions, candidate traps, and optimal responses.
4.  **Examples (`examples/`)**: Pure NumPy-based reference implementations (zero external runtime dependencies) showcasing the algorithms in action.
5.  **Practice (`practice/`)**: Code workspace files containing algorithms to implement, along with built-in tests and verification logic.
6.  **Quiz (`quiz/`)**: Multiple-choice assessment questions providing comprehensive diagnostic feedback.

### 2. Editorial Standards
All content complies with the publishing constitution under the `editorial/` directory:
*   **Mathematical Style**: Enforces rigid LaTeX matrices. Scalars are italic ($z$), vectors are bold lowercase ($\mathbf{x}$), and parameter matrices are bold uppercase ($\mathbf{W}$). All LaTeX code inside JSON files is double-escaped to prevent parsing failures.
*   **Code Quality**: Enforces zero-dependency algorithmic implementations in pure Python using standard library elements and NumPy, with no empty placeholders.
*   **Tone & Voice**: Written as a professional, expert-authored technical textbook, focusing on logical progression, continuous referencing, and removing duplication across the curriculum hierarchy.

### 3. Server Architecture
The `platform/server/` layer provides runtime API logic, database integrations, and code execution pipelines:
*   **Execution Environment**: Powered by a dedicated Python 3.10 virtual environment (`platform/server/python-venv-3.10.11`).
*   **Dependency Management**: Specified in `platform/server/requirements.txt`.
*   **API Modules**: Under `platform/server/api/` and `platform/server/ai/` to coordinate interactive lessons and quiz evaluations.

---

## Development and Verification

### Seeding Curriculum Data
To reset or populate the subject-specific structural JSON configurations, use:
```bash
python scratch/seed_nested_syllabi_final.py
```

### Content Validation
A custom verification suite is provided to scan all subjects under `knowledge-base/` for:
1.  Schema conformance (correct key sets, proper nested types).
2.  Latex syntax and escape checks (verifying that no invalid backslash characters break standard JSON parsers).
3.  Absolute file path exposures (checking for path leaks from local filesystems).
4.  Emoji usage (ensuring zero emojis exist in educational content to preserve academic tone).

Run the validation suite via:
```bash
python scratch/validate_ai_notes.py
```

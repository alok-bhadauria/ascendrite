# Ascendrite: Advanced Curriculum and Interactive Knowledge Infrastructure

Ascendrite is an enterprise-grade curriculum management and interactive learning platform designed to transform traditional, rigid course structures into granular, code-driven learning roadmaps. It prioritizes content depth, mathematical rigor, and progress-tracking analytics, providing a single source of truth for study materials.

---

## Codebase Architecture

The codebase is organized under a decoupled multi-tier architecture to maintain separation of concerns. This allows content databases, visualization systems, and tracking services to evolve independently.

```
ascendrite/
├── README.md                           # Core system documentation
├── docs/                               # Systems design and platform architecture specifications
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
│   ├── ai/                             # Artificial Intelligence subject category
│   │   ├── machine-learning/           # Machine Learning subject
│   │   ├── deep-learning/              # Deep Learning subject
│   │   ├── nlp/                        # Natural Language Processing subject
│   │   ├── genai/                      # Generative AI subject
│   │   └── ai-agents/                  # AI Agents and Orchestration subject
│   ├── core-cs/                        # Core Computer Science subject category
│   │   ├── dbms/                       # Database Management Systems subject
│   │   ├── sql/                        # Structured Query Language subject
│   │   ├── os/                         # Operating Systems subject
│   │   └── cn/                         # Computer Networks subject
│   ├── software-engineering/           # Software Engineering subject category
│   │   ├── java/                       # Java Programming subject
│   │   ├── oop/                        # Object-Oriented Programming subject
│   │   ├── dsa/                        # Data Structures and Algorithms subject
│   │   ├── spring-boot/                # Spring Boot framework subject
│   │   └── system-design/              # Distributed System Design subject
│   ├── web-development/                # Web Development subject category
│   │   ├── html-css-git/               # HTML, CSS, and Git version control subject
│   │   ├── javascript/                 # Core JavaScript subject
│   │   ├── css-frameworks/             # CSS Utility Frameworks subject
│   │   ├── reactjs/                    # ReactJS library subject
│   │   ├── nodejs-expressjs/           # NodeJS and ExpressJS backend subject
│   │   ├── typescript/                 # TypeScript language subject
│   │   └── nextjs/                     # Next.js framework subject
│   └── aptitude/                       # General Aptitude subject category
│       ├── quantitative-aptitude/      # Quantitative Aptitude mathematics subject
│       └── verbal-aptitude/            # Verbal Aptitude grammar and logic subject
├── platform/                           # Tracking platform code
│   ├── assets/                         # Static graphical and system assets
│   ├── client/                         # Next.js/React interactive tracking frontend
│   └── server/                         # Python API server and environment configuration
└── scratch/                            # Helper scripts, validation tools, and templates
```

---

## Core Subsystems

### 1. Decentralized Knowledge Base
Curriculum content is fully decentralized, machine-readable, and parsed offline. Each subject folder under `knowledge-base/` contains:
*   **`syllabus.json`**: The academic source of truth defining Modules -> Topics -> Subtopics.
*   **`subject-metadata.json`**: Theme colors, difficulty flags, and estimated learning times.
*   **`subject-map.json`**: Topic-level dependency trees and prerequisite resolution maps.
*   **`knowledge-assets.json`**: Curated bibliographies, glossary terms, and external citations.
*   **`book-metadata.json`**: Textbook-specific frontmatter, publisher details, and copyright licenses.

For every topic defined in the syllabus, a standardized seven-layer asset suite is generated strictly in JSON format (enforcing the omission of raw markdown and source code files from the database folders):
1.  **Notes (`notes/*.json`)**: Highly detailed textbook-grade lessons containing LaTeX-formatted mathematical equations and callout blocks (e.g., "Student Trap", "Engineering Note").
2.  **Revision (`revision/*.json`)**: High-density study cards summarizing key equations, algorithms, and concepts in structured fields.
3.  **Interview (`interview/*.json`)**: Staff-engineer level mock interview guides containing targeted questions, candidate traps, and optimal responses.
4.  **Examples (`examples/*.json`)**: Pure NumPy-based reference implementations (zero external runtime dependencies) showcasing the algorithms in action, wrapped in JSON string attributes.
5.  **Practice (`practice/*.json`)**: Code workspace templates containing algorithms to implement, along with built-in tests and verification logic in JSON.
6.  **Quiz (`quiz/*.json`)**: Multiple-choice assessment questions providing comprehensive diagnostic feedback.
7.  **Diagrams (`diagrams/*.json`)**: Structural diagram layouts mapped in code (e.g. Mermaid blocks) to be rendered dynamically by the web platform.

### 2. Editorial Standards
All content complies with the publishing constitution under the `editorial/` directory:
*   **Mathematical Style**: Enforces rigid LaTeX matrices. Scalars are italic ($z$), vectors are bold lowercase ($\mathbf{x}$), and parameter matrices are bold uppercase ($\mathbf{W}$). All LaTeX code inside JSON files is double-escaped to prevent parsing failures.
*   **Code Quality**: Enforces zero-dependency algorithmic implementations in pure Python or JavaScript using standard library elements, with no empty placeholders.
*   **Tone & Voice**: Written as a professional, expert-authored technical textbook, focusing on logical progression, continuous referencing, and removing duplication across the curriculum hierarchy.

---

## Development and Verification

### Seeding and Conversion
To convert any raw curriculum contents or consolidate markdown guides into the topic-by-topic JSON structure, execute:
```bash
python scratch/convert_curriculum_to_json.py
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

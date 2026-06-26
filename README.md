# Ascendrite: Advanced Curriculum and Interactive Knowledge Infrastructure

Ascendrite is an enterprise-grade curriculum management and interactive learning visualization platform. The system is designed to transform rigid, high-level course structures into granular, animated learning roadmaps, prioritizing content depth, mathematical rigor, and progress-tracking analytics.

---

## Architecture Overview

The codebase is organized under a decoupled multi-tier architecture to maintain separation of concerns. This allows content databases, visualization systems, and backend services to evolve independently.

```
ascendrite/
├── README.md                           # Core system documentation
├── docs/                               # System designs, UI/UX specifications, and content governance
├── knowledge-base/                     # Decentralized, portable subject repositories
│   ├── ai/                             # Artificial Intelligence & Machine Learning subjects
│   ├── software-engineering/           # Core programming & systems design subjects
│   ├── core-cs/                        # Traditional Computer Science foundations
│   ├── aptitude/                       # Quantitative and verbal evaluation modules
│   └── web-development/                # Modern application development frameworks
├── platform/                           # Animated, 3D-accelerated tracking frontend
└── backend/                            # Serverless API routes and AI model orchestrations
```

---

## Core Subsystems

### 1. Decentralized Knowledge Base

The curriculum content is completely decentralized, enabling porting and offline parsing. Each subject folder under `knowledge-base/` uses a standardized directory structure:

```
knowledge-base/<category>/<subject>/
├── syllabus.json                       # Nested subtopics, taxonomy, and metadata
├── notes/
│   └── notes.md                        # Rigorous study notes with LaTeX-formatted equations
├── quiz/                               # Multiple-choice evaluations for screening and verification
└── practice/                           # Practical exercise specifications, test cases, and solutions
```

*   **Syllabus Schema (`syllabus.json`)**: Configures the module hierarchy, topic IDs, specific industry-readiness focus areas, common student pitfalls, and revision tags.
*   **Study Notes (`notes/notes.md`)**: Contains deep mathematical proofs, matrix calculus derivations, and execution optimization notes, utilizing KaTeX/MathJax-compatible syntax for premium visual styling.
*   **Verification Suites (`quiz/`)**: Houses structured multiple-choice questions designed for self-assessment, gamified progression, and initial interview screening.
*   **Practical Workspace (`practice/`)**: Contains implementation specifications, test cases, and solution code blocks for hands-on, IDE-based user training.

### 2. Interactive Platform

The platform is designed to maximize engagement and clarity through high-fidelity visual representations of subject progression.
*   **Frontend Stack**: React and Next.js utilizing vanilla CSS for performance optimization and custom animation controls.
*   **Visualization Engine**: Renders interactive 3D syllabus maps and dynamic timelines representing node mastery.
*   **Tracking Dashboard**: Evaluates and displays progression metrics, tracking achievements, notes bookmarks, and completion status.

### 3. Service Layer

A lightweight orchestration backend supports data persistence and automation.
*   **Persistence Layer**: Integrates with MongoDB Atlas API to manage user-specific tracking states, quiz performance logs, and metadata.
*   **Asset Management**: Integrates with Cloudinary API for optimized serving of schema diagrams and LaTeX rendering assets.
*   **AI Integration**: Implements LangChain pipelines to provide context-aware query resolution, automatic coding evaluations, and personalized guidance based on curriculum nodes.

---

## Development and Verification

### Seeding Curriculum Data
To reset or populate the subject-specific `syllabus.json` files with the nested subtopic matrices, execute the curriculum seeding routine:
```bash
python scratch/seed_nested_syllabi_final.py
```

### Schema Integrity Verification
A custom testing suite is provided to ensure all decentralized syllabus files conform to JSON formatting rules, schema boundaries, and domain partition constraints. Execute the verification suite via:
```bash
python scratch/validate_json_syllabi.py
```

# Ascendrite Knowledge Base Architecture

Welcome to the architectural specifications and schema layout reference for the Ascendrite Knowledge Base.

---

## 1. Philosophy & Infrastructure Separation

To protect proprietary intellectual property and maintain database scaling boundaries, Ascendrite separates the knowledge base into two systems:
*   **Knowledge Infrastructure (Public)**: Contained inside this repository. Exposes schemas, templates, validation routines, build pipelines, indexes, and sample assets.
*   **Knowledge Assets (Private)**: Stored in a private, secure **Knowledge Storage** system. Includes the production notes, flashcards, quizzes, coding exercises, and diagrams.

The platform never directly reads educational files. Instead, all requests route through the **Knowledge Service** layer:

$$\text{Platform} \longrightarrow \text{Knowledge Service} \longrightarrow \text{Knowledge Storage} \longrightarrow \text{Private Knowledge Assets}$$

The Knowledge Service abstracts the physical storage engines, handling retrieval, validation, indexing, version selection, cache invalidation, capabilities verification, audit logs, and relationship resolution.

---

## 2. Directory Layout & Organization

The public `knowledge-base/` directory acts as the infrastructure repository. The existing educational content files residing under the domain subdirectories are migration candidates scheduled for transfer into the private storage system.

```
knowledge-base/
├── README.md                 # Constitutional entry point and specifications
├── domain-taxonomy.json      # Global categorization taxonomy (Domains, Disciplines)
├── knowledge-graph.json      # Structural semantic graph (Concepts, Prerequisites)
├── curriculum-map.json       # Progression map linking subjects to actual assets
│
├── schemas/                  # JSON Schema Draft 2020-12 verification templates
│   ├── subject.schema.json   # Validates subject metadata and theme configs
│   ├── curriculum.schema.json# Validates topic lists and module sequencing
│   ├── topic.schema.json     # Validates reading materials and asset maps
│   ├── revision.schema.json  # Validates flashcard deck models
│   ├── interview.schema.json # Validates mock interview recitations
│   ├── example.schema.json   # Validates code examples DTOs
│   ├── practice.schema.json  # Validates practice test configurations
│   └── quiz.schema.json      # Validates multiple-choice quiz parameters
│
└── [domain-folder]/          # Migration Candidate Folders (e.g. ai, core-cs, software-engineering)
    └── [discipline-folder]/  # Discipline subfolders (e.g. machine-learning under ai)
        └── [subject-folder]/ # Subject directories (e.g. deep-learning)
            ├── subject.json  # Core subject metadata file
            ├── curriculum.json# Subject module and topic sequence mapping
            └── [topic-folder]/# Granular topic directories (e.g. neural-networks)
                ├── notes.json    # Theoretical notes and explanations
                ├── revision.json # Summary flashcard arrays
                ├── interview.json# Recitations and follow-up challenges
                ├── examples.json # Code example blocks
                ├── practice.json # Practice skeletons and test scripts
                └── quiz.json     # Multiple-choice diagnostic quizzes
```

---

## 3. Permanent Identifier Strategy

To prevent database link breakage when files are renamed, slugs change, or directories move, Ascendrite enforces an immutable identifier naming strategy:
*   **UUID Persistence**: Every Domain, Subject, Module, Topic, and Concept is assigned a globally unique, prefix-based identifier (e.g., `subj_0182390a`, `top_0192837f`).
*   **Filesystem Independence**: Database entries map to these identifiers. File paths may evolve, but the identifiers remain frozen once published.
*   **Referential Integrity**: All relational models (such as prerequisites or related links) reference these identifiers exclusively.

---

## 4. Universal Metadata Model

Every JSON file in the knowledge base must inherit from the Universal Metadata Model. The root properties of all assets must include the following keys:

```json
{
  "id": "string (prefix-based UUID)",
  "slug": "string (kebab-case route identifier)",
  "title": "string (display name)",
  "description": "string (concise summary)",
  "version": "string (semver format e.g. 1.0.0)",
  "schema_version": "string (semver format e.g. 2.0.0)",
  "language": "string (ISO 639-1 code e.g. en)",
  "status": "string (draft | review | published | deprecated)",
  "visibility": "string (public | internal | restricted)",
  "difficulty": "string (Beginner | Medium | Hard | Advanced)",
  "estimated_learning_time": "integer (minutes)",
  "prerequisites": "array (list of prerequisite IDs)",
  "learning_outcomes": "array (list of Bloom verbs and statements)",
  "tags": "array (list of index tags)",
  "keywords": "array (list of search keywords)",
  "authors": "array (list of author IDs)",
  "reviewers": "array (list of moderator IDs)",
  "created_at": "string (ISO 8601 UTC timestamp)",
  "updated_at": "string (ISO 8601 UTC timestamp)",
  "references": "array (list of standard specification URLs)",
  "relationships": "object (entity relational mappings)"
}
```

---

## 5. Metadata Inheritance Model

To prevent redundant definitions, metadata properties inherit downward through the taxonomy hierarchy:

```
[Domain]
  │ (defines global taxonomy categories)
  ▼
[Discipline]
  │ (provides subject grouping boundaries)
  ▼
[Subject]
  │ (defines dynamic theme colors, language, and default difficulty)
  ▼
[Module]
  │ (sequences topic paths, aggregates total learning hours)
  ▼
[Topic]
  │ (defines specific concept nodes, tools, and visual frameworks)
  ▼
[Concept]
  │ (defines granular testing coordinates)
  ▼
[Asset]
    (inherits properties, specifying only format-specific structures)
```

---

## 6. Relationship & Semantic Graph Architecture

Relationships are represented dynamically inside the `relationships` metadata block. This structure allows the platform to build semantic learning paths without reading the core text:

*   **`prerequisites`**: List of IDs that must be completed prior to initialization.
*   **`dependencies`**: System packages, library versions, or compilers required for execution.
*   **`recommended_progression`**: Adjacent topic IDs suggested for subsequent study.
*   **`related_topics`**: Mapped topic IDs sharing similar conceptual tags.
*   **Asset Linkages**: Explicit references mapping to helper assets:
    *   `example_links`: Associated code implementation files.
    *   `diagram_links`: Mermaid visualization maps.
    *   `practice_links`: Testing skeleton files.
    *   `assessment_links`: MCQ diagnostic files.
    *   `revision_links`: Flashcard review arrays.
    *   `interview_links`: Technical interview preparation files.
    *   `project_links`: Cumulative module project files.

---

## 7. AI-Oriented Metadata Schema

To support future Retrieval-Augmented Generation (RAG) pipelines and multi-agent indexing:

*   `embedding_status`: String indicating if vector layers have been computed (`pending | indexed`).
*   `vector_identifier`: String reference to the database vector coordinate.
*   `summary`: A high-density paragraph summarizing technical concepts for LLM context injection.
*   `token_estimate`: Integer tracking prompt token weights.
*   `reading_level`: Floating value representing explanation complexity indexes.
*   `concept_weight`: Float ($0.0 \le w \le 1.0$) defining importance of this topic in the parent discipline.
*   `retrieval_priority`: Integer ($0 \le p \le 10$) prioritizing RAG context selection.
*   `confidence_score`: Float indicating accuracy validation confidence.
*   `citation_quality`: String grading source references documentation (e.g. `RFC-authoritative`).

---

## 8. Learning & Educational Intelligence Metadata

These fields support the platform's personalization, recommendation, and progress tracking systems:

*   `bloom_level`: Integer ($1$ to $6$) matching cognitive objectives.
*   `cognitive_objective`: Explicit description of targeted cognitive shifts.
*   `knowledge_type`: Enum mapping to `Factual | Conceptual | Procedural | Metacognitive`.
*   `industry_relevance`: Float rating how frequently this skill is used in production systems.
*   `interview_frequency`: Float rating how often this topic appears in technical interviews.
*   `revision_priority`: Enum determining flashcard scheduler prioritization.
*   `project_relevance`: Float mapping concepts to actual project tasks.
*   `estimated_mastery_time`: Integer representing estimated study time required to achieve mastery.

---

## 9. Ingestion & Publishing Workflow

The knowledge base relies on validation tools during publishing pipelines to enforce standards:
1.  **Local Schema Check**: Changes to files must pass `pytest` schema tests validating against files under `schemas/`.
2.  **Graph Integrity Linting**: The pipeline runs integrity checks verifying that all referenced IDs are registered and contain no circular loops.
3.  **Moderation Acceptance**: Changes must be approved via the moderation queue before merging.
4.  **Index Compilation**: Merges to `main` compile active entries into the unified `curriculum-map.json` and `knowledge-graph.json` files, updating the database.

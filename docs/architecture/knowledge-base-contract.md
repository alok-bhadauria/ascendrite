# Ascendrite Knowledge Base Contract

This document serves as the formal specification and directory constitution governing the Ascendrite Knowledge Base. Every validator, ingestion engine, content exporter, and runtime interface must comply with this contract.

---

## 1. Directory Structure Specifications

The knowledge base is structured as a hierarchical directory tree under the `knowledge-base/` root folder:

```
knowledge-base/
├── platform-structure.json       # Index of all categories and subjects
├── domain-taxonomy.json          # Dictionary of domain concept tags
├── curriculum-map.json           # Prerequisite mapping indices
└── [category-slug]/              # e.g., software-engineering/
    └── [subject-slug]/           # e.g., java/
        ├── subject-metadata.json # Subject profiles and configuration
        ├── syllabus.json         # Topological modules and topics structure
        ├── subject-map.json      # Routing links and indexes
        ├── knowledge-assets.json # External readings and publications
        ├── book-metadata.json    # PDF compilation watermark and layout rules
        ├── notes/                # Comprehensive topic notes JSONs
        ├── revision/             # Bullet-point study guides
        ├── interview/             # Flashcard interview Q&A blocks
        ├── quiz/                 # Multiple-choice exam JSONs
        ├── practice/             # Code challenges and exercises
        ├── examples/             # Code example configurations
        └── diagrams/             # Mermaid conceptual diagrams
```

### Folder Purpose Descriptions
*   `notes/`: Core study guide documents representing the textbook reference content.
*   `revision/`: Dense bullet points for revision.
*   `interview/`: Stacks of recall cards featuring interview questions.
*   `quiz/`: Core topic assessments.
*   `practice/`: Structural coding labs.
*   `examples/`: Sample setups showing execution patterns.
*   `diagrams/`: Graphical architectures using Mermaid syntax.

---

## 2. Naming Conventions

All directory names, file names, and identifiers must be deterministic and comply with lowercase kebab-case naming parameters.

*   **Directories**: Only lowercase alphanumeric characters and hyphens: `^[a-z0-9]+(-[a-z0-9]+)*$` (e.g. `software-engineering`).
*   **Files**: Filenames must match the canonical identifier of the resource they represent, followed by `.json` (e.g. topic `java-m1-t1` resides in `notes/java-m1-t1.json`).
*   **Slugs**: Must be lowercased and contain no spaces or special characters except hyphens.

---

## 3. Canonical Identifier Rules

Identifiers act as permanent coordinate systems and must never change after creation. Relocation of a topic or asset is managed via database deprecation, never by rewriting an ID.

*   **Subject ID**: `[subject-slug]` (e.g., `java`).
*   **Module ID**: `[subject-slug]-m[module-number]` (e.g., `java-m1`).
*   **Topic ID**: `[subject-slug]-m[module-number]-t[topic-number]` (e.g., `java-m1-t1`).
*   **Asset ID**: Mapped to their type abbreviations:
    - *Quiz*: `[topic-id]-quiz` (e.g., `java-m1-t1-quiz`).
    - *Diagram*: `[topic-id]-dia[N]` (e.g., `java-m1-t1-dia1`).
    - *Example*: `[topic-id]-ex[N]` (e.g., `java-m1-t1-ex1`).
    - *Practice*: `[topic-id]-prac[N]` (e.g., `java-m1-t1-prac1`).

---

## 4. JSON Schema Contracts

Every document is formatted as a JSON object containing required structural fields and metadata.

### 4.1 Subject Metadata (`subject-metadata.json`)
*   **Required Fields**: `id`, `slug`, `display_name`, `theme` (object with `primary_color`, `secondary_color`), `difficulty`, `estimated_hours`.
*   **Optional Fields**: `description`.

### 4.2 Syllabus (`syllabus.json`)
*   **Required Fields**: `subject_id`, `modules` (array of modules containing `module_id`, `title`, `topics`), `prerequisites_map` (key-value mapping of prerequisites).
*   **Constraint**: Topics listed in the syllabus must have matching files in the `notes/` directory.

### 4.3 Notes (`notes/[topic-id].json`)
*   **Required Fields**: `topic_id`, `subject_id`, `title`, `learning_outcomes` (list), `content_sections` (array of title, content, callouts).
*   **Relational Bindings**: `topic_id` must match file name prefix.

### 4.4 Quiz (`quiz/[topic-id]-quiz.json`)
*   **Required Fields**: `quiz_id` (matches file name), `questions` (array of `question_id`, `text`, `options`, `correct_answer`, `explanation`).

---

## 5. Asset Type Specifications

| Asset Type | Purpose | Primary Content Element |
| :--- | :--- | :--- |
| **`notes`** | Concepts learning text. | Markdown string sections. |
| **`revision`** | Memory retention triggers. | Summary card sections list. |
| **`interview`** | Active recall testing. | Stacks of Question/Answer cards. |
| **`quiz`** | Multiple choice assessment. | Multiple choices options. |
| **`practice`** | Practical codings labs. | Boilerplate code & test specs. |
| **`examples`** | Practical blueprint setups. | Fully runnable code files. |
| **`diagrams`** | Flow diagrams. | Mermaid markdown strings. |

---

## 6. Cross-Reference & Linkage Rules

1.  **Ownership Hierarchy**: Every asset belongs to exactly one topic. Every topic belongs to exactly one subject. Every subject belongs to exactly one category.
2.  **Concept Mapping**: Notes may reference tag concepts defined globally in `domain-taxonomy.json`. Referencing undefined concepts is prohibited.
3.  **Asset References**: If a topic JSON lists an example asset under its resources, the matching example JSON file must exist under the `examples/` directory.
4.  **No Orphans**: Files inside `notes/`, `quiz/`, `practice/`, `examples/`, `diagrams/`, `revision/`, or `interview/` directories that are not registered in their subject's `syllabus.json` are orphans and will be flagged as validation errors.

---

## 7. Versioning Rules

-   **`schema_version`**: Incremented when JSON keys or data topologies are added or altered. Validated dynamically by validator rules.
-   **`content_version`**: Incremented during edits. Does not affect parser execution unless minor compatibility thresholds are broken.
-   **Deprecation Policy**: Obsolete assets are marked with `is_deprecated: true` but retained in database snapshots until major release migrations.

---

## 8. Validation Rules

The Validation Engine must enforce the following checks without warnings:
1.  **ID Mismatch**: Resource ID inside JSON payload must equal file name prefix.
2.  **Naming Violations**: File names and IDs must comply with kebab-case conventions.
3.  **Duplicate IDs**: Two files cannot share the same canonical ID.
4.  **Circular Prerequisites**: A topic cannot require a prerequisite that directly or indirectly requires the topic itself.
5.  **Broken Links**: Ref references (e.g. concept mappings) must point to existing records in root indices.
6.  **Missing Metadata**: Documents must contain `schema_version` and valid metadata timestamps.

---

## 9. Ingestion Pipeline Workflow

1.  **Scan**: Reads directory trees recursively, sorting targets by category and subject.
2.  **Parse**: Validates syntax, deserializes files to memory models.
3.  **Validate**: Evaluates structural and cross-reference constraints.
4.  **Dry Run**: Returns test outputs without executing database mutations.
5.  **Apply**: Executes bulk transactions using MongoDB upserts.
6.  **Rollback**: Restores original state if exceptions occur.

---

## 10. Export Serialization Rules

1.  **Strict Indentation**: Formatted with exactly 2-space indentation.
2.  **Key Ordering**: Keys inside exported JSON documents are sorted alphabetically.
3.  **Unicode Safety**: Non-ASCII characters (e.g. LaTeX brackets) are preserved in UTF-8 encoding.

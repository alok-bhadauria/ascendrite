# Knowledge Base Integration: Parsing Pipelines and Asset Validation

---

## 1. Decentralized Ingestion Pipeline
Ascendrite implements a portable, git-friendly content database architecture. The entire curriculum resides in `knowledge-base/` using structured JSON templates. 

During API server startup, an ingestion parser scans the categories:

```
[Server Startup]
  |
  +-- Read subject folder directories (ai/, core-cs/, web-development/, etc.)
  +-- Locate and validate 'syllabus.json' structures
  +-- Parse subject-metadata, subject-map, and knowledge-assets
  +-- Load and parse notes, revision, interview, example, practice, quiz, and diagrams JSON files
  +-- Compile into an in-memory curriculum cache (hash-map search indices)
```

By keeping the curriculum cache in-memory, content searches and lesson routing runs at $O(1)$ lookup time, entirely bypassing database latency.

---

## 2. Global Metadata Layer & Mapping

To transition from a folder-reliant ingestion layout to a fully metadata-driven systems architecture, Ascendrite integrates a global metadata layer at the root of `knowledge-base/`.

### 2.1 Metadata File Specifications

1.  **`platform-structure.json`**: Bridges physical directory paths to logical category and subject IDs.
    *   *System Responsibility*: Eliminates hardcoded category folders. The parser queries this file to find directories and load assets dynamically.
    *   *Future Scalability*: Relocating folders or changing storage schemes requires zero backend modifications; only this index file requires updates.
2.  **`domain-taxonomy.json`**: Defines the timeless academic domains, disciplines, and subject groupings.
    *   *System Responsibility*: Establishes standard categorization boundaries. Represents pure classification rather than sequential teaching paths.
    *   *Future Scalability*: Adapts to any educational taxonomy change without altering curriculum mapping or server parsing engines.
3.  **`knowledge-graph.json`**: Represents concepts and their semantic dependencies.
    *   *System Responsibility*: Maps conceptual nodes (e.g. Vector Space, SVD, Event Loop) and topological edges (e.g. `prerequisite_of`, `extends`).
    *   *Future Scalability*: Powers interactive graph visualizers, AI learning recommendations, and vector database/RAG retrieval pipelines.
4.  **`curriculum-map.json`**: Connects conceptual nodes with actual practice materials.
    *   *System Responsibility*: Maps progression order. Sequences modules and topics for students and links topics directly to conceptual graph nodes.
    *   *Future Scalability*: Enables customizable/dynamic learning paths. For instance, creating a fast-track or deep-dive learning track simply requires creating a new curriculum mapping layout referencing the same conceptual nodes.

### 2.2 Local Subject Metadata
*   **`syllabus.json`**: Structures the hierarchy (Modules -> Topics -> Subtopics) using strict unique ID vectors.
*   **`subject-metadata.json`**: Customizes client theme color codes, course levels, and learning budgets.
*   **`subject-map.json`**: Implements topological sorting to map prerequisite path constraints:
    ```json
    {
      "topic_id": "cn-m3-t1",
      "prerequisites": ["cn-m2-t5", "cn-m2-t4"]
    }
    ```
    The client evaluates user progress records against this map to lock/unlock downstream lessons.

---

## 3. Dynamic Diagram & Source Code Embedding
Since all curriculum assets are JSON, structural visual diagrams and running code strings are represented using serialization formatting:
*   **Diagrams (`diagrams/*.json`)**: Contain a `code` string block mapped using Mermaid format. The web client reads this block and compiles the syntax into a responsive SVG diagram.
*   **Examples (`examples/*.json`)**: Contain executable scripts wrapped in JSON blocks. The API server serves these strings, enabling the web client to render them inside a custom editor widget.

---

## 4. Content Validation Suite & Schema Enforcement

To prevent invalid formatting and design regression in production bundles, Ascendrite runs a multi-stage validation check:

### 4.1 JSON Schema Validation (Draft 2020-12)
All files under `knowledge-base/` are subject to validation schemas residing under `knowledge-base/schemas/`. These files use the JSON Schema Draft 2020-12 standard to ensure support for modern constraints, recursive references, and future schema updates:
*   `subject.schema.json`: Validates canonical subject configuration settings and theme definitions.
*   `curriculum.schema.json`: Validates subject-specific syllabus module/topic mappings.
*   `topic.schema.json`: Validates detail notes, outcome lists, and callout matrices.
*   `revision.schema.json`: Validates revision cheat-sheet flashcards.
*   `interview.schema.json`: Validates interview prep questions and answers.
*   `example.schema.json` & `practice.schema.json`: Validate executable code assets.
*   `quiz.schema.json`: Validates multiple-choice diagnostic options and explanations.

### 4.2 Cross-Repository Integrity Validation (`validate_knowledge_integrity.py`)
A custom verification script checks repository-wide integrity, mapping, and key relationships across metadata files. This runner detects:
1.  **Orphaned References**: Subject or concept IDs referenced in the taxonomy or curriculum mapping that do not exist physically in the codebase.
2.  **Duplicate Identifiers**: Duplicate module, topic, or asset IDs across different subjects.
3.  **Broken Asset Mappings**: Logical asset IDs inside `curriculum-map.json` that cannot be resolved physically via `platform-structure.json` mappings.
4.  **Inconsistent Metadata**: Mismatches between index keys and local subject configs.

### 4.3 Content Compilation Validation (`validate_ai_notes.py`)
The pre-commit content runner enforces basic formatting rules:
1.  **JSON Validation**: Verifies that standard parser deserialization executes cleanly.
2.  **Emoji Verification**: Rejects any files containing Unicode emoji blocks to preserve a professional, academic tone.
3.  **Local Path Safety**: Checks for absolute paths or protocol leaks.
4.  **Schema Consistency**: Verifies that files match expected styles and formats.

### 4.4 Subject Metadata Evolution Strategy
To support progression without breaking API endpoints, changes to subject configuration parameters follow a clear evolution path:
*   **Canonical Properties**: The new standardized properties (e.g. `id`, `slug`, `display_name`, `theme`, `estimated_hours`) are treated as the canonical source of truth for new components and API responses.
*   **Legacy Fields Deprecation**: Old parameters (e.g. `subject_id`, `name`, `estimated_learning_hours`, `subject_theme_colors`) are preserved temporarily for backward compatibility. They are formally marked as deprecated, and are scheduled for removal in future versions once all consumers migrate.


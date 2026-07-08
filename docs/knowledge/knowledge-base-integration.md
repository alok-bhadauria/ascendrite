# Knowledge Base Integration: Parsing Pipelines and Asset Validation

## Document Metadata
*   **Purpose**: Outlines the knowledge ingestion pipelines, global metadata indexes, JSON Schema validation systems, and pre-commit checks.
*   **Scope**: Governs subject folders ingestion, schema validation files, and repository integrity checks.
*   **Intended Audience**: Knowledge engineers, content contributors, and backend platform developers.
*   **Related Documents**:
    *   [Product Philosophy](../governance/product-philosophy.md)
    *   [Learning Philosophy](../governance/learning-philosophy.md)
    *   [Directory Structure](../governance/directory-structure.md)
*   **Ownership**: Knowledge Systems Architect & Head of Editorial Division

---

## 1. Decentralized Ingestion Pipeline
The platform shall ingest a git-friendly offline content database residing in `knowledge-base/`:
*   **Server Startup Loading**: During initialization, the ingestion parser must read directories, compile syllabus layout trees, and parse lesson profiles.
*   **Curriculum Memory Cache**: Parsed data structures shall be loaded into a read-only memory cache (hash-map indices). The API must serve curriculum queries directly from this cache to ensure $O(1)$ response latency.
*   **Decoupled Directories**: The ingestion system must not hardcode category names or subject directory names. Path locations must be dynamically resolved from the configuration files.

---

## 2. Global Metadata Mapping Architecture
The ingestion parser and presentation clients shall resolve structures using the four core global metadata indexes residing at the root of `knowledge-base/`:

1.  **`platform-structure.json`**: Maps physical directories and file naming configurations.
    *   *System Rule*: Decouples application routes from storage systems.
2.  **`domain-taxonomy.json`**: Defines the academic classification hierarchy tree (Domain -> Discipline -> Subject Group -> Subject).
    *   *System Rule*: Restricts to academic classifications. It must not contain modules, topics, or asset references.
3.  **`knowledge-graph.json`**: Models conceptual concept nodes and dependency links.
    *   *System Rule*: Contains aliases, keywords, and relationship edge strengths.
4.  **`curriculum-map.json`**: Details curriculum progressions and sequences.
    *   *System Rule*: Binds subjects, modules, and topics to logical asset IDs, avoiding duplicate taxonomy definitions.

---

## 3. Local Subject Metadata & Progression Rules
*   **`syllabus.json`**: Standardizes the course tree (Modules -> Topics -> Subtopics) utilizing unique, immutable topic IDs.
*   **`subject-metadata.json`**: Configures colors, estimated hours, and difficulty.
*   **`subject-map.json`**: Implements topological sorting to map prerequisite path constraints. The client must evaluate student progress records against this map to dynamically lock or unlock downstream topics.

---

## 4. Quality Control & Schema Enforcement
To prevent design regression, the system must enforce a multi-stage validation check before commits:

### 4.1 JSON Schema Validation (Draft 2020-12)
All files under `knowledge-base/` must validate against the schemas inside `knowledge-base/schemas/` adhering to the JSON Schema Draft 2020-12 standard:
*   `subject.schema.json`: Validates subject-metadata configurations.
*   `curriculum.schema.json`: Validates course syllabi.
*   `topic.schema.json`: Validates text details, outcomes, and callout sections.
*   `revision.schema.json` & `interview.schema.json`: Validate flashcards and Q&As.
*   `example.schema.json` & `practice.schema.json`: Validate runnable code blocks.
*   `quiz.schema.json`: Validates diagnostic assessments and answer keys.

### 4.2 Integrity Checks
*   **Cross-Repository Verification**: A validation script (`validate_knowledge_integrity.py`) must scan metadata indexes to detect orphaned IDs, duplicate values, or broken asset links.
*   **Sanitization Rules**: Content runners (`validate_ai_notes.py`) must reject files containing Unicode emojis, absolute paths, or unescaped characters.

### 4.3 Subject Metadata Evolution
*   **Canonical Properties**: New systems shall query canonical fields (`id`, `slug`, `display_name`, `theme`, `estimated_hours`, `difficulty`).
*   **Legacy Preservation**: Legacy fields (`subject_id`, `name`, `estimated_learning_hours`, `subject_theme_colors`) must remain in configuration files for backward compatibility. They are deprecated and scheduled for removal in future versions.

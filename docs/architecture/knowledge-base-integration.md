# Knowledge Base Integration: Parsing Pipelines and Asset Validation

## Document Metadata
*   **Purpose**: Outlines the knowledge ingestion pipelines, global metadata indexes, JSON Schema validation systems, and pre-commit checks.
*   **Scope**: Governs subject folders ingestion, schema validation files, and repository integrity checks.
*   **Intended Audience**: Knowledge engineers, content contributors, and backend platform developers.
*   **Related Documents**:
    *   [Product Philosophy](../governance/product-philosophy.md)
    *   [Learning Philosophy](../governance/learning-philosophy.md)
    *   [Directory Structure](../development/repository-structure.md)
*   **Ownership**: Knowledge Systems Architect & Head of Editorial Division

---

## 1. Decentralized Ingestion Pipeline & Source of Truth

The knowledge base operates in two distinct lifecycle stages:

1.  **Initial Migration Phase**: The platform reads the static, git-friendly content database from the repository `knowledge-base/`. A validation pipeline validates, indexes, and ingests these records into the MongoDB database.
2.  **Post-Ingestion Production Phase**: MongoDB becomes the **sole authoritative source of truth** for all curriculum data. The original repository folder is no longer maintained. Content editing, curation, and moderation occur directly within the platform's database.

*   **Runtime Exports**: When backups or offline packages are required, runtime exports are generated from MongoDB and written to the untracked runtime directory `ascendrite-data/knowledge-base/`.
*   **Historical Snapshots**: Archive snapshots of taxonomy versions can be exported and archived inside `ascendrite-private/` for recovery.
*   **Curriculum Memory Cache**: Serving endpoints query a read-only memory cache populated from MongoDB at startup, ensuring $O(1)$ response latency.
*   **Decoupled Directories**: Path structures and domain taxonomy groupings are resolved dynamically from configurations, avoiding hardcoded path targets.

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

---

## 5. Runtime Migration Toolkit

To facilitate the initial import and ongoing export loops of knowledge, a runtime Migration Toolkit is maintained as an operational utility.

*   **Location**: Resides in `ascendrite-data/migration-toolkit/` (outside Git repository).
*   **Toolkit Utilities**:
    - **Knowledge Import**: Reads repository schema layouts and writes verified content objects to the MongoDB instance.
    - **Knowledge Export**: Exports active MongoDB curriculum catalogs as portable JSON packages into `ascendrite-data/knowledge-base/`.
    - **Integrity Validation**: Runs topological audits, prerequisites checks, and checks for DAG loops against the live database state.
    - **Operational Reports**: All output results, migration telemetry, and diagnostics are logged to `ascendrite-data/migration-toolkit/reports/`. The old top-level `migrations/` directory has been deprecated and removed.

# Ascendrite Migration Toolkit Architecture Reference

This document serves as the authoritative architectural specification and runtime blueprint for the Ascendrite Migration Toolkit.

---

## 1. Goals & Principles

The Migration Toolkit is an administrative utility designed to manage the lifecycle of curriculum knowledge assets. It is responsible for migrating local, version-controlled markdown/JSON assets into MongoDB collections while verifying database fidelity against repository sources.

### Core Objectives
*   **Decoupled Runtime**: Lives outside the main client/server application codebases.
*   **Idempotency**: Runs multiple times without duplicate insertions or unnecessary updates.
*   **Absolute Verification**: Proves that MongoDB records represent the local files with 100% integrity.
*   **Graceful Degradation**: Recovers safely if database environments lack transactional replica sets.

---

## 2. Directory Layouts

### Repository Layout
The toolkit source code is decoupled from the main app workspace and lives in the untracked runtime directory:
```
G:\Projects\ascendrite-data\migration-toolkit/
├── requirements.txt
├── cli.py                     # Click CLI entry point
├── config.py                  # Pydantic configuration module
├── constants.py               # default path strings & variables
├── logger.py                  # Logger pipeline (writes console & run files)
├── core/
│   ├── scanner.py             # File scanner
│   ├── parser.py              # Pydantic schema parser
│   ├── validator.py           # Semantic graph validator
│   ├── dry_run.py             # Ingestion planner
│   ├── importer.py           # MongoDB apply engine
│   ├── verifier.py            # Integrity checker
│   └── utils.py               # UTC clocks, SHA hashing, & WorkspaceManager
├── models/
│   └── schemas.py             # Subject, Syllabus, Topic, Asset models
├── validators/
│   └── common.py
├── reports/                   # Timestamped execution logs & summaries
└── tests/
    └── test_toolkit.py        # Integration & unit tests
```

---

## 3. The Ingestion Pipeline

The pipeline runs sequentially, using the output of each phase to proceed:

```
[Local files] ──► Scanner ──► Parser ──► Validator ──► Dry Run ──► Apply ──► MongoDB
```

### Module Responsibilities
1.  **Scanner (`scanner.py`)**: Walks the `knowledge-base/` category subdirectories. Identifies all JSON assets, parses file-size and timestamps, and registers them in `repository-manifest.json`.
2.  **Parser (`parser.py`)**: Deserializes raw files into Pydantic models. Resolves parent relationships (`subject_id`, `topic_id`) dynamically from file path locations to decouple document contents from locations.
3.  **Validator (`validator.py`)**: Performs semantic validation checking for circular prerequisites (DFS solver), naming conventions compliance, broken taxonomy pointers, and orphaned assets.
4.  **Dry Run Engine (`dry_run.py`)**: Formulates mock import plans specifying simulated collection inserts, updates, and errors without executing writes.
5.  **Apply Engine (`importer.py`)**: Persists graph nodes to MongoDB using `replace_one(..., upsert=True)`. Sets operational metadata (`migrated_at`) and falls back gracefully to sequential writes if transactions fail.
6.  **Verifier Engine (`verifier.py`)**: Extracts database payloads, cross-references them against local graph states, and reports mismatches or missing elements.

---

## 4. Ingestion & Verification Strategies

### Idempotency Strategy
The importer uses the resource's canonical ID (`id` or `subject_id`) as query key matches. It reads existing records and compares payloads (ignoring dynamic metadata timestamps). If identical, the write is skipped, maintaining sub-second verification runs.

### Transactions Fallback
Ingestion writes are wrapped in multi-document transactions. On local, standalone MongoDB instances lacking replica sets, the engine catches transactional exceptions, issues a warning, and executes fallback sequential writes safely.

---

## 5. CLI Usage & Reports

### Subcommands
*   `dry-run`: Runs scanner, parser, validator, and logs ingestion plans.
*   `apply`: Persists validated local files into the database.
*   `verify`: Audits MongoDB state against repository files.

### Report Outputs (`reports/` folder)
*   `repository-manifest.json`: Scanned file catalog.
*   `parser-report.json`: Serialization error records.
*   `validation-report.json`: Semantic links results.
*   `migration-summary.json` & `migration-report.json`: Write metrics.
*   `verification-summary.json` & `verification-report.json`: Count mismatch audits.
*   `human-readable-migration.md` & `human-readable-verification.md`: Markdown logs.

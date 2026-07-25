# Developer Automation & Database Scripts

This directory houses automation utilities, schema initializers, and seeding scripts to configure the local Ascendrite database ecosystems.

---

## 1. Core Automation Utilities

### 1.1 Database Initializer (`init_databases.py`)
Configures all backend tables, collections, indices, and baseline credentials:
*   **PostgreSQL**: Checks for the target application database, connects using administrative credentials, and executes the relational table schemas defined in [init_postgres.sql](init_postgres.sql).
*   **MongoDB**: Establishes unique indices (e.g. `email` on `users`, compound keys on `user_identities`, and `subject_id/topic_id` matches) to ensure database integrity.
*   **User Seeding**: Seeds local testing accounts (cleans existing records first to allow updates to credentials configurations):
    - **Admin**: `admin@ascendrite.com` / `Admin@123`
    - **Contributor**: `creator@ascendrite.com` / `Creator@123`
    - **Student**: `learner@ascendrite.com` / `Learner@123`

### 1.2 Curriculum Ingestion Seeder (`seed_database.py`)
Scans knowledge catalog folders and populates MongoDB collections:
*   **Taxonomy parsing**: Reads subject profiles (`subject-metadata.json`) and course modules syllabuses (`syllabus.json`) under category paths.
*   **Text content updates**: Reads topic markdown notes (`notes/*.json`) and writes them directly into the document store.

---

## 2. Configuration Settings

The curriculum seeder resolves path locations using **[local-seeds.json](../config/local-seeds.json)**:
```json
{
  "kb_path": "platform/server/app/knowledge-base",
  "categories": [
    "ai",
    "core-cs",
    "software-engineering",
    "web-development"
  ]
}
```

---

## 3. How to Run Scripts

Run these utilities from the virtualenv environment inside `platform/server/`:

### 3.1 Initialize Databases
Runs schema DDL setup and seeds test accounts:
```bash
python ../../scripts/init_databases.py
```

### 3.2 Ingest Curriculum Metadata
Imports courses syllabuses and notes:
```bash
python ../../scripts/seed_database.py --config ../../config/local-seeds.json
```

### 3.3 Interactive Launch Console
Alternatively, developers can execute both scripts sequentially inside the **Ascendrite Platform Manager** console by booting `./run-ascendrite.bat` and choosing option `[8] Initialize & Seed Databases`.

# Ascendrite Developer Setup Guide

Welcome to the Ascendrite engineering team! This guide provides everything a new developer needs to configure their workstation, boot the stack, and verify curriculum integrity.

---

## 1. Prerequisites & Required Software

Ensure you have the following system software installed and added to your system `PATH`:
*   **Python**: Version `3.10.11` (specifically mapped inside virtual environments).
*   **Node.js**: Version `18+` (npm package manager).
*   **PostgreSQL**: Version `18` (Running on default port `5432`).
*   **MongoDB**: Version `7.0+` (Running on default port `27017`).
*   **Redis / Memurai**: Cache server (Running on default port `6379`).
*   **RustFS**: Local storage service (Running on port `9000` / Console on `9001`).

---

## 2. Directory Taxonomy & Boundaries

Ascendrite separates repository source codes from volatile data and private secrets:

```
G:\Projects\
├── ascendrite/                  # [GIT] Application codebase & docs
├── ascendrite-data/             # [UNTRACKED] Runtime storage, logs, & Migration Toolkit
└── ascendrite-private/          # [UNTRACKED] Credentials, certificates, & keys
```

### Path Constraints
*   **Repository Boundaries**: Source code files should remain strictly portable and resolve paths dynamically.
*   **Runtime Boundaries**: Log outputs, database dumps, and temporary workspace files reside under `ascendrite-data/`.
*   **Private Secrets**: Encryption passwords and keys must remain inside `ascendrite-private/secrets/` and must never be committed to Git.

---

## 3. Configuration Setup

1.  Navigate to the repository root directory `ascendrite/`.
2.  Duplicate the template configuration contract `.env.example` as a new file named `.env.local`.
3.  Update the database passwords and identities inside `.env.local` to match your local PostgreSQL and MongoDB credentials. Keep the variables identical in structure and ordering to `.env.example`.

---

## 4. Booting the Application Stack

The platform is designed around a single, unified orchestration entry point.

### Running the Manager
Double-click or run the primary batch file from your command line:
```powershell
.\run-ascendrite.bat
```

### Startup Summary Workflow
1.  **Environment Check**: Validates path bindings and directory mappings.
2.  **Infrastructure Services**: Automatically queries Windows services (`postgresql-x64-18`, `MongoDB`, `Memurai`, `RustFS`). If the local RustFS service is not found, it runs the minimized background fallback script `scripts/services/rustfs-start.bat`.
3.  **App Spawners**: Spawns the Backend FastAPI application on port `8000` and the Client SPA on port `5173`.
4.  **URLs Console**: Option `[6]` opens Swagger documentation and frontend interfaces in your browser.

---

## 5. Ingestion Pipeline & Validation

Curriculum contents are managed locally inside `knowledge-base/` category folders. To sync changes to MongoDB, run the administrative toolkit:

### Ingestion Commands
Navigate to `G:\Projects\ascendrite-data\migration-toolkit/` using the platform's python environment:
```powershell
# Simulate and validation checks
python cli.py dry-run

# Persist repository changes into MongoDB
python cli.py apply

# Verify database matches repository files exactly
python cli.py verify
```

### Preflight Sanity Checks
Ensure no documentation format regressions occur by running the local validation tools:
```powershell
python scratch/validate_docs_standards.py
python scratch/validate_knowledge_integrity.py
python scratch/validate_ai_notes.py
```

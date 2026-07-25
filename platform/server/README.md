# Ascendrite Backend Domain Engine

This directory contains the FastAPI modular monolith backend REST API engine for the Ascendrite platform.

---

## 1. Architectural Structure

The backend engine follows a strict **Clean Architecture / Layered Domain** pattern to maintain clear module boundaries:
*   **API Layer (`app/api/`)**: Exposes endpoint controllers, handles route serialization, and resolves dependency injections.
*   **Service Layer (`app/modules/*/services/`)**: Enforces validation invariants, manages content transition lifecycles, and triggers database transactions.
*   **Repository Layer (`app/modules/*/repositories/`)**: Abstracted datastore gateways ensuring entities interact with databases via agnostic interface contracts.
*   **Domain Models Layer (`app/modules/*/models/`)**: Defines pure data models, validation constraints, and database formats.

---

## 2. Core Domain Modules

*   **`authentication`**: Handles secure cookie-backed JWT login sessions, refresh token rotations, and tokens audit logs.
*   **`users`**: Manages human and AI actor identities, credentials records, and platform roles (Student, Contributor, Admin).
*   **`knowledge`**: Manages curriculum taxonomies, subjects, syllabi, modules, and topic notes schemas.
*   **`learning`**: Manages learner progress Mastered completions maps, notes, and study planners.
*   **`creator`**: Manages editing workspaces, draft updates, and moderator-approval publishing workflows.
*   **`collaboration`**: Handles discussion comment threads and workspace task assignments.
*   **`administration`**: Manages global system configs (e.g. maintenance flags) and aggregates diagnostic stats.

---

## 3. Database Responsibilities

To optimize read/write performance, the engine segregates data across storage layers:
*   **PostgreSQL**: relational schema database housing transactional records (users, identities, sessions, settings, comments).
*   **MongoDB**: document catalog containing subjects, syllabuses, modules, topics, and notes text materials.
*   **Redis**: memory database cache serving transient rate limit configurations and telemetries.
*   **S3 (RustFS)**: local-first object storage for curriculum assets and uploads.

---

## 4. Development Workflow

Ensure your `.env.local` configuration is set up at the repository root before running commands.

### 4.1 Set up Local Virtual Environment
Boot the Python virtualenv and install project dependencies:
```bash
python -m venv .venv
# Activate on Windows:
.venv\Scripts\activate
# Activate on macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

### 4.2 Start API Server
Launches the FastAPI application locally on port `8000`:
```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```
Exposes documentation directories dynamically:
*   **Interactive Swagger UI**: `http://127.0.0.1:8000/docs`
*   **ReDoc specifications**: `http://127.0.0.1:8000/redoc`

### 4.3 Run Integration Tests
Executes the pytest test suite checking core router endpoints:
```bash
python -m pytest -v
```
Tests automatically use isolated connection databases and purge mock data documents upon lifecycle completion.

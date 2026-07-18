# Backend Architecture Compass

This document serves as the authoritative implementation guide and architectural reference for the Ascendrite backend server.

---

## 1. Modular Organization

All backend server modules live under `platform/server/app/` and follow strict modular monolith and clean architecture decoupling rules:

```
platform/server/app/
├── api/                       # API Controllers and endpoints routing (v1)
├── core/                      # Constants, error models, settings, and password/JWT security
├── infrastructure/            # Technical adapters to external systems
│   ├── database/              # PostgreSQL and MongoDB connection drivers
│   └── storage/               # RustFS external object storage interfaces
├── modules/                   # Self-contained domain-bounded contexts
│   ├── users/                 # Profile and role repository models and schemas
│   ├── authentication/        # User session lifecycle and authorization flows
│   ├── knowledge/             # Subject, Syllabus, Topic, Asset documents repositories
│   ├── learning/              # Enrollment tracks, topic completion, bookmarks services
│   ├── assessments/           # Quiz evaluation rules and submission scores
│   └── analytics/             # System activity telemetry audits
├── middleware/                # Custom HTTP interceptors (exceptions)
└── utils/                     # Shared general utilities
```

### Rules of Dependency Flow
1.  **Strict Upward Imports Only**: A lower module must never import from a higher module.
2.  **Service Isolation**: Controllers can only import from `services/` or Pydantic `schemas/`. They must never access repositories or models directly.
3.  **Repository Isolation**: Services access databases strictly through interface-decoupled repository objects.

---

## 2. Implemented Foundation Status

*   **FastAPI application bootstrap**: Centralized application factory patterns inside `app/main.py` with async lifespan context hooks.
*   **Database access layer**: Ready-to-use engine connection configurations for PostgreSQL (`postgres.py` using SQLAlchemy sessionmakers) and MongoDB (`mongodb.py` using MotorClient).
*   **Decoupled storage layers**: Storage bucket abstractions mapped under `app/infrastructure/storage/rustfs.py`.
*   **Security Foundation**: Hashing algorithms and JWT signing helpers mapped under `app/core/security.py`.
*   **API Response Standards**: Exception interceptor middleware (`app/middleware/exceptions.py`) converting custom core errors (`app/core/errors.py`) to unified JSON outputs.

## 3. Configuration & Provider Architecture

### A. Configuration Precedence & Profile Helpers
Configurations are strongly typed and resolved from:
1.  **Environment Variables**: Overrides local configurations in production.
2.  **Root `.env.local`**: Custom developer configuration values.
3.  **Application Defaults**: Preconfigured fallback settings.

The active runtime profile (`APP_ENV`) exposes helper query properties:
*   `is_development`: Development environment.
*   `is_testing`: Pytest sandbox context.
*   `is_production`: Production container runtime environment.
*   `is_feature_enabled(name)`: Operations check for feature toggles.

### B. Feature Flags Classification
Feature flags are structured configurations prefixing operational and developer rules:
*   **Operational Flags**: `FEATURE_ENABLE_AI`, `FEATURE_ENABLE_BACKGROUND_WORKERS`, `FEATURE_ENABLE_EMAIL`.
*   **Development Flags**: `FEATURE_ENABLE_SEARCH`, `FEATURE_ENABLE_REGISTRATION`, `FEATURE_ENABLE_ANALYTICS`.

### C. Provider Interfaces Abstraction
External infrastructure drivers are decoupled behind abstract provider interfaces:
*   **`StorageProvider`**: Decouples binary payload interactions. Swaps implementations (Local `RustFS` $\rightarrow$ AWS S3 $\rightarrow$ Azure Blob) without editing business modules.
*   **`AIProvider`**: Decouples Generative model queries. Swaps implementations (OpenAI $\rightarrow$ Gemini $\rightarrow$ Ollama) for RAG curriculum processing.

Provider concrete implementations are bound to API endpoints dynamically using FastAPI native dependency injection (`Depends`), preventing service locator anti-patterns.

---

## 4. Operational Foundation

### A. Endpoint Responsibilities
*   `GET /api/v1/health`: Consolidates overall system health contract (timestamp, uptime, version, dependencies).
*   `GET /api/v1/health/liveness`: Fast process check returning simple status (used by load balancers and orchestrators).
*   `GET /api/v1/health/readiness`: Validates active database connection reachability (PostgreSQL, MongoDB).
*   `GET /api/v1/system/metadata`: Consolidates non-sensitive runtime attributes (Python version, build channel, startup timestamp).

### B. Security Classification
*   **PUBLIC**: `/api/v1/health/liveness` & `/api/v1/system/metadata`. Open to public telemetry services. No sensitive system variables or connection settings are exposed.
*   **INTERNAL**: `/api/v1/health` & `/api/v1/health/readiness`. Restricted to cloud network clusters or internal VPC access to protect detailed system health metrics and latency records.
*   **AUTHENTICATED / ADMIN**: Diagnostic tracing endpoints (future) require bearer tokens and admin capabilities.

### C. Request Lifecycle & Correlation
1.  **Ingress**: The request interceptor middleware retrieves or generates a unique correlation UUID (`X-Correlation-ID`).
2.  **Propagation**: The correlation ID is stored in a thread-safe `contextvars` context local.
3.  **Logging**: Every system log printed during request processing automatically references the request's correlation ID.
4.  **Egress**: The middleware appends `X-Correlation-ID` and `X-Process-Time` to response headers, mapping the correlation tracker into the response payload on exceptions.

### D. Structured Logging
In production, standard logging formats logs as JSON records containing:
*   `timestamp` (ISO 8601 UTC)
*   `level` (Severity level)
*   `request_id` (Correlation tracker)
*   `route` (Called path)
*   `duration_ms` (Time elapsed)
*   `message` (Log body)

---

## 5. Development Commands

### Running unit and config tests
Run pytest from the backend workspace root directory:
```powershell
python-venv-3.10.11\Scripts\python.exe -m pytest -v tests
```

### Running uvicorn local development server
```powershell
python-venv-3.10.11\Scripts\uvicorn main:app --host 127.0.0.1 --port 8000
```

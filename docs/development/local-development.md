# Local Development

## Document Metadata
*   **Purpose**: Details workspace initialization steps, system prerequisites, database setups, and runtime commands.
*   **Scope**: Governs developer machine configurations and local emulation utilities.
*   **Intended Audience**: All software engineers, quality assurance testers, and coding agents.
*   **Related Documents**:
    *   [Environment Configuration](environment-configuration.md)
    *   [Repository Structure](repository-structure.md)
*   **Ownership**: Operations Coordinator & Lead DevOps Engineer

---

## 1. Local Prerequisites

Before initializing the workspace, ensure your developer machine has the following tools installed:
*   **Docker & Docker Compose**: For running containerized database services.
*   **Python**: Version 3.10 or higher.
*   **Node.js**: LTS version (v18 or higher) with `npm`.
*   **Git**: For version control.

---

## 2. Workspace Initialization

Run the following setup commands to clone the repository and initialize project dependencies:

```bash
# Clone the repository
git clone git@github.com:ascendrite/platform.git
cd platform

# Initialize backend dependencies
cd backend
python -m venv .venv
source .venv/bin/activate  # Or .venv\Scripts\activate on Windows
pip install -r requirements.txt

# Initialize frontend dependencies
cd ../frontend
npm install
```

---

## 3. Database Services

To start local database container services:

```bash
# Run from repository root directory
docker-compose -f docker-compose.dev.yml up -d
```
This launches containerized MongoDB and Redis instances.

---

## 4. Ingesting Mock Syllabus Data

Before running tests or client applications, load mock knowledge bases:

```bash
# Execute local database seed script
python scripts/seed_database.py --config config/local-seeds.json
```
This validates and imports domain schemas from the `knowledge-base/` folder.

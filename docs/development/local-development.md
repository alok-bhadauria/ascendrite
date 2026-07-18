# Local Development

## Document Metadata
*   **Purpose**: Details workspace initialization steps, system prerequisites, local Windows services configurations, and runtime commands.
*   **Scope**: Governs developer machine configurations and local emulation utilities.
*   **Intended Audience**: All software engineers, quality assurance testers, and coding agents.
*   **Related Documents**:
    *   [Environment Configuration](environment-configuration.md)
    *   [Repository Structure](repository-structure.md)
*   **Ownership**: Operations Coordinator & Lead DevOps Engineer

---

## 1. Local Prerequisites & Directory Philosophy

Local development enforces a strict boundary separation between binaries, application code, runtime state data, and private/sensitive developer assets:

```
E:\Softwares\
    Third-party software, database binaries, executables, SDKs, CLIs,
    and service wrappers (e.g. E:\Softwares\RustFS\, E:\Softwares\Amazon\AWSCLIV2\).

E:\Projects\Ascendrite\ (Repository - Tracked in Git)
    Active source repository, frontend/backend application codebase, 
    scripts, and schemas.

E:\Projects\ascendrite-data\ (Runtime Data - Outside Git)
    Persistent local database files, backups, active catalogs, logs, 
    and the Migration Toolkit operational utilities.

E:\Projects\ascendrite-private\ (Private Assets - Outside Git)
    Local secrets, credentials registries, certificates, and historical 
    knowledge archive snapshots.
```

Ensure your developer machine has the following utilities installed:
*   **Python**: Version 3.10.x (specifically matching verified Python 3.10.11 runtime).
*   **Node.js**: LTS version (v18 or higher) with `npm`.
*   **Git**: For version control.
*   **AWS CLI**: Version 2.35.19 (installed under `E:\Softwares\Amazon\AWSCLIV2`) for S3 compatibility testing.

---

## 2. Workspace Initialization

Run the following setup commands to clone the repository and initialize project dependencies:

```bash
# Clone the repository
git clone git@github.com:alok-bhadauria/ascendrite.git
cd Ascendrite

# Initialize backend dependencies
cd platform/server
python -m venv .venv
source .venv/bin/activate  # Or .venv\Scripts\activate on Windows
pip install -r requirements.txt

# Initialize frontend dependencies
cd ../client
npm install

# Initialize local environment configuration (Repository Root)
cd ../..
copy .env.example .env.local  # Or 'cp .env.example .env.local' on macOS/Linux
# (Edit .env.local manually to populate local database passwords)
```

---

## 3. Local Windows Services Setup

Ascendrite uses native Windows services in the local development environment rather than Docker containers. The following database and storage engines must be configured:

### 3.1 PostgreSQL 18.4
*   **Service Name**: `postgresql-x64-18` (or target active PG service)
*   **Host/Port**: `127.0.0.1:5432`
*   **Management**: Manage via Windows Services console (`services.msc`) or command line:
    ```cmd
    net start postgresql-x64-18
    net stop postgresql-x64-18
    ```

### 3.2 MongoDB Community Server 8.0.26
*   **Service Name**: `MongoDB`
*   **Host/Port**: `127.0.0.1:27017`
*   **Management**:
    ```cmd
    net start MongoDB
    net stop MongoDB
    ```

### 3.3 Memurai Developer Edition 4.2.3 (Redis API 7.4.9)
*   **Service Name**: `Memurai`
*   **Host/Port**: `127.0.0.1:6379`
*   **Management**:
    ```cmd
    net start Memurai
    net stop Memurai
    ```

### 3.4 RustFS 1.0.0-beta.8 (S3-Compatible Object Storage)
*   **Service Name**: `AscendriteRustFS` (managed via WinSW wrapper `AscendriteRustFS.exe`)
*   **API / Console**: `127.0.0.1:9000` (Console: `127.0.0.1:9001`)
*   **Persistent Data Path**: `E:\Projects\ascendrite-data\rustfs\data`
*   **Management**:
    *   Via Windows Service:
        ```cmd
        net start AscendriteRustFS
        ```
    *   Via manual launcher batch script:
        ```cmd
        E:\Projects\Ascendrite\scripts\services\rustfs-start.bat
        ```

---

## 4. Ingesting Curriculum Metadata

Before running tests or client applications, load mock knowledge bases:

```bash
# Execute local database seed script
python scripts/seed_database.py --config config/local-seeds.json
```
This validates and imports domain taxonomy schemas from the `knowledge-base/` folder into MongoDB.

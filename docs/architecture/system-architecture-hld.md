# High-Level Design (HLD): Software Architecture and Scalability Planning

---

## 1. High-Level Architecture Overview
Ascendrite utilizes a decoupled multi-tier architecture to maintain separation of concerns. This ensures content delivery, user tracking, and execution sandboxes can scale independently.

```
+-------------------------------------------------------------+
|                     User Browser / Client                   |
|  - ReactJS SPA / Client-side rendering                      |
|  - Interactive visualizers (Canvas, SVGs, CSS animations)   |
+-------------------------------------------------------------+
                              |
                     REST API Calls (HTTPS)
                              |
                              v
+-------------------------------------------------------------+
|                      API Gateway / Reverse Proxy            |
|  - SSL termination, load balancing, rate limiting           |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|                      FastAPI App Servers                    |
|  - Stateless execution instances                            |
|  - Ingests decentralized JSON knowledge-base                |
|  - Progress logging, auth verification, progress compute    |
+-------------------------------------------------------------+
               |                               |
        MongoDB Queries                  Local Disk Reads
               |                               |
               v                               v
+------------------------------+ +----------------------------+
|        MongoDB Atlas         | |  JSON Knowledge Base Files |
|  - Users, progress, quizzes  | |  - Notes, revision, etc.   |
+------------------------------+ +----------------------------+
```

---

## 2. Layered Modular System Design
To ensure the platform remains technology-agnostic and maintains loose coupling, the API server follows a Clean Architecture layout divided into four layers:

```
+-------------------------------------------------------------------+
| 1. Routing / Presentation Layer (FastAPI APIRouters, DTOs)        |
+-------------------------------------------------------------------+
                                 |
                                 v
+-------------------------------------------------------------------+
| 2. Application Service Layer (Business rules, progress math)      |
+-------------------------------------------------------------------+
                                 |
                                 v
+-------------------------------------------------------------------+
| 3. Abstraction Interface Layer (Repository, DB/Storage Interface) |
+-------------------------------------------------------------------+
                                 |
                                 v
+-------------------------------------------------------------------+
| 4. Data / Infrastructure Layer (MongoDB Driver, OS File Access)   |
+-------------------------------------------------------------------+
```

### Dependency Inversion Rule
No inner layer can possess dependency references to an outer layer. All data access occurs via Abstract Base Classes (ABCs) defined in the Interface Layer. This ensures we can swap the infrastructure layer (e.g. migrating from MongoDB to PostgreSQL) without modifying business logic in the Service Layer.

---

## 3. Scalability Planning
The platform is designed to scale horizontally across multiple instances:
*   **Stateless Execution:** API servers store zero session state or local data. All session state is stored in JWT tokens and database storage. This allows us to spin up infinite server instances behind a round-robin load balancer.
*   **Database Scaling:** MongoDB Atlas utilizes replica sets for read scaling, with the path to configure sharding clusters for write scaling as volume expands.
*   **CDN Caching:** The static JSON knowledge-base assets (notes, revision cards, schemas) are compiled and cached on Content Delivery Networks (CDNs) at the edge, reducing server loads to dynamic state API calls (progress logs, auth validations).

---

## 4. Deployment Architecture
The target production deployment topology relies on cloud-native orchestration:
*   **Containerization:** The API server and React client are packaged into separate Docker container images to isolate dependencies.
*   **Orchestration (Kubernetes):** Containers are deployed onto a Kubernetes cluster (EKS/GKE). A replica set manages pod scaling, and an Ingress controller routes traffic.
*   **CI/CD Pipelines:** Automated pipelines (GitHub Actions) execute lints, run the validation script `validate_ai_notes.py`, build Docker images, and deploy containers on main branch merges.

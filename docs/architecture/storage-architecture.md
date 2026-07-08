# Storage Architecture

## Document Metadata
*   **Purpose**: Defines the platform storage architecture, local folder layouts, and object persistence boundaries.
*   **Scope**: Governs backend local storage directories, vector store indexing layouts, and caching layers.
*   **Intended Audience**: Backend software engineers, database administrators, and operations engineers.
*   **Related Documents**:
    *   [Backend Architecture](backend-architecture.md)
    *   [Database Schema](database-schema.md)
*   **Ownership**: Lead Storage Architect & Head of Platform Engineering

---

## 1. Storage Boundaries

Ascendrite separates storage into logical layers, ensuring complete isolation between system code, public knowledge catalogs, and personal user files. The platform utilizes three distinct storage categories:

*   **Knowledge Assets Storage**: Contains version-controlled educational JSON schemas and syllabus maps.
*   **Workspace Storage**: Holds personal files, scratchpads, user-uploaded resources, and configuration settings.
*   **Vector Embeddings Storage**: Stores high-dimensional vector representations of knowledge assets to support semantic retrieval.

---

## 2. Directory Layout Specs

Local storage paths on backend instances follow a strict hierarchical structure to maintain clean separation and ease backup operations:

```
/var/lib/ascendrite/
├── knowledge/            # Immutable, versioned system syllabus data
│   └── catalogs/         # Domain, discipline, and subject JSON assets
├── workspaces/           # Stateful actor workspace files
│   └── [actor_id]/       # Sandboxed storage per learner/author
│       ├── files/        # Uploaded resources and notes
│       └── scratch/      # Temporary execution and scratchpad scripts
└── cache/                # Volatile session and lock data (Redis-backed)
```

---

## 3. Vector Database Indexing

For semantic search and Retrieval-Augmented Generation (RAG):
*   Vector embeddings are computed using unified embedding models and indexed in a vector store.
*   The schema indexes concept definitions and module metadata, mapping high-dimensional vectors to corresponding catalog IDs.
*   Updates to knowledge assets trigger asynchronous index rebuild runs, ensuring context accuracy.

---

## 4. Cache Persistence Rules

To minimize database read latencies, Redis is deployed as a high-speed volatile cache:
*   Session validation tokens are stored with an explicit Time-to-Live (TTL) expiration boundary.
*   Frequently queried catalog indices are cached in memory and invalidated automatically upon content publication.

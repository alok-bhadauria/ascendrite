# Database Schema: Database Architecture and Storage Layout

## Document Metadata
*   **Purpose**: Details the datastore schemas, indexes, collections configurations, and database abstractions.
*   **Scope**: Governs backend datastore queries, model schemas, and data persistence layers.
*   **Intended Audience**: Database administrators, backend engineers, and systems architects.
*   **Related Documents**:
    *   [Backend Architecture](backend-architecture.md)
    *   [Security Standards](../security/security-standards.md)
*   **Ownership**: Head of Platform Engineering

---

## 1. Database Architecture
The platform datastore holds user metadata, progress logs, quiz submissions, and settings. The system is designed to separate business operations from physical driver engines:
*   **Flexible Ingestion**: Real-time progress structures are modeled using documents matching nested hierarchy models.
*   **Decoupled Driver**: The database is accessed exclusively via interface layers (Repository Pattern), ensuring the core service layer remains agnostic of whether the database is SQL (PostgreSQL) or NoSQL (MongoDB Atlas).

---

## 2. Collection Schemas and Entity Models

### 2.1 `users` Collection
Stores user profiles, roles, and authentication hashes. The role mapping must support Version 1 actors and maintain compatibility for reserved enterprise extensions:
```json
{
  "_id": "ObjectId",
  "email": "string (unique)",
  "password_hash": "string",
  "first_name": "string",
  "last_name": "string",
  "role": "string (Guest | Learner | Moderator | Admin | Recruiter | Organization | Organization Member)",
  "is_deleted": "boolean (soft delete support)",
  "created_at": "ISODate",
  "updated_at": "ISODate"
}
```

### 2.2 `progress` Collection
Tracks dynamic progress maps for users.
```json
{
  "_id": "ObjectId",
  "user_id": "ObjectId",
  "subject_id": "string (kebab-case)",
  "completed_topics": [
    {
      "topic_id": "string",
      "completed_at": "ISODate",
      "duration_seconds": "integer",
      "quiz_score": "float (percentage)"
    }
  ],
  "last_active_at": "ISODate"
}
```

### 2.3 `quiz_submissions` Collection
Logs answer histories for assessments.
```json
{
  "_id": "ObjectId",
  "user_id": "ObjectId",
  "topic_id": "string",
  "score": "integer",
  "total_questions": "integer",
  "answers": [
    {
      "question_id": "string",
      "selected_option": "integer",
      "is_correct": "boolean"
    }
  ],
  "submitted_at": "ISODate"
}
```

---

## 3. Indexing Strategy
To ensure database operations complete within sub-millisecond response windows, the database engine must enforce these index configurations:
*   `users`: A unique, single-field index on `email` to accelerate authentication lookups.
*   `progress`: A compound, unique index on `(user_id, subject_id)` to quickly load and cache active subject records.
*   `quiz_submissions`: A compound index on `(user_id, topic_id)` to track diagnostic score profiles.

---

## 4. Repository Abstraction and SQL Swappability
API services must not call database drivers directly. 
*   **Abstraction Interface**: Interface classes define data retrieval methods using abstract methods.
*   **Decoupled Driver**: Switching from NoSQL schemas to SQL tables (such as PostgreSQL) shall require only creating a new repository implementation class conforming to the base interfaces, keeping application services unmodified.
*   **Soft Deletion**: The datastore must implement soft-deletion schemas (`is_deleted: true`) for user profiles to comply with security auditing requirements.

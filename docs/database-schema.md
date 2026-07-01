# Database Schema: Database Architecture and Storage Layout

---

## 1. Database Architecture
Ascendrite utilizes **MongoDB Atlas** for progress tracking, user settings, and session storage. The document-oriented layout matches hierarchical learning data structures (such as progress profiles and quiz submissions) while providing high-performance read/write characteristics.

---

## 2. Collections and Document Schemas

### `users` Collection
Stores user account profiles, authentication hashes, and roles.
```json
{
  "_id": "ObjectId",
  "email": "string (unique)",
  "password_hash": "string",
  "first_name": "string",
  "last_name": "string",
  "role": "string (Student | Contributor | Admin)",
  "created_at": "ISODate",
  "updated_at": "ISODate"
}
```

### `progress` Collection
Logs topic progress metrics for users.
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

### `quiz_submissions` Collection
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
To ensure query latency remains sub-millisecond as scaling occurs, the database maintains these indices:
*   `users`: Unique index on `email` to accelerate authentication and guarantee username uniqueness.
*   `progress`: Compound index on `(user_id, subject_id)` to quickly fetch subject progress states.
*   `quiz_submissions`: Index on `(user_id, topic_id)` to fetch score history profiles.

---

## 4. Repository Abstraction Layer
To prevent framework locking, database accesses must not directly write MongoDB driver commands inside application code. Data access is abstracted using a repository interface:

```python
class UserRepository(ABC):
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    async def save(self, user: User) -> User:
        pass
```

This interface is implemented inside the infrastructure layer (`MongoUserRepository`), allowing migration to SQL databases by creating a new `SQLAlchemyUserRepository` implementation without breaking application services.

# Migration Mapping Report — Backend Consolidation

This document catalogs the path transitions during the Stage 1.5 consolidation.

## Path Changes Mappings
*   `app/models/user.py` -> `app/modules/users/models/user.py`
*   `app/repositories/user.py` -> `app/modules/users/repositories/user.py`
*   `app/schemas/user.py` -> `app/modules/users/schemas/user.py`
*   `app/services/auth.py` -> `app/modules/authentication/services/auth.py`
*   `app/services/curriculum.py` -> `app/modules/knowledge/services/curriculum.py`
*   `app/models/progress.py` -> `app/modules/learning/models/progress.py`
*   `app/repositories/progress.py` -> `app/modules/learning/repositories/progress.py`
*   `app/schemas/progress.py` -> `app/modules/learning/schemas/progress.py`
*   `app/services/progress.py` -> `app/modules/learning/services/progress.py`
*   `app/models/quiz_submission.py` -> `app/modules/assessments/models/quiz_submission.py`
*   `app/repositories/quiz_submission.py` -> `app/modules/assessments/repositories/quiz_submission.py`
*   `app/schemas/quiz_submission.py` -> `app/modules/assessments/schemas/quiz_submission.py`
*   `app/database/postgres.py` -> `app/infrastructure/database/postgres.py`
*   `app/database/mongodb.py` -> `app/infrastructure/database/mongodb.py`
*   `app/database/redis.py` -> `app/infrastructure/database/redis.py`
*   `app/storage/rustfs.py` -> `app/infrastructure/storage/rustfs.py`

## Folders Deleted
*   `platform/server/api/` (duplicate root folder)
*   `platform/server/core/` (duplicate root folder)
*   `platform/server/models/` (duplicate root folder)
*   `platform/server/repositories/` (duplicate root folder)
*   `platform/server/schemas/` (duplicate root folder)
*   `platform/server/services/` (duplicate root folder)
*   `app/models/` (consolidated)
*   `app/repositories/` (consolidated)
*   `app/schemas/` (consolidated)
*   `app/services/` (consolidated)
*   `app/database/` (consolidated)
*   `app/storage/` (consolidated)

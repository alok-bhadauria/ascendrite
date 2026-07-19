from abc import ABC, abstractmethod
from typing import Any, List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.modules.assessments.models.results import AssessmentResultModel
from app.repositories.base import BaseRepository

class AssessmentResultRepository(BaseRepository[AssessmentResultModel], ABC):
    @abstractmethod
    async def get_by_session(self, session_id: str) -> Optional[AssessmentResultModel]:
        pass

    @abstractmethod
    async def get_by_user(self, user_id: Any) -> List[AssessmentResultModel]:
        pass

class MongoAssessmentResultRepository(AssessmentResultRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["assessment_results"]

    def _to_db_doc(self, model: AssessmentResultModel) -> dict:
        doc = model.model_dump(by_alias=True, exclude={"id"})
        # Convert keys
        for key in ["user_id"]:
            if key in doc and doc[key] is not None:
                val = doc[key]
                if isinstance(val, str) and ObjectId.is_valid(val):
                    doc[key] = ObjectId(val)
                elif not isinstance(val, ObjectId):
                    try:
                        doc[key] = ObjectId(str(val))
                    except Exception:
                        pass
        return doc

    def _to_query_id(self, val: Any) -> Any:
        if isinstance(val, str) and ObjectId.is_valid(val):
            return ObjectId(val)
        return val

    async def get_by_id(self, id: Any) -> Optional[AssessmentResultModel]:
        try:
            doc = await self.collection.find_one({"_id": self._to_query_id(id)})
            return AssessmentResultModel(**doc) if doc else None
        except Exception:
            return None

    async def get_by_session(self, session_id: str) -> Optional[AssessmentResultModel]:
        try:
            doc = await self.collection.find_one({"session_id": session_id})
            return AssessmentResultModel(**doc) if doc else None
        except Exception:
            return None

    async def get_by_user(self, user_id: Any) -> List[AssessmentResultModel]:
        try:
            cursor = self.collection.find({"user_id": self._to_query_id(user_id)})
            return [AssessmentResultModel(**doc) for doc in await cursor.to_list(length=100)]
        except Exception:
            return []

    async def get_all(self) -> List[AssessmentResultModel]:
        cursor = self.collection.find()
        return [AssessmentResultModel(**doc) for doc in await cursor.to_list(length=100)]

    async def create(self, entity: AssessmentResultModel) -> AssessmentResultModel:
        doc = self._to_db_doc(entity)
        result = await self.collection.insert_one(doc)
        entity.id = str(result.inserted_id)
        return entity

    async def update(self, id: Any, entity: AssessmentResultModel) -> Optional[AssessmentResultModel]:
        doc = self._to_db_doc(entity)
        result = await self.collection.replace_one({"_id": self._to_query_id(id)}, doc)
        if result.matched_count:
            return entity
        return None

    async def delete(self, id: Any) -> bool:
        result = await self.collection.delete_one({"_id": self._to_query_id(id)})
        return result.deleted_count > 0

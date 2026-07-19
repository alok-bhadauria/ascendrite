from abc import ABC, abstractmethod
from typing import Any, List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.modules.collaboration.models.team import TeamModel, TeamMembershipModel
from app.repositories.base import BaseRepository

class TeamRepository(BaseRepository[TeamModel], ABC):
    @abstractmethod
    async def get_by_owner(self, owner_id: Any) -> List[TeamModel]:
        pass

class MongoTeamRepository(TeamRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["collaboration_teams"]

    def _to_db_doc(self, model: TeamModel) -> dict:
        doc = model.model_dump(by_alias=True, exclude={"id"})
        for key in ["owner_id"]:
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

    async def get_by_id(self, id: Any) -> Optional[TeamModel]:
        try:
            doc = await self.collection.find_one({"_id": self._to_query_id(id)})
            return TeamModel(**doc) if doc else None
        except Exception:
            return None

    async def get_by_owner(self, owner_id: Any) -> List[TeamModel]:
        try:
            cursor = self.collection.find({"owner_id": self._to_query_id(owner_id)})
            return [TeamModel(**doc) for doc in await cursor.to_list(length=100)]
        except Exception:
            return []

    async def get_all(self) -> List[TeamModel]:
        cursor = self.collection.find()
        return [TeamModel(**doc) for doc in await cursor.to_list(length=100)]

    async def create(self, entity: TeamModel) -> TeamModel:
        doc = self._to_db_doc(entity)
        result = await self.collection.insert_one(doc)
        entity.id = str(result.inserted_id)
        return entity

    async def update(self, id: Any, entity: TeamModel) -> Optional[TeamModel]:
        doc = self._to_db_doc(entity)
        result = await self.collection.replace_one({"_id": self._to_query_id(id)}, doc)
        if result.matched_count:
            return entity
        return None

    async def delete(self, id: Any) -> bool:
        result = await self.collection.delete_one({"_id": self._to_query_id(id)})
        return result.deleted_count > 0


class TeamMembershipRepository(BaseRepository[TeamMembershipModel], ABC):
    @abstractmethod
    async def get_by_team(self, team_id: Any) -> List[TeamMembershipModel]:
        pass

    @abstractmethod
    async def get_by_user(self, user_id: Any) -> List[TeamMembershipModel]:
        pass

    @abstractmethod
    async def get_membership(self, team_id: Any, user_id: Any) -> Optional[TeamMembershipModel]:
        pass

class MongoTeamMembershipRepository(TeamMembershipRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["collaboration_team_memberships"]

    def _to_db_doc(self, model: TeamMembershipModel) -> dict:
        doc = model.model_dump(by_alias=True, exclude={"id"})
        for key in ["team_id", "user_id", "invited_by"]:
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

    async def get_by_id(self, id: Any) -> Optional[TeamMembershipModel]:
        try:
            doc = await self.collection.find_one({"_id": self._to_query_id(id)})
            return TeamMembershipModel(**doc) if doc else None
        except Exception:
            return None

    async def get_by_team(self, team_id: Any) -> List[TeamMembershipModel]:
        try:
            cursor = self.collection.find({"team_id": self._to_query_id(team_id)})
            return [TeamMembershipModel(**doc) for doc in await cursor.to_list(length=100)]
        except Exception:
            return []

    async def get_by_user(self, user_id: Any) -> List[TeamMembershipModel]:
        try:
            cursor = self.collection.find({"user_id": self._to_query_id(user_id)})
            return [TeamMembershipModel(**doc) for doc in await cursor.to_list(length=100)]
        except Exception:
            return []

    async def get_membership(self, team_id: Any, user_id: Any) -> Optional[TeamMembershipModel]:
        try:
            doc = await self.collection.find_one({
                "team_id": self._to_query_id(team_id),
                "user_id": self._to_query_id(user_id)
            })
            return TeamMembershipModel(**doc) if doc else None
        except Exception:
            return None

    async def get_all(self) -> List[TeamMembershipModel]:
        cursor = self.collection.find()
        return [TeamMembershipModel(**doc) for doc in await cursor.to_list(length=100)]

    async def create(self, entity: TeamMembershipModel) -> TeamMembershipModel:
        doc = self._to_db_doc(entity)
        result = await self.collection.insert_one(doc)
        entity.id = str(result.inserted_id)
        return entity

    async def update(self, id: Any, entity: TeamMembershipModel) -> Optional[TeamMembershipModel]:
        doc = self._to_db_doc(entity)
        result = await self.collection.replace_one({"_id": self._to_query_id(id)}, doc)
        if result.matched_count:
            return entity
        return None

    async def delete(self, id: Any) -> bool:
        result = await self.collection.delete_one({"_id": self._to_query_id(id)})
        return result.deleted_count > 0

from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.modules.knowledge.models.academic import SubjectModel, SyllabusModel, ModuleModel, TopicModel, StructuralState
from app.modules.knowledge.repositories.base import SubjectRepository, SyllabusRepository, ModuleRepository, TopicRepository

class MongoSubjectRepository(SubjectRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["subjects"]

    async def create(self, subject: SubjectModel) -> SubjectModel:
        doc = subject.model_dump(by_alias=True)
        await self.collection.insert_one(doc)
        return subject

    async def get_by_id(self, subject_id: str) -> Optional[SubjectModel]:
        doc = await self.collection.find_one({"_id": subject_id})
        return SubjectModel(**doc) if doc else None

    async def update(self, subject_id: str, subject: SubjectModel) -> SubjectModel:
        doc = subject.model_dump(by_alias=True)
        await self.collection.replace_one({"_id": subject_id}, doc)
        return subject

    async def list_all(self) -> List[SubjectModel]:
        cursor = self.collection.find({"status": {"$ne": StructuralState.DELETED.value}})
        docs = await cursor.to_list(length=100)
        return [SubjectModel(**doc) for doc in docs]


class MongoSyllabusRepository(SyllabusRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["syllabuses"]

    async def create(self, syllabus: SyllabusModel) -> SyllabusModel:
        doc = syllabus.model_dump(by_alias=True)
        await self.collection.insert_one(doc)
        return syllabus

    async def get_by_id(self, syllabus_id: str) -> Optional[SyllabusModel]:
        doc = await self.collection.find_one({"_id": syllabus_id})
        return SyllabusModel(**doc) if doc else None

    async def update(self, syllabus_id: str, syllabus: SyllabusModel) -> SyllabusModel:
        doc = syllabus.model_dump(by_alias=True)
        await self.collection.replace_one({"_id": syllabus_id}, doc)
        return syllabus

    async def list_by_subject(self, subject_id: str) -> List[SyllabusModel]:
        cursor = self.collection.find({
            "subject_id": subject_id,
            "status": {"$ne": StructuralState.DELETED.value}
        })
        docs = await cursor.to_list(length=100)
        return [SyllabusModel(**doc) for doc in docs]


class MongoModuleRepository(ModuleRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["modules"]

    async def create(self, module: ModuleModel) -> ModuleModel:
        doc = module.model_dump(by_alias=True)
        await self.collection.insert_one(doc)
        return module

    async def get_by_id(self, module_id: str) -> Optional[ModuleModel]:
        doc = await self.collection.find_one({"_id": module_id})
        return ModuleModel(**doc) if doc else None

    async def update(self, module_id: str, module: ModuleModel) -> ModuleModel:
        doc = module.model_dump(by_alias=True)
        await self.collection.replace_one({"_id": module_id}, doc)
        return module

    async def list_by_syllabus(self, syllabus_id: str) -> List[ModuleModel]:
        cursor = self.collection.find({
            "syllabus_id": syllabus_id,
            "status": {"$ne": StructuralState.DELETED.value}
        }).sort("order", 1)
        docs = await cursor.to_list(length=100)
        return [ModuleModel(**doc) for doc in docs]


class MongoTopicRepository(TopicRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["topics"]

    async def create(self, topic: TopicModel) -> TopicModel:
        doc = topic.model_dump(by_alias=True)
        await self.collection.insert_one(doc)
        return topic

    async def get_by_id(self, topic_id: str) -> Optional[TopicModel]:
        doc = await self.collection.find_one({"_id": topic_id})
        return TopicModel(**doc) if doc else None

    async def update(self, topic_id: str, topic: TopicModel) -> TopicModel:
        doc = topic.model_dump(by_alias=True)
        await self.collection.replace_one({"_id": topic_id}, doc)
        return topic

    async def list_by_module(self, module_id: str) -> List[TopicModel]:
        cursor = self.collection.find({
            "module_id": module_id,
            "status": {"$ne": StructuralState.DELETED.value}
        }).sort("order", 1)
        docs = await cursor.to_list(length=100)
        return [TopicModel(**doc) for doc in docs]

from app.modules.knowledge.models.content import KnowledgeContentModel, PublicationState
from app.modules.knowledge.repositories.base import KnowledgeContentRepository

class MongoKnowledgeContentRepository(KnowledgeContentRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["knowledge_contents"]

    async def create(self, content: KnowledgeContentModel) -> KnowledgeContentModel:
        doc = content.model_dump(by_alias=True)
        await self.collection.insert_one(doc)
        return content

    async def get_by_id(self, content_id: str) -> Optional[KnowledgeContentModel]:
        doc = await self.collection.find_one({"_id": content_id})
        return KnowledgeContentModel(**doc) if doc else None

    async def update(self, content_id: str, content: KnowledgeContentModel) -> KnowledgeContentModel:
        doc = content.model_dump(by_alias=True)
        await self.collection.replace_one({"_id": content_id}, doc)
        return content

    async def list_by_topic(self, topic_id: str) -> List[KnowledgeContentModel]:
        cursor = self.collection.find({
            "topic_id": topic_id,
            "status": {"$ne": PublicationState.DELETED.value}
        })
        docs = await cursor.to_list(length=100)
        return [KnowledgeContentModel(**doc) for doc in docs]


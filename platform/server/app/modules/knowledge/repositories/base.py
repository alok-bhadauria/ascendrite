from abc import ABC, abstractmethod
from typing import List, Optional
from app.modules.knowledge.models.academic import SubjectModel, SyllabusModel, ModuleModel, TopicModel

class SubjectRepository(ABC):
    @abstractmethod
    async def create(self, subject: SubjectModel) -> SubjectModel:
        pass
    @abstractmethod
    async def get_by_id(self, subject_id: str) -> Optional[SubjectModel]:
        pass
    @abstractmethod
    async def update(self, subject_id: str, subject: SubjectModel) -> SubjectModel:
        pass
    @abstractmethod
    async def list_all(self) -> List[SubjectModel]:
        pass

class SyllabusRepository(ABC):
    @abstractmethod
    async def create(self, syllabus: SyllabusModel) -> SyllabusModel:
        pass
    @abstractmethod
    async def get_by_id(self, syllabus_id: str) -> Optional[SyllabusModel]:
        pass
    @abstractmethod
    async def update(self, syllabus_id: str, syllabus: SyllabusModel) -> SyllabusModel:
        pass
    @abstractmethod
    async def list_by_subject(self, subject_id: str) -> List[SyllabusModel]:
        pass

class ModuleRepository(ABC):
    @abstractmethod
    async def create(self, module: ModuleModel) -> ModuleModel:
        pass
    @abstractmethod
    async def get_by_id(self, module_id: str) -> Optional[ModuleModel]:
        pass
    @abstractmethod
    async def update(self, module_id: str, module: ModuleModel) -> ModuleModel:
        pass
    @abstractmethod
    async def list_by_syllabus(self, syllabus_id: str) -> List[ModuleModel]:
        pass

class TopicRepository(ABC):
    @abstractmethod
    async def create(self, topic: TopicModel) -> TopicModel:
        pass
    @abstractmethod
    async def get_by_id(self, topic_id: str) -> Optional[TopicModel]:
        pass
    @abstractmethod
    async def update(self, topic_id: str, topic: TopicModel) -> TopicModel:
        pass
    @abstractmethod
    async def list_by_module(self, module_id: str) -> List[TopicModel]:
        pass

from app.modules.knowledge.models.content import KnowledgeContentModel

class KnowledgeContentRepository(ABC):
    @abstractmethod
    async def create(self, content: KnowledgeContentModel) -> KnowledgeContentModel:
        pass
    @abstractmethod
    async def get_by_id(self, content_id: str) -> Optional[KnowledgeContentModel]:
        pass
    @abstractmethod
    async def update(self, content_id: str, content: KnowledgeContentModel) -> KnowledgeContentModel:
        pass
    @abstractmethod
    async def list_by_topic(self, topic_id: str) -> List[KnowledgeContentModel]:
        pass


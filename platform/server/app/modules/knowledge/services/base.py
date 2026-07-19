from abc import ABC, abstractmethod
from typing import List, Optional
from app.core.runtime.context import RuntimeContext
from app.modules.knowledge.models.academic import SubjectModel, SyllabusModel, ModuleModel, TopicModel, StructuralState

class AcademicStructureService(ABC):
    @abstractmethod
    async def create_subject(self, name: str, code: str, description: str, category: str, context: RuntimeContext) -> SubjectModel:
        pass
    @abstractmethod
    async def get_subject(self, subject_id: str, context: RuntimeContext) -> SubjectModel:
        pass
    @abstractmethod
    async def list_subjects(self, context: RuntimeContext) -> List[SubjectModel]:
        pass
    @abstractmethod
    async def update_subject(self, subject_id: str, name: str, code: str, description: str, category: str, context: RuntimeContext) -> SubjectModel:
        pass
    @abstractmethod
    async def delete_subject(self, subject_id: str, context: RuntimeContext) -> SubjectModel:
        pass

    @abstractmethod
    async def create_syllabus(self, subject_id: str, name: str, version: str, description: str, context: RuntimeContext) -> SyllabusModel:
        pass
    @abstractmethod
    async def get_syllabus(self, syllabus_id: str, context: RuntimeContext) -> SyllabusModel:
        pass
    @abstractmethod
    async def list_syllabuses_by_subject(self, subject_id: str, context: RuntimeContext) -> List[SyllabusModel]:
        pass
    @abstractmethod
    async def update_syllabus(self, syllabus_id: str, name: str, version: str, description: str, context: RuntimeContext) -> SyllabusModel:
        pass
    @abstractmethod
    async def delete_syllabus(self, syllabus_id: str, context: RuntimeContext) -> SyllabusModel:
        pass

    @abstractmethod
    async def create_module(self, syllabus_id: str, name: str, order: int, description: str, context: RuntimeContext) -> ModuleModel:
        pass
    @abstractmethod
    async def get_module(self, module_id: str, context: RuntimeContext) -> ModuleModel:
        pass
    @abstractmethod
    async def list_modules_by_syllabus(self, syllabus_id: str, context: RuntimeContext) -> List[ModuleModel]:
        pass
    @abstractmethod
    async def update_module(self, module_id: str, name: str, order: int, description: str, context: RuntimeContext) -> ModuleModel:
        pass
    @abstractmethod
    async def delete_module(self, module_id: str, context: RuntimeContext) -> ModuleModel:
        pass

    @abstractmethod
    async def create_topic(self, module_id: str, name: str, order: int, description: str, context: RuntimeContext) -> TopicModel:
        pass
    @abstractmethod
    async def get_topic(self, topic_id: str, context: RuntimeContext) -> TopicModel:
        pass
    @abstractmethod
    async def list_topics_by_module(self, module_id: str, context: RuntimeContext) -> List[TopicModel]:
        pass
    @abstractmethod
    async def update_topic(self, topic_id: str, name: str, order: int, description: str, context: RuntimeContext) -> TopicModel:
        pass
    @abstractmethod
    async def delete_topic(self, topic_id: str, context: RuntimeContext) -> TopicModel:
        pass

from app.modules.knowledge.models.content import KnowledgeContentModel, PublicationState

class KnowledgeContentService(ABC):
    @abstractmethod
    async def create_content(
        self,
        topic_id: str,
        category: str,
        title: str,
        body: str,
        assets: List[str],
        context: RuntimeContext
    ) -> KnowledgeContentModel:
        pass

    @abstractmethod
    async def get_content(self, content_id: str, context: RuntimeContext) -> KnowledgeContentModel:
        pass

    @abstractmethod
    async def update_content(
        self,
        content_id: str,
        title: str,
        body: str,
        assets: List[str],
        context: RuntimeContext
    ) -> KnowledgeContentModel:
        pass

    @abstractmethod
    async def list_content_by_topic(self, topic_id: str, context: RuntimeContext) -> List[KnowledgeContentModel]:
        pass

    @abstractmethod
    async def delete_content(self, content_id: str, context: RuntimeContext) -> KnowledgeContentModel:
        pass

    @abstractmethod
    async def transition_publication_state(
        self,
        content_id: str,
        new_status: PublicationState,
        context: RuntimeContext
    ) -> KnowledgeContentModel:
        pass


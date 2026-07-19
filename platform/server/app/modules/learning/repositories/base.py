from abc import ABC, abstractmethod
from typing import List, Optional, Any
from app.modules.learning.models.learning_session import LearningSessionModel
from app.modules.learning.models.learning_attempt import LearningAttemptModel
from app.modules.learning.models.experience import LearningExperienceModel

class LearningSessionRepository(ABC):
    @abstractmethod
    async def create(self, session: LearningSessionModel) -> LearningSessionModel:
        pass

    @abstractmethod
    async def get_by_id(self, session_id: Any) -> Optional[LearningSessionModel]:
        pass

    @abstractmethod
    async def update(self, session_id: Any, session: LearningSessionModel) -> Optional[LearningSessionModel]:
        pass

    @abstractmethod
    async def get_active_session_by_user(self, user_id: Any) -> Optional[LearningSessionModel]:
        pass

class LearningAttemptRepository(ABC):
    @abstractmethod
    async def create(self, attempt: LearningAttemptModel) -> LearningAttemptModel:
        pass

    @abstractmethod
    async def get_by_id(self, attempt_id: Any) -> Optional[LearningAttemptModel]:
        pass

    @abstractmethod
    async def update(self, attempt_id: Any, attempt: LearningAttemptModel) -> Optional[LearningAttemptModel]:
        pass

    @abstractmethod
    async def list_by_user(self, user_id: Any) -> List[LearningAttemptModel]:
        pass

    @abstractmethod
    async def list_by_session(self, session_id: Any) -> List[LearningAttemptModel]:
        pass

    @abstractmethod
    async def get_last_attempt(self, user_id: Any, resource_id: str) -> Optional[LearningAttemptModel]:
        pass

class LearningExperienceRepository(ABC):
    @abstractmethod
    async def create(self, experience: LearningExperienceModel) -> LearningExperienceModel:
        pass

    @abstractmethod
    async def get_by_id(self, experience_id: Any) -> Optional[LearningExperienceModel]:
        pass

    @abstractmethod
    async def update(self, experience_id: Any, experience: LearningExperienceModel) -> Optional[LearningExperienceModel]:
        pass

    @abstractmethod
    async def get_active_experience_by_user(self, user_id: Any, experience_type: str) -> Optional[LearningExperienceModel]:
        pass

    @abstractmethod
    async def list_by_session(self, session_id: Any) -> List[LearningExperienceModel]:
        pass


from typing import List, Optional
from pydantic import Field
from models.base import AuditModel, PyObjectId, MongoBaseModel

class AnswerDetail(MongoBaseModel):
    question_id: str
    selected_option: int
    is_correct: bool

class QuizSubmissionModel(AuditModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: PyObjectId
    topic_id: str
    score: int
    total_questions: int
    answers: List[AnswerDetail] = Field(default_factory=list)

from datetime import datetime
from typing import List
from pydantic import BaseModel, Field

class AnswerSubmit(BaseModel):
    question_id: str
    selected_option: int = Field(..., ge=0)

class QuizSubmitRequest(BaseModel):
    topic_id: str
    answers: List[AnswerSubmit]

class AnswerDetailSchema(BaseModel):
    question_id: str
    selected_option: int
    is_correct: bool

class QuizSubmissionResponse(BaseModel):
    id: str
    user_id: str
    topic_id: str
    score: int
    total_questions: int
    answers: List[AnswerDetailSchema]
    created_at: datetime

    class Config:
        from_attributes = True

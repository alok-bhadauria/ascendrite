from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from app.models.base import MongoBaseModel, PyObjectId
from app.modules.assessments.models.question import QuestionType, EvaluationDefinition

class QuestionCreate(BaseModel):
    question_type: QuestionType
    title: str
    statement: str
    explanation: str
    solution: Optional[str] = None
    hints: List[str] = Field(default_factory=list)
    options: List[str] = Field(default_factory=list)
    evaluation_definition: EvaluationDefinition
    visibility: str = "active"
    publication_status: str = "draft"
    metadata: Dict[str, Any] = Field(default_factory=dict)

class QuestionUpdate(BaseModel):
    title: Optional[str] = None
    statement: Optional[str] = None
    explanation: Optional[str] = None
    solution: Optional[str] = None
    hints: Optional[List[str]] = None
    options: Optional[List[str]] = None
    evaluation_definition: Optional[EvaluationDefinition] = None
    visibility: Optional[str] = None
    publication_status: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class QuestionResponse(MongoBaseModel):
    id: PyObjectId = Field(..., alias="_id")
    question_type: QuestionType
    title: str
    statement: str
    explanation: str
    solution: Optional[str] = None
    hints: List[str]
    options: List[str]
    evaluation_definition: EvaluationDefinition
    visibility: str
    publication_status: str
    version: int
    metadata: Dict[str, Any]

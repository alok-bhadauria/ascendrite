from datetime import datetime, timezone
from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from app.models.base import AuditModel, PyObjectId

class QuestionType(str, Enum):
    MCQ = "MCQ"
    MULTIPLE_SELECT = "MultipleSelect"
    TRUE_FALSE = "TrueFalse"
    FILL_BLANK = "FillBlank"
    CODING = "Coding"

class EvaluationDefinition(BaseModel):
    correct_option_index: Optional[int] = None
    correct_option_indices: Optional[List[int]] = None
    correct_text: Optional[str] = None
    correct_bool: Optional[bool] = None
    test_cases: Optional[List[Dict[str, Any]]] = None

class QuestionModel(AuditModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    question_type: QuestionType
    title: str
    statement: str
    explanation: str
    solution: Optional[str] = None
    hints: List[str] = Field(default_factory=list)
    options: List[str] = Field(default_factory=list)
    evaluation_definition: EvaluationDefinition
    visibility: str = "active"  # active | inactive
    publication_status: str = "draft"  # draft | published
    version: int = 1
    metadata: Dict[str, Any] = Field(default_factory=dict)

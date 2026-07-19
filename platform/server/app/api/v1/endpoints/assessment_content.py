from typing import List
from fastapi import Depends, status
from app.core.routing import APIRouter
from app.core.runtime.context import RuntimeContext
from app.api.v1.dependencies import (
    get_runtime_context,
    get_assessment_content_service
)
from app.modules.assessments.services.content import AssessmentContentService
from app.modules.assessments.models.question import QuestionModel
from app.modules.assessments.models.assessment import AssessmentModel
from app.modules.assessments.schemas.question import (
    QuestionCreate,
    QuestionUpdate,
    QuestionResponse
)
from app.modules.assessments.schemas.assessment import (
    AssessmentCreate,
    AssessmentUpdate,
    AssessmentResponse
)

router = APIRouter()

# --- Question Bank ---

@router.post("/questions", response_model=QuestionResponse, status_code=status.HTTP_201_CREATED, tags=["Assessment Content"])
async def create_question(
    payload: QuestionCreate,
    service: AssessmentContentService = Depends(get_assessment_content_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Create a new educational question bank item"""
    question = QuestionModel(**payload.model_dump())
    return await service.create_question(question, context)

@router.get("/questions/{question_id}", response_model=QuestionResponse, tags=["Assessment Content"])
async def get_question(
    question_id: str,
    service: AssessmentContentService = Depends(get_assessment_content_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Retrieve details of a question bank item"""
    return await service.get_question(question_id, context)

@router.put("/questions/{question_id}", response_model=QuestionResponse, tags=["Assessment Content"])
async def update_question(
    question_id: str,
    payload: QuestionUpdate,
    service: AssessmentContentService = Depends(get_assessment_content_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Update details of a question bank item"""
    return await service.update_question(question_id, payload.model_dump(exclude_unset=True), context)


# --- Assessment Definitions ---

@router.post("/definitions", response_model=AssessmentResponse, status_code=status.HTTP_201_CREATED, tags=["Assessment Content"])
async def create_assessment(
    payload: AssessmentCreate,
    service: AssessmentContentService = Depends(get_assessment_content_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Create a new educational assessment definition"""
    assessment = AssessmentModel(**payload.model_dump())
    return await service.create_assessment(assessment, context)

@router.get("/definitions/{assessment_id}", response_model=AssessmentResponse, tags=["Assessment Content"])
async def get_assessment(
    assessment_id: str,
    service: AssessmentContentService = Depends(get_assessment_content_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Retrieve details of an assessment definition"""
    return await service.get_assessment(assessment_id, context)

@router.put("/definitions/{assessment_id}", response_model=AssessmentResponse, tags=["Assessment Content"])
async def update_assessment(
    assessment_id: str,
    payload: AssessmentUpdate,
    service: AssessmentContentService = Depends(get_assessment_content_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Update details of an assessment definition"""
    return await service.update_assessment(assessment_id, payload.model_dump(exclude_unset=True), context)

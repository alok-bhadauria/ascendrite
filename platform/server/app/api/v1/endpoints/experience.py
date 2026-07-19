from typing import List
from fastapi import Depends, status
from app.core.routing import APIRouter
from app.core.runtime.context import RuntimeContext
from app.api.v1.dependencies import (
    get_runtime_context,
    get_learning_experience_service
)
from app.modules.learning.services.experience import LearningExperienceService
from app.modules.learning.schemas.experience import (
    LearningExperienceStartRequest,
    LearningStepSubmitRequest,
    LearningExperienceCompleteRequest,
    LearningExperienceResponse
)

router = APIRouter()

@router.post("/start", response_model=LearningExperienceResponse, status_code=status.HTTP_201_CREATED, tags=["Learning Experience"])
async def start_experience(
    payload: LearningExperienceStartRequest,
    service: LearningExperienceService = Depends(get_learning_experience_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Start an educational experience workflow for the human principal (Note, Quiz, etc.)"""
    return await service.start_experience(
        context=context,
        resource_id=payload.resource_id,
        experience_type=payload.experience_type,
        metadata=payload.metadata
    )

@router.get("/active", response_model=List[LearningExperienceResponse], tags=["Learning Experience"])
async def get_active_experiences(
    service: LearningExperienceService = Depends(get_learning_experience_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Retrieve all active learning experience states for the principal"""
    return await service.get_active_experiences(context=context)

@router.post("/{experience_id}/step", response_model=LearningExperienceResponse, tags=["Learning Experience"])
async def submit_experience_step(
    experience_id: str,
    payload: LearningStepSubmitRequest,
    service: LearningExperienceService = Depends(get_learning_experience_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Record step-by-step progress/answers within the active experience"""
    return await service.submit_experience_step(
        context=context,
        experience_id=experience_id,
        step_data=payload.step_data
    )

@router.post("/{experience_id}/complete", response_model=LearningExperienceResponse, tags=["Learning Experience"])
async def complete_experience(
    experience_id: str,
    payload: LearningExperienceCompleteRequest,
    service: LearningExperienceService = Depends(get_learning_experience_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Complete an active experience, logging corresponding learner attempt and progress evidence"""
    return await service.complete_experience(
        context=context,
        experience_id=experience_id,
        score=payload.score,
        response_data=payload.response_data
    )

@router.post("/{experience_id}/abandon", response_model=LearningExperienceResponse, tags=["Learning Experience"])
async def abandon_experience(
    experience_id: str,
    service: LearningExperienceService = Depends(get_learning_experience_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Mark an active learning experience as abandoned"""
    return await service.abandon_experience(context=context, experience_id=experience_id)

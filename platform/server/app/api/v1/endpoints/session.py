from typing import Optional
from fastapi import Depends, status
from app.core.routing import APIRouter
from app.core.runtime.context import RuntimeContext
from app.api.v1.dependencies import (
    get_runtime_context,
    get_learning_session_service,
    get_learning_attempt_service
)
from app.modules.learning.services.session import LearningSessionService
from app.modules.learning.services.attempt import LearningAttemptService
from app.modules.learning.schemas.session import (
    LearningSessionStartRequest,
    LearningSessionResponse,
    LearningAttemptStartRequest,
    LearningAttemptCompleteRequest,
    LearningAttemptResponse
)

router = APIRouter()

# ------------------------------------------------------------------------------
# LEARNING SESSIONS ENDPOINTS
# ------------------------------------------------------------------------------

@router.post("/sessions/start", response_model=LearningSessionResponse, status_code=status.HTTP_201_CREATED, tags=["Learning"])
async def start_session(
    payload: LearningSessionStartRequest,
    service: LearningSessionService = Depends(get_learning_session_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Start a lightweight contiguous learning session for the active learner principal"""
    return await service.start_session(context=context, metadata=payload.metadata)

@router.post("/sessions/{session_id}/close", response_model=LearningSessionResponse, tags=["Learning"])
async def close_session(
    session_id: str,
    service: LearningSessionService = Depends(get_learning_session_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Explicitly close an active learning session"""
    return await service.close_session(session_id=session_id, context=context)

@router.get("/sessions/active", response_model=Optional[LearningSessionResponse], tags=["Learning"])
async def get_active_session(
    service: LearningSessionService = Depends(get_learning_session_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Retrieve the current active learning session for the principal context if one exists"""
    return await service.get_active_session(context=context)

# ------------------------------------------------------------------------------
# LEARNING ATTEMPTS ENDPOINTS
# ------------------------------------------------------------------------------

@router.post("/attempts/start", response_model=LearningAttemptResponse, status_code=status.HTTP_201_CREATED, tags=["Learning"])
async def start_attempt(
    payload: LearningAttemptStartRequest,
    service: LearningAttemptService = Depends(get_learning_attempt_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Record the beginning of a learning activity/attempt on a specific resource"""
    return await service.start_attempt(
        session_id=payload.session_id,
        resource_id=payload.resource_id,
        resource_type=payload.resource_type,
        context=context,
        metadata=payload.metadata
    )

@router.post("/attempts/{attempt_id}/complete", response_model=LearningAttemptResponse, tags=["Learning"])
async def complete_attempt(
    attempt_id: str,
    payload: LearningAttemptCompleteRequest,
    service: LearningAttemptService = Depends(get_learning_attempt_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Record attempt completion and details of response choices/evidence"""
    return await service.complete_attempt(
        attempt_id=attempt_id,
        score=payload.score,
        response_data=payload.response_data,
        context=context,
        metadata=payload.metadata
    )

@router.post("/attempts/{attempt_id}/abandon", response_model=LearningAttemptResponse, tags=["Learning"])
async def abandon_attempt(
    attempt_id: str,
    service: LearningAttemptService = Depends(get_learning_attempt_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Mark attempt as abandoned/interrupted"""
    return await service.abandon_attempt(attempt_id=attempt_id, context=context)

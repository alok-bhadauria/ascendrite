from fastapi import Depends, status
from app.core.routing import APIRouter
from app.core.runtime.context import RuntimeContext
from app.api.v1.dependencies import (
    get_runtime_context,
    get_assessment_runtime_service
)
from app.modules.assessments.services.runtime import AssessmentRuntimeService
from app.modules.assessments.models.runtime import AssessmentResponseItem
from app.modules.assessments.schemas.runtime import (
    AssessmentSessionStartRequest,
    AnswerSubmitRequest,
    AssessmentSessionResponse
)

router = APIRouter()

@router.post("/start", response_model=AssessmentSessionResponse, status_code=status.HTTP_201_CREATED, tags=["Assessment Runtime"])
async def start_session(
    payload: AssessmentSessionStartRequest,
    service: AssessmentRuntimeService = Depends(get_assessment_runtime_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Start an active assessment runtime session for the principal"""
    return await service.start_session(payload.assessment_id, context)

@router.get("/{session_id}", response_model=AssessmentSessionResponse, tags=["Assessment Runtime"])
async def get_session(
    session_id: str,
    service: AssessmentRuntimeService = Depends(get_assessment_runtime_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Retrieve details of an active or completed assessment session"""
    return await service.get_session(session_id, context)

@router.post("/{session_id}/answer", response_model=AssessmentSessionResponse, tags=["Assessment Runtime"])
async def submit_answer(
    session_id: str,
    payload: AnswerSubmitRequest,
    service: AssessmentRuntimeService = Depends(get_assessment_runtime_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Submit or update a single answer response within the session"""
    response_item = AssessmentResponseItem(**payload.model_dump())
    return await service.submit_answer(session_id, response_item, context)

@router.post("/{session_id}/submit", response_model=AssessmentSessionResponse, tags=["Assessment Runtime"])
async def submit_session(
    session_id: str,
    service: AssessmentRuntimeService = Depends(get_assessment_runtime_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Finalize and submit the active assessment session for scoring and evaluation"""
    return await service.submit_session(session_id, context)

@router.post("/{session_id}/cancel", response_model=AssessmentSessionResponse, tags=["Assessment Runtime"])
async def cancel_session(
    session_id: str,
    service: AssessmentRuntimeService = Depends(get_assessment_runtime_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Cancel the active assessment session"""
    return await service.cancel_session(session_id, context)

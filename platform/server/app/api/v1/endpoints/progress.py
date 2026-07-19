from datetime import datetime, timezone
from app.core.routing import APIRouter
from fastapi import Depends, HTTPException, status
from app.modules.users.models.user import UserModel
from app.core.runtime.context import RuntimeContext
from app.modules.learning.schemas.progress import TopicProgressLog, SubjectProgressResponse
from app.modules.learning.services.progress import ProgressService
from app.api.v1.dependencies import get_progress_service, get_current_user, get_runtime_context

router = APIRouter()

@router.get("/{subject_id}", response_model=SubjectProgressResponse, tags=["Progress"])
async def get_progress(
    subject_id: str,
    current_user: UserModel = Depends(get_current_user),
    progress_service: ProgressService = Depends(get_progress_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Retrieve completion details and logged topics for a subject"""
    progress_resp = await progress_service.get_subject_progress_response(
        user_id=str(current_user.id),
        subject_id=subject_id,
        context=context
    )
    if not progress_resp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Subject with ID '{subject_id}' does not exist in curriculum."
        )
    return progress_resp

@router.post("/{subject_id}/log", response_model=SubjectProgressResponse, tags=["Progress"])
async def log_progress(
    subject_id: str,
    log_data: TopicProgressLog,
    current_user: UserModel = Depends(get_current_user),
    progress_service: ProgressService = Depends(get_progress_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Log or update learning session progress for a specific syllabus topic (evidence-based helper)"""
    # Create a mock attempt to feed as evidence (maintaining backward-compatible API helper)
    from app.modules.learning.models.learning_attempt import LearningAttemptModel, AttemptStatus
    mock_attempt = LearningAttemptModel(
        user_id=current_user.id,
        resource_id=log_data.topic_id,
        resource_type="topic",
        status=AttemptStatus.COMPLETED,
        duration_seconds=log_data.duration_seconds,
        score=log_data.quiz_score,
        end_time=datetime.now(timezone.utc)
    )
    
    result = await progress_service.record_attempt_evidence(mock_attempt, context)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to log progress. Subject '{subject_id}' or topic may be invalid."
        )
    
    return await progress_service.get_subject_progress_response(
        user_id=str(current_user.id),
        subject_id=subject_id,
        context=context
    )

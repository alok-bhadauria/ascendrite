from fastapi import APIRouter, Depends, HTTPException, status
from app.modules.users.models.user import UserModel
from app.modules.learning.schemas.progress import TopicProgressLog, SubjectProgressResponse
from app.modules.learning.services.progress import ProgressService
from app.api.v1.dependencies import get_progress_repository, get_current_user
from app.modules.learning.repositories.progress import ProgressRepository

router = APIRouter()

@router.get("/{subject_id}", response_model=SubjectProgressResponse, tags=["Progress"])
async def get_progress(
    subject_id: str,
    current_user: UserModel = Depends(get_current_user),
    progress_repo: ProgressRepository = Depends(get_progress_repository)
):
    """Retrieve completion details and logged topics for a subject"""
    progress_service = ProgressService(progress_repo)
    progress_resp = await progress_service.get_subject_progress_response(current_user.id, subject_id)
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
    progress_repo: ProgressRepository = Depends(get_progress_repository)
):
    """Log or update learning session progress for a specific syllabus topic"""
    progress_service = ProgressService(progress_repo)
    result = await progress_service.log_topic_progress(current_user.id, subject_id, log_data)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to log progress. Subject '{subject_id}' or topic may be invalid."
        )
    
    # Return updated subject progress details
    return await progress_service.get_subject_progress_response(current_user.id, subject_id)

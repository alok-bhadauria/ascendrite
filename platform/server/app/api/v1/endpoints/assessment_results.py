from typing import List
from fastapi import Depends
from app.core.routing import APIRouter
from app.core.runtime.context import RuntimeContext
from app.api.v1.dependencies import (
    get_runtime_context,
    get_assessment_evaluation_service
)
from app.modules.assessments.services.evaluation import AssessmentEvaluationService
from app.modules.assessments.schemas.results import AssessmentResultResponse

router = APIRouter()

@router.get("/session/{session_id}", response_model=AssessmentResultResponse, tags=["Assessment Results"])
async def get_result_by_session(
    session_id: str,
    service: AssessmentEvaluationService = Depends(get_assessment_evaluation_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Retrieve details of an evaluated assessment result by its session ID"""
    return await service.get_result_by_session(session_id, context)

@router.get("/user/{user_id}", response_model=List[AssessmentResultResponse], tags=["Assessment Results"])
async def get_results_by_user(
    user_id: str,
    service: AssessmentEvaluationService = Depends(get_assessment_evaluation_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Retrieve a list of evaluated assessment results for the user"""
    # Enforce ownership check inside endpoints
    if user_id != str(context.principal.id) and context.principal.role != "Admin":
        from app.core.errors import ForbiddenException
        raise ForbiddenException("You are not authorized to view results of another user.")
    return await service.repo.get_by_user(user_id)

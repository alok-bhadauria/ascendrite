from typing import List
from fastapi import Depends
from app.core.routing import APIRouter
from app.core.runtime.context import RuntimeContext
from app.api.v1.dependencies import (
    get_runtime_context,
    get_learning_insights_service
)
from app.modules.learning.services.insights import LearningInsightsService
from app.modules.learning.schemas.insights import (
    LearningHistoryItem,
    EducationalRecommendation,
    WeakAreaResponse,
    LearnerDashboardResponse
)

router = APIRouter()

@router.get("/dashboard", response_model=LearnerDashboardResponse, tags=["Learning Insights"])
async def get_dashboard(
    service: LearningInsightsService = Depends(get_learning_insights_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Retrieve the unified learner dashboard summary state"""
    return await service.get_dashboard(context=context)

@router.get("/history", response_model=List[LearningHistoryItem], tags=["Learning Insights"])
async def get_history(
    limit: int = 50,
    service: LearningInsightsService = Depends(get_learning_insights_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Retrieve chronological timeline history of learner events and attempts"""
    return await service.get_history(context=context, limit=limit)

@router.get("/recommendations", response_model=List[EducationalRecommendation], tags=["Learning Insights"])
async def get_recommendations(
    service: LearningInsightsService = Depends(get_learning_insights_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Retrieve deterministic, explainable recommendations for next study actions"""
    return await service.get_recommendations(context=context)

@router.get("/weak-areas", response_model=List[WeakAreaResponse], tags=["Learning Insights"])
async def get_weak_areas(
    service: LearningInsightsService = Depends(get_learning_insights_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Retrieve identified weak learning topic concepts that require review"""
    return await service.get_weak_areas(context=context)

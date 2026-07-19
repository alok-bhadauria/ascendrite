from typing import List, Dict, Any
from fastapi import Depends, status
from app.core.routing import APIRouter
from app.core.runtime.context import RuntimeContext
from app.api.v1.dependencies import (
    get_runtime_context,
    get_learning_utilities_service
)
from app.modules.learning.services.utilities import LearningUtilitiesService
from app.modules.learning.schemas.utilities import (
    CollectionCreateRequest,
    CollectionResourceAddRequest,
    LearningCollectionResponse,
    GoalCreateRequest,
    LearningGoalResponse
)

router = APIRouter()

# --- Collections (Bookmarks/Favorites) ---

@router.post("/collections", response_model=LearningCollectionResponse, status_code=status.HTTP_201_CREATED, tags=["Learning Utilities"])
async def create_collection(
    payload: CollectionCreateRequest,
    service: LearningUtilitiesService = Depends(get_learning_utilities_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Create a new resource collection (bookmarks/favorites list)"""
    return await service.create_collection(payload.collection_type, payload.name, context)

@router.get("/collections", response_model=List[LearningCollectionResponse], tags=["Learning Utilities"])
async def get_collections(
    service: LearningUtilitiesService = Depends(get_learning_utilities_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Retrieve all resource collections for the principal"""
    return await service.get_collections(context)

@router.post("/collections/{collection_id}/resources", response_model=LearningCollectionResponse, tags=["Learning Utilities"])
async def add_to_collection(
    collection_id: str,
    payload: CollectionResourceAddRequest,
    service: LearningUtilitiesService = Depends(get_learning_utilities_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Add a resource reference to a collection"""
    return await service.add_to_collection(collection_id, payload.resource_id, payload.resource_type, context)

@router.delete("/collections/{collection_id}/resources/{resource_id}", response_model=LearningCollectionResponse, tags=["Learning Utilities"])
async def remove_from_collection(
    collection_id: str,
    resource_id: str,
    service: LearningUtilitiesService = Depends(get_learning_utilities_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Remove a resource reference from a collection"""
    return await service.remove_from_collection(collection_id, resource_id, context)


# --- Planner Goals ---

@router.post("/goals", response_model=LearningGoalResponse, status_code=status.HTTP_201_CREATED, tags=["Learning Utilities"])
async def create_goal(
    payload: GoalCreateRequest,
    service: LearningUtilitiesService = Depends(get_learning_utilities_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Create a new learning planner goal"""
    return await service.create_goal(payload.target_date, payload.topic_ids, context)

@router.get("/goals", response_model=List[LearningGoalResponse], tags=["Learning Utilities"])
async def get_goals(
    service: LearningUtilitiesService = Depends(get_learning_utilities_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Retrieve all learning planner goals for the principal"""
    return await service.get_goals(context)

@router.put("/goals/{goal_id}/status", response_model=LearningGoalResponse, tags=["Learning Utilities"])
async def update_goal_status(
    goal_id: str,
    status: str,
    service: LearningUtilitiesService = Depends(get_learning_utilities_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Update the completion status of a planner goal"""
    return await service.update_goal_status(goal_id, status, context)


# --- Timelines ---

@router.get("/recent/accessed", response_model=List[Dict[str, Any]], tags=["Learning Utilities"])
async def get_recently_accessed(
    limit: int = 10,
    service: LearningUtilitiesService = Depends(get_learning_utilities_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Retrieve a timeline of recently accessed resources"""
    return await service.get_recently_accessed(context, limit)

@router.get("/recent/completed", response_model=List[Dict[str, Any]], tags=["Learning Utilities"])
async def get_recently_completed(
    limit: int = 10,
    service: LearningUtilitiesService = Depends(get_learning_utilities_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Retrieve a list of recently completed learning items"""
    return await service.get_recently_completed(context, limit)

from typing import List, Dict, Any, Optional
from fastapi import Depends, Query
from app.core.routing import APIRouter
from app.core.runtime.context import RuntimeContext
from app.api.v1.dependencies import (
    get_runtime_context,
    get_discovery_service
)
from app.modules.learning.services.discovery import DiscoveryService
from app.modules.learning.schemas.discovery import DiscoverableResource

router = APIRouter()

@router.get("/search", response_model=List[DiscoverableResource], tags=["Educational Discovery"])
async def search(
    query: Optional[str] = None,
    resource_type: Optional[str] = None,
    difficulty: Optional[str] = None,
    topic_id: Optional[str] = None,
    service: DiscoveryService = Depends(get_discovery_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Search for discoverable educational resources across the platform"""
    filters = {}
    if resource_type:
        filters["resource_type"] = resource_type
    if difficulty:
        filters["difficulty"] = difficulty
    if topic_id:
        filters["topic_id"] = topic_id
    return await service.search(query=query or "", filters=filters, context=context)

@router.get("/related", response_model=List[DiscoverableResource], tags=["Educational Discovery"])
async def get_related_resources(
    resource_id: str,
    resource_type: str,
    service: DiscoveryService = Depends(get_discovery_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Retrieve related discoverable resources for a given resource context"""
    return await service.get_related_resources(resource_id, resource_type, context)

@router.get("/explore", response_model=Dict[str, List[DiscoverableResource]], tags=["Educational Discovery"])
async def explore(
    service: DiscoveryService = Depends(get_discovery_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Retrieve exploration lists of popular or recently added educational resources"""
    return await service.explore(context)

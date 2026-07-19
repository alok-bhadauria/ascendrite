from fastapi import Depends, status, Query
from typing import List, Dict, Any
from app.core.routing import APIRouter
from app.core.runtime.context import RuntimeContext
from app.api.v1.dependencies import (
    get_runtime_context,
    get_collaboration_activity_service
)
from app.modules.collaboration.services.activity import CollaborationActivityService

router = APIRouter()

@router.get("/activity", response_model=List[Dict[str, Any]], tags=["Collaboration Tracing"])
async def get_activities(
    resource_id: str = Query(...),
    service: CollaborationActivityService = Depends(get_collaboration_activity_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Retrieve history timeline logs for a specific authoring resource"""
    activities = await service.get_activities(resource_id, context)
    return [a.model_dump() for a in activities]

@router.get("/notifications", response_model=List[Dict[str, Any]], tags=["Collaboration Tracing"])
async def get_notifications(
    service: CollaborationActivityService = Depends(get_collaboration_activity_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Retrieve active unread collaborative workflow reminders for context actor"""
    notifications = await service.get_notifications(context)
    return [n.model_dump() for n in notifications]

@router.post("/notifications/{notification_id}/read", status_code=status.HTTP_204_NO_CONTENT, tags=["Collaboration Tracing"])
async def mark_notification_as_read(
    notification_id: str,
    service: CollaborationActivityService = Depends(get_collaboration_activity_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Mark a pending team/assignment notification as read"""
    await service.mark_notification_as_read(notification_id, context)

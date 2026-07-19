from fastapi import Depends, status, Query
from typing import List, Dict, Any
from app.core.routing import APIRouter
from app.core.runtime.context import RuntimeContext
from app.api.v1.dependencies import (
    get_runtime_context,
    get_collaboration_workflow_service
)
from app.modules.collaboration.services.workflow import CollaborationWorkflowService

router = APIRouter()

@router.post("/assignments", status_code=status.HTTP_201_CREATED, tags=["Collaboration Workflows"])
async def assign_resource(
    resource_id: str = Query(...),
    resource_type: str = Query(...),
    assignee_id: str = Query(...),
    service: CollaborationWorkflowService = Depends(get_collaboration_workflow_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Assign an authoring workspace resource task to a collaborator"""
    assignment = await service.assign_resource(resource_id, resource_type, assignee_id, context)
    return assignment.model_dump()

@router.put("/assignments/{assignment_id}/status", tags=["Collaboration Workflows"])
async def update_assignment_status(
    assignment_id: str,
    status: str = Query(...),
    service: CollaborationWorkflowService = Depends(get_collaboration_workflow_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Update progress status of a collaboration assignment task"""
    assignment = await service.update_assignment_status(assignment_id, status, context)
    return assignment.model_dump()

@router.post("/comments", status_code=status.HTTP_201_CREATED, tags=["Collaboration Discussion"])
async def add_comment(
    resource_id: str = Query(...),
    content: str = Query(...),
    service: CollaborationWorkflowService = Depends(get_collaboration_workflow_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Post a contextual collaborator feedback comment thread to a resource"""
    comment = await service.add_comment(resource_id, content, context)
    return comment.model_dump()

@router.get("/comments", response_model=List[Dict[str, Any]], tags=["Collaboration Discussion"])
async def get_comments(
    resource_id: str = Query(...),
    service: CollaborationWorkflowService = Depends(get_collaboration_workflow_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Retrieve all contextual comments attached to a specific workspace resource"""
    comments = await service.get_comments(resource_id, context)
    return [c.model_dump() for c in comments]

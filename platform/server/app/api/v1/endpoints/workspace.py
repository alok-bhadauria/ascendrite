from fastapi import Depends, status
from typing import List
from app.core.routing import APIRouter
from app.core.runtime.context import RuntimeContext
from app.api.v1.dependencies import (
    get_runtime_context,
    get_creator_workspace_service
)
from app.modules.creator.services.workspace import ContentWorkspaceService
from app.modules.creator.schemas.draft import (
    DraftCreateRequest,
    DraftUpdateRequest,
    DraftResourceResponse
)

router = APIRouter()

@router.post("/", response_model=DraftResourceResponse, status_code=status.HTTP_201_CREATED, tags=["Creator Workspace"])
async def create_draft(
    payload: DraftCreateRequest,
    service: ContentWorkspaceService = Depends(get_creator_workspace_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Create a new editing draft for a resource type"""
    return await service.create_draft(payload.resource_type, payload.content, context)

@router.get("/{draft_id}", response_model=DraftResourceResponse, tags=["Creator Workspace"])
async def get_draft(
    draft_id: str,
    service: ContentWorkspaceService = Depends(get_creator_workspace_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Retrieve details of a specific workspace draft"""
    return await service.get_draft(draft_id, context)

@router.put("/{draft_id}", response_model=DraftResourceResponse, tags=["Creator Workspace"])
async def update_draft(
    draft_id: str,
    payload: DraftUpdateRequest,
    service: ContentWorkspaceService = Depends(get_creator_workspace_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Update content of a workspace draft"""
    return await service.update_draft(draft_id, payload.content, context)

@router.post("/{draft_id}/duplicate", response_model=DraftResourceResponse, tags=["Creator Workspace"])
async def duplicate_draft(
    draft_id: str,
    service: ContentWorkspaceService = Depends(get_creator_workspace_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Duplicate an existing workspace draft"""
    return await service.duplicate_draft(draft_id, context)

@router.post("/{draft_id}/validate", response_model=DraftResourceResponse, tags=["Creator Workspace"])
async def validate_draft(
    draft_id: str,
    service: ContentWorkspaceService = Depends(get_creator_workspace_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Run structural correctness validation on draft content"""
    return await service.validate_draft(draft_id, context)

@router.delete("/{draft_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Creator Workspace"])
async def delete_draft(
    draft_id: str,
    service: ContentWorkspaceService = Depends(get_creator_workspace_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Archive or discard an editing workspace draft"""
    await service.archive_draft(draft_id, context)
